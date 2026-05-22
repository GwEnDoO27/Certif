import os
import re
import shutil
import logging
from typing import Dict, List, Optional
import tempfile
from datetime import datetime
import asyncio
from pathlib import Path

UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

from fastapi import (
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
    APIRouter,
)


def require_valid_uid(request: Request) -> str:
    user_uid = request.cookies.get("userId") or request.cookies.get("userID")
    if not user_uid or not UUID_RE.match(user_uid):
        raise HTTPException(status_code=401, detail="Invalid or missing user identifier")
    return user_uid
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from schemas.model import User
from db.database import Base, SessionLocal, engine
from Logging.logging_config import configure_user_logging
from utils.utils import NewUser, query_code_comptas, query_code_gen_aux, query_journal_code
from utils.convert import code_comptas, code_comptas_gen_aux, code_journal
from utils.format import format

# Créer les tables
Base.metadata.create_all(bind=engine)

# Configuration
TEMP_BASE_DIR = tempfile.gettempdir()
CLEANUP_DELAY_SECONDS = 300  # 5 minutes

# Modèles Pydantic pour la validation
class CodeUpdate(BaseModel):
    comptas: Optional[Dict[str, str]] = None
    other: Optional[Dict[str, str]] = None
    journal: Optional[Dict[str, str]] = None

class CodeResponse(BaseModel):
    comptas: Dict[str, str]
    other: Dict[str, str]
    journal: Dict[str, str]

# Fonction pour récupérer la session de la base de données
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Thread de vérification des nouveaux utilisateurs
import threading
import time

def check_new_users():
    while True:
        with SessionLocal() as db:
            print("Checking for new users...")
            NewUser(db)
        time.sleep(30)

thread = threading.Thread(target=check_new_users, daemon=True)
thread.start()

# Fonctions utilitaires
def get_user_temp_directory(user_uid: str) -> tuple[str, str, str]:
    """Retourne les chemins des répertoires temporaires pour un utilisateur"""
    if not UUID_RE.match(user_uid or ""):
        raise HTTPException(status_code=400, detail="Invalid user identifier")
    user_temp_dir = os.path.join(TEMP_BASE_DIR, user_uid)
    upload_dir = os.path.join(user_temp_dir, "uploads")
    download_dir = os.path.join(user_temp_dir, "downloads")
    print(f"Dossier uploads : {upload_dir}, Dossier dl: {download_dir}, Temp dir : {user_temp_dir}")
    return user_temp_dir, upload_dir, download_dir

async def cleanup_user_directory(user_uid: str, delay: int = 0):
    """Nettoie le répertoire temporaire d'un utilisateur après un délai"""
    if delay > 0:
        await asyncio.sleep(delay)
    
    try:
        user_temp_dir, _, _ = get_user_temp_directory(user_uid)
        if os.path.exists(user_temp_dir):
            shutil.rmtree(user_temp_dir)
            print(f"Répertoire temporaire {user_temp_dir} supprimé avec succès")
    except Exception as e:
        print(f"Erreur lors de la suppression du répertoire {user_temp_dir}: {str(e)}")

# Créer le routeur API
api_router = APIRouter()

# ========== ROUTE 1: GESTION DES CODES ==========
@api_router.get("/codes")
async def get_all_codes(
    request: Request,
    db: Session = Depends(get_session),
):
    """
    Récupère tous les codes (comptas + other)
    """
    user_uid = request.cookies.get("userId") or request.cookies.get("userID")
    if not user_uid:
        raise HTTPException(status_code=401, detail="User ID not found")
    
    logger = configure_user_logging(user_uid, level=logging.INFO)
    
    # Vérification de l'utilisateur
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        logger.error(f"Pas d'utilisateur trouvé avec cet UID: {user_uid}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Récupération de tous les codes pour l'utilisateur {user_uid}")
    
    try:
        code_comptas_map = query_code_comptas(db, user_uid, logger)
        code_gen_aux_map = query_code_gen_aux(db, user_uid, logger)
        code_journal_map = query_journal_code(db, user_uid=user_uid, logger=logger)
        
        response = {
            "comptas": code_comptas_map,
            "other": code_gen_aux_map,
            "journal": code_journal_map
        }
        
        logger.info(f"Codes récupérés avec succès pour {user_uid}")
        return response
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des codes: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching codes")

@api_router.post("/codes")
async def update_all_codes(
    request: Request,
    db: Session = Depends(get_session),
):
    """
    Met à jour les codes (comptas et/ou other et/ou journal)
    """
    user_uid = request.cookies.get("userId") or request.cookies.get("userID")
    if not user_uid:
        raise HTTPException(status_code=401, detail="User ID not found")
    
    logger = configure_user_logging(user_uid, level=logging.INFO)
    
    # Vérification de l'utilisateur
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        logger.error(f"Pas d'utilisateur trouvé avec cet UID: {user_uid}")
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        data = await request.json()
        
        logger.info(f"Mise à jour des codes pour l'utilisateur {user_uid}")
        
        results = {}
        
        # Mise à jour des codes comptables si fournis
        if "comptas" in data and data["comptas"] is not None:
            logger.info(f"Mise à jour des codes comptables")
            results["comptas"] = code_comptas(db, user.id, data["comptas"], logger)
        
        # Mise à jour des codes généraux/auxiliaires si fournis
        if "other" in data and data["other"] is not None:
            logger.info(f"Mise à jour des codes généraux et auxiliaires")
            results["other"] = code_comptas_gen_aux(db, user.id, data["other"], logger)
        
        # Mise à jour du code general si fournis
        if "journal" in data and data["journal"] is not None:
            logger.info(f"Mise à jour des codes généraux et auxiliaires")
            results["journal"] = code_journal(db, user.id, data["journal"], logger)
        
        if not results:
            raise HTTPException(status_code=400, detail="No codes provided for update")
        
        logger.info(f"Codes mis à jour avec succès pour {user_uid}")
        return results
        
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des codes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating codes: {str(e)}")

# ========== ROUTE 2: CONVERSION DE FICHIERS ==========
@api_router.post("/conversion")
async def conversion_file_endpoint(
    request: Request,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_session),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """
    Route de conversion tout-en-un :
    1. Upload les fichiers dans un répertoire temporaire
    2. Les formate avec les codes configurés de l'utilisateur
    3. Retourne le fichier Excel formaté
    4. Nettoie automatiquement après un délai
    """
    user_uid = request.cookies.get("userId") or request.cookies.get("userID")
    if not user_uid:
        raise HTTPException(status_code=401, detail="User ID not found")
    
    logger = configure_user_logging(user_uid, level=logging.INFO)
    logger.info(f"Début du processus de conversion pour l'utilisateur {user_uid}")
    
    # Vérification de l'utilisateur
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        logger.error(f"Pas d'utilisateur trouvé avec cet UID: {user_uid}")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Créer la structure de répertoires temporaires
    user_temp_dir, upload_dir, download_dir = get_user_temp_directory(user_uid)
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(download_dir, exist_ok=True)
    
    try:
        # Étape 1 : Upload des fichiers
        logger.info(f"Étape 1/3 : Upload de {len(files)} fichier(s)")
        print(f"Étape 1/3 : Upload de {len(files)} fichier(s)")
        
        uploaded_files = []
        total_size = 0
        
        for uploaded_file in files:
            # Validation du type de fichier
            if not uploaded_file.filename.endswith('.txt'):
                logger.warning(f"Fichier ignoré (pas .txt): {uploaded_file.filename}")
                print(f"Fichier ignoré (pas .txt): {uploaded_file.filename}")
                continue
            
            safe_filename = Path(uploaded_file.filename).name
            file_location = os.path.join(upload_dir, safe_filename)
            
            try:
                content = await uploaded_file.read()
                total_size += len(content)
                
                with open(file_location, "wb") as file_object:
                    file_object.write(content)
                    logger.info(f"Fichier {safe_filename} sauvegardé ({len(content)} bytes)")
                    print(f"Fichier {safe_filename} sauvegardé ({len(content)} bytes)")
                    uploaded_files.append(safe_filename)
                    
            except Exception as e:
                logger.error(f"Erreur lors de la sauvegarde du fichier {safe_filename}: {str(e)}")
                print(f"Erreur lors de la sauvegarde du fichier {safe_filename}: {str(e)}")
                # Continuer avec les autres fichiers
                continue
        
        if not uploaded_files:
            raise HTTPException(
                status_code=400,
                detail="Aucun fichier .txt valide n'a été fourni"
            )
        
        logger.info(f"Upload terminé: {len(uploaded_files)} fichier(s), {total_size/1024:.1f} KB au total")
        
        # Étape 2 : Formatage des fichiers
        logger.info(f"Étape 2/3 : Formatage des fichiers avec les codes de l'utilisateur")
        print(f"Étape 2/3 : Formatage des fichiers avec les codes de l'utilisateur")
        try:
            format(upload_dir, download_dir, user_uid, db, logger)
        except Exception as e:
            logger.error(f"Erreur lors du formatage: {str(e)}")
            print(f"Erreur lors du formatage: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors du formatage des fichiers: {str(e)}"
            )
        
        # Étape 3 : Vérification et préparation du fichier de sortie
        logger.info(f"Étape 3/3 : Préparation du fichier de sortie")
        print(f"Étape 3/3 : Préparation du fichier de sortie")
        output_file = os.path.join(download_dir, "combined.xlsx")
        print(f"Output file {output_file}")
        
        if not os.path.exists(output_file):
            logger.error("Le fichier de sortie n'a pas été créé")
            print("Le fichier de sortie n'a pas été créé")
            raise HTTPException(
                status_code=500,
                detail="Le formatage a échoué, aucun fichier de sortie généré"
            )
        
        # Informations sur le fichier de sortie
        file_size = os.path.getsize(output_file)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        logger.info(f"Conversion réussie: {output_file} ({file_size_mb} MB)")
        print(f"Conversion réussie: {output_file} ({file_size_mb} MB)")
        
        # Programmer le nettoyage après un délai
        background_tasks.add_task(
            cleanup_user_directory, 
            user_uid, 
            CLEANUP_DELAY_SECONDS
        )
        
        # Retourner le fichier Excel
        return FileResponse(
            path=output_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=f"factures_MB_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            headers={
                "Content-Disposition": f"attachment; filename=factures_MB_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            }
        )
        
    except HTTPException:
        # Re-lancer les HTTPException
        raise
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur inattendue lors du traitement: {str(e)}"
        )

# ========== ROUTES OPTIONNELLES ==========

@api_router.get("/status")
async def get_status(
    request: Request,
):
    """Vérifie le statut du service et des fichiers temporaires de l'utilisateur"""
    user_uid = request.cookies.get("userId") or request.cookies.get("userID")
    if not user_uid:
        return {"status": "ok", "user": None}
    
    user_temp_dir, upload_dir, download_dir = get_user_temp_directory(user_uid)
    
    status = {
        "status": "ok",
        "user": user_uid,
        "temp_files": {
            "exists": os.path.exists(user_temp_dir),
            "upload_dir": os.path.exists(upload_dir),
            "download_dir": os.path.exists(download_dir),
            "output_ready": os.path.exists(os.path.join(download_dir, "combined.xlsx"))
        }
    }
    
    if os.path.exists(upload_dir):
        status["temp_files"]["uploaded_files"] = os.listdir(upload_dir)
    
    return status

@api_router.post("/cleanup")
async def cleanup_temp_files(
    request: Request,
):
    """Nettoie manuellement les fichiers temporaires de l'utilisateur"""
    user_uid = request.cookies.get("userId") or request.cookies.get("userID")
    if not user_uid:
        raise HTTPException(status_code=401, detail="User ID not found")
    
    logger = configure_user_logging(user_uid, level=logging.INFO)
    
    user_temp_dir, _, _ = get_user_temp_directory(user_uid)
    
    if os.path.exists(user_temp_dir):
        try:
            shutil.rmtree(user_temp_dir)
            logger.info(f"Fichiers temporaires nettoyés pour l'utilisateur {user_uid}")
            return {"message": "Temporary files cleaned successfully"}
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error cleaning files: {str(e)}")
    else:
        return {"message": "No temporary files found"}

# ========== ROUTES LEGACY POUR COMPATIBILITÉ ==========

@api_router.get("/codecomptas")
async def get_codecomptas_legacy(
    request: Request, 
    db: Session = Depends(get_session)
):
    """Route legacy - utilise directement le code existant"""
    user_uid = request.cookies.get("userId")
    logger = configure_user_logging(user_uid, level=logging.INFO)
    
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        logger.error(f"Pas d'utilisateur trouvé avec cet UID: {user_uid}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Récupération pour l'utilisateur {user_uid} des codes comptabilités")
    code_map = query_code_comptas(db, user_uid, logger)
    logger.info(f"Map des codes comptas {code_map} pour {user_uid}")
    
    return code_map

@api_router.post("/codecomptas")
async def update_codecomptas_legacy(
    request: Request, 
    data: Dict[str, str], 
    db: Session = Depends(get_session)
):
    """Route legacy - utilise directement le code existant"""
    user_uid = request.cookies.get("userId")
    logger = configure_user_logging(user_uid, level=logging.INFO)
    
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        logger.error(f"Pas d'utilisateur trouvé avec cet UID: {user_uid}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Changement pour l'utilisateur {user_uid} des codes comptabilités")
    updated_code_map = code_comptas(db, user.id, data, logger)
    logger.info(f"Map mise à jour des codes comptas {updated_code_map} pour {user_uid}")
    
    return updated_code_map

@api_router.get("/codeother")
async def get_codeother_legacy(
    request: Request, 
    db: Session = Depends(get_session)
):
    """Route legacy - utilise directement le code existant"""
    user_uid = request.cookies.get("userId")
    logger = configure_user_logging(user_uid, level=logging.INFO)
    
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        logger.error(f"Pas d'utilisateur trouvé avec cet UID: {user_uid}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Récupération pour l'utilisateur {user_uid} des codes généraux et auxiliaires")
    code_map = query_code_gen_aux(db, user_uid, logger)
    logger.info(f"Map des codes généraux et auxiliaires {code_map} pour {user_uid}")
    
    return code_map

@api_router.post("/codeother")
async def update_codeother_legacy(
    request: Request, 
    data: Dict[str, str], 
    db: Session = Depends(get_session)
):
    """Route legacy - utilise directement le code existant"""
    user_uid = request.cookies.get("userId")
    logger = configure_user_logging(user_uid, level=logging.INFO)
    
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        logger.error(f"Pas d'utilisateur trouvé avec cet UID: {user_uid}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Changement pour l'utilisateur {user_uid} des codes généraux et auxiliaires")
    updated_code_map = code_comptas_gen_aux(db, user.id, data, logger)
    logger.info(f"Map mise à jour des codes généraux et auxiliaires {updated_code_map} pour {user_uid}")
    
    return updated_code_map


@api_router.get("/journal")
async def get_codeother_legacy(
    request: Request, 
    db: Session = Depends(get_session)
):
    """Route legacy - utilise directement le code existant"""
    user_uid = request.cookies.get("userId")
    logger = configure_user_logging(user_uid, level=logging.INFO)
    
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        logger.error(f"Pas d'utilisateur trouvé avec cet UID: {user_uid}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Récupération pour l'utilisateur {user_uid} des codes généraux et auxiliaires")
    journal_map = query_journal_code(db, user_uid, logger)
    logger.info(f"Map des codes généraux et auxiliaires {journal_map} pour {user_uid}")
    
    return journal_map

@api_router.post("/journal")
async def update_codeother_legacy(
    request: Request, 
    data: Dict[str, str], 
    db: Session = Depends(get_session)
):
    """Route legacy - utilise directement le code existant"""
    user_uid = request.cookies.get("userId")
    logger = configure_user_logging(user_uid, level=logging.INFO)
    
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        logger.error(f"Pas d'utilisateur trouvé avec cet UID: {user_uid}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Changement pour l'utilisateur {user_uid} des codes généraux et auxiliaires")
    updated_journal_code = code_journal(db, user.id, data, logger)
    logger.info(f"Map mise à jour des codes généraux et auxiliaires {updated_journal_code} pour {user_uid}")
    
    return updated_journal_code
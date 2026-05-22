import os
import logging
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, PatternFill, Alignment
import xlsxwriter
from utils.convert import formatting_csv, merged_csv
from utils.sort import sorting_mag


def create_excel_with_sheets(download_path: str, user_uid: str, logger: logging.Logger):
    """
    Crée un fichier Excel avec une feuille par magasin en utilisant xlsxwriter.
    """
    print("=== NOUVELLE FONCTION create_excel_with_sheets APPELÉE ===")
    logger.info("=== NOUVELLE FONCTION create_excel_with_sheets APPELÉE ===")
    try:
        # Repérer tous les CSV racine
        print(f"Recherche des fichiers CSV dans: {download_path}")
        all_files = os.listdir(download_path)
        print(f"Tous les fichiers trouvés: {all_files}")
        
        file_list = [
            os.path.join(download_path, f)
            for f in all_files
            if f.endswith('.csv')
        ]
        
        print(f"Fichiers CSV trouvés: {file_list}")
        
        if not file_list:
            logger.warning("Aucun fichier CSV à convertir")
            print("Aucun fichier CSV à convertir")
            return

        excel_path = os.path.join(download_path, "combined.xlsx")
        
        # Supprimer le fichier existant s'il existe
        if os.path.exists(excel_path):
            os.remove(excel_path)
        
        # Créer le workbook avec xlsxwriter - options pour éviter la corruption
        workbook = xlsxwriter.Workbook(excel_path, {
            'strings_to_numbers': False,  # Désactiver la conversion automatique
            'nan_inf_to_errors': True,    # Convertir NaN/Inf en erreurs Excel
            'default_date_format': 'dd/mm/yyyy'
        })
        
        # Formats pour les différents types de données
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#366092',
            'align': 'center'
        })
        
        # Format pour les nombres
        number_format = workbook.add_format({
            'num_format': '0.00'
        })
        
        # Format pour les cellules vides
        empty_format = workbook.add_format({
            'font_color': 'white'
        })
        
        for file in file_list:
            try:
                print(f"Tentative de lecture du fichier: {file}")
                # Lire le CSV
                try:
                    df = pd.read_csv(file, encoding='utf-8')
                    print(f"Fichier lu avec succès: {file}")
                except UnicodeDecodeError:
                    print(f"Erreur UTF-8, tentative avec latin-1: {file}")
                    df = pd.read_csv(file, encoding='latin-1')
                    print(f"Fichier lu avec latin-1: {file}")
                except Exception as e:
                    print(f"Erreur de lecture du fichier {file}: {e}")
                    continue
                
                if df.empty:
                    print(f"DataFrame vide pour {file}")
                    continue
                
                # Nom du magasin
                store_name = os.path.splitext(os.path.basename(file))[0]
                
                # Nettoyer le nom de la feuille
                forbidden_chars = ['[', ']', '*', '?', ':', '/', '\\']
                sheet_name = store_name
                for char in forbidden_chars:
                    sheet_name = sheet_name.replace(char, '_')
                sheet_name = sheet_name[:31]
                
                # Créer la feuille
                worksheet = workbook.add_worksheet(sheet_name)
                
                # Nettoyer les données
                numeric_columns = ['DEBIT', 'CREDIT', 'MONTANT']
                for col in df.columns:
                    if col in numeric_columns:
                        # Remplacer les NaN par 0 pour les colonnes numériques
                        df[col] = df[col].fillna(0)
                        # Convertir en numérique et gérer les erreurs
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                    else:
                        # Pour les autres colonnes, remplacer NaN par chaîne vide
                        df[col] = df[col].fillna('')
                        df[col] = df[col].astype(str)
                        df[col] = df[col].str.replace(r'[\x00-\x1f\x7f-\x9f]', '', regex=True)
                
                # Écrire les en-têtes
                headers = df.columns.tolist()
                print(f"Headers pour {sheet_name}: {headers}")
                print(f"Nombre de lignes de données: {len(df)}")
                print(f"Premières lignes du DataFrame:")
                print(df.head())
                
                for col_num, header in enumerate(headers):
                    worksheet.write(0, col_num, header, header_format)
                
                # Approche très simple : écrire toutes les données avec write()
                print(f"Écriture des données pour {sheet_name}: {len(df)} lignes, {len(df.columns)} colonnes")
                
                for row_num, row in enumerate(df.values, 1):
                    for col_num, value in enumerate(row):
                        try:
                            if pd.isna(value):
                                worksheet.write_blank(row_num, col_num, None)
                            elif headers[col_num] in numeric_columns:
                                # Nombres
                                num_val = float(value) if value != '' else 0
                                worksheet.write(row_num, col_num, num_val, number_format)
                            else:
                                # Texte
                                worksheet.write(row_num, col_num, str(value))
                        except Exception as e:
                            # En cas d'erreur, écrire comme string
                            worksheet.write(row_num, col_num, str(value))
                            print(f"Erreur cellule [{row_num}, {col_num}]: {e}")
                
                print(f"Données écrites pour {sheet_name}: {len(df)} lignes")
                logger.info(f"Données écrites pour {sheet_name}: {len(df)} lignes")
                
                # Auto-ajuster les colonnes
                for col_num, header in enumerate(headers):
                    max_length = len(header)
                    for value in df[header]:
                        max_length = max(max_length, len(str(value)))
                    worksheet.set_column(col_num, col_num, min(max_length + 2, 50))
                
                logger.info(f"Feuille '{sheet_name}' créée avec {len(df)} lignes")
                
            except Exception as e:
                logger.error(f"Erreur lors du traitement de {file}: {e}")
                continue
        
        # Fermer le workbook proprement
        try:
            workbook.close()
        except Exception as e:
            logger.error(f"Erreur lors de la fermeture du workbook: {e}")
            raise
        
        # Vérifier que le fichier a été créé correctement
        if not os.path.exists(excel_path):
            raise Exception("Le fichier Excel n'a pas pu être créé")
        
        file_size = os.path.getsize(excel_path)
        if file_size == 0:
            raise Exception("Le fichier Excel créé est vide")
        
        logger.info(f"Fichier Excel créé avec xlsxwriter : {excel_path} ({file_size} bytes)")
        print(f"Fichier Excel créé avec xlsxwriter : {excel_path} ({file_size} bytes)")
        
    except Exception as e:
        logger.error(f"Erreur lors de la création du fichier Excel avec xlsxwriter: {e}")
        raise

def convert_edi_to_excel(
    upload_path: str,
    download_path: str,
    user_uid: str,
    db,
    logger: logging.Logger
):
    """
    Parcourt chaque dossier magasin sous upload_path :
    1) appelle formatting_csv pour chaque .edi/.txt,
    2) fusionne en <magasin>.csv via merged_csv,
    3) à la fin, crée un fichier Excel avec une feuille par magasin.
    """
    logger.info("=== Début de convert_edi_to_excel ===")
    os.makedirs(download_path, exist_ok=True)

    # 1) Pour chaque dossier magasin
    for entry in os.scandir(upload_path):
        if not entry.is_dir():
            continue
        
        mag = entry.name
        # Nettoyer le nom du magasin (enlever les apostrophes)
        mag_clean = mag.rstrip("'")
        mag_upload = entry.path
        mag_download = os.path.join(download_path, mag_clean)
        os.makedirs(mag_download, exist_ok=True)

        # 1a) formatting_csv sur chaque fichier .edi/.txt du magasin
        for fn in os.listdir(mag_upload):
            if not fn.lower().endswith((".edi", ".txt")):
                continue
            
            formatting_csv(
                file_path=os.path.join(mag_upload, fn),
                input_folder=mag_upload,
                output_folder=mag_download,
                user_uid=user_uid,
                db=db,
                logger=logger
            )

        # 2) Fusion des CSV du magasin en download_path/<mag_clean>.csv
        merged_csv(mag_clean, download_path, logger)

    # 3) Création du fichier Excel avec une feuille par magasin
    create_excel_with_sheets(download_path, user_uid, logger)
    
    logger.info("=== Fin de convert_edi_to_excel ===")

def format(upload_path, download_path, user_uid, db, logger: logging.Logger):
    """
    Formate les fichiers EDI en Excel avec une feuille par magasin
    Args:
        upload_path: Chemin absolu vers le dossier uploads
        download_path: Chemin absolu vers le dossier downloads
        user_uid: ID de l'utilisateur
        db: Session de base de données
        logger: Logger configuré
    """
    logger.info(f"Début du formatage Excel")
    logger.info(f"Upload path: {upload_path}")
    logger.info(f"Download path: {download_path}")

    # Vérifier si les répertoires existent
    if not os.path.exists(upload_path):
        os.makedirs(upload_path, exist_ok=True)
        logger.info(f"Créé le répertoire upload: {upload_path}")
    
    if not os.path.exists(download_path):
        os.makedirs(download_path, exist_ok=True)
        logger.info(f"Créé le répertoire download: {download_path}")

    # Obtenir la liste des fichiers dans le dossier uploads
    uploaded_files = [f for f in os.listdir(upload_path) if f.endswith(".txt")]
    if not uploaded_files:
        logger.warning("No EDI files found in the 'uploads' directory.")
        return

    logger.info(f"Trouvé {len(uploaded_files)} fichiers à traiter")

    # Traiter chaque fichier avec sorting_mag
    for filename in uploaded_files:
        file_path = os.path.join(upload_path, filename)
        logger.info(f"Processing file: {file_path}")
        try:
            # Passer les chemins absolus à sorting_mag
            sorting_mag(file_path, upload_path, download_path, user_uid, logger)
        except Exception as e:
            logger.error(f"An error occurred while processing {filename}: {e}")
            print(f"An error occurred while processing {filename}: {e}", flush=True)

    # Convertir tous les fichiers après le tri
    try:
        convert_edi_to_excel(
            upload_path,
            download_path,
            user_uid,
            db,
            logger
        )
    except Exception as e:
        print(f"An error occurred in convert: {e}", flush=True)
        logger.error(f"An error occurred in convert: {e}")
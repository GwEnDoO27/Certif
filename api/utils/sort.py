import os
import shutil
import logging
from utils.searching import verify_if_mag_exists, whos_mag


def sorting_mag(file_path, upload_path, download_path, user_uid, logger: logging.Logger):
    """
    Trie les fichiers dans les dossiers des magasins
    
    Args:
        file_path: Chemin complet du fichier à trier
        upload_path: Chemin absolu du dossier uploads (ex: /tmp/user_uid/uploads)
        download_path: Chemin absolu du dossier downloads (ex: /tmp/user_uid/downloads)
        user_uid: ID de l'utilisateur
        logger: Logger configuré
    """
    mag = whos_mag(file_path, logger)
    if mag:
        already_exists = verify_if_mag_exists(mag, upload_path, download_path)
        if already_exists:
            sort_files(file_path, mag, upload_path, download_path, logger)
            logger.info(f"File '{file_path}' has been sorted into the '{mag}' folder.")

def sort_files(file_path, mag, upload_path, download_path, logger):
    """
    Deplace le fichier dans le dossier du magasin
    
    Args:
        file_path: Chemin complet du fichier
        mag: Nom du magasin
        upload_path: Chemin absolu du dossier uploads
        download_path: Chemin absolu du dossier downloads
        logger: Logger
    """
    sanitized_name = os.path.basename(file_path).replace("'", "")
    logger.info(f"Sanitized name: {sanitized_name}")
    
    # Utiliser les chemins absolus
    mag_folder = os.path.join(upload_path, mag)
    mag_download_folder = os.path.join(download_path, mag)
    
    # Créer les dossiers si nécessaire
    if not os.path.exists(mag_folder):
        os.makedirs(mag_folder, exist_ok=True)
        logger.info(f"Created upload folder: {mag_folder}")
    
    if not os.path.exists(mag_download_folder):
        os.makedirs(mag_download_folder, exist_ok=True)
        logger.info(f"Created download folder: {mag_download_folder}")
    
    # Déplacer le fichier
    destination = os.path.join(mag_folder, sanitized_name)
    shutil.move(file_path, destination)
    logger.info(f"Moved file to: {destination}")

import os
import logging


def whos_mag(file_path, logger: logging.Logger):
    """Recherche le nom du magasin dans le fichier EDI"""
    try:
        with open(file_path, "r", encoding="ISO-8859-1") as file:
            lines = file.readlines()
    except FileNotFoundError:
        logger.error(f"Error: The text file '{file_path}' can't be found.")
        return None
    
    for line in lines:
        mag_name = name_of_mag(line)
        if mag_name:
            return mag_name
    
    return None

def name_of_mag(line):
    """Recherche le nom du magasin dans le fichier EDI"""
    if line.startswith("RFF+GN"):
        line = line.rstrip("'")
        parts = line.split("+")
        if len(parts) > 1:
            mag = parts[1].split(":")
            if len(mag) > 1:
                mag = mag[1]
                return mag.strip()
    return None

def verify_if_mag_exists(mag, upload_path, download_path):
    """
    Recherche si le magasin a un dossier a son nom
    
    Args:
        mag: Nom du magasin
        upload_path: Chemin absolu du dossier uploads
        download_path: Chemin absolu du dossier downloads
    
    Returns:
        bool: True si les dossiers existent ou ont été créés
    """
    mag_upload_folder = os.path.join(upload_path, mag)
    mag_download_folder = os.path.join(download_path, mag)
    
    # Créer les dossiers s'ils n'existent pas
    os.makedirs(mag_upload_folder, exist_ok=True)
    os.makedirs(mag_download_folder, exist_ok=True)
    
    return True

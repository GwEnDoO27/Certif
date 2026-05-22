import csv
import os
import sys

import pandas as pd #type: ignore
from schemas.model import UserCodeMap,UserCodeGenAux,UserJournal

from utils.utils import query_code_comptas
from schemas.model import User
import logging
import glob

if len(sys.argv) > 1:
    file_name = sys.argv[1]



def code_comptas(db, user_id: int, new_data: dict, logger: logging.Logger) -> dict:
    """
    Met à jour (ou crée) la map des codes comptables de l'utilisateur.

    Args:
        db: session SQLAlchemy
        user_id: identifiant interne de l'utilisateur
        new_data: dict des mises à jour
        logger: logger configuré

    Returns:
        La map de codes mise à jour.
    """
    try:
        ucm = db.query(UserCodeMap).filter_by(user_id=user_id).first()
        if not ucm:
            logger.info("Création d'une nouvelle entrée UserCodeMap")
            default = {
                "001 SURGELE": "601100",
                "002 ALIMENTAIRE": "601100",
                "003 EMBALLAGE": "602201",
                "004 FOURN.OP": "606302",
                "005 HABILLEMENT": "606303",
                "006 FOURN.BUR": "606401",
                "007 JOUETS et DIV": "602202",
                "008 CADEAU/PLV": "623401",
                "009 ADMINSTR & STAT": "602610",
                "00R EMBALLAGE REUSE": "602612",
                "00X DIVERS": "471000",
                "00O EMBALLAGE REUSE | OUT": "602612",
            }
            ucm = UserCodeMap(user_id=user_id, code_map=default)
        # filtration et mise à jour
        filtered = {k:v for k,v in new_data.items() if v and v.strip()}
        ucm.code_map = {**ucm.code_map, **filtered}
        db.add(ucm)
        db.commit()
        db.refresh(ucm)
        logger.info("UserCodeMap mis à jour avec succès")
        return ucm.code_map
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur code_comptas: {e}")
        raise



def code_comptas_gen_aux(db, user_id: int, new_data: dict, logger: logging.Logger) -> dict:
    """
    Met à jour (ou crée) la map des codes auxilliaires de l'utilisateur.

    Args:
        db: session SQLAlchemy
        user_id: identifiant interne de l'utilisateur
        new_data: dict des mises à jour
        logger: logger configuré

    Returns:
        La map de codes mise à jour.
    """
    try:
        ucg = db.query(UserCodeGenAux).filter_by(user_id=user_id).first()
        if not ucg:
            logger.info("Création d'une nouvelle entrée UserCodeGenAux")
            default = {
                "Code General 401000": "401000",
                "Code General 411000": "411000",
                "Code General 445660": "445660",
                "Code Auxilliaire 401000": "401LR",
                "Code Auxilliaire 411000": "411MB",
                "Code Auxilliaire 445660": "",
            }
            ucg = UserCodeGenAux(user_id=user_id, code_map_gen_aux=default)
        filtered = {k:v for k,v in new_data.items() if v and v.strip()}
        ucg.code_map_gen_aux = {**ucg.code_map_gen_aux, **filtered}
        db.add(ucg)
        db.commit()
        db.refresh(ucg)
        logger.info("UserCodeGenAux mis à jour avec succès")
        return ucg.code_map_gen_aux
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur code_comptas_gen_aux: {e}")
        raise

def code_journal(db, user_id: int, new_data: dict, logger: logging.Logger) -> dict:
    """
    Met à jour (ou crée) la map de journal de l'utilisateur,
    et persiste immédiatement la nouvelle map.
    """
    try:
        # 1. on récupère l'ancien, s'il existe
        cd = db.query(UserJournal).filter_by(user_id=user_id).first()
        if not cd:
            logger.info("Création d'une nouvelle entrée UserJournal")
            cd = UserJournal(
                user_id=user_id,
                journal_map={"Journal": "ACM"}
            )

        # 2. on fusionne l'existant + les nouvelles valeurs
        filtered = {k: v for k, v in new_data.items() if v and v.strip()}
        cd.journal_map = {**(cd.journal_map or {}), **filtered}

        # 3. on persiste
        db.add(cd)
        db.commit()
        db.refresh(cd)

        logger.info("UserJournal mis à jour avec succès")
        return cd.journal_map

    except Exception as e:
        db.rollback()
        logger.error(f"Erreur code_journal: {e}")
        raise




# Extract the values from the EDI file
def extract_bill_values(file_path: str, db, user_uid: str, logger: logging.Logger) -> dict:
    """
    Lit un EDI, extrait référence, date, valeurs ligne et totaux (TVA, avance, net).
    """
    logger.debug(f"Extraction des valeurs depuis {file_path}")
    try:
        code_map = query_code_comptas(db, user_uid, logger)
    except Exception as e:
        logger.error(f"Impossible de récupérer code_map: {e}")
        raise

    try:
        with open(file_path, "r", encoding="ISO-8859-1") as f:
            lines = [l.strip().rstrip("'") for l in f if l.strip()]
    except Exception as e:
        logger.error(f"Erreur lecture fichier EDI: {e}")
        raise

    if not lines or "EDI" not in lines[0]:
        msg = "Fichier non-EDI ou vide"
        logger.error(msg)
        raise ValueError(msg)

    # initialisation
    moa_vals, tot_vals, gen_vals = [], [], []
    found, tva, net, adv = set(), 0.0, 0.0, 0.0
    ref, date_fmt = "", ""

    # codes généraux
    for line in lines:
        for code, mapped in code_map.items():
            if code in line and code not in found:
                gen_vals.append(mapped)
                found.add(code)

    # référence BGM
    for line in lines:
        if line.startswith("BGM"):
            parts = line.split("+")
            ref = parts[2] if len(parts)>=3 else ""
            break

    # date DTM 137
    for line in lines:
        if line.startswith("DTM"):
            parts = line.split("+")[1].split(":")
            if parts[0]=="137" and len(parts)>=2 and len(parts[1])==8:
                d = parts[1]
                date_fmt = f"{d[6:8]}/{d[4:6]}/{d[0:4]}"
                break

    # valeurs articles (IMD→MOA)
    for idx, line in enumerate(lines):
        if line.startswith("IMD") and (idx==0 or not lines[idx-1].startswith("PIA")):
            for j in range(idx+1, len(lines)):
                if lines[j].startswith("MOA"):
                    val = lines[j].split("+")[1].split(":")[1]
                    moa_vals.append(val)
                    break

    # totaux après UNS
    uns = False
    for line in lines:
        if line.startswith("UNS"):
            uns = True
            continue
        if uns and line.startswith("MOA"):
            code, val = line.split("+")[1].split(":")
            try:
                num = float(val)
            except:
                continue
            tot_vals.append(num)
            if code.startswith("124") and tva==0: tva = num
            elif code.startswith("218") and adv==0: adv = num
            elif code.startswith("39") and net==0: net = num
        elif uns and not line.startswith("MOA"):
            break

    total = round(max(tot_vals) if tot_vals else 0, 2)
    logger.debug(f"Extractions: ref={ref}, date={date_fmt}, TVA={tva}, avance={adv}, net={net}")

    return {
        "articles_values": moa_vals,
        "advance": abs(adv),
        "tva": tva,
        "net_payable": abs(net),
        "reference": ref,
        "date": date_fmt,
        "general_values": gen_vals,
    }



def get_document_type(file_path: str, logger: logging.Logger) -> str:
    """
    Détermine si l'EDI est une Facture ou un Avoir via BGM+380/381.
    """
    logger.debug(f"Détection du type de document pour {file_path}")
    try:
        with open(file_path, "r", encoding="ISO-8859-1") as f:
            for line in f:
                if line.startswith("BGM+381"):
                    return "Avoir"
                if line.startswith("BGM+380"):
                    return "Facture"
    except FileNotFoundError:
        logger.warning(f"Fichier introuvable: {file_path}")
    except Exception as e:
        logger.error(f"Erreur get_document_type: {e}")
    return "Facture"




def formatting_csv(
    file_path: str,
    input_folder: str,
    output_folder: str,
    user_uid: str,
    db,
    logger: logging.Logger
):
    """
    Extrait les valeurs de l’EDI (comme avant) et génère UN CSV par fichier EDI :
    output_folder/<nom_du_fichier>.csv
    """
    logger.info(f"formatting_csv : {file_path}")
    os.makedirs(output_folder, exist_ok=True)

    # 1) Récupération des codes auxiliaires
    try:
        user    = db.query(User).filter_by(uid=user_uid).first()
        aux_map = code_comptas_gen_aux(db, user.id, {}, logger)
    except Exception as e:
        logger.error(f"Erreur récupération codes auxiliaires: {e}")
        return

    # 2) Extraction des données depuis l’EDI
    try:
        bill     = extract_bill_values(file_path, db, user_uid, logger)
        doc_type = get_document_type(file_path, logger)
    except Exception:
        logger.error("Extraction des données échouée, on skip.")
        return

    try: 
        user_journal  = db.query(User).filter_by(uid=user_uid).first()
        journal_map = code_journal(db, user_journal.id, {}, logger)
        print(f"Code du journal {journal_map}")
    except Exception as e :
        logger.error(f"Erreur récupération code journal: {e}")
        print(f"Erreur récupération code journal: {e}")
        return
    # 3) Création de la même liste de dicts qu'avant
    data = []
    base = {
        "DATE":      bill["date"],
        "REFERENCE": bill["reference"],
        "LIBELLE":   f"{'Avoir' if doc_type=='Avoir' else 'Achat'} MB {bill['reference']}"
    }
    if doc_type == "Avoir":
        data += [
            {"JOURNAL": journal_map["Journal"] ,**base, "GENERAL": aux_map["Code General 401000"], "AUXILIAIRE": aux_map["Code Auxilliaire 401000"], "DEBIT": bill["net_payable"], "CREDIT": ""},
            {"JOURNAL": journal_map["Journal"]  ,**base, "GENERAL": aux_map["Code General 411000"], "AUXILIAIRE": aux_map["Code Auxilliaire 411000"], "DEBIT": bill["advance"],      "CREDIT": ""},
            {"JOURNAL": journal_map["Journal"]  ,**base, "GENERAL": aux_map["Code General 445660"], "AUXILIAIRE": aux_map["Code Auxilliaire 445660"], "DEBIT": "",               "CREDIT": bill["tva"]},
        ]
    else:
        data += [
            {"JOURNAL": journal_map["Journal"]  ,**base, "GENERAL": aux_map["Code General 401000"], "AUXILIAIRE": aux_map["Code Auxilliaire 401000"], "DEBIT": "",               "CREDIT": bill["net_payable"]},
            {"JOURNAL": journal_map["Journal"]  ,**base, "GENERAL": aux_map["Code General 411000"], "AUXILIAIRE": aux_map["Code Auxilliaire 411000"], "DEBIT": "",               "CREDIT": bill["advance"]},
            {"JOURNAL": journal_map["Journal"]  ,**base, "GENERAL": aux_map["Code General 445660"], "AUXILIAIRE": aux_map["Code Auxilliaire 445660"], "DEBIT": bill["tva"],      "CREDIT": ""},
        ]
    for val, gen in zip(bill["articles_values"], bill["general_values"]):
        entry = {
            "JOURNAL": journal_map["Journal"]  ,
            **base,
            "GENERAL":    gen,
            "AUXILIAIRE": "",
            "DEBIT":      val if doc_type!="Avoir" else "",
            "CREDIT":     val if doc_type=="Avoir" else ""
        }
        data.append(entry)

    column_order = [
        "JOURNAL",
        "DATE", 
        "GENERAL",
        "AUXILIAIRE", 
        "REFERENCE",
        "LIBELLE",
        "DEBIT",
        "CREDIT"
    ]

    # 4) Écriture du CSV *unique* pour ce fichier EDI
    csv_name = os.path.splitext(os.path.basename(file_path))[0] + ".csv"
    csv_path = os.path.join(output_folder, csv_name)
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=column_order)
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"CSV généré: {csv_path}")
        print(f"CSV généré: {csv_path}")
    except Exception as e:
        logger.error(f"Erreur écriture CSV: {e}")
        print(f"Erreur écriture CSV: {e}")




def merged_csv(store_name: str, download_path: str, logger: logging.Logger):
    """
    Concatène tous les CSV dans download_path/<store_name>/*.csv
    en un seul download_path/<store_name>.csv
    """
    store_dir = os.path.join(download_path, store_name)
    pattern   = os.path.join(store_dir, "*.csv")
    files     = glob.glob(pattern)
    logger.info(f"Fusion de {len(files)} CSV pour le magasin '{store_name}'")
    print(f"Fusion de {len(files)} CSV pour le magasin '{store_name}'")

    if not files:
        logger.warning(f"Aucun CSV à fusionner dans {store_dir}")
        print(f"Aucun CSV à fusionner dans {store_dir}")
        return

    try:
        df_list = [pd.read_csv(f) for f in files]
        merged  = pd.concat(df_list, ignore_index=True)
        out_csv = os.path.join(download_path, f"{store_name}.csv")
        merged.to_csv(out_csv, index=False, encoding="utf-8")
        logger.info(f"CSV fusionné créé : {out_csv}")
        print(f"CSV fusionné pour '{store_name}': {out_csv}")
    except Exception as e:
        logger.error(f"Erreur fusion CSV pour {store_name} : {e}")
        print(f"Erreur fusion CSV pour {store_name} : {e}")


def merged_csv_page(download_path: str, user_uid: str, logger: logging.Logger):
    """
    Combine tous les CSV magasins en un seul fichier combined.csv,
    en ajoutant une colonne 'MAGASIN' indiquant la source.
    Args:
        download_path: Chemin absolu du dossier downloads
        user_uid: ID de l'utilisateur (non utilisé ici)
        logger: Logger configuré
    """
    try:
        # repérer tous les CSV racine (sortis par merged_csv)
        file_list = [
            os.path.join(download_path, f)
            for f in os.listdir(download_path)
            if f.endswith('.csv') and f != 'combined.csv'
        ]
        logger.info(f"CSV à combiner en global: {len(file_list)}")
        print(f"CSV à combiner en global: {len(file_list)}")

        if not file_list:
            logger.warning("Aucun fichier CSV à combiner")
            print("Aucun fichier CSV à combiner")
            return

        df_list = []
        for file in file_list:
            try:
                df = pd.read_csv(file, encoding='latin1')
                store = os.path.splitext(os.path.basename(file))[0]
                df_list.append(df)
                logger.debug(f"Ajouté {file} comme MAGASIN={store}")
                print(f"Ajouté {file} comme MAGASIN={store}")
            except Exception as e:
                logger.error(f"Erreur ajout CSV {file}: {e}")
                print(f"Erreur ajout CSV {file}: {e}")
                continue

        combined = pd.concat(df_list, ignore_index=True)
        out_path = os.path.join(download_path, "combined.csv")
        combined.to_csv(out_path, index=False, encoding='latin1')
        logger.info(f"Fichier global combined.csv généré : {out_path}")
        print(f"Fichier global combined.csv généré : {out_path}")

    except Exception as e:
        logger.error(f"An error occurred in merged_csv_page: {e}")
        print(f"An error occurred in merged_csv_page: {e}")
        raise

from schemas.model import UserCodeMap, User, UserCodeGenAux, UserJournal
import requests
import logging
from Logging.logging_config import configure_user_logging 
from typing import Optional
from sqlalchemy.orm import Session #type: ignore

def query_code_comptas(db: Session, user_uid: str, logger: logging.Logger) -> Optional[str]:
    """
    Récupère le code_map pour un utilisateur donné en utilisant SQLAlchemy
    """
    try:
        # Récupérer l'utilisateur par UID
        user = db.query(User).filter(User.uid == user_uid).first()

        if user is None:
            logger.info(f"User with UID {user_uid} not found.")
            return None
        
        # Récupérer le code_map associé à l'utilisateur
        user_code_map = db.query(UserCodeMap).filter(UserCodeMap.user_id == user.id).first()

        if user_code_map is None:
            logger.info(f"No code map found for user {user_uid}")
            return None

        return user_code_map.code_map
    
    except Exception as error:
        logger.error(f"Erreur lors de la requête code_comptas pour l'utilisateur {user_uid}: {error}")
        raise


def query_code_gen_aux(db, user_uid, logger: logging.Logger):
    user = db.query(User).filter(User.uid == user_uid).first()

    if user is None:
        print(f"User with UID {user_uid} not found. Aborting query.")
        logger.error(f"User with UID {user_uid} not found. Aborting query.")
        return None

    user_code_map_gen_aux = db.query(UserCodeGenAux).filter(UserCodeGenAux.user_id == user.id).first()

    if user_code_map_gen_aux is None:
        print(f"No code_gen_aux found for user {user_uid}. Returning None.")
        logger.info(f"No code_gen_aux found for user {user_uid}. Returning None.")
        return None

    logger.info(f"Code_gen_aux found for user {user_uid}.")
    print(f"Code_gen_aux found for user {user_uid}.")
    return user_code_map_gen_aux.code_map_gen_aux



def query_journal_code(db,user_uid:str,logger: logging.Logger):
    user =db.query(User).filter(User.uid ==user_uid).first()

    if user is None:
        print(f"User with UID {user_uid} not found. Aborting query.")
        logger.error(f"User with UID {user_uid} not found. Aborting query.")
        return None

    user_journal_map = db.query(UserJournal).filter(UserJournal.user_id == user.id).first()

    if user_journal_map is None:
        print(f"No journal found for user {user_uid}. Returning None.")
        logger.info(f"No journal found for user {user_uid}. Returning None.")
        return None

    logger.info(f"journal found for user {user_uid}.")
    print(f"journal found for user {user_uid}.")
    print(f"Journal {user_journal_map.journal_map}")
    return user_journal_map.journal_map


def get_user():
    try:
        response = requests.get(f"http://backend:8002/sys/get-users")
        data = response.json()
        print("Data users",data)
        return data
    except Exception as e:
        print("Error", e)
        return None
    

def NewUser(db):
    # Récupérer les utilisateurs directement depuis la base de données
    users = db.query(User).all()  # On récupère tous les utilisateurs de la table User
    if not users:
        print("No users found in the database")
        return {"detail": "No users found in the database"}, 404
    
    new_users_added = []
    
    for user in users:
        user_uid = user.uid
        
        # Vérifie si l'utilisateur existe déjà dans la table user_code_maps
        existing_user_code_map = db.query(UserCodeMap).filter(UserCodeMap.user_id == user.id).first()
        
        # Vérifie si l'utilisateur existe déjà dans la table user_code_gen_aux
        existing_user_code_gen_aux = db.query(UserCodeGenAux).filter(UserCodeGenAux.user_id == user.id).first()

        #Vérifie si l'utilisateur existe déjà dans la table journal
        existing_user_journal_code = db.query(UserJournal).filter(UserJournal.user_id == user.id).first()


        if existing_user_code_map is None or existing_user_code_gen_aux is None or existing_user_journal_code is None:
            #print(f"User with uid {user_uid} not fully set up. Adding code maps and code gen aux.")
            try:
                # Crée un nouvel utilisateur dans la table User si nécessaire
                if existing_user_code_map is None:
                    new_user_code_map = UserCodeMap(user_id=user.id, code_map={
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
                    })
                    db.add(new_user_code_map)
                
                if existing_user_code_gen_aux is None:
                    new_user_code_map_gen_aux = UserCodeGenAux(user_id=user.id, code_map_gen_aux={
                        "Code General 401000": "401000",
                        "Code General 411000": "411000",
                        "Code General 445660": "445660",
                        "Code Auxilliaire 401000": "401LR",
                        "Code Auxilliaire 411000": "411MB",
                        "Code Auxilliaire 445660": "",
                    })
                    db.add(new_user_code_map_gen_aux)

                if existing_user_journal_code is None:
                    new_user_journal_code  = UserJournal(user_id=user.id, journal_map ={
                        "Journal":"ACM"
                    })  
                    db.add(new_user_journal_code)
                # Commit dans la base de données après ajout des entrées
                db.commit()
                #print(f"Code maps and code gen aux added for user with uid {user_uid} successfully.")
                new_users_added.append(user_uid)
                
            except Exception as e:
                db.rollback()  # Annuler en cas d'erreur
                print(f"Error while committing code map and code gen aux for user {user_uid}: {e}")
                return {"detail": f"Failed to add code maps and code gen aux for user {user_uid}: {str(e)}"}, 500                                      

    if new_users_added:
        return {"detail": f"Added code maps and code gen aux for {len(new_users_added)} users: {new_users_added}"}
    else:
        return {"detail": "No new users added"}

# Documentation technique — Plateforme intranet & API tirages de caisse

> Document destiné aux développeurs et à l'exploitation. Il décrit l'architecture, les API, le modèle de données, le pipeline de traitement et le déploiement.

---

## 1. Vue d'ensemble

La solution est composée de **trois services** partageant une base **PostgreSQL** :

| Service | Techno | Port | Rôle |
|---|---|---|---|
| `frontend/` | React 19 + Vite (SPA, servie par Nginx) | 3000 | Interface utilisateur |
| `backend/` | Go (Gorilla Mux) | 8002 | Auth, utilisateurs, catalogue, analytics, WebSocket, config McDonald's |
| `api/` | Python FastAPI | 8001 | Traitement des tirages de caisse (EDI → Excel), codes comptables |

```
Frontend (React) ──axios──► Backend Go (8002)   ─┐
                 ──axios──► API Python (8001)    ─┼─► PostgreSQL
                 ──ws──────► Backend Go (/ws)     ─┘
```

Le backend Go porte la logique transverse (sécurité, données, temps réel) ; l'API Python porte le traitement de fichiers (écosystème pandas / xlsxwriter).

---

## 2. Architecture interne

Les deux back-ends suivent le même découpage en couches :

```
Handler (HTTP)  →  Service (logique métier)  →  Repository (persistance)
```

- **Go** : un dossier par domaine (`auth`, `admin`, `applications`, `analyse`, `websocket`, `Macdos`).
- **Python** : `main.py` (app + CORS), `routers.py` (endpoints), `utils/` (`convert.py`, `format.py`, `searching.py`, `sort.py`), `schemas/` (modèles SQLAlchemy).
- **Front** : `components/` (Landing, Auth, Admin, `pages/Convert`, UI, Widgets), `services/` (appels API), `hooks/` (`useWebSocket`, `useAnalytics`…), `context/` (`ThemeContext`).

---

## 3. Référence des API

### 3.1 Backend Go — préfixe `/sys` (port 8002)

**Public (sans session)**

| Méthode | Route | Description |
|---|---|---|
| POST | `/sys/login` | Authentification, création de session + cookie `userId` |
| POST | `/sys/logout` | Fermeture de session |

**Authentifié (`AuthMiddleware`)**

| Méthode | Route | Description |
|---|---|---|
| GET | `/sys/verify-token` | Vérifie la validité de la session |
| GET | `/sys/verify-admin` | Vérifie le statut administrateur |
| GET | `/sys/user-applications` | Catalogue filtré pour l'utilisateur |
| GET | `/sys/get-icons` | Icônes des applications |
| POST/GET | `/sys/analyses/...` | Événements et statistiques (connexions, API, heures de pointe) |
| POST | `/sys/get-macdos-configs-names` | Liste des configs McDonald's |
| GET | `/sys/get-macdos-config-{name_config}` | Lecture d'une config McDonald's |
| PUT | `/sys/update-macdos-config-{name_config}` | Mise à jour d'une config McDonald's |

**Administrateur (`AuthMiddleware` + `AdminMiddleware`)**

| Méthode | Route | Description |
|---|---|---|
| GET | `/sys/get-users` / `/sys/get-user/{uid}` | Lister / consulter les utilisateurs |
| POST | `/sys/new-user` | Créer un utilisateur (mot de passe haché bcrypt) |
| PUT | `/sys/update-user/{uid}` | Modifier un utilisateur |
| DELETE | `/sys/delete-user/{uid}` | Supprimer un utilisateur |
| POST/DELETE | `/sys/add-app/{uid}` / `/sys/remove-app/{uid}` | Attribuer / retirer une application |
| POST/PUT/DELETE | `/sys/create-new-app` / `/sys/edit-app/{id}` / `/sys/delete-app/{id}` | CRUD du catalogue |
| GET | `/sys/get-apps` / `/sys/get-groups` | Lister applications / groupes |
| POST | `/sys/create-group`, `/sys/upload` | Créer un groupe, uploader un fichier (icône) |

**Autres**

| Méthode | Route | Description |
|---|---|---|
| GET | `/ws` | WebSocket de présence temps réel |
| GET | `/health` | Sonde de santé |
| GET | `/uploads/...` | Fichiers statiques protégés (`AuthMiddleware`) |

### 3.2 API Python — préfixe `/api` (port 8001)

| Méthode | Route | Description |
|---|---|---|
| POST | `/api/conversion` | **Cœur métier** : upload `.EDI`/`.txt` → Excel (une feuille par restaurant) |
| GET | `/api/codes` | Récupère tous les codes (comptables, généraux/auxiliaires, journal) |
| POST | `/api/codes` | Met à jour tout ou partie des codes |
| GET/POST | `/api/codecomptas` | Codes comptables (legacy) |
| GET/POST | `/api/codeother` | Codes généraux/auxiliaires (legacy) |
| GET/POST | `/api/journal` | Codes journal (legacy) |
| GET | `/api/status` | État du traitement |
| POST | `/api/cleanup` | Nettoyage manuel des fichiers temporaires |

> L'identité de l'appelant est portée par le cookie `userId` (UUID). L'API valide son format par regex avant tout traitement (protection contre l'injection / le path traversal).

---

## 4. Modèle de données (extrait)

| Table | Rôle | Champs clés |
|---|---|---|
| `users` | Comptes | `uid` (UUID), `email`, `password` (bcrypt), `role`, `is_admin`, `company` |
| `sessions` | Sessions actives | `user_uid`, `expires_at` (+24 h) |
| `applications` | Catalogue | `id`, `nom`, `icone`, `categorie`, groupe |
| `user_applications` | Attribution N–N | `user_uid`, `app_id` |
| `codes_comptables` | Mapping caisse → compte | `user_id`, `code_map` (**JSONB**) |
| `codes_gen_aux` | Comptes généraux/auxiliaires | `user_id`, `code_map_gen_aux` (**JSONB**) |
| `codes_journal` | Code journal | `user_id`, `code_map` (**JSONB**) |
| `config_fascicule` | Config McDonald's par établissement | `name_config`, contenu |
| `events` | Analytics | type, utilisateur, horodatage |

Les mappings de codes sont stockés en **JSONB** : un mapping par utilisateur, fusionné à la mise à jour (`{**existant, **nouveau}`), les valeurs vides étant ignorées.

---

## 5. Pipeline de traitement des tirages de caisse

Endpoint : `POST /api/conversion` (`routers.py` → `utils/format.py` → `utils/convert.py`).

```
1. Upload         → sauvegarde des .EDI/.txt dans /tmp/{uid}/uploads (un dossier par restaurant)
2. Parsing EDI    → extract_bill_values() : segments EDIFACT (BGM, DTM, MOA, IMD, UNS)
                    get_document_type() : Facture (BGM+380) vs Avoir (BGM+381)
3. Mapping        → application des codes comptables de l'utilisateur (SELECT … JSONB)
4. Fusion         → merged_csv() : un CSV consolidé par restaurant
5. Excel          → create_excel_with_sheets() (xlsxwriter) : une feuille par restaurant → combined.xlsx
6. Réponse        → FileResponse (factures_MB_<date>.xlsx)
7. Nettoyage      → background task : suppression de /tmp/{uid}/* après délai (RGPD)
```

Points d'attention :
- **Encodages variables** (ISO-8859-1 / UTF-8) : parsing tolérant, sans masquer les vraies erreurs de format.
- **Parsing ligne à ligne** piloté par préfixe de segment : streaming, pas de chargement complet en mémoire.
- **Robustesse par lot** : un fichier invalide est ignoré individuellement, le traitement des autres continue.

---

## 6. Sécurité (synthèse)

- Authentification par **session + cookie**, mots de passe **bcrypt**, comparaison en temps constant.
- **RBAC** : vérification du rôle admin côté serveur (`AdminMiddleware`), jamais uniquement côté front.
- **Défense en profondeur** : front (routes protégées) → Go (middlewares sur `/sys`) → Python (validation UUID + existence en base).
- **Filtrage du catalogue par jointure SQL** : un utilisateur ne reçoit jamais d'application non attribuée.
- **RGPD** : fichiers transients supprimés automatiquement ; données de test fictives ou anonymisées.

---

## 7. Configuration & déploiement

### Variables d'environnement (base de données)

| Variable | Description |
|---|---|
| `DB_HOST` | Hôte PostgreSQL |
| `DB_PORT` | Port PostgreSQL |
| `DB_NAME` | Nom de la base |
| `DB_USER` | Utilisateur |
| `DB_PASSWORD` | Mot de passe |

L'origine CORS autorisée est configurable (ex. `https://preprod.azert.fr`).

### Lancement en local

```bash
# Frontend
cd frontend && npm install && npm run dev        # http://localhost:3000

# API Python
cd api && pip install -r requirements.txt && python run.py   # http://localhost:8001

# Backend Go
cd backend && go mod download && go run ./cmd/main.go        # http://localhost:8002
```

### Déploiement

- **Dockerfile** dans chaque composant ; image front servie par Nginx.
- **Kubernetes (K3s)** : manifests dans `api/k8s/` et `backend/k8s/`.
- **Reverse proxy Traefik** : terminaison TLS et routage HTTPS.
- **Persistance** : les uploads applicatifs sont montés sur un volume (`/app/uploads` via PVC).
- **CI/CD** : GitHub Actions (tests Go à chaque push sur `main`).

---

## 8. Tests

| Périmètre | Outil | Localisation |
|---|---|---|
| API Python (parsing EDI, codes, auth, tris) | pytest | `api/tests/` |
| Frontend (hooks, contexte, utilitaires) | Vitest | `frontend/src/__tests__/` |
| Backend Go | `go test ./...` | par package |

Les tests de l'API utilisent des **fixtures `tmp_path`** écrivant des EDI inline (`BGM+380` facture, `BGM+381` avoir) et des jeux de codes par défaut, sans dépendre de fichiers externes.

```bash
cd api && pytest                              # tests Python
cd frontend && npm run test                   # tests Vitest
cd backend && go test ./... --tags=exclude_websocket
```

# Diagrammes UML - Portail Intranet d'Entreprise

> Tous les diagrammes utilisent la syntaxe Mermaid. Ils peuvent être rendus via :
> - Mermaid Live Editor (mermaid.live)
> - Extension VS Code "Markdown Preview Mermaid Support"
> - GitHub (rendu natif des blocs Mermaid)

---

## 1. Diagramme de Cas d'Utilisation

```mermaid
graph TB
    subgraph "Portail Intranet"

        subgraph "Authentification"
            UC1[Se connecter]
            UC2[Se déconnecter]
            UC3[Vérifier sa session]
        end

        subgraph "Gestion des utilisateurs"
            UC4[Créer un utilisateur]
            UC5[Modifier un utilisateur]
            UC6[Supprimer un utilisateur]
            UC7[Lister les utilisateurs]
            UC8[Attribuer une application]
            UC9[Retirer une application]
        end

        subgraph "Gestion des applications"
            UC10[Créer une application]
            UC11[Modifier une application]
            UC12[Supprimer une application]
            UC13[Voir le catalogue]
            UC14[Créer un groupe]
        end

        subgraph "Outils métier"
            UC15[Convertir EDI → Excel]
            UC16[Fusionner fichiers Excel]
            UC17[Traiter fichiers Silae]
            UC18[Détecter les doublons]
            UC19[Vérifier la TVA]
            UC20[Traiter le FEC]
            UC21[Gérer codes comptables]
        end

        subgraph "Analytics & Temps Réel"
            UC22[Consulter les statistiques]
            UC23[Voir les utilisateurs connectés]
            UC24[Enregistrer un événement]
        end
    end

    Visiteur((Visiteur)) --> UC1
    Utilisateur((Utilisateur)) --> UC2
    Utilisateur --> UC3
    Utilisateur --> UC13
    Utilisateur --> UC23

    Comptable((Comptable)) --> UC15
    Comptable --> UC16
    Comptable --> UC21
    Comptable --> UC17

    Auditeur((Auditeur)) --> UC18
    Auditeur --> UC19
    Auditeur --> UC20

    Admin((Admin)) --> UC4
    Admin --> UC5
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
    Admin --> UC14
    Admin --> UC22
    Admin --> UC24

    Comptable -.->|hérite| Utilisateur
    Auditeur -.->|hérite| Utilisateur
    Admin -.->|hérite| Utilisateur
```

---

## 2. Diagramme de Classes — Backend Go (Clean Architecture)

```mermaid
classDiagram
    direction TB

    class User {
        +int ID
        +string UID
        +string Email
        +string Password
        +time.Time LastSeen
        +string Entreprise
    }

    class Session {
        +string ID
        +string UserID
        +time.Time CreatedAt
        +time.Time ExpiresAt
    }

    class AdminUser {
        +string UID
        +string Username
        +string Email
        +string Role
        +bool Admin
        +[]string Applications
    }

    class App {
        +string ID
        +string Name
        +string BaseURL
        +string IconPath
        +string Groups
    }

    class AppGroup {
        +string ID
        +string Name
    }

    class Event {
        +int ID
        +string APIName
        +string UID
        +string ConnTime
        +string DecoTime
        +string Day
        +string CreatedAt
    }

    class ConnectedUser {
        +string UID
        +string Username
        +bool Connected
        +time.Time LastSeen
        +*websocket.Conn Conn
    }

    class OnlineUserManager {
        +map~string,*ConnectedUser~ Users
        +sync.RWMutex Mutex
        +*UserRepository Repo
        +AddUser(uid, username, conn)
        +RemoveUser(uid)
        +BroadcastUsers()
        +ListenPings(uid, conn, done)
    }

    class AuthService {
        +*SessionRepository Repo
        +Login(email, password) (User, Session, error)
        +VerifySession(sessionID) (Session, error)
        +MarkSessionAsDisconnected(sessionID)
        +CleanExpiredSessions()
    }

    class AdminService {
        +Rep Repo
        +VerifyAdmin(userID) (bool, error)
        +CreateUser(req) error
        +UpdateUser(req) error
        +DeleteUser(uid) error
        +GetUserInfo(uid) (AdminUser, error)
        +ListUsersWithApps() ([]AdminUser, []string, error)
        +AddAppToUser(uid, appName) error
        +RemoveAppFromUser(uid, appName) error
        +CreateApp(req) error
        +UpdateApp(req) error
        +DeleteApp(appID) error
        +GetAllApps() ([]App, error)
        +GetAllGroups() ([]AppGroup, error)
        +CreateGroup(name) error
    }

    class AnalyseService {
        +Rep Repo
        +AddEvent(event) error
        +GetEvents() ([]Event, error)
        +ConnByDays(req) ([]DayStat, error)
        +StatsActiveUsers(from, to) ([]DayStat, error)
        +StatsByAPI(from, to) ([]APIStat, error)
        +StatsPeakHours(from, to) ([]HourStat, error)
    }

    class AdminRep {
        <<interface>>
        +IsAdmin(userID) (bool, error)
        +EmailExists(email) (bool, error)
        +CreateUser(user, hashedPassword, uid) error
        +UpdateUser(user, hashedPassword) error
        +UpdateUserWithoutPassword(user) error
        +DeleteUser(uid) error
        +FetchUserDetails(uid) (AdminUser, error)
        +FetchUsersWithApps() ([]AdminUser, []string, error)
        +AddAppPermission(uid, appName) error
        +RemoveAppPermission(uid, appName) error
        +CreateApp(app) error
        +UpdateApp(app) error
        +DeleteApp(appID) error
        +FetchAllApps() ([]App, error)
        +FetchAllGroups() ([]AppGroup, error)
        +CreateGroup(name) error
    }

    class ApplicationRepositoryInterface {
        <<interface>>
        +FetchApplicationsByUserID(userID) ([]App, error)
    }

    AuthService --> Session : crée
    AuthService --> User : authentifie
    AdminService ..|> AdminRep : utilise
    AdminService --> AdminUser : gère
    AdminService --> App : gère
    OnlineUserManager --> ConnectedUser : maintient
    AnalyseService --> Event : agrège
    User "1" --> "*" Session : possède
    AdminUser "1" --> "*" App : accède à
    App "*" --> "1" AppGroup : appartient à
```

---

## 3. Diagramme de Classes — API Python (SQLAlchemy)

```mermaid
classDiagram
    direction TB

    class User {
        +Integer id PK
        +String(36) uid UNIQUE
        +relationship code_maps
        +relationship code_maps_gen_aux
        +relationship code_journal
    }

    class UserCodeMap {
        +Integer id PK
        +Integer user_id FK
        +JSON code_map
        +relationship user
    }

    class UserCodeGenAux {
        +Integer id PK
        +Integer user_id FK
        +JSON code_map_gen_aux
        +relationship user
    }

    class UserJournal {
        +Integer id PK
        +Integer user_id FK
        +JSON journal_map
        +relationship user
    }

    class CodeUpdate {
        <<Pydantic>>
        +Optional~Dict~ comptas
        +Optional~Dict~ other
        +Optional~Dict~ journal
    }

    class CodeResponse {
        <<Pydantic>>
        +Dict comptas
        +Dict other
        +Dict journal
    }

    User "1" --> "0..*" UserCodeMap : code_maps
    User "1" --> "0..*" UserCodeGenAux : code_maps_gen_aux
    User "1" --> "0..*" UserJournal : code_journal
```

---

## 4. Diagramme de Séquence — Authentification

```mermaid
sequenceDiagram
    actor U as Utilisateur
    participant F as Frontend React
    participant B as Backend Go :8002
    participant DB as PostgreSQL

    U->>F: Saisie email + mot de passe
    F->>B: POST /sys/login {email, password}
    B->>DB: SELECT uid, email, password FROM users WHERE email = ?
    DB-->>B: Données utilisateur + hash bcrypt
    B->>B: bcrypt.CompareHashAndPassword(hash, password)

    alt Mot de passe correct
        B->>DB: INSERT INTO sessions (id, user_id, expires_at)
        DB-->>B: Session créée
        B-->>F: 200 OK + Set-Cookie: userId=sessionID (HttpOnly, Secure, SameSite=Strict)
        F->>F: Stockage cookie + redirection Dashboard
        F-->>U: Affichage Dashboard
    else Mot de passe incorrect
        B-->>F: 401 Unauthorized
        F-->>U: Message d'erreur "Identifiants incorrects"
    end

    Note over B: Goroutine nettoyage toutes les 6h
    B->>DB: DELETE FROM sessions WHERE expires_at < NOW()
```

---

## 5. Diagramme de Séquence — Conversion de Fichier EDI

```mermaid
sequenceDiagram
    actor U as Utilisateur (Comptable)
    participant F as Frontend React
    participant API as API Python :8001
    participant FS as Système de fichiers
    participant DB as PostgreSQL

    U->>F: Upload fichier(s) .txt via FileDropZone
    F->>API: POST /api/conversion (multipart/form-data + cookie userId)

    API->>API: Vérification cookie userId
    API->>DB: SELECT * FROM users WHERE uid = ?
    DB-->>API: Utilisateur trouvé

    API->>FS: Création /tmp/{uid}/uploads/ et /tmp/{uid}/downloads/
    API->>FS: Sauvegarde fichier(s) uploadé(s)

    loop Pour chaque fichier .txt
        API->>FS: Lecture fichier EDI (ISO-8859-1)
        API->>API: extract_bill_values() — parsing lignes EDI
        API->>API: get_document_type() — Facture (BGM+380) ou Avoir (BGM+381)
        API->>API: sorting_mag() — identification magasin (RFF+GN:)
        API->>DB: Récupération codes comptables utilisateur
        API->>API: format() — génération fichier Excel avec Pandas/openpyxl
        API->>FS: Export Excel dans /tmp/{uid}/downloads/
    end

    API->>API: merged_csv() — fusion des résultats
    API-->>F: 200 OK {fichier prêt, chemin téléchargement}
    F->>API: GET /api/download
    API->>FS: Lecture fichier résultat
    API-->>F: FileResponse (fichier Excel)
    F-->>U: Téléchargement automatique

    Note over API: Nettoyage automatique après 5 min
    API->>FS: Suppression /tmp/{uid}/
```

---

## 6. Diagramme de Séquence — WebSocket (Présence Temps Réel)

```mermaid
sequenceDiagram
    actor U as Utilisateur
    participant F as Frontend React
    participant WS as WebSocket Manager (Go)
    participant DB as PostgreSQL
    participant Others as Autres clients WS

    U->>F: Connexion au portail
    F->>WS: WS /ws (Upgrade HTTP → WebSocket)
    WS->>WS: OnlineUserManager.AddUser(uid, username, conn)
    WS->>DB: GetAllUsersWithActivity()
    DB-->>WS: Liste utilisateurs + lastSeen
    WS->>Others: Broadcast {type: "users_update", users: [...]}
    WS->>F: {type: "users_update", users: [...]}

    loop Toutes les 30 secondes
        WS->>F: Ping WebSocket natif
        F-->>WS: Pong
        WS->>WS: Reset ReadDeadline (60s)
    end

    loop Toutes les 30 secondes
        WS->>DB: GetAllUsersWithActivity()
        WS->>Others: Broadcast users_update
        WS->>F: Broadcast users_update
    end

    U->>F: Fermeture navigateur / déconnexion
    F--xWS: Connexion fermée
    WS->>DB: MarkUserDisconnectedWithTime(uid, lastSeen)
    WS->>WS: OnlineUserManager.RemoveUser(uid)
    WS->>Others: Broadcast {user offline}
```

---

## 7. Diagramme de Séquence — CRUD Utilisateur (Admin)

```mermaid
sequenceDiagram
    actor A as Admin
    participant F as Frontend React
    participant MW as AuthMiddleware + AdminMiddleware
    participant B as Backend Go :8002
    participant DB as PostgreSQL

    A->>F: Accès page Admin
    F->>MW: POST /sys/new-user (cookie session)
    MW->>DB: SELECT expires_at FROM sessions WHERE id = ?
    DB-->>MW: Session valide
    MW->>DB: SELECT admin FROM users u JOIN sessions s ON s.user_id = u.uid WHERE s.id = ?
    DB-->>MW: admin = true
    MW->>B: Requête transmise au handler

    A->>F: Clic "Nouvel utilisateur"
    A->>F: Remplissage formulaire (email, username, password, role)
    F->>MW: POST /sys/new-user {email, username, password, role, entreprise}
    MW->>B: Requête authentifiée + admin vérifié

    B->>B: AdminService.CreateUser()
    B->>DB: SELECT EXISTS(email)
    DB-->>B: false (email disponible)
    B->>B: bcrypt.GenerateFromPassword(password)
    B->>B: uuid.New() → génération UID
    B->>DB: INSERT INTO users (uid, email, username, password_hash, role, entreprise)
    DB-->>B: OK
    B-->>F: 201 Created

    A->>F: Attribution d'application
    F->>MW: POST /sys/add-app/{uid} {appName}
    MW->>B: Requête authentifiée + admin vérifié
    B->>DB: INSERT INTO user_applications (uid, app_name)
    DB-->>B: OK
    B-->>F: 200 OK

    F-->>A: Liste utilisateurs mise à jour
```

---

## 8. Diagramme de Déploiement

```mermaid
graph TB
    subgraph "Client"
        Browser[Navigateur Web<br/>Chrome / Firefox / Edge]
    end

    subgraph "Cluster Kubernetes K3s"
        subgraph "Ingress"
            Traefik[Traefik<br/>Reverse Proxy<br/>TLS/HTTPS]
        end

        subgraph "Frontend Pod"
            Nginx[Nginx 1.27.4-alpine<br/>Fichiers statiques React]
        end

        subgraph "Backend Pod"
            GoApp[Go Binary<br/>:8002<br/>Auth, Admin, WS, Analytics]
        end

        subgraph "API Pod"
            PyApp[Python FastAPI<br/>Uvicorn :8001<br/>Traitement fichiers]
        end

        subgraph "Stockage"
            PVC1[(PVC uploads<br/>Backend)]
            PVC2[(PVC uploads<br/>API Python)]
            PVC3[(PVC frontend<br/>Config)]
        end

        subgraph "Base de données"
            PG[(PostgreSQL<br/>Base partagée)]
        end
    end

    subgraph "CI/CD"
        GH[GitHub Actions<br/>Tests + Build + Deploy]
        Registry[Docker Registry<br/>Images locales]
    end

    Browser -->|HTTPS| Traefik
    Traefik -->|/| Nginx
    Traefik -->|/sys/*| GoApp
    Traefik -->|/api/*| PyApp

    GoApp --> PG
    PyApp --> PG
    GoApp --> PVC1
    PyApp --> PVC2
    Nginx --> PVC3

    GH -->|Build| Registry
    GH -->|kubectl rollout| Traefik

    Browser -.->|WebSocket /ws| GoApp
```

---

## 9. Diagramme d'Architecture en Couches (Backend Go)

```mermaid
---
config:
  layout: elk
---
flowchart LR
 subgraph subGraph0["Authentification & Profil"]
        UC1["Se connecter"]
        UC2["Se déconnecter"]
  end
 subgraph subGraph1["Administration (Droits Admin)"]
        UC4["Créer/Gérer Utilisateurs"]
        UC8["Assigner un Rôle unique"]
        UC10["Gérer les Applications"]
        UC33["Voir les utilisateurs en lignes"]
  end
 subgraph subGraph2["Espace Comptable"]
        UC15["Outils EDI -> Xlsx"]
        UC21["Codes comptables"]
  end
 subgraph subGraph3["Espace Auditeur"]
        UC18["Détecter les doublons"]
        UC20["Traiter le FEC"]
  end
 subgraph subGraph4["Espace RH"]
        UC30["Gestion avec Silae"]
  end
 subgraph subGraph5["Espace Client"]
        UC13["Logiciel Client 1"]
        UC32["Logiciel Client 2"]
  end
 subgraph subGraph6["Infra"]
        subGraph0
        subGraph1
        subGraph2
        subGraph3
        subGraph4
        subGraph5
  end
    Comptable(("Comptable")) -. est un .-> Utilisateur(("Utilisateur"))
    Auditeur(("Auditeur")) -. est un .-> Utilisateur
    RH(("RH")) -. est un .-> Utilisateur
    Client(("Client")) -. est un .-> Utilisateur
    Admin(("Administrateur")) -. est un .-> Utilisateur
    Admin -- Assigne Rôle --> Utilisateur
    Utilisateur --> UC1 & UC2
    Admin --> UC4 & UC8 & UC10 & UC33
    Comptable --> UC15 & UC21
    Auditeur --> UC18 & UC20
    RH --> UC30
    Client --> UC13 & UC32
```

---

## 10. Diagramme Entité-Relation (MCD)

```mermaid
erDiagram
    UTILISATEUR {
        string uid PK
        string email UK
        string password_hash
        string username
        string role
        boolean admin
        string entreprise
        timestamp last_seen
    }

    SESSION {
        uuid id PK
        string user_id FK
        timestamp created_at
        timestamp expires_at
    }

    APPLICATION {
        serial id PK
        string name
        string base_url
        string icon_path
        string groups
    }

    UTILISATEUR_APPLICATION {
        string uid FK
        string app_name FK
    }

    EVENEMENT {
        serial id PK
        string uid FK
        string api_name
        string conn_time
        string deco_time
        string day
        timestamp created_at
    }

    GROUPE {
        serial id PK
        string name
    }

    CONFIG_MCDO {
        serial id PK
        string nom_config UK
        jsonb config
    }

    CODE_COMPTABLE {
        serial id PK
        integer user_id FK
        jsonb code_map
    }

    CODE_GEN_AUX {
        serial id PK
        integer user_id FK
        jsonb code_map_gen_aux
    }

    CODE_JOURNAL {
        serial id PK
        integer user_id FK
        jsonb journal_map
    }

    UTILISATEUR ||--o{ SESSION : "possède"
    UTILISATEUR ||--o{ UTILISATEUR_APPLICATION : "accède à"
    APPLICATION ||--o{ UTILISATEUR_APPLICATION : "attribuée à"
    UTILISATEUR ||--o{ EVENEMENT : "génère"
    UTILISATEUR ||--o{ CODE_COMPTABLE : "configure"
    UTILISATEUR ||--o{ CODE_GEN_AUX : "configure"
    UTILISATEUR ||--o{ CODE_JOURNAL : "configure"
    APPLICATION }o--|| GROUPE : "appartient à"
```

---

## 11. Diagramme de Composants — Frontend React

```mermaid
graph TB
    subgraph "App.jsx (Router Principal)"
        Router[BrowserRouter]
        CP[ConfigProvider<br/>Chargement config.yaml]
        MP[MicroserviceProvider<br/>requestService, getServiceUrl]
        TP[ThemeProvider<br/>Dark/Light mode]
    end

    subgraph "Pages Publiques"
        Home[Home.jsx<br/>Page d'accueil]
        Login[Login.jsx<br/>Formulaire connexion]
    end

    subgraph "Pages Protégées - Admin"
        Admin[Admin.jsx<br/>Dashboard admin]
        UserList[UserList.jsx<br/>Gestion utilisateurs]
        Apps[Applications.jsx<br/>Catalogue apps]
        Analytics[Analytics.jsx<br/>Statistiques Recharts]
    end

    subgraph "Pages Protégées - Outils Métier (22 pages)"
        Convert[Convert<br/>EDI → Excel]
        Merge[MergeExcel / MergeTxt<br/>Fusion fichiers]
        Silae[Silae × 3 variantes<br/>Traitement paie]
        Audit[AuditDoublons<br/>AuditTvaBq<br/>AuditHelper]
        FEC[FEC / FecAvecCompte<br/>Écritures comptables]
        Other[GrandLivre, TrieurPaie<br/>ComparateurStock, Ares<br/>Presta, PnlRenaud...]
    end

    subgraph "Hooks Personnalisés"
        useWS[useWebSocket<br/>Présence utilisateur]
        useAWS[useAdvancedWebSocket<br/>Rooms]
        useAna[useAnalytics<br/>Tracking événements]
        useScroll[useScrollPosition<br/>Position défilement]
    end

    subgraph "Services (Couche API)"
        SApp[Application.jsx<br/>CRUD applications]
        SUser[UsersPanel.jsx<br/>CRUD utilisateurs]
        SNews[Newsupdates.jsx<br/>Actualités]
    end

    Router --> CP --> MP --> TP
    TP --> Home
    TP --> Login
    TP --> Admin

    Admin --> UserList
    Admin --> Apps
    Admin --> Analytics

    Analytics --> useAna
    Admin --> useWS
    UserList --> SUser
    Apps --> SApp

    Convert --> MP
    Merge --> MP
    Silae --> MP
    Audit --> MP
    FEC --> MP
```

# Fiche de révision — Soutenance TP CDA

**Candidat :** Bénard Gwendal — Zone01 Normandie / Cabinet Martini
**Projet :** Mise en place d'une plateforme pour les collaborateurs et clients permettant de regrouper les différents outils développés
**Source de vérité :** `Fichier Final/A Envoyer/Certif corrigé.docx` — c'est la version remise au jury. Tout ce qui suit est calé dessus.
**Calé sur l'exposé :** `doc/SCRIPT_ORAL_CDA.md`. Les questions de cette fiche suivent ce que tu **dis** à l'oral, et surtout ce que tu **ne dis plus** — les blocs allégés du script (modélisation, tests, WebSocket) sont précisément ceux où le jury viendra creuser.

> **Mode d'emploi.** Parties 1 à 4 = les notions à savoir redire sans hésiter. Partie 5 = **175 questions d'entraînement** en 11 blocs, à faire à froid. Partie 6 = le corrigé. **Partie 7 = 30 questions réellement posées en oral blanc, chacune suivie immédiatement de sa réponse rédigée** — c'est la partie à relire en boucle, pas à passer en interrogation.
> **Les deux blocs les plus rentables** : le **bloc 11**, qui ne contient que des questions déclenchées par une phrase que tu prononces toi-même pendant l'exposé ; et le **bloc 13** (partie 7), qui reprend les arbitrages de ton projet tels qu'un jury les a réellement attaqués.
> Chaque notion est donnée en deux temps : **la définition générale** que le jury vérifie, puis **ta réponse projet** avec le vocabulaire exact du dossier remis.
> Le jury n'a pas accès au code : le dossier fait foi. Tout ce que tu dis doit être cohérent avec lui.

---

## Partie 1 — L'épreuve

### Déroulé type

| Phase | Durée indicative | Ce qui est évalué |
|---|---|---|
| Présentation du projet (exposé) | ~40 min *(ton script est calé sur **46 min**, avec un guide de coupe à **35 min** en fin de `SCRIPT_ORAL_CDA.md`)* | Clarté, structure, capacité à expliquer des choix |
| Questions du jury sur le projet | ~25 min | Profondeur technique réelle, honnêteté |
| Questionnement professionnel (hors projet) | ~15 min | Culture du métier, veille, posture |
| Entretien final | ~10 min | Motivation, projet professionnel |

### Les 11 compétences (REAC CDA 2023)

**AT1 — Développer une application sécurisée**
CP1 Installer et configurer son environnement de travail • CP2 Développer des interfaces utilisateur • CP3 Développer des composants métier • CP4 Contribuer à la gestion d'un projet informatique

**AT2 — Concevoir et développer une application sécurisée organisée en couches**
CP5 Analyser les besoins et maquetter • CP6 Définir l'architecture logicielle • CP7 Concevoir et mettre en place une base de données relationnelle • CP8 Développer des composants d'accès aux données **SQL et NoSQL**

**AT3 — Préparer le déploiement d'une application sécurisée**
CP9 Préparer et exécuter les plans de tests • CP10 Préparer et exécuter le déploiement • CP11 Gérer les versions

> *L'ordre exact des CP varie selon la version du REAC — vérifie sur `doc/Rfrentiel_Activits_Comptences_Evaluation_TP_CDA_(6).pdf`.*

**Où c'est traité dans ton dossier** (les chapitres du docx n'étant pas numérotés, retiens les intitulés) :

| Compétence | Chapitre du dossier remis |
|---|---|
| Environnement de travail | *Choix des technologies* → « Outils de développement » |
| Interfaces utilisateur | *Conception* → « Maquettes et Wireframes », « Principes UX et accessibilité (RGAA) » + *Réalisation* |
| Composants métier | *Conception* → « Diagrammes de classe UML » + *Réalisation* |
| Persistance / BDD relationnelle | *Conception* → « Modélisation des données » (Dictionnaire, MCD, MLD, MPD, Justifications) |
| Architecture multicouche | *Architecture technique* → « Architecture Globale », « Documentation des API » |
| Gestion de projet | *Organisation du projet* (Méthodologie, Planning et sprints, Outils, Commits, Branching) |
| Sécurité | *Sécurité* (les 10 sous-chapitres) |
| Accès aux données SQL/NoSQL | *Architecture Backend/API* + « Justifications de conception » → **« Choix SQL vs NoSQL »** |
| Plans de tests | *Tests* (les 10 sous-chapitres) |
| Déploiement | *Déploiement* (Docker, K8s, CI/CD, environnements, step-by-step, rollback, SemVer) |
| Versions | « Stratégie de branching Git » + « Versioning sémantique » |

---

## Partie 2 — Les notions à connaître

### A. Contexte & gestion de projet

**Cycle de vie d'un projet.** Expression du besoin → cahier des charges → conception → développement → tests → déploiement → maintenance.

**Cycle en V vs agile.**
- *Cycle en V* : spécifications figées en amont, chaque phase de conception a sa phase de test miroir. Adapté quand le besoin est stable et contractuel.
- *Agile* : itérations courtes, feedback continu, backlog priorisé. **Scrum** = rôles (PO, SM, équipe) + sprints + cérémonies. **Kanban** = flux tiré, colonnes à faire / en cours / fait, limitation du travail en cours (WIP).

> **Ta réponse projet :** projet conduit **seul, 3 jours par semaine, sur environ six mois**. J'ai retenu une **démarche itérative et incrémentale suivie en Kanban**, et pas Scrum — dont les rôles et les cérémonies (daily standup, sprint review) supposent une équipe et se vident de leur sens pour une personne seule. « La méthode doit servir le contexte, pas l'inverse. »

**Les cinq points de ta méthodologie**, à savoir citer :
1. **Backlog priorisé** — les user stories constituent le backlog ; à chaque session je tirais la tâche la plus prioritaire (flux tiré, sans timebox artificiel, ce qui absorbe un rythme à temps partiel).
2. **Kanban sur carnet de bord papier** — tâches listées par itération, tâche en cours marquée, terminées rayées, reports recopiés d'une session à l'autre ; relu en début de session pour recharger le contexte.
3. **WIP = 1** — une seule tâche de développement ouverte à la fois, pour ne jamais laisser de chantier à moitié terminé entre deux sessions espacées.
4. **Itérations jalonnées** — six itérations, chacune se concluant par une démonstration au commanditaire et une courte rétrospective personnelle notée dans le carnet.
5. **Définition de « terminé »** — une tâche n'est rayée que si le code est écrit, testé, passé au lint et commité selon les conventions.

⚠️ **Piège de vocabulaire :** le chapitre s'intitule « **Planning et sprints** » dans le dossier remis, mais son contenu est bien du Kanban et des itérations. Si le jury relève le mot « sprints », réponds : *« c'est un abus de langage dans le titre — le corps du chapitre décrit six itérations jalonnées, sans timebox ni cérémonie Scrum, et je viens de vous expliquer pourquoi Scrum n'avait pas de sens seul. »* **Ne dis jamais « sprint », « daily », « rétro d'équipe ».**

**Tes 6 itérations — objectif, livrable, difficulté, enseignement.** Le dossier documente chacune sur ce modèle : c'est ta meilleure réserve d'anecdotes techniques.

| # | Itération | Difficulté rencontrée | Ce que j'en ai tiré |
|---|---|---|---|
| 1 | Tirages de caisse, version autonome (17 j) | Encodages variables des fichiers EDI réels (ISO-8859-1 vs UTF-8) et segments optionnels → rendre le parsing tolérant sans masquer les vraies erreurs | Confronter le code à de vrais jeux de données anonymisés fait émerger des bugs qu'on n'anticipe pas sur le papier |
| 2 | Retours collaborateurs + fondations plateforme (17 j) | J'ai tenté de partager des structures de données entre Go et Python avant de constater que le couplage n'en valait pas la peine → contrat d'API JSON explicite | Investir tôt dans l'outillage (lint + format auto) évite l'accumulation de dette ; livrer l'outil avant la plateforme était le bon ordre |
| 3 | Administration + intégration au portail (13 j) | **J'avais d'abord implémenté la vérification du rôle admin côté frontend uniquement — c'était une faille de contrôle d'accès (A01 OWASP).** Déplacée côté serveur dans un middleware dédié | « Ne jamais faire confiance au client » est passé de slogan à réflexe |
| 4 | Temps réel et analytics (10 j) | Data races sur la map des utilisateurs connectés, détectées par `go test -race` ; la résolution par `sync.RWMutex` a demandé plusieurs itérations pour éviter les interblocages au broadcast | La concurrence ne se teste pas à l'œil — l'outil `-race` a été décisif |
| 5 | Déploiement et sécurisation du VPS (11 j) | Un typo dans la configuration CORS de préproduction bloquait toutes les requêtes authentifiées | Lire méthodiquement les erreurs CORS du navigateur plutôt que modifier la config au hasard ; et traiter la sécurité en fin de projet est un anti-pattern → *security by design* |
| 6 | Finalisation (20 j) | L'incompatibilité psycopg2 / Python 3.14 cassait toute la suite de tests Python → mock au niveau `sys.modules` + bascule SQLite in-memory | Documenter au fil de l'eau aurait été plus efficace que tout rédiger à la fin |

**Séquencement du projet** (à savoir résumer en trois temps) : d'abord le logiciel de tirages de caisse, priorité explicite des collaborateurs, livré en autonome pour apporter de la valeur au plus vite ; ensuite la plateforme, développée en parallèle des retours sur l'outil ; enfin le déploiement (provisioning du VPS vierge, reverse proxy, sécurisation).

**Outils de gestion :** carnet de bord papier (Kanban), GitHub (versioning, branches, PR), GitHub Actions (CI/CD), **Figma** (maquettage). Le carnet papier est un choix délibéré : pour une personne seule, il élimine tout coût d'outillage — l'essentiel étant la discipline de mise à jour, pas l'outil.

**Règles de gestion (RG01–RG09)** — les règles métier, indépendantes de la technique :

| ID | Règle |
|---|---|
| RG01 | Un email identifie de façon unique un utilisateur |
| RG02 | Un mot de passe n'est jamais stocké ni journalisé en clair (hash bcrypt seul) |
| RG03 | Une session expire 24 h après sa création (fenêtre glissante) |
| RG04 | Un utilisateur ne voit que les applications qui lui sont explicitement attribuées |
| RG05 | Seul un Admin crée/modifie/supprime un utilisateur ou une application |
| RG06 | La suppression d'un utilisateur cascade sur sessions, attributions, mappings (droit à l'oubli) |
| RG07 | Les événements d'audit survivent à la suppression du compte |
| RG08 | Les fichiers déposés sont éphémères : supprimés au plus tard 5 min après traitement |
| RG09 | Toute action administrative sensible génère un événement journalisé |

**Git — versioning (CP11).**

- **Conventional Commits** : `<type>(<scope>): <description>`. Types utilisés : `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`, **`security`**.
  Bénéfices revendiqués : historique lisible et filtrable (`git log --grep="^feat"`), détection automatique du type de release (`feat` → MINOR, `fix` → PATCH, `BREAKING CHANGE` → MAJOR), facilité d'onboarding.
- **Stratégie de branching : GitHub Flow.** Une seule branche permanente, `main`, toujours déployable. Toute modification passe par une branche éphémère. **Pull request même en solo**, pour bénéficier de la CI. **Squash & merge** pour garder un historique linéaire. Tags `vMAJOR.MINOR.PATCH` sur `main` à chaque release.
  Préfixes : `feature/` (ex. `feature/admin-dashboard`), `fix/` (`fix/cors-typo`), `chore/` (`chore/upgrade-go-1.24`), `docs/` (`docs/owasp-top10`).
  Cycle : `git checkout -b feature/xxx` depuis `main` à jour → commits conventionnels → push + PR → CI obligatoire (tests + lint) → squash & merge → suppression de la branche.
  **Justification** : GitHub Flow simplifie par rapport à Git Flow (`develop`, `release/*`, `hotfix/*`), cohérent avec une équipe d'un seul développeur, un déploiement continu vers preprod après chaque merge, et l'absence de version LTS à maintenir en parallèle.
- **SemVer** : MAJOR = rupture de compatibilité, MINOR = ajout rétrocompatible, PATCH = correctif. Tag annoté par release.
- Vocabulaire à maîtriser : `merge` vs `rebase`, `squash`, `cherry-pick`, conflit, `revert` (nouveau commit, sûr sur branche partagée) vs `reset` (réécrit l'historique, local seulement).

---

### B. Conception & modélisation

**UML — les diagrammes à savoir lire ET justifier :**

| Diagramme | À quoi il sert | Dans le dossier |
|---|---|---|
| **Cas d'utilisation** | Vue fonctionnelle : acteurs × fonctionnalités. Relations `include` (obligatoire), `extend` (optionnel), généralisation d'acteurs | *Conception* → « Diagramme de cas d'utilisation » |
| **Séquence** | Chronologie des messages. Lignes de vie, messages synchrones/asynchrones, fragments `alt`/`loop` | 3 diagrammes : authentification, conversion EDI, WebSocket |
| **Classes** | Vue statique : classes, attributs, méthodes, visibilités (`+` public, `-` privé, `#` protégé), associations, cardinalités, héritage, composition/agrégation | « Diagrammes de classe UML » |
| **Déploiement** | Répartition physique des artefacts sur les nœuds | « Infrastructure de déploiement » |

> **Ton diagramme de classes a une particularité à savoir expliquer :** il illustre la **couche métier du backend Go suivant Clean Architecture**. On y lit les trois couches — Handler ; Service (`AuthService`, `AdminService`, `AnalyseService`, `OnlineUserManager`) ; Repository (`AdminRep`, `ApplicationRepositoryInterface`, `SessionRepository`, `UserRepository`). **Les interfaces sont la clé du découplage** : `AdminService` dépend de l'interface `AdminRep`, pas d'une implémentation. En production, l'implémentation est une struct branchée sur PostgreSQL ; en test, un mock retourne des valeurs déterministes sans I/O.

**Merise — la chaîne MCD → MLD → MPD :**
- **MCD** (conceptuel) : entités, propriétés, associations avec **cardinalités** (0,1 / 1,1 / 0,n / 1,n). Indépendant de tout SGBD.
- **MLD** (logique) : traduction en relations. Une association 1,n → la clé étrangère passe du côté « n » ; une association n,n → **table de jonction**.
- **MPD** (physique) : le SQL réel, avec types, contraintes, index, `ON DELETE`.

**Normalisation :** **1NF** atomicité (pas d'attribut multivalué) • **2NF** 1NF + aucune dépendance **partielle** sur une partie de la clé • **3NF** 2NF + aucune dépendance **transitive** entre attributs non-clé. (Bonus : BCNF, et la **dénormalisation** assumée.)

> **Ta réponse projet — les trois arguments du dossier :**
> **1NF** — aucun attribut multivalué scalaire. Les mappings comptables (`user_code_maps.code_map`, `user_code_maps_gen_aux.code_map_gen_aux`, `code_journal.journal_map`) et la configuration McDonald's (`fascicule_mcdo.config`) sont en `JSON` **parce qu'ils représentent des structures opaques pour la base — elle n'a ni à les indexer ni à les joindre.**
> **2NF** — pas de dépendance partielle : `user_application_permissions` porte une clé de substitution `id` et une contrainte `UNIQUE(user_id, application_id)` ; son seul attribut propre, `can_access`, dépend bien du couple complet.
> **3NF** — pas de dépendance transitive entre attributs non-clé.

**Les tables à savoir citer :** `users` (`id SERIAL` + `uid TEXT UNIQUE`, email, username, password bcrypt, admin, role, entreprise, last_seen) • `sessions` (le jeton en PK) • `application_groups` • `applications` • `user_application_permissions` (**jonction N:N**) • `events` (analytics) • `user_code_maps` / `user_code_maps_gen_aux` / `code_journal` (JSON) • `fascicule_mcdo`.

**Index** — uniquement les index implicites des contraintes PK/UNIQUE, et le dossier justifie chacun :

| Table | Index implicite | Justification |
|---|---|---|
| `users` | UNIQUE(`uid`), UNIQUE(`email`), UNIQUE(`username`) | Lookup à chaque login / résolution de FK (chemin chaud) |
| `sessions` | PK(`id`) | Lookup du jeton à chaque requête authentifiée |
| `application_groups` | UNIQUE(`name`) | Résolution du libellé de groupe |
| `user_application_permissions` | UNIQUE(`user_id`,`application_id`) | Un seul droit par couple |

Pas d'index secondaire sur les colonnes JSON — aucune requête ne projette sur leur contenu. Index ciblés (p. ex. sur `events`) documentés comme **évolution conditionnelle**.

**Contraintes référentielles :** `ON DELETE CASCADE` sur `user_code_maps.user_id`, `user_code_maps_gen_aux.user_id`, `code_journal.user_id` (vers `users(id)`) → le droit à l'oubli RGPD nettoie les mappings **sans intervention applicative**. FK sur `sessions.user_id` et `user_application_permissions.user_id` vers `users(uid)`, et sur `user_application_permissions.application_id` vers `applications(id)`. `applications.groups` est une **référence faible** (TEXT libre, sans FK) : dénormalisation assumée.

**Choix de types :** `id SERIAL` (clé de substitution, sert les FK Python) **+** `uid TEXT UNIQUE` (identifiant métier stable généré côté Go, référencé par les FK Go) • `sessions.id TEXT` : le jeton fait office de PK, pas de colonne `token` séparée • `JSON` pour les structures opaques • `TIMESTAMP` sans fuseau pour le hub, `TIMESTAMPTZ` pour `events.created_at`, valeurs en UTC.

**Migrations :** schéma initialisé par `InitSchema` (`backend/internal/db/postgres.go`), complété par des migrations SQL **idempotentes** — `001_fix_anomalies.sql` (intégrité et nommage), et `003_alignement_conceptuel.sql` qui porte en base deux règles métier jusque-là garanties par l'application : `UNIQUE(user_id)` sur les trois tables de mapping, et une vraie clé étrangère `applications.groups → application_groups(name)` en `ON UPDATE CASCADE`. Un outil de migration (golang-migrate ou Alembic) est documenté comme amélioration, **conditionnée** à des évolutions de schéma post-production.

**Maquettage / UX.** Wireframe (structure) → maquette (charte) → prototype (cliquable). Maquetté sous **Figma**. Principes : cohérence, feedback immédiat, prévention de l'erreur, responsive. **RGAA 4** = déclinaison française des **WCAG 2.1** : contraste ≥ 4.5:1, navigation clavier, `alt`, labels de formulaire, hiérarchie de titres, rôles ARIA.

---

### C. Technologies — savoir justifier chaque choix

| Couche | Choix | Justification | Alternatives écartées |
|---|---|---|---|
| Frontend | **React 19 + Vite + Tailwind** | Écosystème mature, réutilisabilité par composants ; Vite pour le HMR instantané (ESBuild) ; Tailwind pour l'absence de CSS mort en prod | Vue 3, Angular 17, CRA (déprécié), Bootstrap/MUI |
| Backend | **Go** | Binaire unique sans runtime, typage statique fort, **goroutines** natives, latence stable sous charge | Node.js (typage dynamique), Java Spring (JVM lourde) |
| API traitement | **Python + FastAPI** | pandas / xlsxwriter sans rival sur la donnée tabulaire, ASGI async, validation Pydantic, **OpenAPI auto-généré** | Tout faire en Go — **les bibliothèques Go n'étant pas assez matures pour certains cas complexes de traitement** |
| BDD | **PostgreSQL** | JSON/JSONB natif, extensions riches, intégrité référentielle | MySQL (JSON limité), MongoDB (pas d'intégrité référentielle) |
| Infra | **Docker + K3s + Traefik** | Reproductibilité, rolling updates, auto-healing ; Traefik = ingress natif K8s avec Let's Encrypt intégré | — |

**Patterns frontend revendiqués** (à citer tels quels) : **Lazy Loading** (`React.lazy()` + `Suspense` pour le code splitting) • **Context Pattern** (`ConfigContext`, `MicroservicesContext`, `ThemeContext`) • **Service Layer** (abstraction Axios des appels API) • **Protected Routes** (vérification avant accès aux pages protégées).

**Concepts langage à réviser :**
- **Go** : goroutine, channel, `sync.Mutex` / `sync.RWMutex`, `defer`, interfaces implicites, `go test -race`, erreurs en valeurs de retour.
- **React** : props vs state, `useState` / `useEffect` / `useContext` / `useMemo`, hook personnalisé, Virtual DOM et réconciliation, code splitting.
- **Python/FastAPI** : ASGI vs WSGI, `async`/`await`, Pydantic, injection de dépendances, SQLAlchemy ORM.

---

### D. Architecture

**Application multicouche répartie** = couches réparties sur des processus/machines distincts communiquant par le réseau : SPA React (Nginx) ↔ backend Go ↔ API Python ↔ PostgreSQL, derrière Traefik.

**Flux de communication** (les cinq du dossier) : Frontend → Go (auth, utilisateurs, WebSocket, analytics) • Frontend → Python (fichiers, codes comptables) • Go → PostgreSQL • Python → PostgreSQL • WebSocket bidirectionnel pour la présence.

**Clean Architecture côté Go :**
```
Handler    : parse la requête HTTP, valide les entrées, retourne la réponse
Service    : logique métier, indépendant du transport HTTP — dépend d'INTERFACES
Repository : abstraction de l'accès à la base
Interface  : contrats pour l'injection de dépendances (ex. ApplicationRepository)
Middleware : pipeline transversal (CORS, AuthMiddleware, AdminMiddleware)
```
**Les trois besoins auxquels ça répond** (tableau du dossier) : tester sans base de données (mock d'interface) ; changer de source de données sans impacter que le Repository ; isoler les règles métier RG01–RG09 dans le Service plutôt que les éparpiller dans les handlers.

**Les 6 domaines Go**, tous sur le même triptyque `handler.go` / `service.go` / `repository.go` : `auth`, `admin`, `applications`, `analyse`, `websocket`, `Macdos`. Transverses sous `internal/db` et `internal/middleware`.

**Routage à 3 subrouters :**
- `pub` — `/sys/login`, `/sys/logout` : aucun middleware d'authentification
- `sys` — `/sys/verify-token`, `/sys/user-applications`, `/sys/analyses/*`, `/sys/*-macdos-config*` : `AuthMiddleware`
- `adm` — `/sys/get-users`, `/sys/new-user`, `/sys/delete-user/{uid}`, gestion du catalogue : `AuthMiddleware` + `AdminMiddleware`

**API Python :** logique modulaire plus plate — `routers.py` délègue à des utilitaires **purs** (`convert`, `format`, `searching`, `sort`), ce qui les rend testables sans serveur ; la couche `auth/` valide le cookie **en amont de tout traitement de fichier**.

**Documentation d'API.** FastAPI génère automatiquement une spécification **OpenAPI 3.0** depuis les annotations (Pydantic + type hints) et expose **Swagger UI sur `/docs`** et **ReDoc sur `/redoc`**, régénérée à chaque démarrage : *la source unique de vérité est le code*, aucune dérive possible entre code et doc. L'API Go est documentée **manuellement**.

**REST :** ressources nommées par des noms, verbes HTTP (`GET` sûr et idempotent, `POST` non idempotent, `PUT`/`DELETE` idempotents), codes (200, 201, 204, 400, **401 non authentifié**, **403 authentifié mais non autorisé**, 404, 409, 429, 500), **stateless**.

**WebSocket :** full-duplex sur une connexion TCP persistante obtenue par **upgrade** d'une requête HTTP (`Connection: Upgrade`, `Sec-WebSocket-Key`, réponse `101 Switching Protocols`). À opposer au *polling* et au *SSE* (unidirectionnel).

> **Ton implémentation :** un `OnlineUserManager` = `map[string]*ConnectedUser` protégée par un **`sync.RWMutex`** (`RLock` pour les broadcasts fréquents, `Lock` exclusif pour add/remove). Sans verrou, l'accès concurrent à une map Go provoque une **data race** — comportement indéfini. Détectée par `go test -race`. Heartbeat `ListenPings` pour purger les connexions mortes.

---

### E. Sécurité — la partie la plus questionnée

**OWASP Top 10 — le tableau du dossier**, avec les statuts exacts :

| # | Risque | Mesure | Statut |
|---|---|---|---|
| A01 | Broken Access Control | RBAC 6 rôles, `AuthMiddleware` + `AdminMiddleware` **côté serveur**, 3 subrouters, validation UID UUID côté Python | Implémenté |
| A02 | Cryptographic Failures | bcrypt, HTTPS via Traefik, cookies `Secure`, secrets JWT en variables d'env | Implémenté |
| A03 | Injection | **Requêtes paramétrées** (Go `sql`, SQLAlchemy), regex UUID, `filepath.Base()` | Implémenté |
| A04 | Insecure Design | Architecture en couches, séparation des responsabilités | Implémenté |
| A05 | Security Misconfiguration | CORS avec **allowlist** (WebSocket inclus), suppression du CORS en dur | Implémenté |
| A06 | Vulnerable Components | Dépendances à jour, images officielles | **À vérifier** |
| A07 | Auth Failures | Sessions avec expiration vérifiée en BDD, nettoyage automatique, cookies SameSite | Implémenté |
| A08 | Software Integrity Failures | CI/CD avec tests, Docker multi-stage | Implémenté |
| A09 | Logging & Monitoring | Logging détaillé, analytics des accès | **À renforcer** |
| A10 | SSRF | Pas de requêtes externes dynamiques basées sur l'input utilisateur | *(noté « non implémenté » dans le dossier — voir partie 4)* |

**Authentification — session opaque vs JWT.**
- *JWT* : auto-porteur, signé, stateless, scalable, mais **non révocable** avant expiration.
- *Session serveur* : jeton opaque en base, **révocable immédiatement**, coût = un lookup par requête.

> **Ton choix, tel que le dossier le formule :** « Sessions en base de données : tokens UUID stockés côté serveur, **pas de JWT côté client**. » Justification : la révocabilité primait, et à l'échelle de quelques dizaines d'utilisateurs internes le lookup est indolore.

**Les mesures d'authentification listées dans le dossier** — à connaître dans l'ordre :
bcrypt coût par défaut (10 rounds) • sessions UUID en base, pas de JWT côté client • **cookies `HttpOnly`, `Secure`, `SameSite=Strict`** • expiration automatique • **goroutine de purge toutes les 6 h** • `AuthMiddleware` vérifie présence et validité du cookie **en base** (expiration côté serveur) • `AdminMiddleware` vérifie le flag `admin` en base • secrets JWT de l'API Python externalisés (`JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY`) avec **vérification au démarrage**.

**Améliorations prévues (dossier) :** rate limiting sur les endpoints d'authentification • logging des tentatives de connexion échouées • politique de mot de passe renforcée (complexité, longueur minimale).

> ### ⚠️ Écarts entre le dossier remis et le code réel
> À connaître **pour toi**, pas à réciter. Le dossier fait foi devant le jury, mais si une question va au détail de l'implémentation, tu dois savoir où tu marches :
> - **Cookies.** Le dossier annonce un cookie de session `HttpOnly`, `Secure`, `SameSite=Strict`. Le code (`backend/internal/services/auth/handler/handler.go`) pose en réalité **deux** cookies, `sessionId` et `userId`, en `SameSite=Lax`, `Secure` **conditionnel** (activé seulement si `CORS_ORIGIN` commence par `https://`), **sans `HttpOnly`**, et host-only en dev.
> - **WebSocket.** Le tableau STRIDE annonce « `AuthMiddleware` requis avant l'upgrade ». Le code monte `/ws` à la racine du routeur avec **seulement** `CheckOrigin` (allowlist d'origines) — pas d'`AuthMiddleware`.
> - **Route WebSocket.** Le dossier écrit `sys/ws` ; la route réelle est `/ws`.
> - **Healthcheck.** Le dossier cite `http://localhost:8002/sys/health` ; la route réelle est `/health`.
> - **`/sys/register`.** Le tableau de rate limiting prévoit une limite sur cet endpoint, et le chapitre Authentification dit « l'utilisateur doit pouvoir s'inscrire » — **l'inscription n'existe pas dans l'application** (seul un Admin crée les comptes, RG05).
> - **Le domaine de production est absent de l'allowlist WebSocket.** La capture d'annexe montre le vrai code : `allowedOrigins` contient `https://preprod.azert.fr`, `http://localhost:3000` et `http://127.0.0.1:3000` — **pas `logiciel.cabinet-martini.fr`**. Comme `CheckOrigin` retourne `allowedOrigins[origin]`, une clé absente vaut `false` : le handshake est refusé depuis la production, et la liste étant **en dur**, aucune variable d'environnement ne peut le corriger — contrairement au CORS HTTP, lui configurable par `CORS_ORIGIN` (`backend/internal/middleware/cors.go`).
>   Ce n'est **pas une erreur du dossier** : le corps du texte ne nomme aucun domaine. Mais l'annexe la photographie. Détection très improbable — il faudrait rapprocher cette capture du tableau Environnements situé bien plus loin.
>   **À vérifier avant l'oral :** si l'application tourne encore sur `preprod.azert.fr`, tout va bien ; sinon la présence temps réel est cassée en production, et son échec est silencieux.
>
> Si on te pousse sur l'un de ces points, la sortie honnête est : *« la version du dossier décrit la cible que j'ai spécifiée ; sur ce point précis, l'implémentation actuelle est à X et le correctif est identifié. »* Mieux vaut ça qu'une affirmation que tu ne pourrais pas défendre.
>
> ✅ **Résolu le 18/08** — la capture `CheckOrigin` du chapitre Réalisation, qui montrait une comparaison en dur avec la coquille `cabinet-matini.fr` et contredisait l'annexe, a été supprimée et remplacée par une phrase renvoyant à l'annexe. Le dossier est désormais cohérent sur ce point.

**Hachage :** bcrypt = **lent par conception**, **sel intégré**, **coût paramétrable** (10 rounds ici). À opposer à MD5/SHA-1/SHA-256, rapides donc cassables en masse sur GPU. Modernes : argon2id, scrypt. *Hachage ≠ chiffrement* (sens unique).

**Les attaques à définir en une phrase + leur parade :**

| Attaque | Définition | Parade dans le dossier |
|---|---|---|
| **Injection SQL** | Injection de SQL via une entrée non échappée | Requêtes paramétrées (Go `sql`, SQLAlchemy) |
| **XSS** | Injection de JS exécuté chez un tiers (stocké, réfléchi, DOM) | Échappement natif de React ; **CSP en stratégie cible** |
| **CSRF** | Action authentifiée déclenchée à l'insu de l'utilisateur depuis un site tiers | `SameSite=Strict` + vérification `Origin`/`Referer` sur les requêtes non-GET |
| **Path traversal** | `../../etc/passwd` pour sortir du répertoire prévu | Regex UUID stricte avant construction de chemin (Python), `filepath.Base()` (Go) |
| **CSWSH** | Cross-Site WebSocket Hijacking : un site tiers ouvre une WS avec le cookie de la victime | Liste blanche d'origines (`allowedOrigins`) **évaluée à chaque tentative d'upgrade** — origine absente, handshake refusé |
| **Brute force** | Essai massif de mots de passe | bcrypt lent + rate limiting token bucket |
| **Énumération de comptes** | Deviner les emails valides via des erreurs différenciées | **Message d'erreur générique unique** |
| **Clickjacking** | Superposition invisible en iframe | `X-Frame-Options: DENY` |

**Protection CSRF — les deux mécanismes du dossier :** (1) `SameSite=Strict` sur le cookie de session — le navigateur n'envoie pas le cookie sur une requête initiée depuis un site tiers ; (2) vérification `Origin`/`Referer` côté serveur sur les requêtes non-GET, contre la liste blanche CORS (`https://logiciel.cabinet-martini.fr`, `http://localhost:3000` en dev). Un middleware à jeton CSRF synchronisé (double-submit cookie) reste une évolution possible.

**Headers HTTP de sécurité — stratégie cible** (« middleware Go à enrichir », donc **pas encore tous déployés**) :

| Header | Valeur | Rôle |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Force HTTPS 1 an |
| `X-Frame-Options` | `DENY` | Anti-clickjacking |
| `X-Content-Type-Options` | `nosniff` | Désactive le MIME-sniffing |
| `Content-Security-Policy` | `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:` | Anti-XSS |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limite la fuite d'URL |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=()` | Désactive les API sensibles |

Revue prévue avec **securityheaders.com** avant mise en production.

**Rate limiting — token bucket par IP** (capacité fixe, regénération à taux constant : tolère les bursts courts tout en limitant le taux soutenu) :

| Endpoint | Capacité | Regénération |
|---|---|---|
| `POST /sys/login` | 5 requêtes | 1 / 30 s |
| `POST /sys/register` | 3 requêtes | 1 / 60 s |
| Autres endpoints | 60 requêtes | 1 / s |

Implémentation : middleware Go sur `golang.org/x/time/rate` ou `github.com/didip/tollbooth`. Client identifié par IP source (`X-Forwarded-For` lu depuis Traefik). Réponse **429** + header **`Retry-After`** + logging. **Évolutions :** limitation par utilisateur authentifié ; **bucket dans Redis** pour le multi-instance — actuellement en mémoire, « OK en scaling vertical, KO en horizontal ».

**RBAC — 6 rôles** (tableau du dossier) :

| Rôle | Accès admin | Applications métier |
|---|---|---|
| Admin | Complet | Toutes |
| Dev | À la demande | Toutes |
| Comptable | À la demande | Comptabilité |
| Social | À la demande | Paie / Social |
| Auditeur | À la demande | Audit |
| Client | À la demande | Attribuées |

Vérification à **3 niveaux** (défense en profondeur) : frontend (`AuthenticationWrapper`, `AdminRoute` — **confort d'affichage, jamais une sécurité**) ; backend Go (pipeline de middlewares Gorilla Mux sur les subrouters `sys` et `adm` — **la vraie barrière**) ; API Python (validation UUID + vérification de l'existence de l'utilisateur en base avant tout traitement de fichier).

**STRIDE** (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) — appliqué à trois surfaces :

- **`/sys/login`** — *Spoofing* : bruteforce → bcrypt lent + token bucket 5/30 s. *Information disclosure* : énumération de comptes → message générique unique. *Tampering* : vol/forge du cookie → `HttpOnly` (anti-XSS), `Secure`, `SameSite=Strict`, session validée en base à chaque requête. *DoS* : saturation de bcrypt → 429 rapide **avant tout calcul bcrypt**.
- **`/api/conversion`** — *Tampering/Info disclosure* : path traversal via `userId` forgé → regex UUID **avant** toute construction de chemin, `os.path.join` sur identifiant validé. *Elevation of privilege* : nom de fichier piégé → `filepath.Base()`. *DoS* : upload massif → fichiers isolés par UID + nettoyage à +5 min (RG08). *Repudiation* → journalisation horodatée.
- **WebSocket** — *Spoofing (CSWSH)* → validation `Origin` contre allowlist. *DoS* : connexions zombies → `AuthMiddleware` avant l'upgrade + heartbeat `ListenPings`.

**RGPD :** minimisation (email, nom, rôle) • chiffrement (bcrypt coût 10 + HTTPS Traefik) • **droit à l'oubli** (suppression atomique en transaction — `DeleteUser` efface droits, sessions et mappings avant le compte — doublée d'un `ON DELETE CASCADE` en base sur `events` et les trois tables de mapping ; voir corrigé 157) • limitation de conservation (sessions purgées à 6 h, fichiers temp à 5 min) • traçabilité (logging connexions/déconnexions, événements d'utilisation) • consentement (intranet réservé aux employés authentifiés, **pas de cookies tiers**). **Améliorations prévues :** registre des traitements, politique de confidentialité interne, procédure d'export (droit à la portabilité).

**Logging de sécurité :** événements journalisés avec niveau et données — connexion échouée (`WARN` : email tenté, IP, user-agent, timestamp), connexion réussie (`INFO`), logout, création de compte, suppression de compte (`WARN`), changement de rôle, accès refusé RBAC, rate limit dépassé, erreur 5xx. Format **JSON structuré** (ingestion ELK / Loki / Datadog). **Jamais loggé :** mots de passe, jetons de session complets, données personnelles non nécessaires.

**Gestion des secrets :** rien en dur dans Git. `.env` gitignoré en local • **GitHub Actions secrets** en CI • **Secrets Kubernetes** montés en variables d'environnement en prod. Inventaire : `DB_PASSWORD`, `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY`, `COOKIE_SECRET`. **Fail-fast** : l'API Python refuse de démarrer sans ses clés JWT. Secrets générés par `openssl rand -hex 32` (≥ 32 caractères).

**Veille sécurité :** ANSSI / CERT-FR (hebdo), OWASP (mensuel), GitHub Security Advisories via **Dependabot** (auto), base CVE, scan de dépendances à chaque build CI.

---

### F. Tests

**Pyramide des tests :** large base d'**unitaires** (rapides, isolés) → **intégration** (plusieurs composants, vraies dépendances) → peu d'**E2E** (parcours complet, lents et fragiles mais seuls à valider le réel).

**Vocabulaire :** mock / stub / fake (le stub renvoie des valeurs figées, le mock vérifie les interactions) • couverture de code (indicateur, **pas un objectif**) • TDD (Red → Green → Refactor) • test de non-régression • cas nominal / cas limite / cas d'erreur.

> **Ton dispositif, tel que le dossier le présente :**
> - **Go** — `testify` + `sqlmock`, couvrant Auth, Admin, Applications, Analyse (**11 fichiers de tests**), plus `go test -race` sur le WebSocket ;
> - **Python** — **84 tests pytest collectés, 72 passent aujourd'hui**. Le `conftest.py` **mocke psycopg2 au niveau `sys.modules` avant tout import** et bascule sur **SQLite in-memory** : aucune base à provisionner, isolation totale ;
>   ⚠️ **Ne cite jamais « 84/84 » sans avoir relancé la suite.** Les 12 échecs sont tous des `404` dans `tests/test_routers.py` : les tests appellent `/api/...` alors que `main.py` monte le routeur sous `/api/Facture-Mb`. **C'est le test qui est en retard sur le code, pas une régression fonctionnelle** — et c'est une correction de préfixe, pas de logique. Si tu le corriges avant l'oral, tu reviens à 84/84 ; si tu ne le corriges pas, la phrase à dire est : *« 84 tests, 72 au vert ; les 12 restants échouent sur un préfixe de route obsolète dans le fichier de test, je l'ai identifié et c'est un correctif de test, pas de code. »* Le pire serait d'annoncer 84/84 et qu'on te demande de lancer la suite ;
> - **Frontend** — **29/29 tests Vitest passent** ;
> - **Intégration** — via `TestClient` / TestDB (FastAPI) ;
> - **E2E** — **Playwright**, retenu plutôt que Cypress pour le support natif multi-navigateurs (Chromium, Firefox, WebKit), un auto-waiting plus robuste (moins de tests flaky sur les états asynchrones), une API moderne `async/await`, et une exécution headless compatible CI sans serveur X. **Statut : à mettre en place — la stratégie est documentée comme livrable cible.**

**Les 8 scénarios E2E cibles**, à savoir citer : `auth-01` login valide → accès au catalogue • `auth-02` mot de passe incorrect → message d'erreur • `auth-03` logout → redirection • `admin-01` création d'un Comptable → visible dans la liste • `admin-02` changement de rôle → persistance vérifiée • `admin-03` suppression → modale de confirmation → suppression effective • `outil-01` upload → traitement → téléchargement • `rbac-01` un Comptable tente `/admin` → redirection ou 403.

**Exécution E2E en CI** (job dédié dans `.github/workflows/ci.yml`) : `docker compose up -d` → attente du healthcheck (`curl --retry 10 --retry-delay 2`) → `npx playwright test` → upload du rapport HTML en artefact en cas d'échec.

**Tests manuels :** campagne conduite **avant chaque release**, sur la base d'une matrice de parcours, avec des jeux de données EDI réels anonymisés et des cas construits pour les cas limites.

**Jeu d'essai** — le jury en demande **toujours** un déroulé complet. Prépare celui de la conversion EDI (fichier d'entrée, résultat attendu, résultat obtenu, verdict) et celui de l'authentification (bon mot de passe / mauvais / session expirée).

---

### G. Déploiement

**Docker :** image (modèle immuable) vs conteneur (instance en exécution). **Build multi-stage** = une étape de build lourde, puis copie du seul artefact dans une image runtime minimale → image plus légère et **surface d'attaque réduite** (ni compilateur ni sources).
- Frontend : Node → build Vite → **Nginx**
- Backend : Go alpine → compilation → **le binaire seul** dans une image alpine
- API : image Python + pip + uvicorn

**Kubernetes / K3s** (distribution allégée adaptée à un serveur unique) :
- **Pod** : plus petite unité déployable • **Deployment** : réplicas, rolling updates, rollback • **Service** : IP stable + load balancing interne (**ClusterIP**) • **IngressRoute Traefik** : routage HTTP/HTTPS externe • **PVC** : stockage persistant pour les uploads • **Secret / ConfigMap** : configuration injectée
- Ressources déployées : Deployment + Service + IngressRoute pour les trois services, avec **2 PVC** (frontend), **1** (backend), **2** (API Python)

**CI/CD (GitHub Actions)** : trigger = push sur `main` → tests unitaires Go → build de l'image Docker + push vers le registre local → déploiement par **SSH vers le cluster K3s** et `kubectl rollout restart`.

**Environnements :** développement (`localhost:3000/8001/8002`) • préproduction (`preprod.azert.fr`) • production (`logiciel.cabinet-martini.fr`). URLs de services gérées via `frontend/public/config.yaml`, switch par environnement.

> ⚠️ **Nuance à connaître si on creuse.** Le `config.yaml` réel déclare **quatre** blocs — `developpement`, `production`, `preproduction`, `docker` — et son bloc `preproduction` pointe vers **`dev.azert.fr`**, pas `preprod.azert.fr`. Ce dernier ne survit que dans le dossier `legacy/`, dans l'allowlist WebSocket et dans la valeur de repli du CORS. Le tableau du dossier annonce donc une URL de préproduction qui n'est plus celle du code. Si on te le demande, dis simplement que la préproduction a changé d'adresse et que le tableau n'a pas suivi.

**Rollback — les quatre déclencheurs du dossier :** régression fonctionnelle détectée en production • pic d'erreurs 5xx au-delà du seuil d'alerte • latence dégradée (P95 hors gabarit) • échec d'une migration de données critique.
- **Applicatif (zero data loss)** : Kubernetes conserve l'historique des ReplicaSets → retour en une commande, ou vers une révision spécifique.
- **Combiné code + image** : identifier le tag stable précédent (`git tag --sort=-creatordate | head -5`), redéployer depuis ce tag (la CI rebuild l'image et applique les manifests), vérifier le healthcheck.
- **Base de données** — le point à savoir défendre : **migrations toujours additives et compatibles N-1** (ajout de colonnes nullable, jamais de suppression directe). Cela permet le retour à la version applicative précédente **sans rollback du schéma**, et les suppressions de colonnes sont différées d'**au moins 2 releases**. En cas de migration destructive accidentelle : restauration depuis le **backup quotidien PostgreSQL**.
- **Communication** : notification des utilisateurs si le rollback est impactant, ticket de suivi du correctif.

**Monitoring :** healthcheck, `kubectl logs`, logs JSON structurés prêts pour ELK ou Grafana Loki. **Prometheus + Grafana** documentés en amélioration.

---

### H. Questionnement professionnel (hors projet)

- **Ta veille** : sources, fréquence, une chose apprise récemment et ce que tu en as fait.
- **Éco-conception** : bundle allégé par code splitting, images optimisées, requêtes limitées, sobriété des logs.
- **Le RGPD dans ton quotidien de développeur** : minimisation, pseudonymisation, privacy by design.
- **Travail en équipe** : revue de code, PR même en solo, communication avec des non-techniciens (les comptables du cabinet) — c'est ton point fort.
- **Ton projet professionnel** : Bac+5 « chef de projet et architecture logicielle », approfondissement IA et DevOps (Terraform, Ansible).

---

## Partie 3 — Ton projet en 15 chiffres et faits réflexes

1. **3 services** : React/Vite (3000), Go (8002), Python FastAPI (8001) + PostgreSQL partagé
2. **5 domaines Go** en Clean Architecture : auth, admin, applications, analyse, websocket *(un sixième dossier `Macdos` existe encore mais n'est plus au périmètre — ne pas le citer)*
3. **3 subrouters** : pub / sys (`AuthMiddleware`) / adm (+ `AdminMiddleware`)
4. **6 rôles** : Admin, Dev, Comptable, Social, Auditeur, Client
5. **9 tables** en base, **8 entités** au MCD — la différence, c'est la table de jonction, qui n'existe qu'au niveau logique. Schéma en 3NF.
6. **9 règles de gestion** RG01–RG09
7. **12 besoins fonctionnels** (BF01–BF12) et **5 besoins non fonctionnels** (BNF01–BNF05)
8. **6 itérations** : 17 + 17 + 13 + 10 + 11 + 20 = **88 jours effectifs**, sur environ 6 mois, 3 jours par semaine
9. **~40 collaborateurs**, 3 pôles (comptabilité, social, juridique)
10. **Session 24 h**, purge par goroutine toutes les **6 h**
11. **bcrypt coût 10**
12. **Fichiers temporaires supprimés à +5 min** (RG08)
13. **Tests : 84 pytest collectés / 72 au vert, 29/29 Vitest**, Go = testify + sqlmock sur **11 fichiers** *(les 12 échecs = préfixe de route obsolète dans `test_routers.py`, pas une régression — voir partie 2.F)*
14. **Rate limit login : 5 / 30 s**, réponse **429** + `Retry-After`
15. **Le point de départ** : automatiser le traitement manuel des tirages de caisse `.EDI`, restaurant par restaurant

---

## Partie 4 — Les questions qui fâchent

Ce sont les points attaquables du dossier remis. **La bonne posture n'est jamais de bluffer** : assume, explique le raisonnement, dis ce que tu ferais.

**1. « Vous n'avez pas de NoSQL, or la compétence l'exige. »**
> C'est un arbitrage assumé, pas une lacune — et il est argumenté dans le dossier en quatre points. Mes données sont **intrinsèquement relationnelles** : le cœur du modèle est un graphe utilisateurs → applications → permissions où l'intégrité référentielle est une exigence métier, puisque le droit à l'oubli RGPD repose sur mes `ON DELETE CASCADE` ; une base documentaire m'aurait obligé à réimplémenter ces garanties côté applicatif. Mes **besoins transactionnels sont réels** (création d'un utilisateur puis attribution de ses applications, upsert de configuration en `ON CONFLICT DO UPDATE`). Ma **volumétrie** — des dizaines d'utilisateurs internes, quelques milliers d'événements — est très loin des volumes où la scalabilité horizontale de MongoDB apporte un gain mesurable. Et le **besoin semi-structuré existe bel et bien, mais il est couvert en SQL** : mes mappings et configurations sont des structures opaques à schéma variable, stockées en colonnes `JSON` lues en bloc — c'est précisément le pattern documentaire, sans le coût d'exploitation d'un second moteur (sauvegardes, supervision, sécurité, montées de version). J'ai en revanche identifié où le NoSQL deviendrait pertinent : **Redis** pour externaliser sessions et compteurs de rate limiting dès le passage en multi-instances, et un store documentaire pour les événements analytics si la volumétrie l'exigeait.

**2. « Votre BF05 dit "Authentification sécurisée (JWT)", mais vous m'expliquez que vous n'utilisez pas de JWT. »**
> ⚠️ **C'est la contradiction la plus visible du dossier remis** : le besoin fonctionnel annonce JWT, la réalisation dit « tokens UUID stockés côté serveur, **pas de JWT côté client** ». Prépare la réponse : *« ce besoin exprime la demande telle qu'elle a été formulée au départ, où "JWT" était employé par facilité de langage pour "authentification par jeton". À la conception, j'ai arbitré entre JWT et session serveur et j'ai retenu la session opaque en base, pour la révocabilité immédiate. La formulation du besoin n'a pas été mise à jour — c'est une imprécision de rédaction, l'implémentation et sa justification sont cohérentes. »*
> **Idéalement, corrige le libellé avant impression** en « Authentification sécurisée par jeton de session avec gestion de sessions ».
> *(C'était BF06 avant le retrait de l'ancien BF05 le 22/08 — c'est désormais BF05.)*

**3. « Le rate limiting, il est en place ? »**
> Le dossier est cohérent sur ce point : le chapitre Authentification le liste en **améliorations prévues**, et le chapitre Rate Limiting présente une **stratégie retenue** avec ses seuils et son implémentation cible. Réponds : *« la stratégie est conçue et spécifiée — token bucket, seuils différenciés, 429 avec `Retry-After`, identification via `X-Forwarded-For` — et l'implémentation du middleware est planifiée, pas encore en production. »*

**4. « Vos tests E2E tournent ? »**
> Non, et le dossier le dit explicitement : « les tests E2E sont **à mettre en place**, la stratégie est documentée comme livrable cible ». Ce qui tourne aujourd'hui : **84 tests pytest dont 72 au vert**, 29 tests Vitest, les tests unitaires Go (testify + sqlmock, 11 fichiers). **Ne présente jamais Playwright comme livré** — mais sache citer les 8 scénarios cibles et le job CI, ça montre que le travail de conception est fait.

**5. « Les headers de sécurité sont déployés ? »**
> Le tableau est une **stratégie cible**, avec la mention « middleware Go à enrichir ». Dis-le tel quel, et enchaîne sur la revue prévue via securityheaders.com avant mise en production.

**6. « Pourquoi deux backends ? C'est de la complexité gratuite. »**
> Chaque service fait ce que son langage fait le mieux : Go pour le cœur transactionnel et la concurrence (middleware de session sollicité à chaque requête, hub WebSocket maintenant des dizaines de connexions ouvertes), Python pour le parsing EDI et la génération Excel — l'écosystème pandas/xlsxwriter étant sans rival sur la donnée tabulaire, **les bibliothèques Go n'étant pas assez matures pour certains cas complexes**. **Et j'assume le compromis** : deux back-ends à déployer, monitorer et maintenir, et une cohérence de données gérée au niveau applicatif puisqu'ils partagent la même base plutôt qu'une base par service — ce qui simplifie la cohérence au prix d'un couplage par le schéma. À l'échelle du projet le solde est favorable : chaque service reste petit, testable isolément, et un correctif sur l'outil de conversion ne redéploie pas l'authentification.

**7. « Vous étiez seul : où est la gestion de projet ? »**
> Kanban personnel sur carnet de bord avec **WIP = 1**, backlog priorisé en flux tiré, six itérations jalonnées se concluant chacune par une démonstration au commanditaire et une rétrospective écrite, une définition de « terminé » explicite, GitHub Flow avec pull request même en solo pour bénéficier de la CI. Le pilotage était réel sans cérémonial d'équipe — et je préfère l'assumer plutôt qu'habiller un travail solo en vocabulaire Scrum.

**8. « Vos dates ne concordent pas. »**
> ⚠️ La page de garde annonce « **Novembre 2024 - Septembre 2026** » alors que les contraintes organisationnelles disent « environ **6 mois (novembre 2024 - avril 2025)** ». **À corriger avant impression.** *(Le champ « Temps de développement estimé » est renseigné à 600 h depuis le 22/08.)*

**9. « Sur votre tableau OWASP, A10 est marqué "non implémenté". »**
> C'est une maladresse de rédaction : le SSRF n'est pas « non traité », il est **hors périmètre** parce que l'application ne fait aucune requête sortante construite à partir d'une entrée utilisateur — il n'y a donc pas de surface. **Le statut correct est « N/A » ou « sans objet ».** À corriger dans le tableau, et à formuler ainsi si on te le demande.

**10. « Votre tableau RBAC dit que tous les rôles ont un accès admin "à la demande". »**
> Formulation à clarifier : cela signifie qu'un compte peut se voir accorder le flag administrateur par un Admin existant, **pas** que le rôle donne un accès admin par défaut. Par défaut, seul le rôle Admin accède à l'administration, et la vérification se fait en base via `AdminMiddleware`. Si le jury lit ça comme une faille, c'est ta réponse.

**11. « Vous limitez le débit sur `/sys/register`, mais y a-t-il une inscription ? »**
> Non — la création de comptes est réservée aux administrateurs (RG05). La ligne `/sys/register` du tableau de rate limiting et la phrase « l'utilisateur doit pouvoir s'inscrire » du chapitre Authentification sont des **résidus d'une version antérieure du dossier**. À supprimer avant impression.

**12. « Vous parlez de Cypress dans vos améliorations et de Playwright dans vos tests. »**
> Le chapitre Tests justifie explicitement le choix de **Playwright plutôt que Cypress** ; le chapitre Améliorations écrit « E2E avec Cypress/Playwright ». **Harmonise sur Playwright.**

**13. « Qu'est-ce qui vous a le plus posé problème ? »**
> Tu as **six difficultés documentées, une par itération** — utilise-les, elles sont bien plus convaincantes qu'une réponse générale. Les trois plus fortes : le contrôle d'accès d'abord implémenté côté frontend seul, reconnu comme faille A01 et déplacé côté serveur ; la data race WebSocket détectée par `go test -race` ; et la mise en production d'un VPS vierge sans aide extérieure.

**14. « Montrez-moi l'interface du service d'authentification. »** 🔴 *La plus dangereuse*
> ⚠️ **Elle n'existe pas en production.** `auth.Service` déclare `Repo *rep.SessionRepository` — un type concret. `SessionRepositoryInterface` n'est définie que dans `service_test.go`, où le test crée **une copie de la logique** : le commentaire du fichier dit lui-même « Copie des méthodes de votre Service original pour les tests ».
> **La conséquence :** tes tests d'authentification exercent `ServiceTest.Login`, pas `Service.Login`. Si la comparaison bcrypt était retirée du code de production, **ils passeraient quand même**.
> Or ton script affirme « mes tests d'authentification tournent sans PostgreSQL grâce à l'interface ». La phrase est littéralement vraie mais trompeuse.
> **Deux sorties :** soit tu corriges — sortir l'interface du fichier de test, typer `Service.Repo` avec elle, brancher les tests sur le vrai `Service`, une quinzaine de lignes ; soit tu **changes d'exemple** et illustres le découplage avec `applications` ou `admin`, où l'interface est bien réelle. Trois services sur cinq en ont une, la démonstration tient sans l'authentification.

**15. « Votre entité "Permission des applications" dans le MCD… »**
> Si tu présentes le MCD Looping non corrigé : tu as éclaté le plusieurs-à-plusieurs en une entité intermédiaire. C'est une **table de jonction remontée au niveau conceptuel** — un mélange de niveaux.
> **Et ça coûte une garantie :** sous cette forme, rien n'interdit deux occurrences pour le même couple utilisateur/application, alors que ta base l'interdit avec `UNIQUE(user_id, application_id)`. **Ton MCD serait plus permissif que ton schéma.** Dans la forme directe — une association `accéder` portant `droit d'accès`, `(0,n)` des deux côtés — l'unicité du couple est implicite.
> **À corriger dans Looping avant l'oral.** Voir `MCD_corrige.md`.

**16. « Pourquoi vos tables de mapping n'ont-elles pas de contrainte d'unicité sur l'utilisateur ? »**
> *« Vous avez raison, la contrainte métier n'était pas portée par le schéma : c'est l'application qui garantissait qu'il n'y a qu'un paramétrage par utilisateur. C'est exactement le genre d'écart que je cherche à éliminer — une règle qui vit dans le code alors qu'elle devrait vivre dans la base. La migration 003 la pose : `UNIQUE(user_id)` sur les trois tables, plus une vraie clé étrangère sur `applications.groups`. »*
> C'est une excellente réponse, parce qu'elle montre que tu sais **où** doit vivre une contrainte.

---

## Partie 5 — Questions d'entraînement

> À faire à froid, à l'oral, chronométré (1 à 2 min par réponse). Corrigé en partie 6.

**Où réviser quoi, section d'exposé par section d'exposé.** Après chaque répétition d'une partie du script, enchaîne sur les blocs correspondants — c'est ainsi que la fiche reste en phase avec l'oral.

| § du script | Ce que tu dis | Blocs à travailler |
|---|---|---|
| § 1 Contexte | Le problème, les 5 difficultés, l'outil puis la plateforme | Bloc 1 (1-2), **Bloc 11 (151)** |
| § 2 Cadrage | 12 BF / 5 BNF / 9 RG, contraintes, 6 itérations, GitHub Flow | Bloc 1 (3-18), Bloc 10 (141), **Bloc 11 (152-155)** |
| § 3 Conception | Acteurs, 3 stades de maquettage, dictionnaire → MCD → MLD → MPD, séquence, classes | Bloc 2 (19-39), Bloc 10 (142, 146-147), **Bloc 11 (156-158)** + `REVISION_CONCEPTION.md` en entier |
| § 4 Architecture | 3 services, 2 back-ends, NoSQL arbitré, Handler/Service/Repository, 3 subrouters | Bloc 3, Bloc 4 (58-70), Bloc 10 (143), **Bloc 11 (159-163)** |
| § 5 Réalisation | Tirages de caisse, administration, analytics, présence | Bloc 3 (48-51), Bloc 10 (144-145, 148-150), **Bloc 11 (164-168)** |
| § 6 Sécurité | bcrypt, session vs JWT, 3 niveaux de contrôle, STRIDE, reste à faire | Bloc 5 (74-97), Bloc 9 (138-140), **Bloc 11 (169-172)** |
| § 7 Tests | 84 pytest / 29 Vitest / Go, l'étage E2E manquant | Bloc 6 (98-110), **Bloc 11 (173)** |
| § 8 Déploiement | Multi-stage, K3s, CI/CD, rollback, migrations additives | Bloc 7 (111-124), **Bloc 11 (174)** |
| § 9 Améliorations | Dette assumée vs nouvelle valeur | Bloc 8 (131), **Bloc 11 (175)** |
| Transversal | Les incohérences du dossier remis | **Partie 4 en entier + Bloc 9** |

> **Et la partie 7 par-dessus.** Elle n'est pas un bloc d'entraînement de plus : c'est ce qui a été **réellement demandé** en oral blanc, réponse rédigée sous la question. Rattache-la ainsi — § 2 et § 3 → questions 176-177, 183-186, 191-192, 196-197 ; § 4 → 178, 193, 199, 203 ; § 6 → 179-180, 182, 187, 190, 195, 201, 205 ; § 7 → 188, 202 ; § 8 → 189 ; conception de données → 198, 200.

### Bloc 1 — Projet & gestion de projet
1. Présente ton projet en 90 secondes à quelqu'un qui n'est pas technicien.
2. Quel était le problème métier de départ, et comment l'as-tu identifié ?
3. Quelle méthodologie as-tu suivie, et pourquoi pas Scrum ?
4. Cite tes 6 itérations, leur durée, et ce que chacune a livré.
5. Pour chaque itération, quelle difficulté as-tu rencontrée ?
6. Comment as-tu priorisé les fonctionnalités ?
7. Qu'est-ce que le WIP, et pourquoi l'as-tu limité à 1 ?
8. Quelle était ta définition de « terminé » ?
9. Écris une user story de ton projet au format canonique.
10. Différence entre besoin fonctionnel et non fonctionnel ? Donne-en deux de chaque.
11. Qu'est-ce qu'une règle de gestion ? Cite-en trois des tiennes.
12. Explique ta convention de commits et ses trois bénéfices.
13. Qu'est-ce que GitHub Flow, et pourquoi l'as-tu préféré à Git Flow ?
14. Pourquoi faire une pull request quand on est seul développeur ?
15. Qu'est-ce qu'un squash merge, et qu'est-ce que ça t'apporte ?
16. Explique SemVer. Tu corriges un bug sans changer l'API : quelle version ?
17. Tu dois annuler un commit déjà poussé sur `main` : `revert` ou `reset` ?
18. Comment as-tu estimé ta charge, et t'es-tu trompé ?

### Bloc 2 — Conception & modélisation
19. À quoi sert un diagramme de cas d'utilisation ? Quels sont tes acteurs ?
20. Différence entre `include` et `extend` ?
21. Déroule ton diagramme de séquence de l'authentification, message par message.
22. Que représente une ligne de vie ? Un message synchrone ?
23. Que montre ton diagramme de classes, et pourquoi les interfaces y sont-elles centrales ?
24. Différence entre association, agrégation et composition ?
25. Explique la chaîne MCD → MLD → MPD.
26. Comment traduit-on une association n,n en MLD ? Montre-le sur ton schéma.
27. Comment traduit-on une association 1,n ? De quel côté part la clé étrangère ?
28. Qu'est-ce que la 1NF, la 2NF, la 3NF ? Ton schéma les respecte-t-il ?
29. Tes colonnes `JSON` ne violent-elles pas la 1NF ?
30. Où as-tu dénormalisé, et pourquoi l'assumes-tu ?
31. Différence entre clé primaire, clé étrangère et clé candidate ?
32. Pourquoi `users` a-t-il à la fois `id` et `uid` ?
33. Pourquoi `sessions.id` est-il le jeton lui-même ?
34. Qu'est-ce qu'un index ? Quels index as-tu, et pourquoi pas plus ?
35. Que fait `ON DELETE CASCADE` ? Sur quelles FK, et pour quelle raison métier ?
36. Qu'est-ce qu'une transaction ? Que veut dire ACID ?
37. Comment gères-tu les évolutions de schéma en production ?
38. Qu'est-ce qu'un wireframe, une maquette, un prototype ? Avec quel outil ?
39. Qu'est-ce que le RGAA ? Cite trois critères concrets.

### Bloc 3 — Technologies & code
40. Pourquoi React plutôt que Vue ou Angular ?
41. Pourquoi Vite plutôt que Create React App ?
42. Qu'est-ce que le Virtual DOM et la réconciliation ?
43. Différence entre props et state ?
44. Explique `useEffect` : déclenchement, tableau de dépendances, nettoyage.
45. Cite les quatre patterns frontend que tu revendiques dans ton dossier.
46. Qu'apporte `React.lazy()` et où t'en es-tu servi ?
47. Pourquoi Go pour le backend ? Trois arguments.
48. Qu'est-ce qu'une goroutine ? En quoi diffère-t-elle d'un thread système ?
49. Qu'est-ce qu'une data race ? Comment l'as-tu détectée et corrigée ?
50. Pourquoi un `RWMutex` plutôt qu'un `Mutex` ?
51. Comment fonctionnent les interfaces en Go, et en quoi servent-elles tes tests ?
52. Pourquoi FastAPI pour la partie traitement de fichiers ?
53. Qu'apporte Pydantic ?
54. Différence entre ASGI et WSGI ?
55. Pourquoi PostgreSQL plutôt que MySQL ou MongoDB ?
56. Qu'est-ce qu'un ORM ? Avantages et inconvénients ?
57. Qu'est-ce qu'un linter ? Lesquels utilises-tu sur les trois stacks ?

### Bloc 4 — Architecture
58. Qu'est-ce qu'une application multicouche répartie ? En quoi la tienne en est une ?
59. Explique Handler / Service / Repository. Que connaît chaque couche ?
60. Pourquoi le Service dépend-il d'une interface et non d'une implémentation ?
61. Cite les trois besoins auxquels répond ton découpage en couches.
62. Pourquoi trois services plutôt qu'un monolithe ? Quels compromis assumes-tu ?
63. Tes deux backends partagent la même base : quel risque, et pourquoi l'accepter ?
64. Qu'est-ce que REST ? Cite quatre contraintes.
65. Différence entre 401 et 403 ? Entre 200, 201 et 204 ?
66. `PUT` est-il idempotent ? Et `POST` ? Pourquoi ça compte ?
67. Qu'est-ce qu'OpenAPI ? Comment documentes-tu chacune de tes deux API ?
68. Pourquoi dis-tu que « la source unique de vérité est le code » côté FastAPI ?
69. Qu'est-ce que le CORS ? Que se passe-t-il lors d'une requête preflight ?
70. Décris tes trois subrouters et ce qui protège chacun.
71. Comment fonctionne le WebSocket ? Décris le handshake.
72. Pourquoi WebSocket plutôt que du polling ou du SSE ?
73. Que se passe-t-il de la connexion d'un utilisateur au broadcast de présence ?

### Bloc 5 — Sécurité
74. Cite cinq risques de l'OWASP Top 10 et ta contre-mesure pour chacun.
75. Deux lignes de ton tableau OWASP ne sont pas « implémenté » : lesquelles, et pourquoi ?
76. Comment stockes-tu les mots de passe ? Pourquoi bcrypt et pas SHA-256 ?
77. Qu'est-ce qu'un sel ? bcrypt en génère-t-il un ?
78. Session serveur ou JWT : qu'as-tu choisi et pourquoi ?
79. Comment révoques-tu une session immédiatement ?
80. Quels attributs porte ton cookie de session ? Justifie chacun.
81. Explique une attaque CSRF, puis comment tu t'en protèges — les deux mécanismes.
82. Explique le XSS. Qu'est-ce qui te protège, et qu'est-ce qui manque encore ?
83. Comment empêches-tu l'injection SQL ? Montre le principe d'une requête paramétrée.
84. Qu'est-ce que le path traversal ? Tu as deux parades différentes : lesquelles, et où ?
85. Qu'est-ce que le CSWSH et comment le bloques-tu ?
86. Explique le token bucket. Quels seuils, et pourquoi plus strict sur le login ?
87. Pourquoi ton rate limiting ne fonctionnerait-il pas en multi-instances ?
88. Qu'est-ce que STRIDE ? Déroule les quatre lignes de la surface `/sys/login`.
89. Pourquoi un message d'erreur générique au login ?
90. Décris ton RBAC. Pourquoi vérifier côté serveur si le frontend le fait déjà ?
91. Le contrôle d'accès côté frontend, c'est de la sécurité ? Justifie.
92. Où sont tes secrets, en dev, en CI, en production ?
93. Que se passe-t-il si `JWT_SECRET_KEY` est absent au démarrage ? Pourquoi ce choix ?
94. Cite six mesures RGPD concrètes de ton dossier.
95. Comment implémentes-tu le droit à l'oubli ?
96. Quels événements journalises-tu, et à quel niveau ? Que ne journalises-tu jamais ?
97. Comment fais-tu ta veille sécurité ?

### Bloc 6 — Tests
98. Décris la pyramide des tests. Où mets-tu l'effort et pourquoi ?
99. Différence entre test unitaire, d'intégration et E2E ?
100. Qu'est-ce qu'un mock ? Comment ton architecture le rend-elle possible ?
101. Quels outils utilises-tu côté Go, et sur quels services ?
102. Comment testes-tu l'API Python sans PostgreSQL ?
103. Quels sont tes résultats de tests aujourd'hui ?
104. Pourquoi Playwright plutôt que Cypress ? Quatre raisons.
105. Cite trois de tes scénarios E2E cibles.
106. Donne un cas de test complet : entrée, résultat attendu, obtenu, verdict.
107. Qu'est-ce que `go test -race` et pourquoi l'utilises-tu ?
108. Qu'est-ce qu'un test de non-régression ? Quand tournent les tiens ?
109. Qu'est-ce que le TDD ? L'as-tu pratiqué ?
110. Comment as-tu constitué tes jeux de données, et sont-ils anonymisés ?

### Bloc 7 — Déploiement & CI/CD
111. Différence entre une image et un conteneur Docker ?
112. Qu'est-ce qu'un build multi-stage et qu'est-ce que ça t'apporte concrètement ?
113. Explique Pod, Deployment, Service, Ingress.
114. Pourquoi K3s plutôt que Kubernetes complet ?
115. À quoi sert Traefik chez toi ?
116. Comment tes fichiers uploadés survivent-ils au redémarrage d'un pod ?
117. Décris ton pipeline CI/CD, étape par étape.
118. Comment déploies-tu une nouvelle version sans coupure ?
119. Cite tes quatre déclencheurs de rollback.
120. Un bug critique passe en production : décris ta procédure de rollback applicatif.
121. Et si le problème vient d'une migration de base ? Quelle est ta stratégie ?
122. Pourquoi tes migrations sont-elles « additives et compatibles N-1 » ?
123. Quels environnements as-tu, et comment le frontend sait-il à quelle API parler ?
124. Comment tes secrets arrivent-ils dans les conteneurs en production ?

### Bloc 8 — Posture professionnelle
125. Quelle est ta plus grande difficulté sur ce projet, et comment l'as-tu résolue ?
126. Qu'est-ce que tu referais autrement ?
127. Quelle est la faiblesse technique que tu connais dans ton application ?
128. Comment fais-tu ta veille technologique ? Une chose apprise ce mois-ci ?
129. Comment expliques-tu un choix technique à un comptable ?
130. Qu'as-tu appris de plus important pendant ce projet ?
131. Quelles sont tes trois prochaines évolutions prioritaires, et dans quel ordre ?

### Bloc 9 — Les pièges de ton propre dossier

> Ce bloc n'existe pas dans un manuel : ce sont les questions qu'un jury attentif peut tirer de **tes** incohérences. Ce sont les plus déstabilisantes, parce qu'elles viennent de ce que tu as écrit toi-même.
> C'est la version « interrogation » de la partie 4 : là-bas tu as les réponses rédigées, ici tu dois les produire à froid. Fais ce bloc **sans avoir relu la partie 4**.

132. Votre besoin BF05 annonce « authentification sécurisée (JWT) », mais votre réalisation dit « pas de JWT côté client ». Lequel est vrai ?
133. Dans votre tableau OWASP, A10 est marqué « non implémenté ». Vous n'avez donc rien fait contre le SSRF ?
134. Vous prévoyez une limitation de débit sur `/sys/register`. Y a-t-il une inscription dans votre application ?
135. Votre chapitre Améliorations parle de « Cypress/Playwright », votre chapitre Tests justifie Playwright contre Cypress. Lequel avez-vous retenu ?
136. Votre chapitre s'intitule « Planning et sprints », mais vous dites ne pas faire de Scrum. Expliquez.
137. Combien d'environnements avez-vous, et comment le frontend sait-il à quelle API parler ?
138. Comment votre WebSocket décide-t-il d'accepter une connexion ? Que se passe-t-il si l'origine n'est pas dans la liste ?
139. Votre CORS a-t-il une valeur par défaut si la variable d'environnement n'est pas définie ? Est-ce prudent ?
140. Quel est le défaut de configuration que vous connaissez aujourd'hui dans votre code ?

### Bloc 10 — Ce que les corrections d'août ont changé

> Ces questions portent sur des points **modifiés récemment**. Un jury qui lit la version finale du dossier peut tomber dessus, et tes réponses d'il y a deux semaines ne marchent plus.

141. Combien de besoins fonctionnels avez-vous, et combien concernent l'outil de tirages de caisse ?
142. Combien de tables compte votre base ? Et combien d'entités votre MCD ?
143. Vous n'utilisez plus le terme « ACID » dans votre dossier. Que veut-il dire, et pourquoi PostgreSQL plutôt que MongoDB alors ?
144. Quelles tables l'outil de tirages de caisse utilise-t-il exactement ?
145. Votre dossier ne mentionne plus `fascicule_mcdo`, mais la table existe encore en base et il reste un dossier `Macdos` dans votre backend. Expliquez.
146. Décrivez les trois stades de votre maquettage, et ce que chacun valide. Où se placent alors vos écrans finis ?
147. Pourquoi vos maquettes du troisième stade n'ont-elles aucun texte réel ?
148. Comment le paramétrage des codes comptables est-il enregistré ? Quelles routes, quelles tables ?
149. Dans votre fonction `code_comptas`, pourquoi filtrez-vous les champs vides avant la fusion ?
150. Vous avez trois fonctions quasi identiques pour les trois mappings. Pourquoi ne pas les factoriser ?

### Bloc 11 — Les phrases de ton exposé que le jury va reprendre

> **Le bloc le plus rentable de la fiche.** Chaque question ci-dessous est déclenchée par une phrase que **tu prononces toi-même** pendant l'exposé — le § du script est indiqué. Un jury ne cherche pas des questions : il reprend tes propres affirmations et demande à voir derrière.
> Fais ce bloc **après avoir répété l'exposé à voix haute**, pas avant : c'est ce qui te fera entendre les phrases que tu ne peux pas soutenir.

151. *(§ 1)* « Le projet n'est pas parti d'un cahier des charges, il est parti d'une observation. » Comment passe-t-on d'une observation à douze besoins fonctionnels ? Qui a validé le périmètre, et à quel moment ?
152. *(§ 2.1)* Vous annoncez douze besoins fonctionnels, quatre pour l'outil et huit pour la plateforme. Citez les quatre de l'outil.
153. *(§ 2.1)* Vos besoins non fonctionnels annoncent « moins de deux secondes » et « 99,5 % de disponibilité ». D'où sortent ces valeurs, et comment les mesurez-vous aujourd'hui ?
154. *(§ 2.2)* Vous dites n'avoir eu **qu'une seule** contrainte d'infrastructure imposée. Laquelle — et qu'est-ce que ça implique pour le reste de votre architecture ?
155. *(§ 2.3)* Vous avez piloté le projet sur un carnet papier. Comment prouvez-vous le suivi, et qu'auriez-vous fait à trois développeurs ?
156. *(§ 3.2)* Pourquoi votre deuxième stade de maquettage est-il volontairement **sans couleur** ?
157. *(§ 3.3)* Vous dites : « le droit à l'oubli n'est pas écrit dans mon code, il est garanti par la structure de la base ». Montrez-moi où, et dites-moi ce que la suppression **n'efface pas**. 🔴
158. *(§ 3.3)* Le groupe d'une application est stocké en texte simple : c'est une dénormalisation assumée. À partir de quand devient-elle un vrai problème ?
159. *(§ 4.1)* « Chaque service fait ce que son langage fait le mieux. » Concrètement, qu'est-ce qui aurait été pénible à écrire en Go ? Et qu'est-ce qui aurait été pénible en Python ?
160. *(§ 4.2)* Vous dites que l'absence de NoSQL est un arbitrage, pas un oubli. Quel serait le **premier signal** qui vous ferait introduire Redis, et qu'est-ce que ça changerait dans votre code ?
161. *(§ 4.3)* Vous dites qu'« un développeur qui comprend un des **six** services les comprend tous », mais vous n'en avez cité que **cinq**. Lequel manque ? 🔴
162. *(§ 4.3)* Vous dites que le découpage en trois sous-routeurs « rend l'oubli difficile ». Qu'est-ce qui empêche réellement un développeur de placer une route d'administration dans le mauvais sous-routeur ?
163. *(§ 4.3)* Côté Python, votre documentation d'API est générée depuis le code ; côté Go, elle est maintenue à la main. Pourquoi cette asymétrie, et qu'est-ce qu'elle vous coûte ?
164. *(§ 5.1)* Vous validez l'identifiant par une expression régulière UUID **avant tout traitement**. Que se passe-t-il exactement si je vous envoie `../../etc/passwd` comme identifiant ?
165. *(§ 5.1)* L'itération 2 a déplacé les codes comptables d'un fichier de configuration vers la base. Qu'est-ce que ça a coûté techniquement, et qu'est-ce que ça a changé pour les comptables ?
166. *(§ 5.2)* Votre tableau de bord affiche trois indicateurs. Lesquels, et quelle **décision** chacun permet de prendre ?
167. *(§ 5.2)* Vous dites qu'on peut ajouter une application au portail « sans redéployer ». Jusqu'où va cette promesse ?
168. *(§ 5.2)* « J'y reviens volontiers si ça vous intéresse. » Allez-y : racontez le bug de concurrence en entier, de la détection au correctif.
169. *(§ 6.1)* Votre session en base coûte une lecture par requête. À partir de quelle charge ce choix devient-il un problème, et que feriez-vous alors ?
170. *(§ 6.3)* Vous renvoyez un **429 avant tout calcul bcrypt**. Pourquoi cet ordre est-il le point clé de la mesure ?
171. *(§ 6.3)* Vous dites vous être « inspiré de STRIDE ». Déroulez les **trois surfaces** que vous avez analysées, et dites ce que STRIDE désigne exactement.
172. *(§ 6.4)* Vous listez vous-même quatre points de sécurité non terminés. Pourquoi les annoncer plutôt que d'attendre qu'on les trouve ?
173. *(§ 7)* Vous dites qu'il « manque un étage » à votre pyramide de tests. Qu'est-ce que ça vous empêche de garantir aujourd'hui ?
174. *(§ 8.3)* Vos migrations sont « additives et compatibles N-1 ». Donnez-moi le déroulé complet d'une **suppression de colonne** dans ce cadre.
175. *(§ 9)* Vous classez vos améliorations en « dette assumée » et « nouvelle valeur ». Pourquoi cette distinction, et pourquoi la sécurité en premier ?

---

## Partie 6 — Corrigé (points clés attendus)

### Bloc 1
1. Problème (traitement manuel des tirages de caisse) → première solution (outil autonome) → constat (outils isolés, pas de gestion de droits, pas de visibilité) → plateforme unifiée → résultat pour les 40 collaborateurs.
2. Besoin observé directement en alternance, remonté par les comptables ; pas un besoin théorique.
3. Kanban + 6 itérations. Pas de Scrum : rôles et cérémonies supposent une équipe et se vident de leur sens seul. « La méthode doit servir le contexte. »
4. (1) tirages autonome 17 j, (2) retours + fondations 17 j, (3) admin + intégration 13 j, (4) temps réel + analytics 10 j, (5) déploiement/sécurisation 11 j, (6) finalisation 20 j.
5. Voir le tableau de la partie 2.A — encodages EDI, couplage Go/Python, contrôle d'accès frontend-only, data race, typo CORS, psycopg2.
6. Backlog priorisé en flux tiré : valeur métier immédiate d'abord, puis dépendances techniques (l'authentification devait précéder le catalogue par droits).
7. Work In Progress = nombre de tâches ouvertes simultanément. Limité à 1 pour ne jamais laisser de chantier à moitié terminé entre deux sessions espacées de plusieurs jours.
8. Code écrit, testé, passé au lint, commité selon les conventions.
9. Ex. : « En tant que comptable, je veux déposer plusieurs fichiers EDI et récupérer un Excel consolidé afin de ne plus saisir les tickets manuellement. »
10. BF = ce que fait le système ; BNF = comment (perf < 2 s, OWASP/RGPD, dispo 99,5 %, scalabilité, maintenabilité).
11. Règle métier indépendante de l'implémentation → RG03, RG04, RG08.
12. `<type>(<scope>): <description>`. Bénéfices : historique lisible et filtrable, détection automatique du type de release SemVer, facilité pour de nouveaux contributeurs.
13. Une seule branche permanente `main` toujours déployable, branches éphémères, PR, squash merge, tags. Préféré à Git Flow (`develop`/`release`/`hotfix`) parce que : un seul développeur, déploiement continu vers preprod après chaque merge, pas de version LTS à maintenir.
14. Pour bénéficier de la CI — tests et lint obligatoires avant merge. La PR est le point de contrôle automatisé, pas seulement un rituel de revue.
15. Tous les commits de la branche sont fusionnés en un seul sur `main` → historique linéaire et lisible, un commit = une fonctionnalité.
16. PATCH → 1.2.3 devient 1.2.4.
17. `revert` : il crée un commit d'annulation sans réécrire l'historique, seul choix sûr sur une branche partagée.
18. **88 jours effectifs, soit 600 h** renseignées au dossier, sur environ six mois à trois jours par semaine. Réponse honnête attendue : l'itération 5 (déploiement) et l'itération 6 (20 jours) ont été plus longues que prévu — un serveur vierge à provisionner sans aide extérieure ne s'estime pas quand on n'en a jamais fait.

### Bloc 2
19. Vue fonctionnelle acteurs × fonctionnalités. Acteurs : Admin, Dev, Comptable, Social, Auditeur, Client.
20. `include` = comportement toujours exécuté et factorisé ; `extend` = optionnel sous condition.
21. POST `/sys/login` → handler → service → repository (`SELECT` sur email) → comparaison bcrypt → création de session en base → pose du cookie → 200.
22. Ligne de vie = période d'existence d'un participant ; message synchrone (flèche pleine) = l'appelant attend la réponse.
23. La couche métier du backend Go en Clean Architecture : Handler / Service (`AuthService`, `AdminService`, `AnalyseService`, `OnlineUserManager`) / Repository (`AdminRep`, `ApplicationRepositoryInterface`, `SessionRepository`, `UserRepository`). Les interfaces sont la clé du découplage : `AdminService` dépend de `AdminRep`, pas d'une implémentation — struct PostgreSQL en prod, mock déterministe en test.
24. Association = lien simple ; agrégation = « fait partie de », vies indépendantes (losange vide) ; composition = le composant meurt avec le composite (losange plein).
25. MCD = quoi, sans SGBD → MLD = relations et clés → MPD = SQL réel avec types, contraintes, index.
26. Table de jonction portant les deux FK → `user_application_permissions(user_id, application_id, can_access)` avec `UNIQUE(user_id, application_id)`.
27. La FK va du côté « n » → `sessions.user_id` référence `users.uid`.
28. Voir partie 2.B. Oui, en 3NF, avec une dénormalisation assumée.
29. Non : structures opaques pour la base, jamais indexées ni jointes, lues en bloc. La normalisation porte sur ce que la base doit manipuler comme des valeurs.
30. `applications.groups` en TEXT libre sans FK vers `application_groups` : référence faible, choix de simplicité assumé.
31. PK = identifiant unique choisi ; FK = référence à la clé d'une autre relation ; clé candidate = tout ensemble pouvant jouer le rôle de PK (chez toi `email`, `username`, `uid`).
32. `id SERIAL` = clé de substitution pour les jointures internes et les FK Python ; `uid TEXT` = identifiant métier stable généré côté Go, référencé par les FK Go et exposé au client.
33. Le jeton fait office de clé primaire, il n'y a pas de colonne `token` séparée — lookup direct par l'index de PK sur le chemin chaud du middleware.
34. Structure accélérant les recherches au prix d'un coût en écriture. Uniquement les index implicites PK/UNIQUE, chacun justifié par un chemin d'accès réel ; pas d'index sur les colonnes JSON puisque aucune requête n'y projette.
35. Supprime automatiquement les lignes filles à la suppression du parent → sert le droit à l'oubli (RG06). **Attention à être exact** : la cascade est posée sur `user_code_maps`, `user_code_maps_gen_aux`, `code_journal` et `events`. `sessions` et `user_application_permissions` ont une FK **sans** cascade — leurs lignes sont supprimées explicitement par `DeleteUser`, dans une transaction. Voir corrigé 157, et la contradiction avec RG07 sur `events`.
36. Unité de travail tout-ou-rien. ACID : Atomicité, Cohérence, Isolation, Durabilité.
37. `InitSchema` au démarrage + migrations SQL **idempotentes** (`001_fix_anomalies.sql`, puis `003_alignement_conceptuel.sql`) ; outil dédié prévu, conditionné à des évolutions post-production.
38. Wireframe = structure sans style ; maquette = rendu avec la charte ; prototype = navigable. Outil : **Figma**.
39. Référentiel français déclinant WCAG 2.1 : contraste ≥ 4.5:1, navigation clavier complète, `alt` sur les images porteuses de sens, labels de formulaires, hiérarchie de titres.

### Bloc 3
40. Écosystème mature, réutilisabilité par composants, communauté, recrutement.
41. CRA est déprécié ; Vite offre un HMR quasi instantané (ESBuild) et une configuration légère.
42. Représentation en mémoire de l'arbre d'UI ; la réconciliation compare ancien et nouvel arbre pour n'appliquer au DOM que les différences.
43. Props = reçues du parent, immuables dans l'enfant ; state = interne, sa modification déclenche un re-rendu.
44. Effet exécuté après le rendu ; le tableau de dépendances contrôle le redéclenchement (vide = au montage seulement) ; la fonction de retour nettoie (fermeture de WebSocket typiquement).
45. Lazy Loading (`React.lazy()` + Suspense), Context Pattern (`ConfigContext`, `MicroservicesContext`, `ThemeContext`), Service Layer (abstraction Axios), Protected Routes.
46. Chargement différé → réduction du bundle initial. Utilisé sur les pages du routeur, dont l'outil de conversion.
47. Binaire unique sans runtime, typage statique fort, goroutines natives pour la concurrence.
48. Thread léger multiplexé par le runtime Go sur des threads système ; quelques Ko de mémoire initiale contre plusieurs Mo pour un thread OS.
49. Deux goroutines accédant à la même map dont au moins une en écriture → comportement indéfini. Détectée par `go test -race`, corrigée par `sync.RWMutex` — et la résolution a demandé plusieurs itérations pour éviter les interblocages au broadcast.
50. Les broadcasts sont des lectures fréquentes, parallélisables sous `RLock` ; seuls add/remove prennent le verrou exclusif.
51. Implémentation implicite : un type satisfait une interface dès qu'il en a les méthodes. Le Service dépend de l'interface, donc un mock s'y substitue en test.
52. pandas / xlsxwriter pour l'Excel, ASGI async, Pydantic, OpenAPI auto-généré.
53. Validation et conversion automatiques depuis les annotations de type, et génération du schéma OpenAPI.
54. WSGI est synchrone et bloquant ; ASGI gère l'asynchrone et les connexions longues.
55. JSON/JSONB natif, extensions riches, et surtout l'intégrité référentielle dont dépend le droit à l'oubli — MongoDB ne l'offre pas. *(Le dossier ne cite plus « ACID » depuis le 23/08 ; garde la définition en tête, la question reste possible — voir corrigé 36.)*
56. Mapping objet-relationnel. Avantages : productivité, portabilité, protection native contre l'injection. Inconvénients : requêtes parfois sous-optimales, effet boîte noire, problème N+1.
57. Analyse statique signalant erreurs et écarts de style. ESLint/Prettier (React), golangci-lint (Go), ruff/black (Python) — installés dès l'itération 2.

### Bloc 4
58. Couches réparties sur des processus/machines distincts communiquant par le réseau : SPA Nginx ↔ Go ↔ Python ↔ PostgreSQL, derrière Traefik.
59. Handler = HTTP uniquement ; Service = métier, ne connaît ni HTTP ni SQL ; Repository = seul à connaître PostgreSQL.
60. Pour inverser la dépendance : la logique métier ne dépend plus d'un détail d'infrastructure → mock en test, remplacement de la persistance sans toucher au métier.
61. Tester sans base de données ; changer de source de données sans impacter que le Repository ; isoler les règles RG01–RG09 dans le Service.
62. Chaque langage sur son terrain. Compromis assumés : deux back-ends à déployer et monitorer, cohérence applicative, base partagée.
63. Couplage par le schéma : un changement de table peut casser l'autre service. Accepté parce que la cohérence est plus simple qu'avec deux bases, et le périmètre le permet.
64. Interface uniforme, sans état, client-serveur, ressources identifiées par URI, représentations, cache.
65. 401 = non authentifié ; 403 = authentifié mais non autorisé. 200 = OK avec corps, 201 = créé, 204 = OK sans corps.
66. `PUT` idempotent, `POST` non. Compte pour les rejeux réseau et les stratégies de retry.
67. Spécification standard décrivant une API. FastAPI la génère automatiquement (Swagger UI sur `/docs`, ReDoc sur `/redoc`) ; l'API Go est documentée manuellement.
68. Parce que la spécification est régénérée à chaque démarrage depuis les annotations du code : aucune dérive ne peut s'installer entre code et documentation, ajouter un endpoint suffit à le voir apparaître.
69. Mécanisme navigateur limitant les requêtes cross-origin. Le preflight `OPTIONS` demande au serveur s'il autorise méthode et en-têtes ; réponse via `Access-Control-Allow-*` — allowlist, jamais `*` avec credentials.
70. `pub` sans auth (login/logout), `sys` sous `AuthMiddleware`, `adm` sous `AuthMiddleware` + `AdminMiddleware`.
71. `GET` avec `Connection: Upgrade`, `Upgrade: websocket`, `Sec-WebSocket-Key` → `101 Switching Protocols` → connexion TCP full-duplex.
72. Le polling gaspille des requêtes et ajoute de la latence ; SSE est unidirectionnel. La présence exige du push serveur avec des clients qui s'annoncent.
73. Upgrade après `CheckOrigin` → message d'init `{uid}` → `AddUser` → broadcast de la liste à tous → boucle de ping → à la fermeture `RemoveUser` + nouveau broadcast.

### Bloc 5
74. Voir le tableau de la partie 2.E.
75. **A06 Vulnerable Components → « à vérifier »** (dépendances à jour et images officielles, mais pas de scan systématique en place) et **A09 Logging & Monitoring → « à renforcer »** (logging détaillé mais pas d'agrégation ni d'alerting). A10 SSRF est **sans objet**, pas « non implémenté » — voir partie 4, question 9.
76. bcrypt, coût 10 : lent par conception et salé, là où SHA-256 est rapide donc cassable en masse sur GPU. Modernes : argon2id, scrypt.
77. Valeur aléatoire ajoutée avant hachage pour que deux mots de passe identiques donnent des hash différents (anti rainbow tables). Oui, bcrypt le génère et l'embarque.
78. Session opaque en base — tokens UUID côté serveur, pas de JWT côté client — pour la **révocabilité immédiate**.
79. Suppression de la ligne dans `sessions` → la requête suivante échoue au middleware. Impossible avec un JWT sans liste de révocation.
80. `HttpOnly` (inaccessible au JS, anti-XSS), `Secure` (HTTPS uniquement), `SameSite=Strict` (anti-CSRF), plus une expiration alignée sur la session validée en base à chaque requête.
81. Un site tiers déclenche une requête authentifiée à l'insu de l'utilisateur, le navigateur joignant le cookie. Parades : (1) `SameSite=Strict`, (2) vérification `Origin`/`Referer` côté serveur sur les non-GET contre la liste blanche CORS.
82. Injection de JS exécuté chez un tiers. Protection : échappement natif de React + cookie `HttpOnly`. Manque : la **CSP**, encore en stratégie cible.
83. Requêtes paramétrées : la valeur n'est jamais concaténée dans le SQL, elle est transmise séparément au moteur — `WHERE email = $1` en Go, l'ORM SQLAlchemy côté Python.
84. Sortir du répertoire prévu via `../`. Parades : regex UUID stricte avant construction de chemin puis `os.path.join` (Python) ; `filepath.Base()` sur les noms uploadés (Go).
85. Cross-Site WebSocket Hijacking : le handshake WS n'est pas soumis à la same-origin policy, un site tiers peut ouvrir une WS avec le cookie de la victime. Parade : `CheckOrigin` contre une allowlist.
86. Seau de capacité fixe rempli à taux constant ; chaque requête consomme un jeton, sinon 429. Login à 5 / 1 par 30 s parce que c'est la surface de brute force et que bcrypt y est coûteux en CPU ; 60 / 1 par seconde ailleurs.
87. Les compteurs sont en mémoire par instance → chaque réplique aurait son propre seau. « OK en scaling vertical, KO en horizontal. » Solution : Redis partagé.
88. Spoofing (bruteforce → bcrypt + token bucket) ; Information disclosure (énumération → message générique) ; Tampering (vol de cookie → `HttpOnly`/`Secure`/`SameSite=Strict` + session validée en base) ; DoS (saturation de bcrypt → 429 rapide avant tout calcul bcrypt).
89. Pour empêcher l'énumération de comptes : distinguer « email inconnu » de « mot de passe incorrect » révèle quels comptes existent.
90. 6 rôles, vérification à **trois endroits, et c'est volontaire** : (1) le **navigateur** masque ce à quoi l'utilisateur n'a pas droit — confort d'affichage, **pas** une sécurité ; (2) le **backend Go** vérifie à chaque requête la validité de la session **en base**, puis le rôle requis via `AdminMiddleware` ; (3) l'**API Python** refait sa propre vérification avant de toucher au moindre fichier. Trois barrières indépendantes : si l'une tombe, les autres tiennent. Le serveur doit vérifier parce que le frontend est entièrement sous contrôle de l'utilisateur : n'importe qui peut appeler l'API directement. Même logique pour le catalogue — le filtrage est fait **en base**, le navigateur ne reçoit jamais la liste complète des applications pour en cacher une partie.
91. Non — confort d'affichage. **Et je l'ai appris en le faisant** : à l'itération 3, j'avais implémenté la vérification admin côté frontend seul, ce qui était une faille A01 ; je l'ai déplacée dans un middleware serveur.
92. `.env` gitignoré en dev, GitHub Actions secrets en CI, Secrets Kubernetes en prod. Aucun secret dans Git.
93. L'API Python **refuse de démarrer** : fail-fast, pour éviter de tourner avec une clé vide ou par défaut — une dégradation silencieuse serait pire qu'un crash.
94. Minimisation, chiffrement (bcrypt + HTTPS), droit à l'oubli (`ON DELETE CASCADE`), limitation de conservation (sessions 6 h, fichiers 5 min), traçabilité, consentement (intranet authentifié, pas de cookies tiers).
95. Suppression du compte → une **transaction** supprime droits, sessions et paramétrages comptables puis le compte, avec rollback si un ordre échoue ; en base, les `ON DELETE CASCADE` sur `events` et les trois tables de mapping garantissent qu'aucune ligne ne peut survivre à son propriétaire. **Schéma et code se couvrent mutuellement** — ne dis pas « ce n'est pas dans mon code », c'est faux et vérifiable. Voir corrigé 157.
96. Connexion échouée en `WARN` (email tenté, IP, user-agent, timestamp), connexion réussie et logout en `INFO`, suppression de compte et changement de rôle en `WARN`, 5xx en `ERROR`. Jamais : mots de passe, jetons complets, données personnelles inutiles à la finalité.
97. ANSSI/CERT-FR hebdo, OWASP mensuel, Dependabot automatique, base CVE, scan de dépendances à chaque build. Prépare **un** exemple concret.

### Bloc 6
98. Large base d'unitaires, complétée par de l'intégration via TestClient/TestDB ; peu d'E2E car lents et fragiles.
99. Unitaire = une fonction isolée avec doubles ; intégration = plusieurs composants avec les vraies dépendances ; E2E = parcours complet dans un navigateur.
100. Un double qui simule une dépendance. Possible parce que le Service dépend d'une **interface** Repository.
101. `testify` + `sqlmock`, sur Auth, Admin, Applications et Analyse — **11 fichiers de tests** — plus `go test -race` sur le WebSocket.
102. Le `conftest.py` mocke psycopg2 au niveau `sys.modules` **avant tout import** et bascule sur SQLite in-memory.
103. **84 tests pytest collectés dont 72 au vert**, 29/29 Vitest, tests unitaires Go au vert (dont `-race` sur le WebSocket). Les 12 échecs sont des `404` de préfixe de route dans `tests/test_routers.py`, pas des régressions fonctionnelles — dis-le toi-même plutôt que de te faire prendre sur un « 84/84 ». Ajoute que la couverture est un indicateur, pas un objectif.
104. Support natif multi-navigateurs (Chromium, Firefox, WebKit) ; auto-waiting plus robuste, donc moins de tests flaky sur les états asynchrones ; API moderne `async/await` ; exécution headless compatible CI sans serveur X.
105. Par exemple `auth-02` (mot de passe incorrect → message d'erreur), `admin-03` (suppression avec modale de confirmation), `rbac-01` (un Comptable tente `/admin` → redirection ou 403).
106. Prépare le cas EDI : fichier d'entrée → attendu : Excel une feuille par restaurant, montants mappés, distinction Facture/Avoir → obtenu identique → conforme.
107. Le détecteur de data race de Go : il instrumente l'exécution pour repérer les accès concurrents non synchronisés. Utilisé sur le paquet WebSocket.
108. Rejeu des tests existants après un changement ; ils tournent à chaque push dans la CI, et une campagne manuelle a lieu avant chaque release.
109. Red / Green / Refactor. Réponds honnêtement : pratiqué partiellement, surtout sur les fonctions pures de conversion.
110. Fichiers EDI réels du cabinet, **anonymisés**, plus des cas construits pour les cas limites (fichier vide, encodage inattendu, avoir).

### Bloc 7
111. L'image est le modèle immuable ; le conteneur est une instance en exécution avec sa couche inscriptible.
112. Compilation dans une première étape, copie du seul artefact dans une image runtime minimale → image plus légère, sans compilateur ni sources, surface d'attaque réduite.
113. Pod = plus petite unité déployable ; Deployment = réplicas et rolling updates ; Service = IP stable + load balancing interne ; Ingress = point d'entrée HTTP externe.
114. Distribution allégée adaptée à un serveur unique, avec l'API Kubernetes complète sans le coût opérationnel d'un cluster complet.
115. Reverse proxy et ingress controller natif K8s : terminaison TLS avec Let's Encrypt intégré, routage vers les trois services.
116. Un **PVC** monte un volume persistant, indépendant du cycle de vie du pod.
117. Push sur `main` → tests unitaires Go → build de l'image + push registre → SSH vers le cluster K3s → `kubectl rollout restart`.
118. Rolling update : Kubernetes démarre les nouveaux pods, attend qu'ils soient prêts, puis retire les anciens.
119. Régression fonctionnelle en production ; pic d'erreurs 5xx au-delà du seuil d'alerte ; latence dégradée (P95 hors gabarit) ; échec d'une migration de données critique.
120. Kubernetes conserve l'historique des ReplicaSets → retour en une commande, sans perte de données ; puis notification si impactant et ticket de suivi.
121. Le code revient en arrière mais pas les données. Ma stratégie évite le problème en amont : migrations toujours additives et compatibles N-1. En dernier recours, restauration depuis le backup quotidien PostgreSQL.
122. Parce qu'ainsi la version applicative précédente reste compatible avec le schéma courant : on peut revenir en arrière **sans rollback du schéma**. Les suppressions de colonnes sont différées d'au moins 2 releases.
123. Dev / préproduction (`preprod.azert.fr`) / production (`logiciel.cabinet-martini.fr`) ; le frontend lit `public/config.yaml` avec un switch par environnement.
124. Via des **Secrets Kubernetes** montés en variables d'environnement dans le manifest Deployment — jamais dans l'image ni dans Git.

### Bloc 8
125–131. Pas de corrigé : ce sont **tes** réponses. Écris-les et répète-les à voix haute. Contraintes : une difficulté **réelle** avec sa résolution (tu en as six documentées, une par itération) ; une faiblesse **assumée** suivie du correctif identifié ; et trois évolutions priorisées avec leur raison — l'ordre naturel étant sécurité (rate limiting effectif, headers, token CSRF) → tests E2E → Redis pour le multi-instances et le monitoring Prometheus/Grafana.

### Bloc 9

> **Règle générale pour tout ce bloc :** ne défends jamais l'incohérence, reconnais-la en une phrase et enchaîne immédiatement sur ce qui est vrai. Un jury pardonne une imprécision de rédaction assumée ; il ne pardonne pas un candidat qui s'entête à justifier une contradiction.

132. **La réalisation est vraie.** J'ai des sessions opaques en base, pas de JWT côté client. « JWT » dans le libellé du besoin était employé par facilité de langage pour « authentification par jeton », au moment où le besoin a été formulé. À la conception, j'ai arbitré entre JWT et session serveur et j'ai retenu la session, pour la révocabilité immédiate. **Le libellé du besoin n'a pas été mis à jour — c'est une imprécision de rédaction**, l'implémentation et sa justification sont cohérentes entre elles.
133. **C'est une maladresse de rédaction de ma part.** Le SSRF n'est pas « non traité », il est **hors périmètre** : l'application ne construit aucune requête sortante à partir d'une entrée utilisateur, il n'y a donc pas de surface d'attaque. Le statut correct serait « N/A » ou « sans objet ».
134. **Non.** La création de comptes est réservée aux administrateurs — c'est ma règle RG05. Cette ligne du tableau, comme la phrase « l'utilisateur doit pouvoir s'inscrire », sont des **résidus d'une version antérieure du dossier**, où une inscription libre était envisagée avant d'être écartée.
135. **Playwright**, et le chapitre Tests donne mes quatre raisons : multi-navigateurs natif, auto-waiting plus robuste, API moderne, exécution headless en CI. La mention de Cypress dans les améliorations est un reste de la phase où je comparais encore les deux.
136. Le titre est un abus de langage ; **le contenu du chapitre décrit six itérations jalonnées**, sans timebox ni cérémonie. Il n'y a pas de sprint au sens Scrum : pas de durée fixe, pas de review, pas de rôles. J'aurais dû l'intituler « Planning et itérations ».
137. **Trois** dans le dossier : développement en local, préproduction, production. Le frontend lit `public/config.yaml`, qui porte un bloc d'URLs par environnement. *(Si on creuse : le fichier réel compte un quatrième bloc `docker`, et la préproduction y pointe désormais vers une autre adresse que celle du tableau — voir la nuance en partie 2.G.)*
138. À chaque tentative d'upgrade, le serveur lit l'en-tête `Origin` et le cherche dans une **liste blanche**. Si l'origine n'y figure pas, `CheckOrigin` renvoie `false` et **le handshake est refusé** : la connexion n'est jamais établie. C'est ma parade contre le Cross-Site WebSocket Hijacking, la politique de même origine ne s'appliquant pas au handshake WebSocket.
139. **Oui, et c'est discutable.** Si `CORS_ORIGIN` n'est pas défini, le middleware retombe sur une origine codée en dur. L'avantage est qu'un oubli de configuration ne casse pas le service ; **l'inconvénient est qu'il le fait démarrer avec une valeur silencieusement fausse**. C'est exactement l'inverse du choix que j'ai fait côté API Python, où l'absence de clé JWT fait échouer le démarrage — *fail-fast*. La cohérence voudrait que j'applique le même principe ici.
140. **Réponse à préparer, et à ne donner que si tu as vérifié.** Si c'est confirmé : *« mon allowlist WebSocket est codée en dur et n'a pas suivi le passage en production : elle contient l'origine de préproduction, pas celle de production. Le handshake est donc refusé depuis le domaine de production, et l'échec est silencieux. Le correctif est de la rendre configurable par variable d'environnement, sur le modèle de ce que je fais déjà pour le CORS HTTP. »* C'est une excellente réponse : elle prouve que tu relis ton propre code. Si tu tournes encore sur la préproduction, n'aborde pas le sujet spontanément.

### Bloc 10

141. **Douze**, dont **quatre** pour l'outil de tirages de caisse : importer plusieurs fichiers `.EDI` en une opération, appliquer un mapping de codes paramétrable par client, enregistrer et réutiliser ses codes en base, regrouper par restaurant et restituer un Excel. Les huit autres portent la plateforme, de l'authentification à l'interface responsive.
> *Si on te demande pourquoi douze et pas treize :* un besoin sur la configuration des fascicules McDonald's a été retiré, parce qu'aucune interface ne l'appelle — la fonctionnalité n'était pas livrée, et je préfère un périmètre annoncé qui corresponde au périmètre réel.

142. **Neuf tables** en base : utilisateurs, sessions, applications, groupes d'applications, la table de jonction des permissions, les événements d'analyse, et trois tables de mapping comptable. Le MCD compte **huit entités** — la neuvième table est la table de jonction, qui n'existe qu'au niveau logique, puisqu'au conceptuel c'est une association.
> C'est une bonne question à recevoir : la différence entre les deux chiffres **est** la démonstration que tu as compris le passage MCD → MLD.

143. **Atomicité, Cohérence, Isolation, Durabilité** — les quatre garanties d'une transaction. Le dossier ne met plus le terme en avant, mais l'argument reste : mes besoins transactionnels sont réels (créer un utilisateur puis lui attribuer ses applications), et surtout **MongoDB n'offre pas l'intégrité référentielle** dont dépend mon droit à l'oubli, qui repose entièrement sur mes `ON DELETE CASCADE`.

144. **Trois, et trois seulement** : `user_code_maps`, `user_code_maps_gen_aux` et `code_journal`. Chacune stocke un mapping en colonne `JSON`, rattachée à l'utilisateur par une clé étrangère en `ON DELETE CASCADE`. Tout le reste du traitement opère sur des fichiers transitoires, supprimés cinq minutes après.

145. C'est un **reste de la première version autonome de l'outil**, où la configuration des fascicules était globale et non rattachée à un utilisateur. La table n'a aucune association, le service Go `Macdos` n'a plus aucune interface pour l'appeler, et le besoin correspondant (l'ancien BF05) a été **retiré du dossier le 22/08**, en même temps que l'entité du dictionnaire de données. La phrase à dire : *« c'est un service hérité de l'outil autonome, qui n'a plus d'interface pour l'appeler — je l'ai sorti du périmètre annoncé plutôt que de le présenter comme livré. »*
> ⚠️ **Ne le cite jamais spontanément à l'oral** (le script te le rappelle en § 4.3). Mais si on te le montre, la seule mauvaise réponse est de faire semblant que c'est au périmètre : un périmètre annoncé qui correspond au périmètre réel vaut mieux qu'une fonctionnalité de plus.

146. **Trois stades, et un seul objet de validation par stade.** **Zoning** — découpage en zones fonctionnelles, une couleur par rôle, aucune décision visuelle ; valide l'architecture de l'information. **Wireframe** — boîtes grises et libellés, parcours annoté par des numéros ; valide la structure et le parcours. **Maquette abstraite** — barres grises, un seul accent, aucun texte réel ni icône ; valide la grille, le rythme, les espacements et la hiérarchie typographique. Chaque planche se termine par un bloc d'annotations qui fait le lien vers le composant React correspondant.
> **Les mockups haute fidélité ne sont pas un quatrième stade** : ce sont les **écrans finis**, montrés juste après la démarche (§ 3.2 bis du script). Ils existent bien dans `doc/mockups/` (`01-` à `05-`), mais les présenter comme un stade casserait le fil conducteur, qui est que **chaque stade retire de l'information plutôt que d'en ajouter**, pour ne valider qu'une chose à la fois.
> ⚠️ Le script dit explicitement « trois stades ». Si tu réponds « quatre », tu te contredis toi-même à dix minutes d'intervalle.

147. Précisément pour qu'on **ne puisse pas** valider autre chose. Sans contenu lisible, on ne discute ni du texte, ni des icônes, ni des couleurs — il ne reste que la grille, les espacements et la hiérarchie typographique. Et cette hiérarchie doit fonctionner **par la taille seule** : si elle tient sans mots, elle tiendra avec.

148. Depuis la même page que le traitement, `Convert_main.jsx`, et persisté par l'**API Python**. Cinq routes : `GET` et `POST /codes` chargent et enregistrent les trois mappings d'un bloc — c'est ce que fait l'écran de paramétrage —, et `/codecomptas`, `/codeother`, `/journal` permettent les mises à jour ciblées. Toutes passent par la validation du cookie `userId` (regex UUID puis vérification en base) avant tout accès.

149. Parce que **l'écran renvoie toutes les lignes**, y compris celles que l'utilisateur n'a pas remplies. Sans le filtre `if v and v.strip()`, un champ laissé vide écraserait une correspondance existante. La fusion `{**ucm.code_map, **filtered}` traduit la même intention : un enregistrement est une **mise à jour partielle**, jamais un remplacement complet — c'est ce qui permet de corriger un seul code sans ressaisir tous les autres.
> C'est le meilleur détail à commenter sur cet extrait : la décision vient d'un comportement réel de l'interface, pas d'un principe abstrait.

150. **Elles pourraient l'être, et c'est un défaut que j'assume** : elles ne diffèrent que par le modèle ORM et le nom de la colonne. Une seule fonction paramétrée par le modèle ferait le travail. Je ne l'ai pas fait parce que les trois ont été écrites à des moments différents, au fil des besoins — c'est de la dette technique classique, identifiée mais non remboursée.
> Ne cherche pas à défendre l'indéfendable : reconnaître une duplication vaut mieux que d'inventer une justification.

### Bloc 11

151. Par **observation directe puis restitution**. J'ai vu les comptables traiter les tirages à la main, j'ai creusé avec eux, et cinq difficultés concrètes sont ressorties. Je les ai traduites en besoins fonctionnels priorisés, présentés au cabinet, puis **revalidés à chaque fin d'itération par une démonstration** — six jalons de validation au total. C'est ce qui remplace le cahier des charges initial : le périmètre n'a pas été figé en amont, il a été confirmé par incréments. La contrepartie honnête : sans document contractuel, c'est la démonstration qui fait foi, donc il fallait démontrer souvent.

152. Importer **plusieurs fichiers `.EDI` en une seule opération** ; appliquer un **mapping de codes comptables paramétrable par client** ; **enregistrer et réutiliser** ses codes depuis la base ; **regrouper par restaurant et restituer un Excel** avec une feuille par restaurant. Les huit autres portent la plateforme : authentification, catalogue par droits, administration des comptes, catalogue d'applications, attribution des droits, analytics, présence temps réel, interface responsive.

153. Ce sont des **cibles posées avec le cabinet**, pas des mesures issues d'une campagne de charge — et je le dis tel quel. Les deux secondes viennent de l'usage réel (un traitement de tirages doit rester dans le temps d'attente acceptable au bureau) ; les 99,5 % hors maintenance viennent du fait que l'outil est utilisé en journée ouvrée, pas 24/7. **Aujourd'hui je ne les mesure pas** : c'est exactement ce que le monitoring Prometheus/Grafana, quatrième point de ma dette assumée, doit rendre observable. Un objectif non mesuré est un objectif déclaratif, autant l'assumer.

154. **Un serveur vierge.** C'est la seule chose qui m'ait été imposée côté infrastructure : il a fallu provisionner et configurer l'intégralité de l'environnement — système, sécurité, reverse proxy, base de données, orchestration. L'implication est double : d'une part **tout le reste de l'architecture relève de mes décisions**, donc chaque brique — Traefik, K3s, PostgreSQL, la conteneurisation — est un choix que je dois pouvoir défendre et pas une contrainte à subir ; d'autre part c'est la partie qui a demandé le plus de montée en compétence, en partant de zéro. *(Les deux autres contraintes sont métier : `.EDI` en entrée, Excel en sortie, non négociables ; plus HTTPS et les navigateurs modernes.)*

155. La preuve du suivi, ce sont les **six itérations jalonnées** avec leur durée, leur livrable, leur difficulté et son enseignement — c'est documenté dans le dossier, itération par itération — et l'**historique Git** en Conventional Commits, filtrable, avec une PR par fonctionnalité. Le carnet est l'outil de pilotage quotidien, pas la trace. À trois développeurs, le carnet ne tient plus : il faudrait un board partagé (Jira, GitHub Projects), une définition de « terminé » partagée et une revue de code réelle plutôt qu'une PR de confort — et là, les cérémonies Scrum reprendraient du sens.

156. Parce que **tant qu'il y a du visuel, on discute du visuel** — et on ne regarde plus le parcours. L'absence de couleur est ce qui force la conversation sur la seule chose que ce stade doit valider : la structure et l'enchaînement des écrans, annoté par des numéros. C'est le même principe qui fait que le stade suivant n'a pas de texte réel : **chaque stade retire de l'information pour ne laisser valider qu'une chose**.

157. 🔴 **Question dangereuse — la formulation du script est trop absolue, prépare la version exacte.** Ce qui est vrai : la suppression d'un compte efface bien ses sessions, ses droits, ses paramétrages comptables et son historique, **en une seule transaction**. Ce qui est faux si je le dis tel quel : que tout repose sur le schéma. En réalité c'est **mixte** — `events` et les trois tables de mapping portent un `ON DELETE CASCADE` réel, mais `sessions` et `user_application_permissions` ont une clé étrangère **sans cascade** : c'est `DeleteUser` qui les supprime explicitement, dans une transaction de six ordres, avec rollback si l'un échoue.
> **La formulation à adopter :** *« la suppression est atomique : une transaction supprime les droits, les sessions et les paramétrages puis le compte, et les cascades en base garantissent qu'aucune ligne ne peut survivre à son propriétaire. Le schéma et le code se couvrent mutuellement — la FK sans cascade fait d'ailleurs que la suppression du compte échouerait plutôt que de laisser des orphelins. »* C'est plus juste **et** plus fort que « ce n'est pas dans mon code ».
> ⚠️ **Deuxième piège dans la même question :** ma RG07 dit que « les événements d'audit survivent à la suppression du compte », alors que `events.uid` est en `ON DELETE CASCADE` — donc ils ne survivent pas. **Le code et la règle de gestion se contredisent.** Si on me le montre : *« vous avez raison, et c'est la règle qui a raison sur le code : un journal d'audit ne doit pas disparaître avec son sujet. Le correctif est un `ON DELETE SET NULL` avec conservation d'un identifiant pseudonymisé — ce qui préserve la traçabilité sans conserver de donnée personnelle, donc sans conflit avec le droit à l'oubli. »* **À arbitrer avant l'oral :** soit tu corriges le schéma, soit tu corriges RG07.

158. Elle devient un problème le jour où **le groupe porte de la donnée** — un libellé d'affichage, un ordre de tri, une icône, une politique de droits par groupe. Tant que c'est une étiquette lue telle quelle, la jointure ne rapporte rien et la référence faible suffit. Le signal d'alerte est le renommage : sans contrainte, renommer un groupe désynchronise silencieusement les lignes. **C'est précisément pour ça que la migration 003 pose la vraie clé étrangère, avec `ON UPDATE CASCADE`** — le renommage se propage. Autrement dit : la dénormalisation était assumée, et elle a été remboursée quand le besoin est apparu.

159. **Pénible en Go :** lire un fichier tabulaire aux encodages variables et produire un Excel multi-feuilles mis en forme — `pandas` et `xlsxwriter` font en quelques lignes ce qui demanderait beaucoup de code manuel et des bibliothèques Go moins matures sur les cas complexes. **Pénible en Python :** maintenir des dizaines de connexions WebSocket ouvertes en permanence et un middleware de session sollicité à chaque requête, avec des temps de réponse stables sous charge — c'est exactement le terrain des goroutines. Le critère n'est pas « quel langage je préfère », c'est **quelle charge de travail chaque service porte**.

160. Le premier signal, c'est **le passage à plus d'une instance du backend** — dès qu'on scale horizontalement, deux états en mémoire deviennent faux : les compteurs de rate limiting (chaque réplique aurait son propre seau, donc cinq essais **par instance**) et la liste des utilisateurs connectés du hub WebSocket. Les sessions, elles, sont déjà en base, donc déjà partagées. Ce que ça change dans le code : le seau à jetons et la map de présence passent derrière une interface, avec une implémentation Redis à la place de l'implémentation mémoire — **c'est justement le découplage par interface qui rend ce remplacement local**. Deuxième signal, plus lointain : une volumétrie d'événements analytics qui justifierait un store dédié.

161. 🔴 **C'est une incohérence de mon script, pas une question piège — corrige-la avant l'oral.** Il y a **cinq** domaines métier au périmètre : authentification, administration, applications, analyse, WebSocket. Le sixième dossier est `Macdos`, hérité de l'outil autonome, **sorti du périmètre** en même temps que l'ancien BF05 parce qu'aucune interface ne l'appelle. **Dis « cinq » à l'oral.** Si on te montre le sixième : *« c'est un service hérité de l'outil autonome, qui n'a plus d'interface pour l'appeler — je l'ai sorti du périmètre annoncé plutôt que de le présenter comme livré. »*

162. Honnêtement : **rien ne l'empêche techniquement**, c'est une convention structurelle, pas un verrou. Ce que le découpage change, c'est que la protection est **portée par le routeur et non par la route** : le développeur n'a pas à penser à ajouter un middleware, il a à choisir le bon sous-routeur — et une route d'administration placée dans `sys` échouerait au premier test manuel, puisque n'importe quel utilisateur authentifié y accéderait. On a déplacé le risque d'un oubli silencieux (middleware manquant sur une route) vers une erreur visible (mauvais groupe de routes). **C'est une réduction de risque, pas une garantie** — la garantie viendrait d'un test automatisé qui vérifie que toute route `/adm/*` renvoie 403 sans droits admin. C'est d'ailleurs un de mes scénarios E2E cibles, `rbac-01`.

163. L'asymétrie vient de l'outillage, pas d'un principe : **FastAPI génère la spécification OpenAPI depuis les annotations de type**, gratuitement, régénérée à chaque démarrage — la source unique de vérité est le code, aucune dérive n'est possible. Go n'a pas d'équivalent natif ; il aurait fallu ajouter un générateur à base d'annotations en commentaires (`swaggo`) et l'entretenir. **Ce que ça me coûte : une documentation Go qui peut dériver du code**, et c'est le seul endroit du projet où la documentation n'est pas dérivée de la source. Si le portail devait s'ouvrir à des intégrateurs externes, ce serait le premier chantier.

164. **Rien ne se passe : la requête est rejetée avant qu'aucun chemin ne soit construit.** La chaîne exacte est celle-là — la regex UUID stricte s'exécute **avant** le `os.path.join`, donc `../../etc/passwd` ne franchit jamais l'étape de validation, aucun répertoire de travail n'est créé, aucun fichier n'est lu ni écrit. C'est précisément l'ordre qui fait la sécurité : valider après avoir construit le chemin ne servirait à rien. Et côté Go, sur les **noms de fichiers uploadés**, j'applique la seconde parade, `filepath.Base()`, qui supprime toute composante de chemin. Deux surfaces différentes, deux parades adaptées.

165. **Coût technique :** trois tables avec une colonne `JSON` par type de mapping, des routes de lecture et d'écriture côté API Python, un écran de paramétrage côté React, et la logique de **mise à jour partielle** — les champs vides sont filtrés avant fusion pour qu'un champ laissé vide n'écrase pas une correspondance existante. **Changement pour les comptables : l'autonomie.** Avant, modifier un code voulait dire me le demander et attendre un déploiement ; après, chacun gère ses propres codes depuis l'interface. C'est le meilleur exemple du projet de retour utilisateur qui change une décision d'architecture : **l'itération 2 existe uniquement parce qu'ils ont dit que l'outil les rendait dépendants de moi.**

166. **Les connexions dans le temps**, jour par jour → décide si le portail est réellement adopté ou seulement installé. **L'usage par application** → décide où investir et quel outil on peut arrêter de maintenir ; c'est l'information la plus utile au cabinet, parce que personne ne savait quels outils servaient vraiment. **Les heures de pointe** → décide quand programmer une maintenance pour déranger le moins de monde. Chaque indicateur répond à une décision, sinon c'est de la décoration : c'est le manque de visibilité identifié au départ qui a dicté ces trois-là.

167. Elle va **jusqu'à la mise à disposition, pas jusqu'à l'outil**. Ce qu'on ajoute par l'interface, c'est une **entrée de catalogue** — nom, adresse, icône, groupe — et l'attribution des droits qui va avec : l'application apparaît immédiatement chez les utilisateurs concernés, sans redéploiement du portail. Ce qui n'est pas couvert : l'outil lui-même doit exister et être déployé quelque part, et s'il doit partager l'authentification du portail, il faut qu'il sache lire la session. La promesse exacte est donc : **le coût d'intégration d'un nouvel outil a été ramené à une saisie**, parce que l'authentification, les droits et le déploiement existent déjà — c'était le but de la centralisation.

168. Le déroulé complet : le hub WebSocket maintient en mémoire une `map` des utilisateurs connectés. Chaque connexion est gérée par sa propre **goroutine**, et plusieurs goroutines écrivaient et lisaient cette map simultanément — c'est une **data race** : deux accès concurrents dont au moins un en écriture, sans synchronisation, ce qui rend le comportement indéfini (résultat faux, ou panique du runtime). **Invisible en développement**, parce que seul un utilisateur se connectait à la fois ; elle ne se serait manifestée qu'en production, sous charge, de façon non reproductible. Elle a été détectée par **`go test -race`**, qui instrumente l'exécution pour repérer les accès non synchronisés. Le correctif est un **`sync.RWMutex`** : verrou exclusif pour `AddUser`/`RemoveUser`, verrou **partagé** en lecture pour les broadcasts — qui sont fréquents et parallélisables, d'où le `RWMutex` plutôt qu'un `Mutex` simple. La résolution a demandé plusieurs itérations pour éviter les **interblocages au broadcast** : diffuser en tenant le verrou en écriture bloquait tout le hub. **L'enseignement : la concurrence ne se teste pas à l'œil** — sans l'outil, ce bug partait en production.

169. Aujourd'hui la question ne se pose pas : **une lecture indexée par clé primaire, à l'échelle de quarante personnes, est indolore** — j'ai échangé de la performance dont je n'ai pas besoin contre du contrôle dont j'ai besoin, la révocabilité immédiate. Le seuil, ce n'est pas un nombre d'utilisateurs, c'est le moment où **la base devient le goulot** : plusieurs instances de backend tapant toutes sur PostgreSQL à chaque requête. La réponse à ce moment-là est **Redis** — les sessions y sont lues en mémoire, partagées entre instances, et restent révocables par suppression de clé. **Je garde la révocabilité, je change juste de magasin** : le JWT resterait le mauvais choix pour mon besoin.

170. Parce que **la mesure protège une ressource différente selon l'ordre**. bcrypt est volontairement lent, donc coûteux en CPU : c'est ce qui protège les mots de passe d'une attaque par essais massifs, mais c'est aussi ce qui fait du login une surface de **déni de service** — un attaquant qui envoie des milliers de tentatives sature le processeur du serveur, même si aucune ne réussit. Si le 429 était renvoyé **après** le calcul, le rate limiting protégerait les comptes mais pas le serveur : chaque requête refusée aurait quand même coûté un hachage complet. **En le renvoyant avant, une requête au-delà du quota coûte une consultation de compteur en mémoire, pas un bcrypt.** C'est la même leçon que la regex UUID : dans une défense, **l'ordre des étapes fait partie de la défense**.

171. **STRIDE** est un modèle d'analyse de menaces : **S**poofing (usurpation), **T**ampering (altération), **R**epudiation (répudiation), **I**nformation disclosure (divulgation), **D**enial of service (déni de service), **E**levation of privilege (élévation de privilège). L'intérêt par rapport à un simple parcours de l'OWASP Top 10 — que j'ai fait aussi, risque par risque — c'est qu'on raisonne **par surface d'exposition** plutôt que par liste de vulnérabilités. **Mes trois surfaces : (1) l'authentification** — usurpation par force brute (bcrypt lent + token bucket 5 essais / 1 jeton toutes les 30 s), divulgation par **énumération de comptes** (message d'erreur générique et unique, quelle que soit la cause de l'échec), déni de service (429 renvoyé **avant** tout calcul bcrypt) ; **(2) le traitement de fichiers** — **path traversal** (regex UUID avant toute construction de chemin, `filepath.Base` côté Go) et saturation du disque (nettoyage automatique à cinq minutes) ; **(3) le WebSocket** — **Cross-Site WebSocket Hijacking**, le handshake n'étant pas soumis à la politique de même origine, parade par liste blanche d'origines évaluée à chaque tentative d'upgrade.

172. Parce qu'ils **seront de toute façon visibles** en creusant le dossier, et que la façon dont une faiblesse apparaît change entièrement ce qu'elle démontre. Trouvée par le jury, c'est un angle mort. Annoncée par moi, classée par priorité et accompagnée du correctif, c'est une **décision de gestion de risque** : je sais ce qui n'est pas fini, je sais dans quel ordre le finir, et j'ai choisi de livrer ce qui apportait de la valeur plutôt que de tout retarder. Les quatre points : limite de tentatives de connexion définie mais pas active en production, en-têtes de sécurité spécifiés mais pas déployés, journalisation des échecs de connexion, politique de mot de passe plus stricte. Ce ne sont pas des découvertes, ce sont des lignes de backlog.

173. Ça m'empêche de garantir **le parcours complet, du clic au résultat, dans un vrai navigateur**. Mes tests unitaires prouvent que chaque fonction fait ce qu'elle doit, mes tests d'intégration que les composants s'assemblent — mais rien ne prouve automatiquement qu'un comptable qui se connecte, dépose un fichier et clique sur « télécharger » obtient bien son Excel. **C'est aujourd'hui couvert manuellement**, par une campagne de parcours avant chaque mise en production, avec de vrais fichiers anonymisés : donc la garantie existe, elle n'est simplement **pas automatisée**, donc pas rejouée à chaque commit. Le risque concret est une régression d'intégration qui passe la CI. L'outil est choisi (**Playwright**), les huit scénarios sont écrits, le job CI est prêt — **mais les tests ne sont pas développés, et je ne les présente pas comme livrés.**

174. En trois releases, jamais en une. **Release N :** on cesse d'écrire dans la colonne, le code ne la lit plus — la colonne existe toujours, donc la version N-1 continue de fonctionner, et un rollback applicatif est possible **sans toucher au schéma**. **Release N+1 :** on vérifie en production que plus rien ne l'utilise (logs, requêtes). **Release N+2 :** la migration de suppression est jouée, une fois qu'aucune version applicative encore déployable n'en dépend. Le principe qui gouverne tout ça : **le rollback applicatif est instantané, le rollback de données ne l'est pas** — Kubernetes ramène le code en une commande, mais les données ne reviennent pas en arrière. Donc on s'arrange pour ne jamais avoir besoin de rollback de schéma. En dernier recours, il reste la restauration depuis la sauvegarde quotidienne PostgreSQL — avec la perte de données que ça implique, ce qui est précisément ce qu'on cherche à éviter.

175. Parce que **les deux ne se décident pas de la même façon**. La dette assumée — sécurité, tests E2E, Redis, monitoring — ne rend pas le produit plus riche, elle le rend plus **solide** : c'est du risque connu, chiffrable, et la décision m'appartient techniquement. La nouvelle valeur — notifications, export PDF, tableau de bord personnalisable — ce sont de vraies fonctionnalités, mais **je ne les engage que si le besoin se confirme auprès des pôles** : les inscrire au dossier ne suffit pas à les justifier. Les mélanger dans une seule liste ferait croire qu'on peut arbitrer entre « sécuriser » et « ajouter une fonctionnalité » sur le même critère. **Et la sécurité passe en premier parce que c'est ce qui réduit le plus de risque pour le moins d'effort** — c'est le critère de tri, et c'est lui qui compte plus que la liste elle-même.

---

## Partie 7 — Questions posées en oral blanc (question → réponse)

> **Le bloc le plus proche du réel de toute la fiche** : ces trente questions ont été **réellement posées** lors d'oraux blancs. Contrairement aux parties 5 et 6, la réponse est **juste sous la question** — c'est fait pour être relu en boucle, pas pour être passé en interrogation.
> Deux profils s'y lisent nettement : le jury « académique » teste des **définitions générales** (bloc 12) ; le jury qui a lu ton dossier teste tes **arbitrages personnels** (bloc 13). Le second est plus dur, et c'est celui qui fait la note.
> **La règle qui vaut pour les trente :** définition courte et exacte d'abord (une à deux phrases), **puis** l'ancrage dans ton projet. Jamais l'inverse — un jury qui n'entend pas la définition suppose que tu ne l'as pas.

### Bloc 12 — Questions jury (définitions et généralités)

**176. « À qui est adressé le MCD, et à quoi sert-il d'un point de vue métier ? »**
> Le MCD est le **seul livrable de conception que le métier peut lire et valider**. Il est adressé conjointement à la maîtrise d'ouvrage — chez moi le commanditaire et les responsables de pôle — et à la maîtrise d'œuvre. Sa raison d'être est d'être **indépendant de tout SGBD** : on n'y parle ni de type de colonne, ni de clé étrangère, ni de PostgreSQL, mais d'entités, de propriétés et de **cardinalités**. C'est ce qui permet de poser au comptable une question qu'il peut trancher : *« un utilisateur peut-il accéder à plusieurs applications, et une application être attribuée à plusieurs utilisateurs ? »* — la réponse, oui des deux côtés, c'est un `(0,n)–(0,n)`, et c'est **une décision métier, pas technique**. D'un point de vue métier il sert donc à trois choses : **fixer le vocabulaire commun** (ce que j'appelle « utilisateur » désigne la même chose pour tout le monde), **valider les règles de gestion** avant d'écrire une ligne de code — c'est cent fois moins cher de corriger une cardinalité sur un schéma que sur une base en production —, et **servir de référence** quand on se demande plus tard pourquoi la base est faite ainsi.

**177. « C'est quoi une relation avec une cardinalité (1,1) ? »**
> Une cardinalité se lit **entité par entité** et donne le nombre minimum et maximum de fois qu'une occurrence de cette entité participe à l'association. **(1,1) signifie : chaque occurrence participe une fois et une seule** — ni zéro, ni deux. C'est donc à la fois une **obligation** (le minimum à 1 interdit l'existence isolée) et une **exclusivité** (le maximum à 1 interdit le partage).
> La conséquence conceptuelle est celle que vous visez : quand une entité est en (1,1), elle **ne peut pas exister sans l'autre** — c'est une **entité faible**, dont l'existence et souvent l'identité dépendent de l'entité forte. En traduction MLD, une association (1,1)–(0,n) fait descendre la clé étrangère du côté (1,1), avec une contrainte `NOT NULL` qui porte précisément cette obligation ; en (1,1)–(1,1), les deux entités fusionnent le plus souvent en une seule table, puisque rien ne les sépare.
> **Chez moi :** `sessions` est exactement ça — une session appartient à un utilisateur et un seul, et n'a aucun sens sans lui. Côté utilisateur c'est (0,n) : on peut être connecté sur plusieurs postes, ou pas connecté du tout. D'où `sessions.user_id NOT NULL` référençant `users(uid)`, et la suppression explicite des sessions dans `DeleteUser`.

**178. « Qu'est-ce qu'un ORM, et quelle est sa valeur ajoutée ? »**
> **Object-Relational Mapping** : une couche qui fait correspondre les **tables** d'une base relationnelle à des **classes** du langage, les lignes à des objets et les colonnes à des attributs. On manipule des objets, l'ORM génère le SQL.
> **Valeur ajoutée, dans l'ordre où je la constate :** (1) **la sécurité par défaut** — l'ORM produit des requêtes paramétrées, donc l'injection SQL devient l'exception qu'il faut délibérément provoquer plutôt que le défaut qu'il faut penser à éviter ; (2) **la portabilité** — le même modèle tourne sur PostgreSQL en production et sur SQLite en mémoire dans mes tests, ce qui est exactement ce qui me permet d'exécuter ma suite pytest sans provisionner de base ; (3) **une source unique de vérité** — le schéma est décrit une fois, dans les modèles ; (4) **la productivité** sur le CRUD répétitif.
> **Et son coût, que j'assume :** une couche d'abstraction de plus, un risque de requêtes inefficaces qu'on ne voit pas (le N+1), et une performance moindre sur les requêtes complexes.
> **Mon choix est asymétrique et c'est délibéré : SQLAlchemy 2.0 côté Python, pas d'ORM côté Go.** Le Go utilise `database/sql` avec le driver `lib/pq` et des requêtes paramétrées écrites à la main. La raison : côté Python je fais du CRUD sur des modèles stables, l'ORM est un gain net ; côté Go je suis sur le chemin chaud — vérification de session à chaque requête — avec des requêtes courtes que je veux lire telles qu'elles s'exécutent. **Le pattern Repository me donne déjà le découplage** que l'ORM apporterait, sans la couche d'abstraction : si je change de source de données, je change le Repository, pas le Service.

**179. « Citez-moi trois attaques courantes et le moyen de les contrer. »**
> **1. L'injection SQL.** Une entrée utilisateur est concaténée dans une requête et interprétée comme du SQL — `' OR 1=1 --` dans un champ email fait tomber l'authentification. **La parade est unique et absolue : les requêtes paramétrées.** La valeur n'est jamais concaténée, elle est transmise séparément au moteur, qui la traite comme une donnée et jamais comme du code. Chez moi : `database/sql` côté Go, SQLAlchemy côté Python. **Aucune concaténation de chaîne dans une requête, nulle part.**
> **2. Le XSS** (Cross-Site Scripting). Un attaquant fait exécuter du JavaScript dans le navigateur d'un autre utilisateur — typiquement pour voler son cookie de session. Trois formes : stocké (en base, servi à tous), réfléchi (renvoyé dans la réponse), DOM. **La parade : l'échappement systématique à l'affichage**, que React fait nativement — tout ce qu'on interpole en JSX est échappé, sauf si on force `dangerouslySetInnerHTML`, que je n'utilise pas. La seconde ligne est une **Content-Security-Policy** qui interdit l'exécution de script inline — elle est **spécifiée dans mon dossier, pas encore déployée**, et je le dis comme tel.
> **3. Le CSRF** (Cross-Site Request Forgery). Un site tiers déclenche une action authentifiée à l'insu de l'utilisateur, en profitant du fait que le navigateur envoie automatiquement le cookie de session. **La parade : `SameSite=Strict` sur le cookie**, qui empêche le navigateur de l'envoyer sur une requête initiée depuis un autre domaine, doublée d'une **vérification `Origin`/`Referer` côté serveur** sur les requêtes non-GET.
> *(Si le jury en veut une quatrième, la plus intéressante de mon dossier est le **CSWSH** — Cross-Site WebSocket Hijacking : le handshake WebSocket **n'est pas soumis à la politique de même origine**, donc un site tiers peut ouvrir une connexion avec le cookie de la victime. Parade : une allowlist d'origines évaluée à chaque tentative d'upgrade dans `CheckOrigin`.)*

**180. « C'est quoi les CORS, et quel côté de l'application protègent-elles ? »**
> **Attention, c'est une question piège, et le piège est dans le mot « protègent ».** CORS — *Cross-Origin Resource Sharing* — **ne protège pas le serveur. Il protège l'utilisateur, et il est appliqué par le navigateur.**
> Le mécanisme réel : par défaut, un navigateur applique la **politique de même origine** — une page servie par `site-a.fr` ne peut pas lire la réponse d'une requête vers `site-b.fr`. CORS est le protocole qui permet au serveur de **lever sélectivement** cette restriction, en répondant `Access-Control-Allow-Origin` avec la liste des origines autorisées. Pour les requêtes non simples, le navigateur envoie d'abord une **requête de pré-vol** `OPTIONS`, et n'envoie la vraie requête que si la réponse l'autorise.
> **Ce qu'il faut dire clairement au jury :** c'est un **assouplissement contrôlé**, pas une barrière. Un attaquant avec `curl` ou Postman ignore totalement CORS — aucun navigateur, aucune politique. **CORS n'a jamais remplacé l'authentification et l'autorisation côté serveur** : chez moi, c'est `AuthMiddleware` et `AdminMiddleware` qui protègent le serveur, CORS protège le navigateur de mes utilisateurs contre un site tiers qui voudrait lire mes réponses avec leur cookie.
> **Mon implémentation :** une **allowlist** dans `backend/internal/middleware/cors.go`, pilotée par `CORS_ORIGIN` — jamais `Access-Control-Allow-Origin: *`, qui est de toute façon incompatible avec `credentials: include`, et l'allowlist s'applique aussi au WebSocket via `CheckOrigin`.
> **Anecdote à sortir si on creuse :** en itération 5, un typo dans la configuration CORS de préproduction a bloqué **toutes** les requêtes authentifiées. Ce que j'en ai retiré : lire méthodiquement l'erreur CORS du navigateur plutôt que modifier la configuration au hasard — le message dit exactement quelle origine a été refusée.

**181. « À quoi sert votre diagramme de séquence ? »**
> Un diagramme de séquence décrit la **chronologie des échanges** entre participants pour **un scénario précis** — l'axe vertical est le temps, chaque participant a une **ligne de vie**, chaque flèche est un message. Là où le diagramme de classes montre une **structure figée**, le diagramme de séquence montre un **comportement dans le temps** : les deux sont complémentaires, et c'est ce qu'il faut dire si on vous demande pourquoi les deux.
> **Ce qu'il m'a réellement servi à faire — et c'est ça que le jury attend, pas la définition :** il rend visible **l'ordre des étapes**, et dans mon cas l'ordre *est* la sécurité. Sur l'authentification, on lit que la session est créée **après** la vérification bcrypt, et que le cookie est posé **après** la création de la session. Sur la conversion EDI, on lit que la **validation UUID de l'identifiant précède toute construction de chemin de fichier** — c'est précisément ce qui bloque le path traversal, et c'est un ordre, pas un contrôle. Sur le WebSocket, on lit que la vérification d'origine intervient **avant l'upgrade**, pas après.
> **J'en ai trois :** authentification, conversion EDI, connexion WebSocket. Je peux dérouler celui de l'authentification message par message : `POST /sys/login` → Handler (parse et valide) → Service → Repository (`SELECT` paramétré sur l'email) → `bcrypt.CompareHashAndPassword` → création de session en base → pose du cookie → `200`. Et sur le chemin d'échec : **un message d'erreur générique unique**, quelle que soit la cause — email inconnu ou mot de passe faux — pour ne pas permettre l'énumération de comptes.

**182. « Qu'est-ce qu'un JWT, et à quoi sert-il ? »**
> **JSON Web Token** : un jeton **auto-porteur et signé**, en trois parties séparées par des points — un *header* (algorithme), un *payload* (les revendications : identifiant, rôle, date d'expiration `exp`) et une **signature** cryptographique. Les deux premières parties sont en **Base64URL, donc lisibles par n'importe qui** — un JWT n'est pas chiffré, seulement signé. La signature garantit l'**intégrité** : si un attaquant modifie `"role": "user"` en `"role": "admin"`, la signature ne correspond plus et le serveur rejette le jeton.
> **À quoi il sert :** à authentifier **sans état côté serveur**. Le serveur n'a rien à stocker ni à consulter : il vérifie la signature avec sa clé et fait confiance au contenu. C'est ce qui le rend excellent pour les architectures **distribuées et multi-instances** — n'importe quelle instance valide n'importe quel jeton, sans base partagée.
> **Sa faiblesse structurelle, et c'est le cœur de ma réponse : un JWT n'est pas révocable.** Tant qu'il n'a pas expiré, il est valide — un compte supprimé, un rôle rétrogradé, un jeton volé restent exploitables jusqu'à l'expiration. Les contournements existent (durée très courte + *refresh token*, liste de révocation) mais **la liste de révocation réintroduit exactement l'état côté serveur que le JWT prétendait supprimer**.
> **Mon choix est l'inverse, et je l'assume : session opaque en base.** Un UUID sans signification stocké côté serveur, coût d'une lecture indexée par clé primaire à chaque requête. J'ai échangé une performance dont je n'ai pas besoin — quarante utilisateurs internes — contre un contrôle dont j'ai besoin : **la révocabilité immédiate**. Un `DELETE` sur une ligne coupe l'accès à la seconde suivante.
> ⚠️ **Sois prêt sur la suite immédiate :** mon besoin **BF05 dit « authentification sécurisée (JWT) »** alors que ma réalisation dit « pas de JWT côté client ». Voir la question 2 de la partie 4 — c'est la contradiction la plus visible du dossier.

**183. « Qu'est-ce que le Product Owner ? »**
> Le **Product Owner** est, dans Scrum, le **responsable de la valeur du produit**. Il porte la voix du métier et des utilisateurs auprès de l'équipe de développement. Concrètement, trois responsabilités : il **détient et priorise le backlog** — c'est lui qui décide de l'ordre, et cette décision lui appartient seul ; il **définit le « quoi » et le « pourquoi »**, jamais le « comment », qui reste à l'équipe ; et il **accepte ou refuse** les incréments livrés en fin de sprint. C'est un rôle à **une seule personne** — un PO partagé entre plusieurs personnes produit des priorités contradictoires.
> **Ce qu'il n'est pas**, et c'est souvent ce que le jury vérifie : ni un chef de projet (il n'affecte pas les ressources ni les délais), ni un rédacteur de spécifications, ni le supérieur hiérarchique de l'équipe.

**184. « C'est quoi un Scrum Master ? »**
> Le **Scrum Master** est le **garant du cadre Scrum et le facilitateur de l'équipe**. Trois responsabilités : il **fait respecter le cadre** — les événements, les artefacts, la définition de « terminé » ; il **lève les obstacles** qui ralentissent l'équipe, qu'ils soient techniques ou organisationnels ; et il **protège l'équipe** des sollicitations extérieures pendant le sprint.
> Sa posture, c'est le point qui distingue une bonne réponse : c'est un **leadership de service**, pas d'autorité. **Il n'est le chef de personne, il n'attribue pas les tâches** — c'est l'équipe qui s'auto-organise — et il ne décide pas des priorités, qui appartiennent au PO.
> **La distinction à énoncer nettement : le PO décide *quoi* construire et dans quel ordre, le Scrum Master veille à *comment* l'équipe travaille, l'équipe de développement décide *comment* c'est construit techniquement.**

**185. « Pouvez-vous citer le nom d'un rôle clé de la méthode agile ? »**
> Scrum en définit **trois, et trois seulement** : le **Product Owner** (la valeur et la priorisation), le **Scrum Master** (le cadre et la facilitation), et l'**équipe de développement** — pluridisciplinaire, auto-organisée, typiquement de trois à neuf personnes, et **collectivement responsable** de l'incrément livré. L'ensemble forme la *Scrum Team*.
> **Le piège à éviter absolument : « chef de projet » n'est pas un rôle agile.** C'est précisément ce que Scrum a supprimé, en répartissant ses attributions entre les trois rôles — la priorisation au PO, la levée d'obstacles au Scrum Master, l'organisation du travail à l'équipe.
> **Et pour moi :** ces trois rôles supposent une équipe. **Seul, je les ai portés tous les trois**, ce qui vide les cérémonies de leur sens — d'où mon choix de Kanban, expliqué en question 191.

**186. « Avez-vous un droit de jugement sur la charte graphique fournie par le client ou le PO ? »**
> **La réponse honnête est : pas un droit de veto, mais un devoir d'alerte** — et c'est cette distinction qui compte.
> **Ce qui relève du client, sans discussion :** l'identité visuelle, les couleurs de marque, la typographie, le ton. Ce n'est pas mon domaine, et mon goût personnel n'est pas un argument professionnel. Sur ces points, je m'exécute.
> **Ce sur quoi j'ai un devoir professionnel de signaler, même si on ne me le demande pas :** l'**accessibilité**. Si la charte impose un gris clair sur blanc qui descend sous un ratio de contraste de **4.5:1**, ce n'est plus une question de goût — c'est un **critère RGAA 4**, la déclinaison française des WCAG 2.1, et l'accessibilité numérique est une **obligation légale** pour de nombreuses structures. Même chose pour l'information portée par la couleur seule, illisible pour un daltonien, ou pour une taille de police sous le seuil de lisibilité. Là, je ne juge pas : **je documente l'écart, j'explique le risque, et je propose une variante conforme qui reste fidèle à la charte** — un contraste renforcé sans changer la teinte, par exemple.
> **La formulation qui marche :** *« la charte, c'est la décision du client ; la conformité, c'est ma responsabilité professionnelle. Je ne discute pas la première, mais je ne peux pas livrer en silence quelque chose que je sais non conforme — et si le client maintient son choix après mon alerte, c'est sa décision, elle est tracée, et je livre. »*
> **Dans mon cas concret :** il n'y avait pas de charte imposée, je l'ai proposée et fait valider par le commanditaire — et j'ai intégré les critères RGAA dès le maquettage Figma plutôt qu'en correction après coup.

**187. « Comment avez-vous géré la sécurité du transfert des documents ? »**
> Je la découpe en **quatre temps, parce que le transfert n'est qu'un des quatre** — et c'est le découpage qui fait la qualité de la réponse.
> **1. En transit.** **HTTPS/TLS de bout en bout**, terminé par Traefik avec des certificats Let's Encrypt renouvelés automatiquement. Aucun document ne circule en clair, et `Strict-Transport-Security` est dans ma stratégie d'en-têtes pour interdire toute retombée en HTTP.
> **2. À l'entrée — l'autorisation avant le traitement.** L'API Python **valide le cookie de session avant tout traitement de fichier** : on ne dépose pas un fichier anonymement. Puis l'identifiant utilisateur passe une **expression régulière UUID stricte** — et cette validation intervient **avant toute construction de chemin**, ce qui est le point clé : un `../../etc/passwd` envoyé comme identifiant ne franchit pas la regex, il est rejeté en `400` avant qu'`os.path.join` soit appelé. Le **nom du fichier** est réduit à son composant final par `Path(filename).name` — un chemin relatif ne survit pas —, l'**extension est filtrée** en allowlist, et la taille est plafonnée à **50 Mo** au niveau de Nginx.
> **3. Au repos — et c'est mon meilleur argument.** Les fichiers ne sont **pas stockés durablement**. Chaque utilisateur a un répertoire temporaire **isolé, nommé par son UUID** : deux utilisateurs ne partagent jamais de répertoire, et aucun ne peut nommer celui d'un autre puisque le chemin est construit à partir de son identifiant de session validé, jamais d'un paramètre de requête libre. Aucun de ces fichiers n'est exposé par une URL publique — il n'existe **aucune route qui serve un fichier par son nom**.
> **4. Après — la suppression.** C'est **RG08** : les fichiers sont éphémères. Le nettoyage est programmé en tâche de fond avec `CLEANUP_DELAY_SECONDS = 300`, soit **cinq minutes après le traitement**, et le répertoire entier est supprimé par `shutil.rmtree`. **La meilleure protection d'une donnée, c'est de ne pas la conserver** — et ça sert aussi la limitation de conservation du RGPD.
> **Ce que j'assume :** les fichiers ne sont **pas chiffrés au repos** pendant ces cinq minutes. Vu qu'ils vivent cinq minutes sur un volume qui n'est monté que par le pod de l'API, l'arbitrage est assumé ; le jour où on traiterait des données plus sensibles, le chiffrement au niveau du volume est la réponse, pas le chiffrement applicatif.

**188. « Les tests unitaires, ça sert à quoi ? »**
> Un test unitaire vérifie **une unité de code isolée** — une fonction, une méthode — **sans ses dépendances réelles**, qui sont remplacées par des mocks. Il doit être **rapide** (millisecondes), **déterministe** (même résultat à chaque exécution) et **indépendant** des autres tests.
> **Ce qu'il apporte, dans l'ordre de ce que j'ai réellement constaté :** (1) **la non-régression** — c'est le premier bénéfice, pas la détection de bugs : ils me disent qu'une modification n'a rien cassé ailleurs, et c'est ce qui rend un refactoring possible sans peur ; (2) une **documentation exécutable** — un test lisible montre comment la fonction est censée être appelée et ce qu'elle retourne aux limites, et **cette documentation ne peut pas mentir**, puisqu'elle échoue si elle devient fausse ; (3) une **pression sur la conception** — du code difficile à tester est presque toujours du code mal découpé : c'est ce qui m'a poussé à extraire des **interfaces** et à garder mes utilitaires Python **purs**, sans effet de bord ; (4) un **retour rapide**, en secondes plutôt qu'après un déploiement.
> **Leur limite, à énoncer soi-même :** ils prouvent que chaque pièce fonctionne, **jamais que l'assemblage fonctionne**. D'où la **pyramide** : une large base d'unitaires, une couche d'intégration, et quelques E2E. **Et la couverture de code est un indicateur, pas un objectif** — 100 % de couverture avec des assertions faibles ne prouve rien.
> **Chez moi :** `testify` + `sqlmock` côté Go sur onze fichiers, avec `go test -race` sur le WebSocket — c'est lui qui a détecté la data race du hub ; **84 tests pytest** côté Python, dont 72 au vert aujourd'hui, les douze restants échouant sur un **préfixe de route obsolète dans le fichier de test** ; **29/29 Vitest** côté frontend. **L'étage E2E manque** : Playwright est choisi, les huit scénarios sont écrits, les tests ne sont pas développés — je ne les présente pas comme livrés.

**189. « Que veut dire CI/CD, et à quoi ça sert ? »**
> **CI = Intégration Continue.** À chaque push, une chaîne automatisée récupère le code, le compile, exécute les tests et le linter. L'objectif est de **détecter une régression en minutes plutôt qu'en semaines**, et surtout d'éviter le *merge hell* — l'intégration douloureuse de branches qui ont divergé pendant un mois. **Un échec de CI bloque la pull request** : c'est ce qui fait de la qualité une contrainte automatique plutôt qu'une intention.
> **CD = Déploiement Continu** (ou Livraison Continue — la nuance vaut d'être citée : la *livraison* rend chaque version **déployable** en un clic, le *déploiement* la met en production **automatiquement**). L'objectif : rendre la mise en production **banale, reproductible et fréquente**. Un déploiement rare est un déploiement risqué, parce qu'il embarque des centaines de changements — quand il casse, on ne sait pas lequel.
> **Ma chaîne :** push sur `main` → tests unitaires Go → build d'image Docker **multi-stage** → push vers le registre → déploiement par SSH vers le cluster K3s et `kubectl rollout restart`. Le rolling update de Kubernetes fait la bascule **sans coupure**, et conserve l'historique des ReplicaSets — donc **le rollback est une commande**.
> **Le lien avec mes tests, à faire explicitement :** c'est précisément pour bénéficier de la CI que **j'ouvre une pull request même seul**. Sans CI, une PR solo n'est qu'un rituel ; avec CI, c'est un point de contrôle automatisé que je ne peux pas contourner un soir de fatigue.

**190. « C'est quoi l'OWASP ? »**
> **Open Worldwide Application Security Project** : une **fondation à but non lucratif**, communautaire et indépendante des éditeurs, qui produit de la documentation, des outils et des standards **libres** sur la sécurité applicative. Ce n'est **ni une norme légale, ni une certification** — c'est une référence de place, mais c'est *la* référence : elle est citée par le RGPD dans son état de l'art, par l'ANSSI et par les référentiels d'audit.
> **Son livrable le plus connu est le Top 10** : le classement des dix catégories de risques applicatifs les plus critiques, révisé tous les trois à quatre ans à partir de données réelles. Dans la version 2021 : **A01 Broken Access Control** — passé numéro un, ce qui est significatif —, A02 Cryptographic Failures, A03 Injection, A04 Insecure Design, A05 Security Misconfiguration, A06 Vulnerable Components, A07 Identification and Authentication Failures, A08 Software and Data Integrity Failures, A09 Security Logging and Monitoring Failures, A10 SSRF.
> **Mais l'OWASP ne se réduit pas au Top 10**, et le dire vaut des points : il produit aussi l'**ASVS** (le standard de vérification, bien plus détaillé), les **Cheat Sheets**, le **SAMM** (modèle de maturité) et des outils comme **ZAP** ou **Dependency-Check**.
> **Chez moi :** le Top 10 est parcouru **risque par risque** dans un tableau du dossier, avec la mesure et son **statut réel**. Deux points ne sont pas au vert et je les annonce : **A06** (composants vulnérables) est « à vérifier » — Dependabot est en place, un scan de dépendances systématique en CI reste à formaliser — et **A09** (journalisation) est « à renforcer ». **A10 SSRF est sans objet**, l'application ne construisant aucune requête sortante à partir d'une entrée utilisateur : il n'y a pas de surface. *(⚠️ Il est écrit « non implémenté » dans le dossier remis — c'est une maladresse de rédaction à corriger, voir question 9 de la partie 4.)*

**191. « Quelles sont les opérations fondamentales sur une base de données ? »**
> **Les quatre du CRUD** — *Create, Read, Update, Delete* — qui correspondent en SQL à **`INSERT`, `SELECT`, `UPDATE`, `DELETE`**, et en REST à `POST`, `GET`, `PUT`/`PATCH`, `DELETE`. C'est la réponse attendue.
> **Ce qui fait la différence, c'est la précision derrière.** Le SQL se divise en sous-langages : le **DML** (*Data Manipulation Language*) porte le CRUD ; le **DDL** (*Definition*) crée et modifie les structures — `CREATE`, `ALTER`, `DROP` ; le **DCL** (*Control*) gère les droits — `GRANT`, `REVOKE` ; le **TCL** (*Transaction Control*) délimite les transactions — `BEGIN`, `COMMIT`, `ROLLBACK`.
> **Et le point que j'ajouterais :** ces quatre opérations n'ont d'intérêt que **groupées en transactions**. Créer un utilisateur puis lui attribuer ses applications, ce sont deux `INSERT` qui doivent réussir ou échouer **ensemble** — sinon on obtient un compte sans droits. C'est l'**atomicité**, le A d'ACID, et c'est une des raisons de mon choix de PostgreSQL. Ma suppression d'utilisateur est le cas typique : `DeleteUser` efface droits, sessions et mappings **dans une seule transaction**, et les `ON DELETE CASCADE` complètent le nettoyage au niveau du schéma.

---

### Bloc 13 — Questions personnelles (arbitrages de ton projet)

> ⚠️ **Ces quinze-là sont les plus dures de toute la fiche**, parce qu'elles ne testent pas une définition : elles testent si **ta décision tient debout**. La structure gagnante est toujours la même — *ce que j'ai fait* → *pourquoi, dans mon contexte* → *ce que ça coûte* → *à partir de quand j'en changerais*. Le quatrième temps est celui que la plupart des candidats oublient, et c'est celui qui prouve que le choix était un arbitrage et pas un défaut.

**192. « Vous dites ne pas avoir eu de Product Owner sur ce projet ? »**
> **Pas de Product Owner au sens Scrum du terme, non — mais la fonction a bien été remplie, et elle a été répartie.** Le rôle formel suppose une équipe ; la fonction, elle, existe dans tout projet : quelqu'un doit décider **quoi construire et dans quel ordre**.
> Concrètement : **le commanditaire — l'expert-comptable associé — jouait le rôle de sponsor et d'arbitre métier.** C'est lui qui a validé le périmètre, et c'est lui qui a tranché la seule vraie question de priorisation du projet : **livrer d'abord l'outil de tirages de caisse en autonome, avant la plateforme**, parce que c'est là qu'était la douleur immédiate. Cette décision n'est pas la mienne, elle est la sienne, et elle a structuré tout le séquencement du projet. **Les responsables de pôle** étaient mes utilisateurs de référence : chacune de mes six itérations se terminait par une démonstration, et leurs retours alimentaient le backlog de l'itération suivante — l'itération 2 est **entièrement** issue des retours sur l'itération 1.
> **Ce que je portais moi**, et c'est là qu'il faut être honnête : la **traduction** de ces besoins en douze besoins fonctionnels, cinq besoins non fonctionnels et neuf règles de gestion, la priorisation fine au sein d'une itération, et l'acceptation technique.
> **La limite que je reconnais :** être à la fois celui qui définit le besoin et celui qui le réalise, c'est **être juge et partie** — on se donne inconsciemment des besoins qu'on sait faire. Ce qui m'a protégé, c'est la démonstration en fin de chaque itération : **un utilisateur devant l'écran, ça ne se négocie pas.**
> **La phrase de sortie :** *« je n'avais pas de PO parce qu'il n'y avait pas d'équipe. Mais la décision de priorité venait du métier, pas de moi — et c'est ça, la fonction du PO. »*

**193. « Vous choisissez Go pour sa concurrence — pourquoi ne pas avoir utilisé l'asynchrone de Python ? »**
> **Commençons par corriger la prémisse : je l'utilise.** Mon API Python est en **FastAPI sur ASGI**, avec des routes `async` et des tâches de fond `asyncio` — c'est littéralement une `BackgroundTask` asynchrone qui programme le nettoyage des fichiers à cinq minutes. **La question n'est donc pas Go *contre* Python asynchrone : c'est pourquoi chaque service utilise le modèle qui correspond à sa charge.**
> **Les deux modèles ne résolvent pas le même problème.** L'`asyncio` de Python est une **concurrence coopérative sur un seul thread** : une boucle d'événements bascule d'une tâche à l'autre **aux points `await`**, c'est-à-dire uniquement quand une tâche attend une I/O. Le modèle est excellent pour ça. Mais il a deux conséquences : **une tâche qui ne rend pas la main bloque tout** — un calcul de plusieurs centaines de millisecondes gèle la boucle entière —, et à cause du **GIL**, un seul thread Python exécute du bytecode à la fois : **pas de parallélisme réel sur plusieurs cœurs**.
> Les **goroutines** de Go sont d'une autre nature : préemptives, **multiplexées par le runtime sur plusieurs threads système**, donc réellement parallèles sur plusieurs cœurs, quelques kilo-octets de mémoire initiale contre plusieurs mégaoctets pour un thread OS. **Un blocage dans une goroutine ne gèle pas les autres.**
> **Ce qui a tranché, concrètement, c'est mon hub WebSocket.** Il maintient des **dizaines de connexions simultanées, persistantes, avec un état partagé mutable** — la map des utilisateurs connectés. C'est le cas où la différence est structurelle : Go m'a donné un modèle réellement parallèle, une **synchronisation explicite par `sync.RWMutex`**, et surtout **`go test -race`**, un détecteur de courses à l'exécution qui n'a pas d'équivalent en Python — c'est lui qui a trouvé ma data race, invisible en développement puisqu'un seul utilisateur se connectait à la fois. **En Python asynchrone, ce bug n'aurait pas existé sous cette forme — le mono-thread le rend impossible — mais je n'aurais pas eu le parallélisme non plus.** Ajoutons ce qui n'est pas de la concurrence : **typage statique fort** sur le cœur transactionnel, et **binaire unique sans runtime**, donc une image Docker minimale.
> **Et le corollaire, qui montre que le raisonnement n'est pas un réflexe :** pour l'API de traitement de fichiers, j'ai fait le choix inverse. La charge y est de l'I/O et du calcul tabulaire, `pandas` et `xlsxwriter` sont sans rival, et **les bibliothèques Go ne sont pas assez matures pour certains cas de parsing complexes**. J'ai pris Python, et son asynchrone, en connaissance de cause.

**194. « Qu'est-ce qu'un EDI ? »**
> **Le sigle a deux sens, et il faut lever l'ambiguïté avant de répondre** — c'est d'ailleurs souvent ce que le jury teste.
> **Sens 1, celui de mon projet — Échange de Données Informatisé** (*Electronic Data Interchange*) : la transmission de documents commerciaux entre systèmes d'information dans un **format structuré et normalisé**, sans ressaisie humaine. Les normes historiques sont **EDIFACT** (ONU, international) et **X12** (Amérique du Nord) ; le principe est un fichier segmenté, chaque segment identifié par un code, chaque ligne portant des données à position fixe ou séparées par un délimiteur. **C'est exactement mon cas d'usage :** les logiciels de caisse des restaurants exportent leurs tirages en fichiers `.EDI`, et mon outil les parse, les consolide et produit un Excel pour les comptables — ce qui remplaçait une **ressaisie manuelle, restaurant par restaurant**. **La difficulté réelle de l'itération 1 est là :** les fichiers du monde réel ne respectent pas la norme — **encodages variables (ISO-8859-1 ou UTF-8) et segments optionnels absents**. Il a fallu rendre le parsing tolérant **sans masquer les vraies erreurs** : c'est un équilibre, pas un `try/except` global.
> **Sens 2 — Environnement de Développement Intégré**, la traduction française d'*IDE* : un logiciel réunissant éditeur, compilateur, débogueur, intégration Git et complétion dans une seule interface. J'utilise **VS Code**, avec les extensions Go, Python et ESLint/Prettier.
> **La réponse à donner :** *« dans mon dossier, EDI désigne l'Échange de Données Informatisé — le format des fichiers de caisse. Si vous parlez de l'Environnement de Développement Intégré, c'est VS Code. »* **Poser la question du sens est une bonne réponse en soi.**

**195. « Quel est le nom officiel de la liste des règles de sécurité d'une application ? »**
> **L'OWASP Top 10** — la référence de place pour les dix catégories de risques applicatifs les plus critiques, publiée par l'*Open Worldwide Application Security Project*, version courante 2021, révisée tous les trois à quatre ans à partir de données réelles.
> **Et si on veut être précis sur le mot « règles », la meilleure réponse est l'OWASP ASVS** — *Application Security Verification Standard* : **c'est littéralement une liste de règles vérifiables**, plusieurs centaines d'exigences réparties en trois niveaux d'exigence croissante. Le Top 10 est une **liste de risques** faite pour sensibiliser ; l'ASVS est une **liste d'exigences** faite pour auditer. **Faire cette distinction, c'est ce qui sépare une bonne réponse d'une réponse récitée.**
> **Selon le contexte, deux autres noms peuvent être attendus :** en France, les **guides d'hygiène informatique et recommandations de l'ANSSI** ; et pour les données personnelles, le **RGPD** — qui n'est pas une liste technique mais un règlement, et qui renvoie justement à l'« état de l'art », donc à l'OWASP.
> **Chez moi :** le Top 10 est parcouru risque par risque dans un tableau du dossier, et je l'ai complété par une analyse **STRIDE** sur trois surfaces — l'authentification, le traitement de fichiers, le WebSocket. Les deux sont complémentaires : le Top 10 raisonne **par vulnérabilité**, STRIDE **par surface d'exposition**.

**196. « Vous n'avez fait que des maquettes, au niveau de la conception visuelle ? »**
> **Non — j'ai suivi trois stades successifs, et chacun valide quelque chose de différent. Les confondre, c'est perdre l'intérêt de la démarche.**
> **1. Les wireframes** — la **structure seule**, sans style : où se place l'information, quel est le parcours, dans quel ordre l'utilisateur rencontre les éléments. On valide **l'organisation**, et on la valide vite parce qu'un wireframe se jette sans regret.
> **2. Les maquettes basse fidélité, volontairement en niveaux de gris.** C'est le stade que le jury interroge le plus, et la réponse est nette : **l'absence de couleur est délibérée**. Tant qu'il y a de la couleur, tout retour d'utilisateur porte sur la couleur — et pendant ce temps, personne ne dit que le bouton d'action est au mauvais endroit. **Retirer le style force la discussion sur la hiérarchie de l'information**, et c'est précisément ce qu'on veut valider à ce stade.
> **3. Les maquettes haute fidélité** — la charte graphique appliquée : couleurs, typographie, iconographie, états des composants, mode clair et mode sombre. On valide **le rendu final**, une fois la structure acquise.
> **Le tout sous Figma**, avec les critères **RGAA 4** intégrés dès le maquettage plutôt qu'en correction après coup : contraste ≥ 4.5:1, hiérarchie de titres, labels de formulaire, navigation clavier.
> **Ce que je n'ai pas fait, et je le dis :** pas de **prototype cliquable** complet — Figma le permet, je ne l'ai pas industrialisé —, et pas de tests utilisateurs formalisés avec protocole. **Ce qui les a remplacés : la démonstration au commanditaire en fin de chacune des six itérations**, sur l'application réelle. Sur un projet interne à quarante utilisateurs accessibles, **le retour sur l'application qui tourne vaut mieux qu'un prototype**, parce qu'il porte sur ce qui existe vraiment. Sur un produit destiné à des utilisateurs inaccessibles, j'aurais tranché l'inverse.
> ⚠️ **Piège à éviter : trois stades, pas quatre.** Ne présente pas les captures d'écrans finis comme un quatrième stade de maquettage — ce sont les **écrans livrés**, pas une maquette.

**197. « On peut revenir sur le MCD, s'il vous plaît ? »**
> **Ce n'est pas une question, c'est une invitation à dérouler — et c'est une bonne nouvelle.** Ne récite pas les huit entités : **raconte le modèle**, du centre vers l'extérieur, en nommant les cardinalités et en justifiant chaque décision.
> **Le déroulé en trois cercles :**
> **Le cœur** — trois entités et une association. `Utilisateur`, `Application`, et entre les deux une association **`accéder` en `(0,n)` des deux côtés** : un utilisateur peut avoir accès à plusieurs applications, une application être attribuée à plusieurs utilisateurs, et les deux peuvent n'en avoir aucune. **Cette association porte une propriété, `droit d'accès`** — c'est le point à souligner, parce que c'est ce qui justifie la table de jonction au MLD. `Application_groups` complète le cercle avec une association `(1,1)–(0,n)` : une application appartient à un groupe et un seul.
> **Autour** — `Session`, en **`(1,1)` côté session, `(0,n)` côté utilisateur** : une session appartient à un utilisateur et un seul et **n'existe pas sans lui** (c'est la réponse à la question 177). Et `Événement`, pour l'analytique.
> **En périphérie** — les trois entités de paramétrage comptable, `user_code_maps`, `user_code_maps_gen_aux`, `code_journal`, chacune en `(0,1)–(1,1)` avec l'utilisateur : un paramétrage par utilisateur, au plus.
> **Les trois choses à dire spontanément, parce qu'elles montrent que tu maîtrises la chaîne :**
> — **8 entités au MCD, 9 tables en base.** La différence, c'est la **table de jonction**, qui naît au passage au MLD : elle **n'existe pas au niveau conceptuel**, où l'association n,n suffit. Savoir expliquer cet écart, c'est prouver qu'on n'a pas dessiné le MCD après coup à partir de la base.
> — **Le schéma est en 3NF**, avec **une dénormalisation assumée** : `applications.groups` est un texte libre sans clé étrangère — une référence faible, choix de simplicité, corrigée par la migration `003`.
> — **Le droit à l'oubli est porté par le modèle**, pas seulement par le code : `ON DELETE CASCADE` sur les mappings, et suppression explicite des sessions et des droits dans une **transaction** — parce que ces deux-là n'ont pas de cascade.
> ⚠️ **À corriger dans Looping avant l'oral :** l'entité `Permission des applications` doit disparaître au profit de l'association `accéder` directe. Sous sa forme actuelle, **le MCD est plus permissif que le schéma** — il autorise deux occurrences pour le même couple utilisateur/application, que `UNIQUE(user_id, application_id)` interdit en base. Voir question 15 de la partie 4.

**198. « Pourquoi ne pas avoir utilisé un soft delete plutôt qu'un `ON DELETE CASCADE` ? Si vous deviez conserver légalement certaines données pour un client ? »** 🔴
> **La question est excellente et elle vise juste : c'est l'arbitrage où deux obligations légales se contredisent.**
> **Le soft delete**, c'est marquer la ligne comme supprimée — une colonne `deleted_at` — au lieu de l'effacer, et filtrer partout à la lecture. Il préserve l'historique, les références restent valides, et **la suppression est réversible**.
> **Pourquoi j'ai choisi la suppression réelle :** parce que mon exigence dominante était le **droit à l'oubli du RGPD** (RG06). Or **un soft delete ne supprime rien** : l'email et le nom restent en base, et **au regard du RGPD, cette donnée est toujours traitée**. Une demande d'effacement satisfaite par un `deleted_at` n'est pas satisfaite. La suppression réelle, doublée du `ON DELETE CASCADE` au niveau du schéma, me donne une garantie **structurelle** plutôt qu'applicative : elle ne dépend pas du fait que chaque développeur pense à filtrer `WHERE deleted_at IS NULL` sur chaque requête — **et c'est le vrai risque du soft delete, un filtre oublié est une fuite de données personnelles silencieuse.**
> **Mais votre objection est juste, et c'est exactement la tension que j'ai résolue autrement :** certaines données doivent survivre à la suppression du compte — la **traçabilité** des actions administratives. C'est ma **RG07** : « les événements d'audit survivent à la suppression du compte ». **La bonne réponse à ce besoin n'est pas le soft delete, c'est l'anonymisation** : on garde l'événement, on **détache l'identité**. En pratique : `ON DELETE SET NULL` sur `events.uid`, ou le remplacement de l'identifiant par un pseudonyme non réversible. **On conserve le fait, on efface la personne** — ce qui satisfait les deux obligations au lieu de les opposer. Si l'obligation de conservation portait sur des données réellement nominatives — une facture, qui doit être conservée dix ans —, la réponse serait **l'archivage dans un stockage séparé, avec sa propre durée et ses propres accès**, et non un drapeau dans la table vivante.
> ⚠️ **Et je dois être honnête sur mon état actuel : `events.uid` est aujourd'hui en `ON DELETE CASCADE`. Donc RG07 est contredite par mon schéma** — les événements d'audit sont supprimés avec le compte. C'est un **écart identifié**, le correctif est un `ON DELETE SET NULL` avec pseudonymisation, et c'est une ligne de mon backlog. **Le dire soi-même vaut infiniment mieux que de se le faire trouver.**

**199. « Pourquoi Nginx pour la SPA, mais pas comme reverse proxy ? »**
> **Deux précisions avant de répondre, parce que la prémisse mérite d'être nuancée.**
> **Premièrement, Nginx fait bien du reverse proxy chez moi — mais à l'intérieur de la stack.** Ma configuration `frontend/conf/default.conf` sert la SPA **et** relaie `/sys/` vers le backend Go, `/api/` vers l'API Python, et `/ws` avec les en-têtes d'upgrade WebSocket. **Ce n'est donc pas « Nginx ou reverse proxy », c'est deux niveaux de routage différents.**
> **Deuxièmement, le rôle de Nginx pour la SPA n'est pas anodin.** Une application React compilée par Vite, c'est du **statique** — Nginx est exactement fait pour ça, et surtout il porte la ligne indispensable : `try_files $uri $uri/ /index.html`. Sans elle, un utilisateur qui recharge `/admin/users` reçoit un 404, parce que cette route n'existe que dans le routeur React, pas sur le disque. **C'est le fallback SPA, et c'est la vraie raison de Nginx ici.** Le multi-stage fait le reste : on compile avec Node, on ne garde que `dist/` dans une image `nginx:alpine-slim` — ni Node, ni sources, ni `node_modules` en production, donc une **surface d'attaque réduite**.
> **Maintenant, la vraie question : pourquoi Traefik en périphérie ?** Parce que le reverse proxy d'entrée dans un cluster Kubernetes n'est pas le même métier. **Traefik est l'ingress controller natif de K3s** — il est là au démarrage, sans installation. Trois choses le rendent supérieur à Nginx **dans ce contexte précis** : (1) il **découvre les services dynamiquement** via des ressources `IngressRoute` déclarées en YAML aux côtés des Deployments — **la configuration vit avec l'application** ; avec Nginx, il faudrait régénérer un fichier de configuration et le recharger à chaque changement de service ; (2) il gère **ACME/Let's Encrypt nativement** — obtention et renouvellement automatiques des certificats, là où Nginx demande certbot et un cron ; (3) il applique les **middlewares en ressources Kubernetes**, versionnées avec le reste.
> **La formule de sortie :** *« Nginx sert et route à l'intérieur du conteneur frontend, parce qu'il excelle sur le statique et le fallback SPA. Traefik route à l'entrée du cluster, parce que le routage d'entrée doit être dynamique et déclaratif — c'est un choix de niveau, pas une préférence entre deux outils. »*

**200. « C'est quoi le principe ACID ? Vous en parlez dans vos choix technologiques. »**
> ⚠️ **Note d'abord que le terme a été retiré du dossier le 23/08 — mais la question reste possible, garde la définition prête.**
> **ACID désigne les quatre garanties d'une transaction :**
> **A — Atomicité.** Une transaction est **tout ou rien**. Si une étape échoue, tout est annulé, et l'on retrouve l'état initial. Il n'existe pas d'état intermédiaire visible.
> **C — Cohérence.** Une transaction fait passer la base **d'un état valide à un autre état valide** : toutes les contraintes — clés étrangères, `UNIQUE`, `NOT NULL`, `CHECK` — sont vérifiées au `COMMIT`. Une transaction qui violerait une contrainte est refusée.
> **I — Isolation.** Les transactions concurrentes **ne se voient pas mutuellement** avant leur validation. C'est réglé par des **niveaux d'isolation** — `Read Committed`, qui est le défaut de PostgreSQL, `Repeatable Read`, `Serializable` — chacun arbitrant entre garanties et concurrence.
> **D — Durabilité.** Une fois le `COMMIT` acquitté, la donnée **survit à une panne** : elle est écrite dans le journal (le WAL) avant d'être confirmée.
> **Pourquoi ça a pesé dans mon choix de PostgreSQL, en deux exemples concrets de mon code :**
> **La création d'un utilisateur** — insérer le compte, puis lui attribuer ses applications. Sans atomicité, un échec entre les deux laisse **un compte sans droits** : un utilisateur qui se connecte et ne voit rien, sans qu'aucune erreur ne soit levée.
> **La suppression d'un utilisateur** — `DeleteUser` efface droits, sessions et mappings **dans une seule transaction**, avant le compte. Sans atomicité, un échec en milieu de course laisse des **sessions orphelines encore valides** : un accès qui survit à la suppression du compte. **C'est une faille de sécurité produite par une panne, pas par une attaque** — et c'est le meilleur argument à donner.
> **Et l'articulation avec le NoSQL, puisque c'est là qu'on vous emmène :** les bases documentaires ont longtemps proposé des garanties plus faibles — cohérence à terme, atomicité limitée au document — au profit de la scalabilité horizontale, selon le compromis du **théorème CAP**. **MongoDB fait des transactions multi-documents depuis la version 4.0**, il faut le savoir et ne pas dire l'inverse. Mais le point reste : **mes garanties d'intégrité, je les veux dans le moteur, pas dans mon code applicatif** — et à ma volumétrie, quelques dizaines d'utilisateurs, la scalabilité horizontale n'achète rien.

**201. « Les fichiers stockés sur le serveur le sont-ils tels quels ? Comment sécurisez-vous ça ? »**
> **Réponse directe : oui, ils sont écrits sur disque tels quels — et non chiffrés au repos. Mais ils vivent cinq minutes, dans un répertoire isolé par utilisateur, et ne sont accessibles par aucune URL.** Voici le détail, et l'arbitrage.
> **Où ils sont.** Chaque utilisateur a un répertoire temporaire **nommé d'après son UUID de session** — `tempfile.gettempdir()/{uuid}/uploads` — donc **isolé par construction** : deux utilisateurs ne partagent jamais de répertoire. Et ce chemin est bâti à partir de son **identifiant validé**, jamais d'un paramètre de requête libre : un utilisateur **ne peut pas nommer le répertoire d'un autre**.
> **Ce qui les protège, dans l'ordre du flux :** (1) le **cookie de session est validé avant tout traitement de fichier** — pas de dépôt anonyme ; (2) l'identifiant passe une **regex UUID stricte avant toute construction de chemin** — c'est l'ordre qui compte, un `../../etc/passwd` est rejeté en `400` avant qu'`os.path.join` soit appelé ; (3) le nom du fichier est réduit à son composant final par **`Path(filename).name`**, donc un chemin relatif ne survit pas ; (4) l'**extension est filtrée en allowlist** ; (5) la taille est **plafonnée à 50 Mo** par Nginx ; (6) **aucune route ne sert un fichier par son nom** — il n'existe pas d'URL publique vers ces répertoires, la seule sortie est la réponse HTTP de conversion, adressée au demandeur authentifié.
> **Et surtout : ils ne restent pas.** RG08 — `CLEANUP_DELAY_SECONDS = 300`, le répertoire entier est supprimé par `shutil.rmtree` **cinq minutes après le traitement**. **La meilleure protection d'une donnée, c'est de ne pas la conserver** : ça réduit la fenêtre d'exposition à quelques minutes, et ça sert la limitation de conservation du RGPD.
> **Ce que j'assume et ce que je ferais ensuite.** **Pas de chiffrement au repos**, pas d'analyse antivirus du contenu déposé, et une **validation d'extension plutôt que de type MIME réel** — un fichier renommé en `.txt` passe le filtre. L'arbitrage tient parce que le contenu est un **export de caisse anonymisé**, pas une donnée personnelle sensible, qu'il vit cinq minutes sur un volume monté par le seul pod de l'API, et que rien ne l'expose. **Si le contenu devenait sensible, l'ordre de mes corrections serait : chiffrement au niveau du volume — pas applicatif —, vérification du type réel par signature de fichier, puis analyse antivirale à l'entrée.** Ce n'est pas fait, c'est identifié, et c'est proportionné au risque actuel.

**202. « Comment êtes-vous sûr que vos tests passeront sur PostgreSQL, si vous ne testez pas avec ce SGBD ? »** 🔴
> **Je ne le suis pas complètement, et c'est la bonne réponse — c'est une limite réelle de mon dispositif, que j'ai identifiée. Mais elle est plus étroite qu'il n'y paraît, et je peux dire exactement où elle commence.**
> **Ce que mes tests couvrent réellement, dispositif par dispositif.** Côté **Go, `sqlmock` ne simule pas une base : il intercepte les appels de `database/sql` et vérifie la requête SQL émise et ses arguments.** Ce que je teste, c'est donc **ma logique métier et le SQL que je produis** — pas l'exécution du moteur. Côté **Python, SQLAlchemy en SQLite in-memory** teste mes **modèles, mes relations et ma logique de service**, avec l'ORM qui absorbe l'essentiel des différences de dialecte. **Et ce que j'y gagne est décisif : une suite qui tourne en secondes, sans base à provisionner, donc rejouée à chaque commit.** Un test qui exige une infrastructure est un test qu'on finit par ne plus lancer.
> **Où est le vrai risque, précisément :** les différences de dialecte et de comportement du moteur — les types spécifiques (`SERIAL`, `JSON`/`JSONB`, `TIMESTAMPTZ`), la sensibilité à la casse, `ON CONFLICT DO UPDATE` que SQLite écrit autrement, **le comportement transactionnel et l'application réelle des `ON DELETE CASCADE`**, et les contraintes d'unicité sous concurrence. **C'est exactement là que mes tests ne prouvent rien** — et c'est important, parce que mon droit à l'oubli repose sur des cascades.
> **Ce qui compense aujourd'hui :** le schéma est créé par `InitSchema` et les migrations SQL **sur la vraie base PostgreSQL**, donc les erreurs de DDL apparaissent au démarrage, pas en silence ; les **migrations sont idempotentes**, rejouables sans effet de bord ; et surtout **la préproduction tourne sur PostgreSQL**, avec une campagne de tests manuels sur des parcours réels **avant chaque release**. **La garantie existe donc — elle n'est simplement pas automatisée**, exactement comme pour mes tests E2E, et c'est la même leçon.
> **Ce que je ferais, et c'est concret :** ajouter à la CI un **service PostgreSQL** — `services: postgres` en GitHub Actions, ou **Testcontainers** — et faire tourner une **couche fine de tests d'intégration sur le vrai moteur** : les migrations s'appliquent, les cascades cascadent, les contraintes d'unicité tiennent. **Pas toute la suite** — je garde les unitaires rapides sur mocks —, seulement la dizaine de tests qui portent sur ce que seul PostgreSQL peut prouver. **C'est le bon découpage de la pyramide : mocks pour la logique, moteur réel pour l'intégrité.**

**203. « Pourquoi Kubernetes ? Vous avez une grosse base d'utilisateurs ? »**
> **Non, et c'est le point : quarante utilisateurs internes. Kubernetes n'est pas ici un choix de scalabilité — ce serait indéfendable — c'est un choix d'exploitation.** Assumer ça d'emblée est plus solide que d'inventer une charge que je n'ai pas.
> **Et la précision qui change la nature de la question : je n'ai pas déployé Kubernetes, j'ai déployé K3s** — une distribution allégée, un binaire d'une centaine de mégaoctets, conçue pour un serveur unique ou l'edge, avec Traefik intégré. **Ce n'est pas un cluster d'entreprise, c'est un orchestrateur mono-nœud sur un VPS.** L'écart de coût opérationnel avec un `docker compose` est bien plus faible que ce que le mot « Kubernetes » laisse entendre.
> **Ce que ça m'apporte réellement, et qui n'a rien à voir avec la charge :** (1) **le rolling update** — la nouvelle version démarre, passe son healthcheck, **puis** l'ancienne s'arrête : mise à jour **sans coupure** en pleine journée de travail, ce qui compte quand les utilisateurs sont des comptables en pleine saison fiscale ; (2) **le rollback en une commande**, parce que Kubernetes conserve l'historique des ReplicaSets — c'est le pilier de ma stratégie de retour arrière, et sans lui je redéploierais à la main sous pression ; (3) **l'auto-healing** — un conteneur qui meurt est relancé, un pod qui ne répond plus au healthcheck est remplacé, sans intervention de ma part un dimanche ; (4) **la configuration déclarative et versionnée** — mon infrastructure est du YAML dans Git, donc reproductible : si le VPS brûle, je réinstalle K3s et j'applique mes manifests ; (5) **les Secrets et les PVC** — les secrets injectés en variables d'environnement plutôt qu'écrits dans un fichier, et le stockage persistant découplé du cycle de vie des conteneurs.
> **Ce que ça coûte, que j'assume :** une courbe d'apprentissage réelle — c'est la difficulté documentée de mon itération 5, provisionner un VPS vierge sans aide extérieure —, une abstraction de plus à déboguer, et un `docker compose` aurait suffi au strict fonctionnement.
> **Ma conclusion, et c'est la phrase à retenir :** *« à quarante utilisateurs, Docker Compose faisait tourner l'application. Ce qu'il ne faisait pas, c'est le déploiement sans coupure et le rollback en une commande — et ce sont les deux choses dont j'ai besoin quand je suis seul à maintenir la plateforme. J'ai payé de la complexité pour de la sérénité d'exploitation, pas pour de la scalabilité. »*

**204. « Avez-vous utilisé de l'IA sur ce projet ? Que pensez-vous de son usage dans le développement ? »**
> **Oui, et je le dis sans détour — c'est une question de posture professionnelle, et l'esquive se voit immédiatement.**
> **Comment je m'en suis servi :** comme d'un **accélérateur sur ce que je sais déjà évaluer**. Explorer une API que je ne connais pas, obtenir une première version d'une fonction de parsing que je réécris ensuite, générer des cas de test auxquels je n'avais pas pensé — les cas limites, surtout —, dérouler une piste de débogage, reformuler de la documentation. **C'est un accélérateur de rédaction et d'exploration, pas un substitut de conception.**
> **Ce que je n'ai pas délégué, et c'est le cœur de ma réponse :** l'**architecture** et les **arbitrages**. Le choix de la session opaque contre le JWT, celui de PostgreSQL contre MongoDB, le découpage en deux back-ends, la structure de mon modèle de données — ce sont des décisions prises **dans mon contexte**, avec ma volumétrie, mes contraintes et mes utilisateurs. **Un modèle ne connaît pas mon contexte : il produit la réponse moyenne de son corpus, qui est souvent la réponse à la mode plutôt que la bonne pour moi.** Sur toutes les questions que vous m'avez posées aujourd'hui, la réponse vient de mon raisonnement — sinon je ne pourrais pas la défendre.
> **Ce que j'en pense, en trois points :** (1) **la responsabilité ne se délègue pas** — je signe le code que je livre, donc **je ne commite rien que je ne saurais expliquer ligne à ligne devant vous**, et c'est exactement le test de cet oral ; (2) **le risque réel n'est pas le mauvais code, c'est le code plausible** — une IA produit du code qui *a l'air* juste, et c'est plus dangereux qu'un code qui plante, parce que ça passe la relecture rapide ; d'où la nécessité des tests, de la revue et du linter, qui ne sont pas négociables ; (3) **il y a des angles morts non techniques** : la sécurité — un modèle propose volontiers une concaténation SQL —, les licences du code suggéré, et **la confidentialité** — je ne soumets pas de données clients ni de secrets, ce qui est une règle absolue dans un cabinet comptable soumis au secret professionnel.
> **Et l'effet sur l'apprentissage, si on me pousse :** le risque est de perdre la compréhension profonde en acceptant sans lire. **Ma règle : je ne colle jamais un bloc que je ne peux pas réécrire moi-même.** Quand je ne comprends pas ce qui m'est proposé, c'est le signal qu'il faut aller lire la documentation — pas accepter.
> **La phrase de sortie :** *« c'est un outil de plus dans la chaîne, au même titre que le linter, la complétion ou Stack Overflow avant lui. Ce qui ne change pas, c'est que la responsabilité de ce qui part en production est la mienne. »*

**205. « Revenons sur l'authentification : si le mot de passe n'est pas stocké, comment faites-vous la vérification ? »**
> **Parce que je n'ai pas besoin du mot de passe pour le vérifier — j'ai besoin de pouvoir vérifier que celui qu'on me présente est le bon. Ce sont deux choses différentes, et c'est toute la différence entre le hachage et le chiffrement.**
> **Ce que je stocke : une empreinte bcrypt.** Le hachage est une **fonction à sens unique** — on calcule facilement l'empreinte à partir du mot de passe, on ne remonte pas dans l'autre sens. **Ce n'est pas du chiffrement** : un chiffrement est réversible avec la clé, un hachage ne l'est pas du tout. **Personne ne peut retrouver le mot de passe depuis ma base — moi non plus.**
> **Comment se passe la vérification, concrètement.** À la connexion, je reçois le mot de passe en clair — **dans le corps d'une requête HTTPS**, donc chiffré en transit. Je récupère l'empreinte stockée pour cet email, puis j'appelle **`bcrypt.CompareHashAndPassword(hash, motDePasseFourni)`**. Et voici le point souvent mal compris : **cette fonction ne déchiffre rien.** Elle **extrait le sel et le coût contenus dans l'empreinte elle-même** — une empreinte bcrypt commence par `$2a$10$` suivi du sel, tout est dedans —, **rehache le mot de passe fourni avec exactement ce sel et ce coût**, et **compare les deux empreintes**. Si elles sont identiques, le mot de passe est le bon. La comparaison est faite **en temps constant**, pour ne pas fuiter d'information par la durée. Le mot de passe en clair n'existe alors qu'en mémoire, le temps de la requête. **Il n'est jamais écrit en base, jamais journalisé — c'est ma RG02.**
> **Pourquoi bcrypt et pas SHA-256 — la question suivante arrive presque toujours :** parce que SHA-256 est **conçu pour être rapide**, et un GPU en calcule des milliards par seconde. **bcrypt est délibérément lent**, avec un **facteur de coût paramétrable** — 10 chez moi, soit 2¹⁰ = 1024 itérations — que l'on peut augmenter à mesure que le matériel progresse. **Un algorithme de hachage de mot de passe est le seul cas où la lenteur est une qualité.** Et bcrypt **intègre un sel aléatoire unique par mot de passe** : deux utilisateurs avec le même mot de passe ont des empreintes différentes, ce qui rend inopérantes les tables arc-en-ciel et interdit de casser toute la base d'un coup. Les alternatives modernes recommandées aujourd'hui sont **argon2id** et **scrypt**, résistantes en mémoire ; bcrypt reste parfaitement acceptable et il est ce qui est disponible nativement en Go avec `golang.org/x/crypto`.
> **Et la suite, si on continue de dérouler :** une fois la comparaison réussie, je crée une **session opaque en base** — un UUID sans signification, pas un JWT —, je pose le cookie, et **le mot de passe ne réintervient plus jamais**. Sur le chemin d'échec, quelle que soit la cause — email inconnu ou mot de passe faux —, **le message d'erreur est générique et unique**, pour ne pas permettre l'énumération de comptes. Et le **429 du rate limiting est renvoyé avant tout calcul bcrypt**, parce que la lenteur de bcrypt, qui me protège de la force brute, ferait autrement du login une surface de déni de service.

---
## Check-list avant impression / soutenance

**Déjà corrigé dans le docx**
- [x] ~~Capture `CheckOrigin` en dur avec la coquille `cabinet-matini.fr`~~ — **18/08**, remplacée par un renvoi à l'annexe.
- [x] ~~« Temps de développement estimé » vide~~ — **22/08**, renseigné à **600 h**.
- [x] ~~Un besoin fonctionnel « fascicules McDonald's » sans réalisation~~ — **22/08**, retiré. **12 BF** désormais, renumérotés.
- [x] ~~`fascicule_mcdo` présentée comme quatrième table de l'outil, et présente au dictionnaire~~ — **22/08**, retirée des deux endroits ; le § 7.4 décrit les vraies routes de l'API Python.
- [x] ~~Les deux images du § 7.4 montraient du code `fascicule_mcdo`~~ — **22/08**, remplacées par le flux `/codes` et l'extrait `code_comptas()`.
- [x] ~~« ACID » dans le dossier~~ — **retiré volontairement** le 23/08. Garde la définition en tête : la question reste possible (corrigés 36 et 143).

**Reste à aligner entre le dossier, le code et le script oral** *(ajouté après le calage sur `SCRIPT_ORAL_CDA.md`)*
- [ ] 🔴 **RG07 contredit le schéma.** La règle dit « les événements d'audit survivent à la suppression du compte », mais `events.uid` est en `ON DELETE CASCADE` (`postgres.go` + migration 001). **Tranche avant l'oral** : soit `ON DELETE SET NULL` avec pseudonymisation, soit RG07 reformulée. Voir corrigé 157.
- [ ] 🔴 **Script § 3.3 — « le droit à l'oubli n'est pas écrit dans mon code ».** C'est trop absolu : `DeleteUser` supprime explicitement droits et sessions dans une transaction, `sessions` et `user_application_permissions` n'ayant pas de cascade. Reformuler en « suppression atomique, garantie par le schéma **et** par la transaction ». Voir corrigé 157.
- [ ] 🔴 **Script § 4.3 — « un des six services ».** Tu n'en cites que cinq, et le sixième (`Macdos`) est justement hors périmètre. **Dis « cinq ».** Voir corrigé 161.
- [ ] **Script § 7 — « 84 tests côté API Python ».** 72 passent aujourd'hui ; les 12 échecs sont des `404` de préfixe dans `tests/test_routers.py` (les tests appellent `/api/...`, `main.py` monte `/api/Facture-Mb`). **Correction d'une ligne dans le test** — soit tu la fais et tu cites 84/84, soit tu annonces « 84 tests, 72 au vert » et tu expliques pourquoi.
- [ ] **Maquettage : trois stades, pas quatre.** Le corrigé 146 est corrigé ; vérifie que le support visuel ne présente pas les mockups comme un quatrième stade.

**Reste à corriger avant impression**
- [ ] **BF05 « Authentification sécurisée (JWT) »** contredit frontalement la réalisation. Reformuler en « authentification par jeton de session ». **Priorité 1.**
- [ ] **Tous les renvois BF du chapitre Réalisation sont décalés** après la renumérotation : authentification → **BF05**, administration → **BF06**, analytics → **BF09**, WebSocket → **BF10**, mode sombre → **BF11**. Le § 7.4 doit dire « BF01 à BF04 » seul, sans « et BF08 ».
- [ ] **§ 7.4, phrase cassée** : « deux volets indissociables : le traitement des fichiers **et la façon dont les tickets sont convertis** » — le second volet n'est plus nommé.
- [ ] **US19 « Configurer les fascicules McDonald's »** et le Périmètre fonctionnel citent encore la configuration McDonald's, alors que le besoin a été retiré.
- [ ] **Dates** : page de garde « Novembre 2024 - Septembre 2026 » vs « environ 6 mois (novembre 2024 - avril 2025) ».
- [ ] **`/sys/register`** dans le tableau de rate limiting et « l'utilisateur doit pouvoir s'inscrire » : l'inscription n'existe pas (RG05).
- [ ] **A10 SSRF marqué « non implémenté »** → doit être « N/A / sans objet ».
- [ ] **« Cypress/Playwright »** en améliorations vs « Playwright plutôt que Cypress » au chapitre Tests → harmoniser.
- [ ] Coquilles de titres : « **OSWAP** Top 10 » → OWASP ; « **thread** modeling » → threat modeling ; « **Planning et sprints** » → « Planning et itérations ».
- [ ] Route WebSocket écrite `sys/ws` et healthcheck `/sys/health` → aligner sur `/ws` et `/health`.
- [ ] Tableau RBAC : clarifier « À la demande » (ne signifie pas un accès admin par défaut).
- [ ] Tableau Environnements : la préproduction annoncée n'est plus celle du `config.yaml` réel.

**À corriger dans Looping**
- [ ] **Supprimer l'entité `Permission des applications`** et la remplacer par une association `accéder` directe entre Utilisateur et Application, portant `droit d'accès`, en `(0,n)` des deux côtés. Sous sa forme actuelle, le MCD est **plus permissif que le schéma** — voir question 15 et `MCD_corrige.md`.

**À décider sur le code**
- [ ] **`auth.Service` dépend d'un type concret**, pas d'une interface — et les tests d'authentification exercent une copie de la logique. Soit tu corriges (≈15 lignes), soit tu changes d'exemple pour illustrer le découplage. **Voir question 14, la plus dangereuse de la liste.**
- [ ] **Appliquer `003_alignement_conceptuel.sql`** ? Il pose le `UNIQUE(user_id)` sur les mappings et la clé étrangère sur `applications.groups`. Nécessite au préalable la normalisation `"" → NULL` côté Go, décrite en pied de migration.

**À vérifier dans le code, pas dans le dossier**
- [ ] **La présence temps réel fonctionne-t-elle sur `logiciel.cabinet-martini.fr` ?** L'allowlist WebSocket ne contient pas ce domaine. Si l'application tourne encore sur `preprod.azert.fr`, tout va bien ; sinon la fonctionnalité est cassée en production, et son échec est silencieux. **C'est la réponse à la question 140** — ne la donne que si tu as vérifié.

**Préparation**
- [ ] Répéter la présentation chronométrée **deux fois à voix haute**
- [ ] Préparer un **jeu d'essai imprimé** (conversion EDI) à montrer si on te le demande
- [ ] Savoir ouvrir instantanément : MCD, MLD, MPD, diagramme de classes, séquence auth, tableau OWASP, tableau STRIDE
- [ ] Mémoriser les six difficultés d'itération — c'est ta meilleure réserve de réponses
- [ ] Préparer trois questions à poser au jury en fin d'entretien

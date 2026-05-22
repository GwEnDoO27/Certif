# Dossier CDA — Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructurer et enrichir `doc/dossier_projet.md` pour qu'il couvre intégralement le référentiel REAC TP CDA (11 CP + 3 CT), en suivant la TDM cible définie dans la spec.

**Architecture:** Édition incrémentale d'un unique fichier Markdown. Chaque tâche modifie une section précise du dossier (par anchor de section, pas par numéro de ligne — les lignes vont bouger). Aucun code applicatif modifié : les items d'implémentation (linters, rate limit, E2E, CHANGELOG, compose) sont documentés comme stratégie/cible.

**Tech Stack:** Markdown (GitHub-flavored), Mermaid pour diagrammes, sources internes du repo (`backend/`, `api/`, `frontend/src/`, `doc/diagrammes.md`, `git log`).

**Spec de référence:** `docs/superpowers/specs/2026-05-22-dossier-cda-design.md`

**Pattern de tâche** : chaque tâche d'écriture suit le squelette :
1. Lire les sources internes pertinentes
2. Écrire la sous-section dans `doc/dossier_projet.md` à l'emplacement indiqué
3. Vérifier (checklist de relecture : longueur, références croisées, cohérence ton)
4. Cocher l'item correspondant dans `doc/TODO_CDA.md`
5. Commit

---

## PHASE 1 — Fondations indépendantes (parallélisables)

### Task 1 : Conventions de commit (§ 3.4)

**Files:**
- Modify: `doc/dossier_projet.md` (insérer une nouvelle sous-section `## 3.4 Conventions de commit` après `## 3.3 Outils de gestion de projet`)
- Modify: `doc/TODO_CDA.md` (cocher "Utiliser les conventions de commit")

**CP couvert:** CP6

- [ ] **Step 1 : Lire l'historique de commits pour repérer les patterns réels**

```bash
git log --oneline -50
git log --pretty=format:"%s" | head -30
```

- [ ] **Step 2 : Rédiger § 3.4 dans `doc/dossier_projet.md`**

Insérer après la sous-section `## 3.3 Outils de gestion de projet` (avant `# 4. Conception`) :

```markdown
## 3.4 Conventions de commit

Le projet adopte la convention **Conventional Commits** (https://www.conventionalcommits.org/) afin de garantir la lisibilité de l'historique, l'automatisation du versioning et la génération du CHANGELOG.

### Format

```
<type>(<scope>) : <description>

[corps optionnel]

[footer optionnel]
```

### Types utilisés

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Documentation seule |
| `style` | Mise en forme (espaces, formatage) — pas de changement de code |
| `refactor` | Refactorisation sans changement de comportement |
| `test` | Ajout ou modification de tests |
| `chore` | Tâches de maintenance (build, dépendances) |
| `ci` | Modifications de la chaîne CI/CD |
| `perf` | Amélioration de performance |
| `security` | Correction ou amélioration de sécurité |

### Exemples tirés du projet

```
feat(auth) : ajout du middleware JWT
fix(api) : protection path traversal sur upload
docs : ajout du diagramme de séquence WebSocket
test(go) : couverture du service Analytics
chore(deps) : montée Go 1.24
```

### Bénéfices

- Historique lisible et filtrable (`git log --grep="^feat"`)
- Génération automatique du CHANGELOG via `git-cliff` ou `standard-version`
- Détection automatique du type de release (SemVer) : `feat` → MINOR, `fix` → PATCH, `BREAKING CHANGE` → MAJOR
- Onboarding facilité pour de nouveaux contributeurs
```

- [ ] **Step 3 : Vérifier**

Checklist :
- La section commence bien par `## 3.4` (deux #)
- Au moins 5 exemples concrets
- Ton homogène avec le reste du dossier (impersonnel, présent)
- Liens fonctionnels

- [ ] **Step 4 : Cocher dans `doc/TODO_CDA.md`**

Remplacer `- [ ] **Utiliser les conventions de commit** (Conventional Commits)` par `- [x]`.

- [ ] **Step 5 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 3.4 conventions de commit"
```

---

### Task 2 : Stratégie de branching (§ 3.5)

**Files:**
- Modify: `doc/dossier_projet.md` (nouvelle sous-section `## 3.5` après § 3.4)
- Modify: `doc/TODO_CDA.md` (cocher "Documenter la stratégie de branching")

**CP couvert:** CP6, CP11

- [ ] **Step 1 : Inspecter l'état des branches**

```bash
git branch -a
git log --graph --oneline --all -20
```

- [ ] **Step 2 : Rédiger § 3.5 dans `doc/dossier_projet.md`**

Insérer après § 3.4 :

```markdown
## 3.5 Stratégie de branching Git

Compte tenu du caractère solo du projet et du rythme de livraison continu, la stratégie **GitHub Flow** est retenue plutôt que Git Flow (jugé trop lourd pour ce contexte).

### Principes

- Une seule branche permanente : `main` (toujours déployable)
- Toute modification passe par une branche `feature/<nom-court>` éphémère
- Pull request (même solo) avant merge dans `main` pour bénéficier de la CI
- Merge en squash pour garder un historique linéaire
- Tags Git `vMAJOR.MINOR.PATCH` posés sur `main` pour chaque release

### Schéma

```
main ──●──●──●──●──●──●─── (toujours déployable)
        \  /    \  /
         ●●      ●●         feature/auth-jwt, feature/analytics
```

### Conventions de nommage

| Préfixe | Usage | Exemple |
|---------|-------|---------|
| `feature/` | Nouvelle fonctionnalité | `feature/admin-dashboard` |
| `fix/` | Correction de bug | `fix/cors-typo` |
| `chore/` | Maintenance | `chore/upgrade-go-1.24` |
| `docs/` | Documentation | `docs/owasp-top10` |

### Cycle de vie d'une branche

1. `git checkout -b feature/xxx` depuis `main` à jour
2. Commits suivant Conventional Commits (§ 3.4)
3. Push + Pull Request
4. CI verte requise (tests + lint)
5. Squash & merge dans `main`
6. Suppression de la branche distante et locale

### Justification du choix

GitHub Flow simplifie le workflow par rapport à Git Flow (`develop`, `release/*`, `hotfix/*`), ce qui est cohérent avec :
- Une équipe d'un seul développeur
- Un déploiement continu vers preprod après chaque merge
- L'absence de version "long-term support" à maintenir en parallèle
```

- [ ] **Step 3 : Cocher dans TODO et commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 3.5 stratégie de branching"
```

---

### Task 3 : Linters & formatters (§ 5.2.1)

**Files:**
- Modify: `doc/dossier_projet.md` (renommer l'actuelle § 5.2 en `## 5.3 Architecture logicielle choisie` et insérer une nouvelle § 5.2)
- Modify: `doc/TODO_CDA.md`

**CP couvert:** CP1

- [ ] **Step 1 : Vérifier la présence de configs existantes**

```bash
ls -la frontend/.eslintrc* frontend/.prettierrc* 2>/dev/null
ls -la backend/.golangci.yml backend/.golangci.yaml 2>/dev/null
ls -la api/ruff.toml api/pyproject.toml api/.flake8 2>/dev/null
```

- [ ] **Step 2 : Réorganiser la § 5.2 actuelle**

Dans `doc/dossier_projet.md`, l'actuelle `## 5.2 Architecture logicielle choisie` devient `## 5.3 Architecture logicielle choisie`. Insérer la nouvelle `## 5.2 Outillage de développement` à sa place.

```markdown
## 5.2 Outillage de développement

### 5.2.1 Linters et formatters

La qualité de code est garantie par une chaîne d'outillage cohérente sur les trois langages du projet. Chaque outil est exécuté localement (hook pre-commit recommandé) et en CI pour bloquer toute régression.

#### Frontend (React / JavaScript)

| Outil | Rôle | Configuration |
|-------|------|---------------|
| **ESLint** | Lint statique | `eslint:recommended` + `plugin:react/recommended` + `plugin:react-hooks/recommended` |
| **Prettier** | Formatage automatique | Largeur 100, single-quote, trailing comma `es5` |

Règles strictes activées :
- `no-unused-vars` : error
- `react-hooks/rules-of-hooks` : error
- `react-hooks/exhaustive-deps` : warn

#### Backend Go

| Outil | Rôle |
|-------|------|
| **golangci-lint** | Méta-linter (govet, errcheck, staticcheck, gosec, gocyclo, ineffassign) |
| **gofmt** | Formatage standard Go |
| **goimports** | Tri automatique des imports |

Linters de sécurité activés via `gosec` : détection des injections SQL non paramétrées, des hashs faibles, des secrets en dur, des permissions fichiers permissives.

#### API Python

| Outil | Rôle |
|-------|------|
| **ruff** | Linter (remplace flake8, isort, pyupgrade, partiellement pylint) |
| **black** | Formatage opinionated |

Configuration ruff : règles `E`, `F`, `W`, `I`, `B`, `UP`, `SIM` activées (style, bugs, simplifications, modernisation).

#### Stratégie d'exécution

```
Développement local :  pre-commit hook → lint + format auto sur fichiers staged
CI (GitHub Actions)  : job dédié "lint" en parallèle des tests, bloque le merge si KO
```

### 5.2.2 IDE et extensions recommandées

L'environnement de référence est **Visual Studio Code**, choisi pour sa polyvalence multi-langages et la richesse de son écosystème.

#### Extensions essentielles

| Extension | Usage |
|-----------|-------|
| **ESLint** (dbaeumer.vscode-eslint) | Lint JS/JSX en temps réel |
| **Prettier** (esbenp.prettier-vscode) | Formatage auto à la sauvegarde |
| **Go** (golang.go) | LSP Go, debug, tests intégrés |
| **Python** (ms-python.python) + **Pylance** | LSP Python, types |
| **Tailwind CSS IntelliSense** (bradlc.vscode-tailwindcss) | Autocomplétion classes Tailwind |
| **Docker** (ms-azuretools.vscode-docker) | Gestion images/conteneurs |
| **GitLens** (eamodio.gitlens) | Annotations Git, historique |
| **REST Client** (humao.rest-client) | Test des endpoints depuis VS Code |
| **Mermaid Preview** (bierner.markdown-mermaid) | Aperçu diagrammes dans Markdown |

#### Settings partagés (`.vscode/settings.json` recommandé)

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "go.lintTool": "golangci-lint",
  "[python]": { "editor.defaultFormatter": "ms-python.black-formatter" }
}
```
```

- [ ] **Step 3 : Cocher et commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 5.2 outillage de développement (linters + IDE)"
```

---

### Task 4 : Glossaire EN (§ 14)

**Files:**
- Modify: `doc/dossier_projet.md` (ajouter colonne EN à la table du glossaire)
- Modify: `doc/TODO_CDA.md` (cocher CT2 items)

**CP couvert:** CT2

- [ ] **Step 1 : Lire le glossaire actuel**

Ouvrir `doc/dossier_projet.md`, section `# 14. Glossaire` (autour des lignes 1560-1600).

- [ ] **Step 2 : Transformer en table à 3 colonnes**

Format cible :

```markdown
| Terme FR | Terme EN | Définition |
|----------|----------|------------|
| Authentification | Authentication | Processus de vérification de l'identité d'un utilisateur |
| Autorisation | Authorization | Vérification des droits d'accès d'un utilisateur authentifié |
| Bus de messages | Message bus | Système de communication asynchrone entre services |
| Cache | Cache | Stockage temporaire de données pour accélérer les accès |
| Conteneurisation | Containerization | Encapsulation d'une application et ses dépendances dans un conteneur isolé |
| Couche | Layer | Niveau d'abstraction dans une architecture en couches |
| Dépendance | Dependency | Bibliothèque ou service nécessaire au fonctionnement |
| Déploiement continu | Continuous Deployment (CD) | Mise en production automatisée à chaque merge |
| Endpoint | Endpoint | Point d'accès d'une API (URL + méthode HTTP) |
| Hachage | Hashing | Transformation irréversible d'une donnée en empreinte |
| Intergiciel | Middleware | Composant interceptant les requêtes/réponses |
| Intégration continue | Continuous Integration (CI) | Tests automatisés à chaque push |
| Jeton | Token | Chaîne d'authentification (ex : JWT) |
| Migration (BDD) | Database migration | Évolution incrémentale du schéma de base de données |
| Mise en cache | Caching | Action de stocker en cache |
| Orchestration | Orchestration | Coordination automatisée de plusieurs conteneurs/services |
| Persistance | Persistence | Sauvegarde durable de données |
| Point d'arrêt | Breakpoint | Marque d'arrêt pour le débogueur |
| Référentiel (Git) | Repository | Stockage d'un projet versionné |
| Refactorisation | Refactoring | Restructuration de code sans changement de comportement |
| Rétrocompatibilité | Backward compatibility | Compatibilité avec les versions antérieures |
| Sérialisation | Serialization | Transformation d'un objet en flux transmissible |
| Tableau de bord | Dashboard | Interface de visualisation synthétique |
| Test d'intégration | Integration test | Test de l'interaction entre composants |
| Test unitaire | Unit test | Test d'une unité de code isolée |
| Web socket | WebSocket | Protocole de communication bidirectionnelle persistante |
```

(Adapter à la liste réelle déjà présente dans le brouillon ; ajouter les termes manquants.)

- [ ] **Step 3 : Cocher et commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add EN translations to glossary (CT2)"
```

---

## PHASE 2 — Conception (préalable à la refonte § 7)

### Task 5 : Dictionnaire de données (§ 4.4.1)

**Files:**
- Modify: `doc/dossier_projet.md` (insérer `### 4.4.1 Dictionnaire de données` AVANT l'actuel `### 4.3.1 MCD`, puis renuméroter)
- Modify: `doc/TODO_CDA.md`

**CP couvert:** CP4

- [ ] **Step 1 : Lire les modèles de données**

```bash
grep -rn "CREATE TABLE\|type.*struct" backend/ | head -50
ls backend/*/repository.go backend/*/model.go 2>/dev/null
ls api/db/
```

Lire les structs Go (modèles) dans `backend/*/`, les modèles SQLAlchemy dans `api/db/`, et le script SQL MPD déjà rédigé (autour des lignes 493-575 du dossier).

- [ ] **Step 2 : Renuméroter les sous-sections existantes**

Actuel → cible :
- `### 4.3.1 MCD` → `### 4.4.2 MCD`
- `### 4.3.2 MLD` → `### 4.4.3 MLD`
- `### 4.3.3 MPD` → `### 4.4.4 MPD`

(L'actuelle § 4.3 Modélisation devient § 4.4 dans le sommaire ; vérifier la cohérence des références croisées.)

- [ ] **Step 3 : Rédiger § 4.4.1 — Dictionnaire de données**

Format : tableau exhaustif par entité.

```markdown
### 4.4.1 Dictionnaire de données

Cette section décrit l'ensemble des entités persistées, leurs attributs, types, contraintes et règles métier. Le dictionnaire constitue la référence pour les modèles MCD/MLD/MPD qui suivent.

#### Entité : `users`

| Attribut | Type SQL | Contraintes | Description |
|----------|----------|-------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT gen_random_uuid() | Identifiant unique |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Identifiant de connexion |
| password_hash | VARCHAR(255) | NOT NULL | Hash bcrypt (coût 12) |
| first_name | VARCHAR(100) | NOT NULL | Prénom |
| last_name | VARCHAR(100) | NOT NULL | Nom |
| role | VARCHAR(20) | NOT NULL, CHECK (role IN ('Admin','Dev','Comptable','Social','Auditeur','Client')) | Rôle métier |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de création |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Dernière modification |
| last_login | TIMESTAMP | NULLABLE | Dernière connexion réussie |

#### Entité : `sessions`

| Attribut | Type SQL | Contraintes | Description |
|----------|----------|-------------|-------------|
| token | VARCHAR(255) | PK | Identifiant de session (cookie) |
| user_id | UUID | FK users(id) ON DELETE CASCADE | Utilisateur propriétaire |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Création |
| expires_at | TIMESTAMP | NOT NULL | Expiration (24h glissantes) |

#### Entité : `applications`

| Attribut | Type SQL | Contraintes | Description |
|----------|----------|-------------|-------------|
| id | UUID | PK | Identifiant |
| name | VARCHAR(100) | NOT NULL | Nom affiché |
| description | TEXT | NULLABLE | Description courte |
| url | VARCHAR(500) | NOT NULL | URL d'accès |
| icon | VARCHAR(100) | NULLABLE | Nom de l'icône (Lucide) |
| roles | VARCHAR(255) | NOT NULL | Rôles autorisés (CSV) |
| enabled | BOOLEAN | NOT NULL, DEFAULT TRUE | Activé / désactivé |
| created_at | TIMESTAMP | NOT NULL | |

#### Entité : `analytics_events`

[à compléter à partir du modèle Go de backend/analyse/]

#### Entité : `mcdonalds_config`

[à compléter à partir du modèle existant]

#### Règles de cohérence transversales

- Tout `user.id` supprimé entraîne la suppression en cascade des `sessions` et `analytics_events` associés
- Toute valeur de `users.role` non listée dans la contrainte CHECK est rejetée
- Les timestamps sont stockés en UTC, conversion en TZ Europe/Paris côté affichage
```

- [ ] **Step 4 : Cocher et commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 4.4.1 dictionnaire de données"
```

---

### Task 6 : Justifications BDD (§ 4.4.5)

**Files:** Modify `doc/dossier_projet.md` (insérer après la sous-section MPD)

**CP couvert:** CP4

- [ ] **Step 1 : Rédiger § 4.4.5**

Insérer après l'actuel `### 4.4.4 MPD` (anciennement 4.3.3) :

```markdown
### 4.4.5 Justifications de conception BDD

#### Normalisation : Troisième forme normale (3NF)

Le schéma respecte la 3NF :
- **1NF** : aucun attribut multivalué ; les listes (ex. `applications.roles`) sont sérialisées en CSV avec une justification explicite (cardinalité ≤ 6, lecture seule majoritaire)
- **2NF** : pas de dépendance partielle (toutes les clés primaires sont mono-attribut UUID)
- **3NF** : pas de dépendance transitive entre attributs non-clé

#### Index

| Table | Index | Justification |
|-------|-------|---------------|
| `users` | UNIQUE(email) | Lookup à chaque login (hot path) |
| `sessions` | PRIMARY KEY(token) | Lookup à chaque requête authentifiée |
| `sessions` | INDEX(user_id) | Listing des sessions actives par user |
| `sessions` | INDEX(expires_at) | Job de nettoyage des sessions expirées |
| `analytics_events` | INDEX(user_id, created_at) | Requêtes par utilisateur / fenêtre temporelle |
| `applications` | INDEX(enabled) | Filtrage du catalogue actif (≥ 95 % des requêtes) |

#### Contraintes référentielles

- **ON DELETE CASCADE** sur `sessions.user_id` et `analytics_events.user_id` : la suppression d'un utilisateur (RGPD — droit à l'oubli) doit nettoyer toutes ses données dérivées sans intervention applicative
- **CHECK constraint** sur `users.role` : impossible d'insérer un rôle invalide même par accès SQL direct

#### Types choisis

- **UUID** plutôt qu'INTEGER auto-incrémenté pour les PK :
  - Sécurité (pas d'énumération séquentielle des ressources)
  - Distribution facile en cas de scaling horizontal
  - Pas de collision en cas de fusion de jeux de données
- **TIMESTAMP** sans fuseau (`TIMESTAMP` et non `TIMESTAMPTZ`) en UTC, conversion côté client
- **VARCHAR** dimensionné selon les contraintes métier (email 255 = max RFC 5321) plutôt que `TEXT` illimité

#### Pas d'utilisation actuelle de migrations

Le projet utilise actuellement un script SQL d'initialisation unique (`init.sql`). Une migration vers `golang-migrate` (Go) ou `Alembic` (Python) est documentée comme amélioration prévue (cf. § 12.1).
```

- [ ] **Step 2 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): add § 4.4.5 justifications BDD (3NF, index, contraintes)"
```

---

### Task 7 : Diagramme de classes UML (§ 4.6)

**Files:** Modify `doc/dossier_projet.md` (nouvelle sous-section après § 4.5)

**CP couvert:** CP3

- [ ] **Step 1 : Repérer le diagramme dans diagrammes.md**

```bash
grep -n "classDiagram\|## " doc/diagrammes.md | head -30
```

Localiser le ou les diagrammes de classes (sections 2-3 de `diagrammes.md` selon `TODO_CDA.md`).

- [ ] **Step 2 : Importer dans le dossier**

Insérer une sous-section `## 4.6 Diagramme de classes UML` après § 4.5 (Diagrammes de séquence). Copier le ou les blocs Mermaid correspondants depuis `doc/diagrammes.md`, avec un texte introductif et un texte explicatif après chaque diagramme.

Structure type :

```markdown
## 4.6 Diagramme de classes UML

Le diagramme suivant représente les principales classes et interfaces de la couche métier du backend Go, illustrant l'architecture Handler → Service → Repository.

```mermaid
[bloc Mermaid copié depuis diagrammes.md]
```

### Lecture du diagramme

- **Couche Handler** : reçoit les requêtes HTTP, valide, délègue
- **Couche Service** : règles métier, orchestration
- **Couche Repository** : accès à la base de données, abstraction des requêtes SQL

Les interfaces (`UserRepository`, `SessionRepository`, etc.) permettent l'injection de dépendances et le mocking en test unitaire (cf. § 9.2).
```

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): add § 4.6 diagramme de classes UML"
```

---

### Task 8 : UX et accessibilité RGAA (§ 4.3)

**Files:** Modify `doc/dossier_projet.md` (nouvelle sous-section entre § 4.2 Maquettes et § 4.4 Modélisation)

**CP couvert:** CP2

- [ ] **Step 1 : Inspecter le code frontend pour les patterns d'accessibilité**

```bash
grep -rn "aria-label\|aria-describedby\|role=" frontend/src/ | head -20
grep -rn "tabIndex\|onKeyDown" frontend/src/ | head -10
```

- [ ] **Step 2 : Rédiger § 4.3**

```markdown
## 4.3 Principes UX et accessibilité

### Principes UX appliqués

| Principe | Mise en œuvre |
|----------|---------------|
| **Cohérence** | Composants partagés (`components/`), palette unique gérée par `ThemeContext`, espacement uniforme via Tailwind |
| **Feedback** | États de chargement explicites (spinners), notifications toast pour les actions, messages d'erreur en ligne sous chaque champ |
| **Prévention de l'erreur** | Validation client avant soumission, confirmations modales pour les actions destructrices (suppression utilisateur, etc.) |
| **Reconnaissance plutôt que rappel** | Catalogue d'applications visuel avec icônes, breadcrumbs sur l'admin |
| **Efficacité experte** | Raccourcis clavier sur les modales (Echap pour fermer), focus management sur l'ouverture |
| **Esthétique minimaliste** | Densité d'information modérée, mode sombre en option |

### Parcours utilisateur principaux

1. **Connexion** → catalogue d'applications filtré par rôle → lancement d'un outil
2. **Administration** → liste filtrable → fiche utilisateur → édition / suppression
3. **Outil métier** → upload fichier → traitement → téléchargement résultat

Chaque parcours est conçu pour minimiser le nombre de clics jusqu'à la valeur métier (objectif : ≤ 3 clics depuis le login pour les actions courantes).

### Accessibilité (référentiel RGAA 4)

Bien que la conformité RGAA AA complète soit positionnée en évolution (cf. § 12.1), les principes suivants sont déjà appliqués :

| Critère RGAA | Application |
|--------------|-------------|
| Contraste (1.3) | Palette respectant un ratio ≥ 4.5:1 (vérifié au niveau du `ThemeContext` clair et sombre) |
| Navigation clavier (12.x) | Tous les boutons et liens sont focusables ; styles `:focus-visible` distincts |
| Alternative textuelle (1.1) | Icônes accompagnées d'un `aria-label` lorsque l'élément est purement visuel (boutons à icône uniquement) |
| Structure (9.x) | Titres hiérarchiques (`<h1>` → `<h2>` → `<h3>`), landmarks (`<nav>`, `<main>`, `<aside>`) |
| Identification (10.x) | Champs de formulaire associés à un `<label>` (ou `aria-labelledby`) |
| Cohérence (11.x) | Composants formulaires partagés (`InputField`, `Select`) garantissant un comportement homogène |

### Améliorations RGAA prévues

- Audit complet via axe-core ou WAVE
- Skip-link (« Aller au contenu principal »)
- Mode contraste renforcé pour utilisateurs malvoyants
- Test avec lecteur d'écran (NVDA, VoiceOver)
```

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): add § 4.3 UX et accessibilité RGAA"
```

---

## PHASE 3 — Refonte de la section 7 (Réalisation)

### Task 9 : Réorganiser la section 7 — squelette des 8 modules

**Files:** Modify `doc/dossier_projet.md` (réécriture du squelette de la section `# 7. Réalisation`)

**Objectif :** remplacer la structure actuelle (7.1 Frontend / 7.2 Backend Go / 7.3 API Python) par 8 modules verticaux. Le contenu détaillé est rapatrié module par module dans les tasks suivantes (10 à 17).

- [ ] **Step 1 : Sauvegarder l'ancien contenu**

Avant suppression, copier les sous-sections actuelles 7.1.* / 7.2.* / 7.3.* dans un buffer mental ou un fichier temporaire. Les fragments seront réutilisés par les Tasks 10 à 17.

- [ ] **Step 2 : Remplacer le contenu de la section 7 par le squelette suivant**

```markdown
# 7. Réalisation

Cette section décrit la réalisation de l'application par **module fonctionnel vertical** (et non par couche technique). Chaque module est présenté selon le même schéma : besoin fonctionnel rappelé, interface utilisateur, logique backend, persistance, flux complet, extrait de code clé.

## 7.1 Authentification et sessions
*[contenu rapatrié par Task 10]*

## 7.2 Administration des utilisateurs
*[contenu rapatrié par Task 11]*

## 7.3 Catalogue d'applications
*[contenu rapatrié par Task 12]*

## 7.4 Outils métier
*[contenu rapatrié par Task 13]*

## 7.5 Tableau de bord analytique
*[contenu rapatrié par Task 14]*

## 7.6 WebSocket — présence temps réel
*[contenu rapatrié par Task 15]*

## 7.7 Configuration McDonald's
*[contenu rapatrié par Task 16]*

## 7.8 Thème (Dark Mode)
*[contenu rapatrié par Task 17]*
```

- [ ] **Step 3 : Commit (squelette intentionnellement vide entre Tasks 9 et 17)**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): réorganiser § 7 en modules verticaux (squelette)"
```

---

### Tasks 10 → 17 : Rédiger chaque module (template homogène)

**Template commun à toutes ces tâches** — pour chaque module § 7.X :

```markdown
## 7.X Nom du module

### 7.X.1 Besoin fonctionnel
[2-4 lignes rappelant le besoin du cahier des charges + référence à l'épic / BFnn correspondant]

### 7.X.2 Interface utilisateur
[Composants React mobilisés (paths exacts), pattern d'état, captures référencées vers annexe B]
[Extrait court (10-20 lignes) d'un composant clé]

### 7.X.3 Backend
[Handler → Service → Repository (Go) ou Router → Util (Python)]
[Paths exacts des fichiers, responsabilités]
[Extrait court d'un handler ou service clé]

### 7.X.4 Base de données
[Tables touchées (référence § 4.4.1), opérations CRUD principales]

### 7.X.5 Flux complet
[Diagramme de séquence référencé ou inline (Mermaid)]
[Description du chemin requête → réponse]

### 7.X.6 Extrait de code clé
[Bloc de code commenté de ~30-50 lignes illustrant le pattern central du module]
```

---

### Task 10 : § 7.1 Authentification et sessions

**Source matter** : actuels § 7.1.1 (Login.jsx), § 7.2.1 (auth Go), § 7.2.2 (middlewares) à rapatrier et compléter.

**CP couvert:** CP2, CP3, CP7, CP8

- [ ] **Step 1 : Lire le code source**

```bash
ls backend/auth/
cat frontend/src/Landing/Login.jsx | head -80
cat frontend/src/Landing/Register.jsx | head -80
```

- [ ] **Step 2 : Rédiger § 7.1 selon le template**

Le contenu existe largement déjà aux lignes ~909-1059 du brouillon (avant la refonte). Le travail consiste à le **réorganiser** selon le template 7.X.1 → 7.X.6, sans réécrire from-scratch.

Contenu clé à inclure :
- 7.1.1 Besoin : BF01 (auth sécurisée) + référence Épic 1
- 7.1.2 UI : `Login.jsx`, `Register.jsx`, `PasswordReset.jsx` + extrait `handleSubmit`
- 7.1.3 Backend :
  - Handler `backend/auth/handler.go` (LoginHandler, RegisterHandler, LogoutHandler)
  - Service `backend/auth/service.go` (hash bcrypt, création de session)
  - Middleware `backend/auth/middleware.go` (vérification cookie, injection user dans contexte)
- 7.1.4 BDD : tables `users`, `sessions` (référence § 4.4.1)
- 7.1.5 Flux : diagramme de séquence (référence § 4.5.1)
- 7.1.6 Code clé : extrait du service avec bcrypt + génération token + insertion session

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): rapatrier § 7.1 authentification (module vertical)"
```

---

### Task 11 : § 7.2 Administration des utilisateurs

**Source matter** : actuel § 7.1.2.

**CP couvert:** CP2, CP3, CP8

- [ ] **Step 1 : Lire**

```bash
ls backend/admin/
ls frontend/src/Admin/
```

- [ ] **Step 2 : Rédiger § 7.2 selon le template**

Contenu :
- 7.2.1 Besoin : BF02 (gestion users + 6 rôles)
- 7.2.2 UI : `Admin/Users.jsx`, `Admin/UserForm.jsx`, filtres, pagination
- 7.2.3 Backend : `backend/admin/` (handler/service/repository)
- 7.2.4 BDD : `users` + audit dans `analytics_events`
- 7.2.5 Flux : création/édition/suppression user
- 7.2.6 Code clé : Repository pattern (interface + implémentation Postgres) — déjà présent en Annexe A.4

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): rapatrier § 7.2 administration users"
```

---

### Task 12 : § 7.3 Catalogue d'applications

**Source matter** : à extraire du code (pas explicitement présent dans le brouillon actuel).

**CP couvert:** CP2, CP3, CP8

- [ ] **Step 1 : Lire**

```bash
ls backend/applications/
grep -rn "applications" frontend/src/ | head -10
```

- [ ] **Step 2 : Rédiger § 7.3 selon le template**

Contenu :
- 7.3.1 Besoin : BF03 (catalogue dynamique)
- 7.3.2 UI : Dashboard utilisateur (catalogue filtré par rôle) + Admin/Applications (CRUD)
- 7.3.3 Backend : `backend/applications/`
- 7.3.4 BDD : `applications` (référence § 4.4.1)
- 7.3.5 Flux : récupération du catalogue par rôle utilisateur
- 7.3.6 Code clé : extrait du filtrage par rôle

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): rédiger § 7.3 catalogue d'applications"
```

---

### Task 13 : § 7.4 Outils métier

**Source matter** : actuels § 7.1.3 (frontend outils) + § 7.3.1, 7.3.2 (Python API).

**CP couvert:** CP3, CP8

- [ ] **Step 1 : Lire**

```bash
ls frontend/src/pages/
ls api/utils/
cat api/routers.py | head -50
```

- [ ] **Step 2 : Rédiger § 7.4 selon le template**

Particularité : section plus longue (multiples sous-outils). Découpage interne possible :
- 7.4.1 Besoin : BF04
- 7.4.2 UI : pages spécialisées dans `frontend/src/pages/` (22 pages selon CLAUDE.md)
- 7.4.3 Backend : Python API (FastAPI) — détail par catégorie :
  - Traitement Excel (`api/utils/format.py`)
  - Conversion EDI (`api/utils/convert.py`)
  - Recherche/tri (`api/utils/searching.py`, `sort.py`)
  - Mappings comptables, FEC, Silae
- 7.4.4 BDD : usage limité (uploads transients, peu de persistance)
- 7.4.5 Flux : upload → traitement → download
- 7.4.6 Code clé : extrait `convert.py` (déjà en Annexe A.3)

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): rapatrier § 7.4 outils métier (Python API)"
```

---

### Task 14 : § 7.5 Tableau de bord analytique

**Source matter** : actuel § 7.2.4.

**CP couvert:** CP2, CP3, CP8

- [ ] **Step 1 : Lire**

```bash
ls backend/analyse/
grep -rn "AdminAnalytics\|Recharts" frontend/src/ | head -10
```

- [ ] **Step 2 : Rédiger § 7.5 selon le template**

Contenu :
- 7.5.1 Besoin : BF05 (suivi activité)
- 7.5.2 UI : `Admin/AdminAnalytics.jsx` + graphiques Recharts (connexions/jour, heures de pointe)
- 7.5.3 Backend : `backend/analyse/`
- 7.5.4 BDD : `analytics_events`
- 7.5.5 Flux : ingestion async des events + endpoint d'agrégation
- 7.5.6 Code clé : agrégation par fenêtre temporelle (extrait service)

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): rapatrier § 7.5 analytics"
```

---

### Task 15 : § 7.6 WebSocket — présence temps réel

**Source matter** : actuels § 7.1.5 (frontend WS) + § 7.2.3 (WS Manager Go).

**CP couvert:** CP3, CP5, CP7

- [ ] **Step 1 : Lire**

```bash
ls backend/websocket/
cat frontend/src/hooks/useWebSocket.jsx | head -50 2>/dev/null
```

- [ ] **Step 2 : Rédiger § 7.6 selon le template**

Contenu :
- 7.6.1 Besoin : BF06 (présence temps réel)
- 7.6.2 UI : hook `useWebSocket`, indicateur de présence dans Dashboard
- 7.6.3 Backend : `backend/websocket/` (Hub pattern, gestion des clients connectés)
- 7.6.4 BDD : peu / pas de persistance (présence éphémère)
- 7.6.5 Flux : handshake WS → join hub → broadcast présence
- 7.6.6 Code clé : extrait du Hub (déjà en Annexe A.5) + validation Origin (Annexe A.6)

Mentionner explicitement la protection **Cross-Site WebSocket Hijacking** (CSWSH).

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): rapatrier § 7.6 WebSocket présence"
```

---

### Task 16 : § 7.7 Configuration McDonald's

**Source matter** : à extraire du code (mentionné dans CLAUDE.md, peu détaillé dans le brouillon).

**CP couvert:** CP3

- [ ] **Step 1 : Lire**

```bash
grep -rn "mcdonald\|McDonald\|mcdo" backend/ frontend/src/ | head -20
```

- [ ] **Step 2 : Rédiger § 7.7**

Si la fonctionnalité est marginale, le module peut être plus court (½ page) :
- 7.7.1 Besoin : configuration client McDonald's spécifique
- 7.7.2 UI : page dédiée
- 7.7.3 Backend : service de configuration
- 7.7.4 BDD : table `mcdonalds_config`
- 7.7.5 Flux : édition admin → persistance
- 7.7.6 Code clé : 1 extrait pertinent

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): rédiger § 7.7 configuration McDonald's"
```

---

### Task 17 : § 7.8 Thème (Dark Mode)

**Source matter** : actuel § 7.1.4.

**CP couvert:** CP2

- [ ] **Step 1 : Lire**

```bash
cat frontend/src/context/ThemeContext.* 2>/dev/null | head -50
```

- [ ] **Step 2 : Rédiger § 7.8** selon le template (module court, ½ à 1 page) :
- 7.8.1 Besoin : BF07
- 7.8.2 UI : ThemeContext + toggle
- 7.8.3 Backend : N/A (preference client uniquement, stockée dans localStorage)
- 7.8.4 BDD : N/A
- 7.8.5 Flux : toggle → update context → re-render
- 7.8.6 Code clé : ThemeContext (extrait)

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): rapatrier § 7.8 thème dark mode"
```

---

## PHASE 4 — Architecture, Sécurité, Tests (parallélisables)

### Task 18 : Documentation API REST / OpenAPI (§ 6.5)

**Files:** Modify `doc/dossier_projet.md` (nouvelle sous-section entre § 6.4 et § 6.5 actuelle qui devient § 6.6)

**CP couvert:** CP5

- [ ] **Step 1 : Inspecter les routes**

```bash
grep -rn "app.get\|app.post\|app.put\|app.delete" api/ | head -30
grep -rn "router.HandleFunc\|HandleFunc\|.Handle(" backend/ | head -30
```

- [ ] **Step 2 : Renuméroter l'actuelle § 6.5 en § 6.6** et insérer la nouvelle § 6.5

```markdown
## 6.5 Documentation des API REST

### 6.5.1 API Python (FastAPI) — OpenAPI auto-généré

FastAPI génère automatiquement une spécification OpenAPI 3.0 et expose une interface Swagger UI interactive à l'adresse `/docs` (et Redoc à `/redoc`). Cette documentation est mise à jour à chaque démarrage du service à partir des annotations Python (Pydantic + type hints).

[Capture : voir Annexe B — interface Swagger UI]

Cette approche garantit que la documentation reste synchronisée avec le code (single source of truth).

### 6.5.2 API Go — Endpoints documentés

Le backend Go n'utilise pas d'outil de génération automatique. La documentation est maintenue manuellement ci-dessous, à partir de l'inspection de `backend/cmd/main.go`.

#### Endpoints publics

| Méthode | Chemin | Description |
|---------|--------|-------------|
| POST | `/api/auth/register` | Inscription d'un nouvel utilisateur |
| POST | `/api/auth/login` | Connexion (renvoie cookie de session) |
| POST | `/api/auth/logout` | Déconnexion |
| GET | `/api/health` | Healthcheck (status 200 si DB joignable) |

#### Endpoints utilisateur authentifié

| Méthode | Chemin | Rôle requis | Description |
|---------|--------|-------------|-------------|
| GET | `/api/me` | Tous | Profil utilisateur courant |
| GET | `/api/applications` | Tous | Catalogue filtré par rôle |
| WS | `/api/ws` | Tous | Connexion WebSocket (présence) |

#### Endpoints administration

| Méthode | Chemin | Rôle requis | Description |
|---------|--------|-------------|-------------|
| GET | `/api/admin/users` | Admin | Liste utilisateurs |
| POST | `/api/admin/users` | Admin | Création utilisateur |
| PUT | `/api/admin/users/{id}` | Admin | Modification |
| DELETE | `/api/admin/users/{id}` | Admin | Suppression |
| GET | `/api/admin/analytics` | Admin | Données analytiques |
| GET | `/api/admin/applications` | Admin | Gestion catalogue |
| ... | ... | ... | ... |

(Liste complète à compléter à partir du code source.)

### 6.5.3 Contrats d'interface

- Format de réponse standardisé : `{"data": ..., "error": null}` en cas de succès, `{"data": null, "error": "message"}` en cas d'erreur
- Codes HTTP respectés : 200, 201, 400, 401, 403, 404, 422, 500
- Sérialisation JSON pour toutes les réponses (sauf téléchargement de fichiers binaires)
```

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 6.5 documentation des API REST"
```

---

### Task 19 : Sécurité — CSRF et headers HTTP (§ 8.5)

**Files:** Modify `doc/dossier_projet.md` (nouvelle sous-section après § 8.4)

**CP couvert:** CP7

- [ ] **Step 1 : Vérifier les headers déjà configurés**

```bash
grep -rn "X-Frame-Options\|Content-Security-Policy\|HSTS\|SameSite" backend/ frontend/ 2>/dev/null
```

- [ ] **Step 2 : Rédiger § 8.5**

```markdown
## 8.5 Protection CSRF et headers de sécurité HTTP

### 8.5.1 Protection CSRF

La protection CSRF repose sur deux mécanismes complémentaires :

1. **Attribut `SameSite=Strict`** sur le cookie de session : empêche le navigateur d'envoyer le cookie lors d'une requête initiée depuis un site tiers (protection native)
2. **Header `Origin` / `Referer` vérifié côté serveur** : pour les requêtes non-GET, le backend rejette toute requête dont l'origine ne correspond pas à la liste blanche CORS

Cette double protection couvre les navigateurs récents (SameSite) et fournit une seconde barrière pour les navigateurs legacy. Une protection par jeton CSRF synchronisé (double-submit cookie) reste documentée comme évolution possible si un middleware tiers est intégré (cf. § 12.1).

### 8.5.2 Headers HTTP de sécurité

Stratégie cible (middleware Go à enrichir si besoin) :

| Header | Valeur | Rôle |
|--------|--------|------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Force HTTPS pendant 1 an |
| `X-Frame-Options` | `DENY` | Empêche l'inclusion en iframe (clickjacking) |
| `X-Content-Type-Options` | `nosniff` | Empêche le MIME-sniffing |
| `Content-Security-Policy` | `default-src 'self'; script-src 'self'; ...` | Restreint les ressources autorisées (anti-XSS) |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limite la fuite d'URL en cross-origin |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=()` | Désactive les API sensibles |

Ces headers sont (ou seront) appliqués globalement via un middleware Go monté en amont du routeur. Une revue avec [securityheaders.com](https://securityheaders.com) est prévue avant mise en production.
```

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 8.5 CSRF et headers de sécurité HTTP"
```

---

### Task 20 : Sécurité — Rate limiting (§ 8.6)

**Files:** Modify `doc/dossier_projet.md` (nouvelle sous-section après § 8.5)

**CP couvert:** CP7

- [ ] **Step 1 : Rédiger § 8.6**

```markdown
## 8.6 Rate limiting

### Motivation

Sans limitation de débit, les endpoints d'authentification sont vulnérables :
- Bruteforce de mots de passe
- Énumération d'utilisateurs (via les messages d'erreur)
- Déni de service applicatif

### Stratégie retenue : Token bucket par IP

Algorithme : **token bucket** (capacité fixe, regénération à taux constant). Cette stratégie tolère les bursts courts (UX) tout en limitant le taux soutenu.

| Endpoint | Capacité | Taux de regénération |
|----------|----------|-----------------------|
| `POST /api/auth/login` | 5 requêtes | 1 / 30 s |
| `POST /api/auth/register` | 3 requêtes | 1 / 60 s |
| `POST /api/auth/password-reset` | 3 requêtes | 1 / 5 min |
| Autres endpoints | 60 requêtes | 1 / s |

### Implémentation

Middleware Go basé sur `golang.org/x/time/rate` (token bucket natif) ou `github.com/didip/tollbooth` (plus complet, support clés multiples).

Identification du client : IP source (`X-Forwarded-For` lu depuis Caddy/Traefik en amont).

### Réponse en cas de dépassement

- Code HTTP : `429 Too Many Requests`
- Header `Retry-After: <secondes>` indiquant le délai d'attente
- Logging de l'événement (cf. § 8.7)

### Évolutions

- Limitation par utilisateur authentifié (pas seulement par IP) pour les endpoints sensibles
- Stockage du bucket dans Redis pour fonctionner en multi-instance (actuellement stockage en mémoire — OK avec scaling vertical, KO en horizontal)
```

- [ ] **Step 2 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 8.6 rate limiting"
```

---

### Task 21 : Sécurité — Logging (§ 8.7)

**Files:** Modify `doc/dossier_projet.md` (après § 8.6)

**CP couvert:** CP7

- [ ] **Step 1 : Rédiger § 8.7**

```markdown
## 8.7 Logging de sécurité

### Événements journalisés

| Événement | Niveau | Données |
|-----------|--------|---------|
| Tentative de connexion échouée | WARN | email tenté, IP source, user-agent, timestamp |
| Connexion réussie | INFO | user_id, IP source, timestamp |
| Logout | INFO | user_id, timestamp |
| Création de compte | INFO | user_id, email, IP source |
| Suppression de compte | WARN | user_id supprimé, admin_id, timestamp |
| Changement de rôle | WARN | user_id, ancien rôle, nouveau rôle, admin_id |
| Accès refusé (RBAC) | WARN | user_id, endpoint demandé, rôle requis |
| Rate limit dépassé | WARN | IP source, endpoint, timestamp |
| Erreur 5xx | ERROR | endpoint, message d'erreur, stack trace |

### Format des logs

JSON structuré (compatible ingestion ELK, Loki, Datadog) :

```json
{
  "timestamp": "2026-05-22T14:23:11Z",
  "level": "WARN",
  "event": "login_failed",
  "ip": "203.0.113.42",
  "email_attempted": "user@example.com",
  "user_agent": "Mozilla/5.0 ..."
}
```

### Stratégie de stockage

- **Court terme** : stdout du conteneur, agrégé par le runtime Kubernetes (kubectl logs)
- **Moyen terme cible** : ingestion vers une stack ELK ou Grafana Loki (cf. § 10.7)
- **Rétention** : 90 jours pour les événements de sécurité (conforme RGPD avec finalité "détection d'intrusion" / "sécurité du SI"), 30 jours pour les logs applicatifs standards

### Ce qui n'est PAS loggé

- Mots de passe (en clair ou hashés)
- Tokens de session complets (uniquement les 8 derniers caractères, à titre de traçabilité)
- Données personnelles non nécessaires à la finalité (principe de minimisation RGPD)
```

- [ ] **Step 2 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 8.7 logging de sécurité"
```

---

### Task 22 : Tests E2E (§ 9.6)

**Files:** Modify `doc/dossier_projet.md` (nouvelle sous-section après § 9.5)

**CP couvert:** CP9

- [ ] **Step 1 : Rédiger § 9.6**

```markdown
## 9.6 Tests end-to-end (E2E)

### Choix d'outil : Playwright

[Playwright](https://playwright.dev/) est retenu plutôt que Cypress pour :
- Support natif multi-navigateurs (Chromium, Firefox, WebKit)
- Auto-waiting (moins de flakiness que Cypress sur les états asynchrones)
- API moderne (`async/await`)
- Compatible CI sans X server

### Architecture des tests E2E

```
e2e/
├── playwright.config.ts
├── fixtures/
│   └── users.ts                  # Comptes de test seedés
├── tests/
│   ├── auth.spec.ts              # Login / logout / register
│   ├── admin-crud.spec.ts        # Admin gérant les users
│   ├── file-upload.spec.ts       # Upload d'un fichier outil métier
│   └── access-control.spec.ts    # Vérification RBAC frontal
└── README.md
```

### Scénarios couverts (cible)

| Scénario | Description |
|----------|-------------|
| **auth-01** | Login avec credentials valides → accès au catalogue |
| **auth-02** | Login avec mot de passe incorrect → message d'erreur affiché |
| **auth-03** | Logout → redirection vers landing |
| **admin-01** | Admin crée un utilisateur Comptable → utilisateur apparaît dans la liste |
| **admin-02** | Admin édite un utilisateur (changement de rôle) → vérifier persistance |
| **admin-03** | Admin supprime un utilisateur → confirmation modale → suppression effective |
| **outil-01** | Comptable upload un fichier Excel → traitement → téléchargement résultat |
| **rbac-01** | Comptable tente d'accéder à `/admin` → redirection ou 403 |

### Exécution en CI

Job dédié dans `.github/workflows/ci.yml` (à ajouter) :
- Démarrage de la stack via docker-compose
- Attente du healthcheck
- Exécution `npx playwright test`
- Upload du rapport HTML en artefact en cas d'échec

### Statut actuel

Les tests E2E sont à mettre en place. La stratégie ci-dessus est documentée comme livrable cible, planifiée en post-soutenance (cf. § 12).
```

- [ ] **Step 2 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 9.6 tests E2E (Playwright)"
```

---

### Task 23 : Tests manuels et jeux de données (§ 9.8)

**Files:** Modify `doc/dossier_projet.md` (après § 9.6, en décalant l'actuelle § 9.6 Résultats en § 9.7)

**CP couvert:** CP9

- [ ] **Step 1 : Renuméroter § 9.6 Résultats → § 9.7** et § 9.7 CI → § 9.9

- [ ] **Step 2 : Rédiger § 9.8 Tests manuels**

```markdown
## 9.8 Tests manuels et jeux de données

Les tests automatisés (unitaires, intégration, E2E) ne couvrent pas tout. Une campagne de tests manuels est conduite avant chaque release, sur la base d'une matrice de parcours.

### Matrice de parcours utilisateur

| Parcours | Rôle | Statut |
|----------|------|--------|
| Inscription + login | Anonyme | ✅ Validé |
| Réinitialisation mot de passe | Anonyme | ✅ Validé |
| Lancement d'une application du catalogue | Tous rôles | ✅ Validé |
| Conversion EDI (upload + download) | Comptable | ✅ Validé |
| Fusion Excel multi-fichiers | Comptable | ✅ Validé |
| Traitement Silae | Social | ✅ Validé |
| Audit FEC | Auditeur | ✅ Validé |
| Création / édition / suppression user | Admin | ✅ Validé |
| Consultation analytics | Admin | ✅ Validé |
| Toggle dark mode | Tous rôles | ✅ Validé |
| Navigation responsive (mobile, tablette) | Tous rôles | ✅ Validé |

### Jeux de données

| Donnée | Source | Usage |
|--------|--------|-------|
| `tests/data/sample.edi` | Anonymisé depuis production | Conversion EDI |
| `tests/data/excel_paie_*.xlsx` | Données fictives | Fusion Excel |
| `tests/data/fec_2024.txt` | Format FEC standard | Audit FEC |
| `tests/data/silae_export.csv` | Données fictives | Traitement Silae |

Tous les jeux de données contiennent des données fictives ou anonymisées, conformément à la politique RGPD du projet.

### Tests par navigateur

| Navigateur | Version testée | Statut |
|------------|----------------|--------|
| Chrome | latest | ✅ |
| Firefox | latest | ✅ |
| Safari | latest | ✅ |
| Edge | latest | ✅ |

### Tests par résolution

| Résolution | Statut |
|------------|--------|
| 1920×1080 (desktop) | ✅ |
| 1366×768 (laptop) | ✅ |
| 768×1024 (tablette portrait) | ✅ |
| 375×667 (mobile portrait) | ✅ |
```

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 9.8 tests manuels et jeux de données"
```

---

## PHASE 5 — Déploiement (CP10-CP11)

### Task 24 : Procédure de déploiement step-by-step (§ 10.5)

**Files:** Modify `doc/dossier_projet.md` (après § 10.4)

**CP couvert:** CP10

- [ ] **Step 1 : Inspecter les manifestes K8s**

```bash
ls backend/k8s/ api/k8s/
cat backend/k8s/deployment.yaml 2>/dev/null | head -30
```

- [ ] **Step 2 : Rédiger § 10.5**

```markdown
## 10.5 Procédure de déploiement step-by-step

### Prérequis

| Outil | Version minimale | Rôle |
|-------|------------------|------|
| `kubectl` | 1.28+ | Pilotage K8s |
| Accès au cluster | — | Kubeconfig configuré (`kubectl config current-context`) |
| `git` | 2.30+ | Récupération du code |
| Variables d'environnement | — | cf. tableau ci-dessous |

### Variables d'environnement

À provisionner dans les Secrets Kubernetes (`backend/k8s/secret.yaml` — gabarit, jamais commit avec valeurs réelles) :

| Variable | Description |
|----------|-------------|
| `DB_HOST` | Hôte PostgreSQL |
| `DB_NAME` | Nom de la base |
| `DB_USER` | Utilisateur applicatif (droits limités, pas de DDL) |
| `DB_PASSWORD` | Mot de passe |
| `DB_PORT` | Port (5432 par défaut) |
| `JWT_SECRET` | Secret de signature des tokens (256 bits min, généré aléatoirement) |
| `CORS_ALLOWED_ORIGINS` | Origines autorisées (production : `https://preprod.azert.fr`) |

### Procédure

1. **Récupération du code**
   ```
   git clone git@github.com:<org>/<repo>.git
   cd <repo>
   git checkout v1.2.0   # tag de la release à déployer
   ```

2. **Création des Secrets**
   ```
   kubectl create secret generic backend-secrets \
     --from-literal=DB_PASSWORD=*** \
     --from-literal=JWT_SECRET=*** \
     -n production
   ```

3. **Application des manifests**
   ```
   kubectl apply -f backend/k8s/ -n production
   kubectl apply -f api/k8s/ -n production
   ```

4. **Vérification du rollout**
   ```
   kubectl rollout status deployment/backend -n production
   kubectl rollout status deployment/api -n production
   kubectl get pods -n production
   ```

5. **Vérification du healthcheck**
   ```
   curl https://preprod.azert.fr/api/health
   # → {"status": "ok", "db": "connected"}
   ```

6. **Tag de la release**
   ```
   git tag -a v1.2.0 -m "Release 1.2.0"
   git push origin v1.2.0
   ```

### Durée typique

- Build des images : ~3 min (CI)
- Rollout K8s : ~30 s (rolling update zero-downtime)
- Validation manuelle post-déploiement : ~5 min
```

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 10.5 procédure de déploiement"
```

---

### Task 25 : Stratégie de rollback (§ 10.6)

**Files:** Modify `doc/dossier_projet.md`

**CP couvert:** CP10

- [ ] **Step 1 : Rédiger § 10.6**

```markdown
## 10.6 Stratégie de rollback

### Cas d'usage déclenchant un rollback

- Régression fonctionnelle détectée en production
- Pic d'erreurs 5xx (> seuil d'alerte)
- Latence dégradée (P95 > seuil)
- Échec d'une migration de données critique

### Rollback applicatif (zero data loss)

Kubernetes conserve l'historique des `ReplicaSets`. Le retour à la version précédente s'effectue en une commande :

```
kubectl rollout undo deployment/backend -n production
kubectl rollout undo deployment/api -n production
```

Pour revenir à une révision spécifique (numérotée par `kubectl rollout history`) :

```
kubectl rollout history deployment/backend -n production
kubectl rollout undo deployment/backend --to-revision=42 -n production
```

### Rollback combiné code + image

1. Identifier le tag stable précédent : `git tag --sort=-creatordate | head -5`
2. Re-déployer à partir de ce tag (CI re-builds l'image et applique les manifests)
3. Vérifier le healthcheck

### Rollback de base de données

Les migrations de schéma sont **toujours additives et compatibles N-1** (ajout de colonnes nullable, jamais de suppression directe). Cela permet :
- Retour à la version applicative précédente sans rollback du schéma
- Suppressions de colonnes différées de 2 releases minimum

En cas de migration destructive accidentelle, restauration depuis le backup quotidien PostgreSQL (cf. § 10.7 et § 12.1).

### Communication

- Notification de l'équipe / des utilisateurs en cas de rollback impactant
- Post-mortem rédigé sous 48h
- Ticket de suivi du correctif
```

- [ ] **Step 2 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 10.6 stratégie de rollback"
```

---

### Task 26 : Monitoring (§ 10.7)

**Files:** Modify `doc/dossier_projet.md`

**CP couvert:** CP10

- [ ] **Step 1 : Rédiger § 10.7**

```markdown
## 10.7 Monitoring et observabilité

### Architecture cible

```
[Apps] ──exposent── /metrics (Prometheus format)
                          │
                          ▼
                   [Prometheus] ──── scrape toutes les 15 s
                          │
                          ▼
                    [Grafana] ──── dashboards + alerting
                          │
                          ▼
                 [Alertmanager] ──── notifications (email, Slack)
```

### Métriques exposées

#### Backend Go
- `http_requests_total{method,path,status}` — compteur de requêtes
- `http_request_duration_seconds{method,path}` — histogramme de latence
- `db_pool_connections{state}` — état du pool PostgreSQL
- `websocket_clients_connected` — gauge des connexions WS actives
- `auth_login_attempts_total{result}` — login réussis / échoués

#### API Python
- Mêmes métriques HTTP via [prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
- Latence par utilitaire (`convert`, `merge_excel`, etc.)

### Dashboards Grafana (cibles)

1. **Vue d'ensemble** : RPS, latence P50/P95/P99, taux d'erreur, uptime
2. **Sécurité** : logins échoués par heure, rate limit déclenché, accès refusés
3. **Base de données** : connexions, requêtes lentes, taille des tables
4. **Infrastructure** : CPU/RAM/Disk par pod, restarts

### Alerting

| Alerte | Seuil | Sévérité |
|--------|-------|----------|
| Taux d'erreur 5xx > 1 % sur 5 min | warning | P2 |
| Taux d'erreur 5xx > 5 % sur 5 min | critical | P1 |
| Latence P95 > 3 s sur 10 min | warning | P2 |
| Pod en CrashLoopBackOff | critical | P1 |
| Disque > 80 % | warning | P2 |
| Disque > 95 % | critical | P1 |

### Statut actuel

Healthcheck basique en place (`/api/health` testant la connexion DB). Stack Prometheus/Grafana documentée comme cible, à déployer post-soutenance.
```

- [ ] **Step 2 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 10.7 monitoring et observabilité"
```

---

### Task 27 : Versioning sémantique et CHANGELOG (§ 10.8)

**Files:** Modify `doc/dossier_projet.md`

**CP couvert:** CP11

- [ ] **Step 1 : Rédiger § 10.8**

```markdown
## 10.8 Versioning sémantique et CHANGELOG

### Versioning sémantique (SemVer)

Format des versions : `MAJOR.MINOR.PATCH` (https://semver.org)

| Composant | Incrément | Exemple |
|-----------|-----------|---------|
| MAJOR | Changement incompatible (breaking API, suppression de feature) | 1.x.x → 2.0.0 |
| MINOR | Ajout de fonctionnalité rétrocompatible | 1.2.x → 1.3.0 |
| PATCH | Correction de bug rétrocompatible | 1.2.3 → 1.2.4 |

### Tags Git

Chaque release est matérialisée par un tag annoté :

```
git tag -a v1.2.0 -m "Release 1.2.0 — ajout du module Analytics"
git push origin v1.2.0
```

### CHANGELOG.md

Format **[Keep a Changelog](https://keepachangelog.com)** maintenu manuellement (ou semi-automatiquement via `git-cliff` à partir des Conventional Commits — cf. § 3.4).

Structure :

```markdown
# Changelog

## [Unreleased]

## [1.2.0] — 2026-05-22
### Added
- Module Analytics (tableau de bord administrateur)
- WebSocket pour présence temps réel

### Changed
- Refonte de l'interface de connexion

### Fixed
- Typo CORS preprod
- Path traversal sur upload de fichiers

### Security
- Validation Origin sur les WebSockets (CSWSH)

## [1.1.0] — 2026-04-18
...
```

### Lien tag ↔ changelog

Chaque entrée du CHANGELOG correspond exactement à un tag Git. Les notes de release GitHub reprennent automatiquement le contenu du CHANGELOG via GitHub Actions.

### Statut

CHANGELOG.md à créer ; format documenté ici comme livrable cible.
```

- [ ] **Step 2 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 10.8 versioning sémantique et CHANGELOG"
```

---

### Task 28 : docker-compose.yml dev local (§ 10.9)

**Files:** Modify `doc/dossier_projet.md`

**CP couvert:** CP10

- [ ] **Step 1 : Vérifier qu'un docker-compose existe ou non**

```bash
ls docker-compose*.yml 2>/dev/null
```

(Selon `git status` il en existe un à la racine.)

- [ ] **Step 2 : Rédiger § 10.9**

```markdown
## 10.9 Développement local avec docker-compose

### Objectif

Permettre à un nouveau développeur de démarrer la stack complète (3 services + BDD) en une commande, sans avoir à installer manuellement Go, Python, PostgreSQL.

### Architecture

```
docker-compose.yml
├── service: postgres        (image: postgres:16-alpine)
├── service: backend         (build: ./backend)
├── service: api             (build: ./api)
└── service: frontend        (build: ./frontend, npm run dev en hot-reload)
```

### Extrait du `docker-compose.yml`

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: intranet
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      retries: 5

  backend:
    build: ./backend
    environment:
      DB_HOST: postgres
      DB_NAME: intranet
      DB_USER: dev
      DB_PASSWORD: dev
      DB_PORT: 5432
      JWT_SECRET: dev_secret_change_me
    ports:
      - "8002:8002"
    depends_on:
      postgres:
        condition: service_healthy

  api:
    build: ./api
    environment:
      DB_HOST: postgres
      # ... (idem)
    ports:
      - "8001:8001"
    depends_on:
      postgres:
        condition: service_healthy

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://localhost:8002
      VITE_PYTHON_API_URL: http://localhost:8001

volumes:
  pgdata:
```

### Commandes essentielles

```
docker compose up -d         # Démarrage en arrière-plan
docker compose logs -f       # Suivi des logs
docker compose down          # Arrêt + suppression des conteneurs
docker compose down -v       # Idem + suppression du volume Postgres (reset BDD)
```

### Bénéfices

- Setup en ~2 minutes (vs ~30 min en installation native)
- Isolation : pas d'impact sur la machine hôte
- Reproductibilité : tout le monde travaille avec la même version de PostgreSQL, des images, etc.
- Sépare clairement le local du déploiement K8s (section 10.2)
```

- [ ] **Step 3 : Commit**

```bash
git add doc/dossier_projet.md doc/TODO_CDA.md
git commit -m "docs(cda): add § 10.9 docker-compose dev local"
```

---

## PHASE 6 — Finalisation

### Task 29 : Relecture intégrale et harmonisation

**Files:** Modify `doc/dossier_projet.md` (passes de cohérence)

- [ ] **Step 1 : Régénérer la table des matières en tête du document**

Réécrire la section `# Table des matières` (autour des lignes 11-28) pour refléter le sommaire final (§ 2 de la spec).

- [ ] **Step 2 : Vérifier la cohérence de numérotation**

```bash
grep -n "^# \|^## \|^### " doc/dossier_projet.md
```

Vérifier qu'il n'y a pas de :
- Sauts de numérotation (§ 4.1 → § 4.3 sans § 4.2)
- Numéros dupliqués (deux § 9.5)
- Liens internes cassés (`[X](#x)`)

- [ ] **Step 3 : Harmonisation stylistique**

Critères :
- Ton impersonnel (« est », « repose », « permet » — éviter « j'ai », « nous »)
- Présent narratif uniquement
- Pas de Markdown imbriqué incohérent (gras dans titres, etc.)
- Acronymes définis à la première occurrence : JWT (JSON Web Token), MCD (Modèle Conceptuel de Données), etc.

- [ ] **Step 4 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): relecture intégrale, TDM et numérotation"
```

---

### Task 30 : Enrichissement bilan personnel (§ 13)

**Files:** Modify `doc/dossier_projet.md` (section 13)

- [ ] **Step 1 : Marquer pour rédaction manuelle**

Le bilan personnel est par nature subjectif. Conserver le contenu existant et ajouter un commentaire d'orientation :

```markdown
> Note de rédaction : la section "Bilan personnel" est complétée manuellement par le candidat avec ses ressentis spécifiques (apprentissages, surprises, points forts/faibles du parcours). Les éléments factuels (technologies acquises, difficultés résolues) peuvent s'appuyer sur les sections 3 à 11.
```

- [ ] **Step 2 : Commit**

```bash
git add doc/dossier_projet.md
git commit -m "docs(cda): orientation pour bilan personnel manuel"
```

---

### Task 31 : Vérification finale matrice REAC

**Files:** Modify `doc/TODO_CDA.md` (mise à jour finale)

- [ ] **Step 1 : Parcourir le TODO_CDA.md ligne par ligne**

Pour chaque CP / CT :
- Cocher les items effectivement couverts par le dossier mis à jour
- Mettre à jour la section « Priorités » en fin de fichier

- [ ] **Step 2 : Ajouter une section finale de bilan dans `TODO_CDA.md`**

```markdown
---

## Couverture finale (post-rédaction du dossier)

| CP / CT | Couverture | Section(s) |
|---------|------------|------------|
| CP1 | ✅ Complète | 5.1, 5.2 |
| CP2 | ✅ Complète | 4.2, 4.3, 7.* |
| CP3 | ✅ Complète | 4.6, 7.* |
| CP4 | ✅ Complète | 4.4.1 à 4.4.5 |
| CP5 | ✅ Complète | 6.1 à 6.6 |
| CP6 | ✅ Complète | 3.1 à 3.5 |
| CP7 | ✅ Complète | 8.1 à 8.9 |
| CP8 | ✅ Complète | 6.3, 6.4, 7.* |
| CP9 | ✅ Complète | 9.1 à 9.9 |
| CP10 | ✅ Complète | 10.1 à 10.9 |
| CP11 | ✅ Complète | 10.8, 3.5 |
| CT1 | ⚠️ Diaporama à préparer | Tout le dossier |
| CT2 | ✅ Complète | 14 (glossaire EN) |
| CT3 | ✅ Complète | 11.1 à 11.3 |

**Reste à produire (hors dossier) :**
- Diaporama de présentation (40 min)
- Captures d'écran (Annexe B)
- Réponses au questionnaire anglais (30 min)
```

- [ ] **Step 2 : Commit**

```bash
git add doc/TODO_CDA.md
git commit -m "docs(cda): bilan final couverture REAC"
```

---

## Récapitulatif

- **31 tâches** au total, regroupées en 6 phases
- **1 fichier principal modifié** : `doc/dossier_projet.md`
- **1 fichier secondaire mis à jour** : `doc/TODO_CDA.md` (suivi REAC)
- **Aucune modification de code applicatif** (ni `backend/`, ni `api/`, ni `frontend/src/`)
- **31 commits atomiques** (un par tâche) — facilite la relecture et le rollback en cas d'erreur de rédaction

## Self-review

**Spec coverage** :
- TDM cible (spec § 2) → tasks 1-31 (mappage 1:1 sous-section ★ → task)
- Matrice REAC (spec § 3) → task 31 (vérification finale)
- Plan section-par-section (spec § 4) → tasks 1-30
- Ordre d'exécution (spec § 5) → ordre des tasks identique aux phases
- Sources internes (spec § 6) → invoquées dans chaque task pertinente
- Contraintes (spec § 7) → respectées (1 fichier markdown, pas de code modifié, identité à remplir manuellement)
- Livrables (spec § 8) → task 31 produit le bilan

**Placeholder scan** : « [à compléter à partir de... ] » apparaît dans les tâches 5 et 18 — c'est intentionnel et explicite (référence à des extractions à faire depuis le code). Pas de « TBD » / « TODO » vague.

**Type consistency** : noms de fichiers et de sections cohérents entre tâches. Toutes les références croisées (§ X.Y → § Z.W) sont valides selon le sommaire cible.

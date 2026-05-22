# Spec — Plan de rédaction du dossier de projet CDA

**Projet** : Portail Intranet d'Entreprise
**Titre visé** : Concepteur Développeur d'Applications (CDA, Niveau 6)
**Document cible** : `doc/dossier_projet.md`
**Date** : 2026-05-22

---

## 1. Contexte et objectif

Un brouillon de dossier existe déjà (`doc/dossier_projet.md`, 1980 lignes, 15 sections). Un référentiel REAC TP CDA est suivi via `doc/TODO_CDA.md`. Une `table des matieres.pdf` issue d'un autre projet (réseau social) sert d'inspiration structurelle.

**Objectif** : produire le plan détaillé permettant de **restructurer + enrichir** le brouillon existant afin de couvrir intégralement le référentiel REAC, avec une organisation hybride (macro du brouillon, granularité PDF en section Réalisation).

**Hors scope de ce plan** :
- Annexes et captures d'écran (faites manuellement par le candidat plus tard)
- Identité candidat / entreprise / session (§ 1.2, § 1.5) → remplis manuellement
- Modifications du code applicatif (les items ★ qui mentionnent une implémentation — linters, rate limit, CSRF, E2E, CHANGELOG, docker-compose — seront documentés comme stratégie/cible si aucun code n'est ajouté)

---

## 2. Sommaire cible (TDM finale)

Macro-structure du brouillon conservée (15 sections REAC-alignées) ; section 7 réorganisée module-par-module ; 17 sous-sections nouvelles (★).

```
1. Introduction
   1.1  Contexte du projet
   1.2  Présentation de l'entreprise           [À remplir manuellement par le candidat]
   1.3  Objectifs
   1.4  Périmètre fonctionnel
   1.5  Identité candidat & cadre certification ★ NEW  [À remplir manuellement]

2. Cahier des charges
   2.1  Expression du besoin (BF / BNF)
   2.2  Contraintes (techniques, organisationnelles)
   2.3  Livrables attendus
   2.4  User Stories (5 épics)

3. Organisation du projet                       (CP6)
   3.1  Méthodologie Agile (Scrum/Kanban)
   3.2  Planning + Gantt + 6 sprints
   3.3  Outils de gestion (Git, GitHub Projects)
   3.4  Conventions de commit (Conventional Commits)    ★ NEW
   3.5  Stratégie de branching Git                      ★ NEW

4. Conception                                   (CP2-CP4)
   4.1  Cas d'utilisation + acteurs/rôles
   4.2  Maquettes & wireframes
   4.3  Principes UX + accessibilité RGAA              ★ NEW
   4.4  Modélisation des données
        4.4.1  Dictionnaire de données                  ★ NEW
        4.4.2  MCD
        4.4.3  MLD
        4.4.4  MPD (script SQL)
        4.4.5  Justification normalisation / index      ★ NEW
   4.5  Diagrammes de séquence
   4.6  Diagramme de classes UML                        ★ NEW

5. Choix des technologies                       (CP1)
   5.1  Tableau comparatif (Front, Back Go, API Py, BDD, Infra)
   5.2  Outillage de développement
        5.2.1  Linters & formatters                     ★ NEW
        5.2.2  IDE et extensions                        ★ NEW
   5.3  Architecture logicielle retenue

6. Architecture technique                       (CP5)
   6.1  Architecture globale
   6.2  Architecture frontend
   6.3  Architecture backend Go
   6.4  Architecture API Python
   6.5  Documentation des API REST (OpenAPI/Swagger)    ★ NEW
   6.6  Infrastructure de déploiement

7. Réalisation                                  (CP2-CP3-CP4-CP7-CP8)
   ── REFONTE COMPLÈTE : organisation module par module ──
   7.1  Authentification & sessions
   7.2  Administration des utilisateurs (CRUD + 6 rôles)
   7.3  Catalogue d'applications
   7.4  Outils métier (Silae, Excel/PDF/CSV, FEC, mappings comptables)
   7.5  Tableau de bord analytique
   7.6  WebSocket — présence temps réel
   7.7  Configuration McDonald's
   7.8  Thème (Dark Mode)

   Template homogène pour chaque module :
        7.X.1  Besoin fonctionnel
        7.X.2  Interface utilisateur (composants React)
        7.X.3  Backend (handlers + services + repository)
        7.X.4  Base de données (tables touchées)
        7.X.5  Flux complet (séquence)
        7.X.6  Extrait de code clé

8. Sécurité                                     (CP7)
   8.1  Analyse OWASP Top 10
   8.2  Authentification & sessions
   8.3  Contrôle d'accès RBAC (6 rôles)
   8.4  Protection RGPD
   8.5  Protection CSRF + headers sécurité             ★ NEW
   8.6  Rate limiting                                  ★ NEW
   8.7  Logging de sécurité                            ★ NEW
   8.8  Gestion des secrets
   8.9  Veille sécurité

9. Tests                                        (CP9)
   9.1  Stratégie globale
   9.2  Tests unitaires Go (testify + sqlmock)
   9.3  Tests unitaires Python (pytest, 84 tests)
   9.4  Tests unitaires Frontend (Vitest, 29 tests)
   9.5  Tests d'intégration
   9.6  Tests E2E (Playwright)                          ★ NEW
   9.7  Résultats & couverture
   9.8  Tests manuels et jeux de données                ★ NEW
   9.9  CI/CD : exécution automatique

10. Déploiement                                 (CP10-CP11)
    10.1  Conteneurisation Docker
    10.2  Orchestration Kubernetes
    10.3  Pipeline CI/CD
    10.4  Environnements (dev, preprod, prod)
    10.5  Procédure de déploiement step-by-step        ★ NEW
    10.6  Stratégie de rollback                        ★ NEW
    10.7  Monitoring (Prometheus/Grafana)              ★ NEW
    10.8  Versioning sémantique + CHANGELOG            ★ NEW
    10.9  docker-compose.yml dev local                 ★ NEW

11. Veille technologique et sécurité            (CT3)
    11.1  Veille techno
    11.2  Veille sécurité (CVE, ANSSI, OWASP)
    11.3  Résultats appliqués au projet

12. Améliorations et perspectives
13. Conclusion (bilan personnel, difficultés, perspectives)
14. Glossaire (FR + EN ★)
15. Annexes (A code, B captures, C tests, D CI/CD, E maquettes, F UML) — HORS SCOPE
```

**Diff résumé** : 17 nouvelles sous-sections, 0 suppression, section 7 entièrement réorganisée par **module** au lieu de par **technologie**.

---

## 3. Matrice de couverture REAC

| CP | Intitulé court | Section(s) dossier | État actuel |
|----|----------------|--------------------|-------------|
| CP1  | Installer/configurer l'environnement | 5.1, 5.2.1, 5.2.2 | Partiel — manque linters/formatters/IDE |
| CP2  | Développer des interfaces utilisateur | 4.2, 4.3, 7.*-UI | Partiel — manque UX/RGAA |
| CP3  | Développer des composants métier | 4.6, 7.*-backend | Partiel — manque diagramme classes |
| CP4  | Développer la persistance | 4.4.1 → 4.4.5 | Partiel — manque dictionnaire + justif normalisation |
| CP5  | Application multicouche répartie | 6.1, 6.5 | Partiel — manque OpenAPI |
| CP6  | Collaboration / gestion de projet | 3.1 → 3.5 | Partiel — manque conventions commit + branching |
| CP7  | Sécurité applicative | 8.1 → 8.9 | Partiel — manque CSRF, headers, rate limit, logging |
| CP8  | Composants d'accès aux données | 7.*-BDD, 6.3, 6.4 | OK — repository pattern documenté |
| CP9  | Plans de tests | 9.1 → 9.9 | Partiel — manque E2E + tests manuels |
| CP10 | Déploiement | 10.1 → 10.9 | Partiel — manque step-by-step + rollback + monitoring + compose |
| CP11 | Gestion de versions | 10.8, 3.5 | Manquant — SemVer + CHANGELOG |
| CT1  | Communication pro | Tout le dossier | Dossier OK ; diaporama hors scope |
| CT2  | Anglais | 14 (glossaire EN) | Manquant |
| CT3  | Veille / partage | 11.1 → 11.3 | Bien couvert |

**Conclusion** : tous les CP sont mappés à au moins une section. Les CP les plus exposés au jury (CP1, CP6, CP7, CP10, CP11) demandent le plus de travail rédactionnel.

---

## 4. Plan section-par-section

Légende état : ✅ OK · ⚠️ Partiel · ⛔ Manquant. Items ★ = nouveaux à rédiger.

### § 1 Introduction — ⚠️
- **1.2 Présentation entreprise** : [À remplir manuellement par le candidat]
- **★ 1.5 Identité candidat + cadre certif** : [À remplir manuellement]

### § 2 Cahier des charges — ✅
- Relecture seule : vérifier que les 5 épics couvrent bien Auth / Admin / Catalogue / Outils / WS / McDo Config

### § 3 Organisation (CP6) — ⚠️
- **★ 3.4 Conventions de commit** : décrire Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`), exemples tirés de `git log`
- **★ 3.5 Stratégie de branching** : schéma + workflow (GitHub Flow recommandé pour solo : `main` + branches `feature/*` éphémères)
- Vérification crédibilité des 6 sprints (durées, livrables alignés)

### § 4 Conception (CP2-CP4) — ⚠️
- **★ 4.3 UX + RGAA** : principes UX appliqués (cohérence, feedback, parcours), choix RGAA (aria-labels, contraste WCAG AA, navigation clavier, focus visible)
- **★ 4.4.1 Dictionnaire de données** : tableau exhaustif `entité × attribut × type × contrainte × description` — source : schémas SQL backend + modèles SQLAlchemy
- **★ 4.4.5 Justifications BDD** : 3NF, index uniques (email), FK avec ON DELETE CASCADE, choix de types
- **★ 4.6 Diagramme de classes UML** : importer depuis `doc/diagrammes.md` (sections 2-3 Mermaid)

### § 5 Choix techno (CP1) — ⚠️
- **★ 5.2.1 Linters/Formatters** : choix et règles
  - Frontend : ESLint (config react/recommended) + Prettier
  - Go : golangci-lint (linters: govet, errcheck, staticcheck, gosec) + gofmt
  - Python : ruff + black
- **★ 5.2.2 IDE & extensions** : VS Code + liste (ESLint, Prettier, Go, Python, Tailwind CSS IntelliSense, Docker, GitLens, REST Client)

### § 6 Architecture (CP5) — ⚠️
- **★ 6.5 API REST/OpenAPI** : capture du Swagger UI FastAPI (auto-généré sur `/docs`) + listing exhaustif des endpoints Go (méthode, path, rôle requis) tiré de `backend/cmd/main.go`

### § 7 Réalisation — REFONTE COMPLÈTE
Réorganisation du contenu existant (actuellement 7.1.* Frontend / 7.2.* Backend Go / 7.3.* API Python) en **8 modules verticaux**, chacun suivant le template :

```
7.X Module
  7.X.1  Besoin fonctionnel (rappel cahier des charges)
  7.X.2  Interface utilisateur (composants React + extraits)
  7.X.3  Backend (handlers → services → repository)
  7.X.4  Base de données (tables touchées + opérations)
  7.X.5  Flux complet (diagramme de séquence référencé)
  7.X.6  Extrait de code clé (commenté)
```

Modules :
- **7.1 Authentification & sessions** — auth Go + middlewares + Login.jsx + Register.jsx (← actuels 7.1.1 + 7.2.1 + 7.2.2)
- **7.2 Administration des utilisateurs** — admin Go + Admin/Users.jsx (← actuel 7.1.2)
- **7.3 Catalogue d'applications** — applications Go + Dashboard.jsx
- **7.4 Outils métier** — Python utils (Silae, Excel merge, EDI, FEC, code mappings) + pages/ (← actuels 7.1.3 + 7.3.*)
- **7.5 Tableau de bord analytique** — analyse Go + AdminAnalytics.jsx (← actuel 7.2.4)
- **7.6 WebSocket — présence temps réel** — websocket Go + useWebSocket (← actuels 7.1.5 + 7.2.3)
- **7.7 Configuration McDonald's**
- **7.8 Thème (Dark Mode)** — ThemeContext (← actuel 7.1.4)

**Important** : la matière première existe déjà ; c'est essentiellement du **réagencement + complément** par module, pas de rédaction from-scratch.

### § 8 Sécurité (CP7) — ⚠️
- **★ 8.5 CSRF + headers** : protection CSRF (SameSite=Strict en cookie d'auth, ou double-submit cookie), headers (CSP, HSTS, X-Frame-Options DENY, X-Content-Type-Options nosniff, Referrer-Policy)
- **★ 8.6 Rate limiting** : token bucket sur endpoints auth (middleware Go avec `golang.org/x/time/rate` ou `tollbooth`)
- **★ 8.7 Logging sécurité** : événements journalisés (login échoué, action admin, accès refusé), format structuré (JSON), rétention (90 jours recommandé)

### § 9 Tests (CP9) — ⚠️
- **★ 9.6 Tests E2E** : choix Playwright, scénarios couverts :
  1. Login → accès catalogue
  2. Admin → création / édition / suppression utilisateur
  3. Utilisateur → upload fichier outil métier → téléchargement résultat
  4. Échec login → message d'erreur affiché
  5. Logout → redirection landing
- **★ 9.8 Tests manuels et jeux de données** : matrice de parcours utilisateur testés + jeux de données pour Silae/FEC/Excel/EDI

### § 10 Déploiement (CP10-CP11) — ⚠️
- **★ 10.5 Procédure step-by-step** : prérequis (kubectl, helm, accès cluster) → vars env → secrets K8s → `kubectl apply -f ...` → migrations → vérification healthchecks
- **★ 10.6 Rollback** : `kubectl rollout undo deployment/xxx` + retour tag Git précédent, procédure documentée
- **★ 10.7 Monitoring** : architecture cible Prometheus + Grafana, métriques exposées (latence, taux erreur, RPS), dashboards essentiels
- **★ 10.8 SemVer + CHANGELOG** : MAJOR.MINOR.PATCH, créer `CHANGELOG.md` au format Keep-a-Changelog, tags Git pour chaque release
- **★ 10.9 docker-compose.yml dev local** : 3 services (frontend, backend, api) + PostgreSQL + volumes + healthchecks

### § 11 Veille (CT3) — ✅
- Relecture seule

### § 12 Améliorations — ✅
- Relecture seule

### § 13 Conclusion — ✅
- Enrichissement optionnel du bilan personnel

### § 14 Glossaire — ⚠️
- **★ Colonne EN** sur chaque terme du glossaire (couvre CT2)

### § 15 Annexes — HORS SCOPE
- Annexes A à F déjà cadrées ; captures, code, tests, CI/CD, maquettes, UML : remplis manuellement par le candidat

---

## 5. Ordre d'exécution

### Phase 0 — Pré-requis
- § 1.2 et § 1.5 marqués `[À remplir manuellement]`
- Décision : items ★ "implémentation" (linters, rate limit, CSRF, E2E, CHANGELOG, compose) → documentés comme **stratégie/cible** ; pas de code modifié dans le repo

### Phase 1 — Fondations indépendantes (parallélisables)
Sections autonomes, sans dépendance. Quick wins.
- § 3.4, § 3.5 (commit, branching)
- § 5.2.1, § 5.2.2 (outillage)
- § 11 relecture
- § 14 glossaire EN

### Phase 2 — Conception (préalable à la refonte § 7)
- § 4.4.1 Dictionnaire de données ← **prioritaire** (fondation)
- § 4.4.5 Justifications BDD
- § 4.6 Diagramme de classes (import depuis `diagrammes.md`)
- § 4.3 UX + RGAA

### Phase 3 — Refonte de la section 7 (gros morceau)
Réagencement du contenu existant en 8 modules, ordre :
7.1 Auth → 7.2 Admin → 7.3 Catalogue → 7.4 Outils métier → 7.5 Analytics → 7.6 WS → 7.7 McDo → 7.8 Thème

### Phase 4 — Architecture & Sécurité & Tests (parallélisables)
- § 6.5 OpenAPI
- § 8.5, § 8.6, § 8.7
- § 9.6, § 9.8

### Phase 5 — Déploiement (CP10-CP11)
- § 10.5 → § 10.6 → § 10.7 → § 10.8 → § 10.9

### Phase 6 — Finalisation
- Relecture intégrale, harmonisation ton et numérotation
- Enrichissement § 13
- TDM auto-mise-à-jour
- Vérification finale matrice REAC

---

## 6. Sources internes mobilisables

| Source | Contenu |
|--------|---------|
| `doc/dossier_projet.md` | Brouillon de base (1980 lignes, 15 sections) |
| `doc/TODO_CDA.md` | Checklist des 11 CP + 3 CT REAC |
| `doc/diagrammes.md` | 11 diagrammes Mermaid (classes, séquences, archi) |
| `doc/Rfrentiel_*.pdf` | Référentiel REAC officiel |
| `doc/table des matieres.pdf` | TDM exemple (réseau social) — inspiration granularité |
| `doc/mockups/`, `doc/schemas/` | Maquettes et schémas existants |
| `doc/html_figma/` | Mockups HTML |
| `backend/` (Go) | Code source pour § 7.* backend, § 4.4.* BDD |
| `api/` (Python) | Code source pour § 7.4 outils métier |
| `frontend/src/` | Code source pour § 7.* UI |
| `backend/k8s/`, `api/k8s/` | Manifests K8s pour § 10 |
| `.github/workflows/` | CI/CD pour § 10.3 |
| `git log` | Conventions de commit, sprints, historique pour § 3 |

---

## 7. Contraintes et hypothèses

- **Format de sortie** : Markdown unique dans `doc/dossier_projet.md` (pas de scission en multi-fichiers)
- **Pas de modification du code applicatif** dans cette phase (documentation only)
- **Annexes** : la structure A-F reste en place ; le contenu est rempli manuellement plus tard
- **Identité (§ 1.2, § 1.5)** : remplis manuellement par le candidat
- **Diaporama** : hors scope (CT1 partiellement couvert par le dossier lui-même)
- **Délai** : non contraint à ce stade

---

## 8. Livrables de l'exécution

1. **`doc/dossier_projet.md` restructuré** — sommaire conforme à la section 2, contenu existant réorganisé + 17 nouvelles sous-sections rédigées
2. **TDM auto-générée** à jour
3. **Mises à jour de `doc/TODO_CDA.md`** : items REAC couverts cochés au fil de l'eau
4. **Aucune modification de code applicatif** (sauf demande explicite ultérieure)

---

## 9. Étape suivante

Une fois cette spec validée par le candidat, invoquer la skill `superpowers:writing-plans` pour produire un **plan d'implémentation exécutable** (découpé en tâches d'écriture concrètes, une par sous-section, dans l'ordre des phases 1 → 6).

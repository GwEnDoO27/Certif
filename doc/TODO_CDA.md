# TODO - Conformité REAC TP CDA (Titre Professionnel Concepteur Développeur d'Applications)

> Analyse du projet Portail Intranet vs les 11 compétences du référentiel REAC 2023

---

## AT1 - Développer une application sécurisée

### CP1 - Installer et configurer son environnement de travail en fonction du projet
- [x] Stack technique définie (React, Go, Python, PostgreSQL)
- [x] Docker pour conteneurisation
- [x] Kubernetes pour orchestration
- [ ] **Documenter la procédure d'installation de l'environnement de dev** (README détaillé avec prérequis)
- [ ] **Documenter le choix des outils** (IDE, extensions, linters, formatters)
- [ ] **Mettre en place un linter frontend** (ESLint avec config stricte)
- [ ] **Mettre en place un linter backend Go** (golangci-lint)
- [ ] **Mettre en place un linter Python** (ruff ou flake8)
- [ ] **Mettre en place un formatter** (Prettier frontend, gofmt backend, black Python)
- [x] **Documenter la veille technologique** (dossier section 11.1)
- [ ] **Créer un document de veille sécurité** (CVE, ANSSI, OWASP)

### CP2 - Développer des interfaces utilisateur
- [x] Frontend React avec composants modulaires (54 fichiers JSX)
- [x] Responsive design avec Tailwind CSS
- [x] Dark mode (ThemeContext)
- [x] Lazy loading des pages (React.lazy)
- [x] Animations (Framer Motion)
- [x] **Créer des maquettes/wireframes** (wireframes ASCII dans le dossier, section 4.2)
- [ ] **Documenter les principes UX appliqués** (ergonomie, parcours utilisateur)
- [ ] **Ajouter la conformité RGAA** (accessibilité : aria-labels, navigation clavier, contraste)
- [ ] **Documenter les choix d'accessibilité** dans le dossier
- [ ] **Ajouter des tests d'interface** (React Testing Library ou Cypress)
- [ ] **Créer des user stories** formalisées pour chaque fonctionnalité
- [ ] **Documenter la gestion d'état** (Context API, flux de données)

### CP3 - Développer des composants métier
- [x] Architecture Handler → Service → Repository (Go backend)
- [x] Modèles de données structurés (Go structs, SQLAlchemy models)
- [x] Services métier : auth, admin, applications, analytics, websocket, McDonald's config
- [x] API Python avec traitement de fichiers Excel/PDF/CSV
- [x] Système de mapping de codes comptables
- [ ] **Documenter les règles métier** dans le dossier (cahier des charges fonctionnel)
- [x] **Créer des diagrammes de classes** (UML) — doc/diagrammes.md sections 2-3
- [x] **Créer des diagrammes de séquence** — doc/diagrammes.md sections 4-7
- [x] **Ajouter la validation des données d'entrée** côté API (validation UUID, filepath.Base sur uploads)
- [x] **Améliorer la couverture de tests unitaires** (Python API : 84 tests, Frontend : 29 tests)
- [ ] **Ajouter des tests d'intégration** documentés
- [x] **Documenter les design patterns utilisés** (dossier sections 6.3, 7.2, annexe A)

### CP4 - Développer la persistance des données
- [x] PostgreSQL avec connexion poolée
- [x] Modèles SQLAlchemy (Python)
- [x] Repository pattern (Go)
- [x] Sessions en base de données avec expiration
- [x] **Créer le MCD (Modèle Conceptuel de Données)** — doc/diagrammes.md section 10
- [x] **Créer le MLD (Modèle Logique de Données)** — dossier section 4.3.2
- [x] **Créer le MPD (Modèle Physique de Données)** — dossier section 4.3.3 (script SQL)
- [ ] **Documenter les choix de conception BDD** (normalisation, index, contraintes)
- [ ] **Ajouter des migrations de base de données** (golang-migrate ou alembic)
- [ ] **Documenter la stratégie de sauvegarde** des données
- [x] **Implémenter/documenter la conformité RGPD** (dossier section 8.4)

---

## AT2 - Concevoir et développer une application sécurisée organisée en couches

### CP5 - Développer une application multicouche répartie
- [x] Architecture microservices (3 services + BDD)
- [x] Communication inter-services via HTTP/REST
- [x] WebSocket pour temps réel
- [x] Frontend SPA avec routing
- [x] **Créer un diagramme d'architecture** — doc/diagrammes.md sections 8-9
- [ ] **Documenter les API REST** (Swagger/OpenAPI pour Python, documentation Go)
- [ ] **Ajouter OpenAPI/Swagger à FastAPI** (déjà intégré mais documenter)
- [ ] **Documenter les contrats d'interface** entre services
- [ ] **Implémenter un mécanisme de health check** complet (actuellement basique)
- [ ] **Ajouter la gestion des erreurs centralisée** côté frontend

### CP6 - Collaborer à la gestion d'un projet informatique
- [x] Git pour le versioning
- [x] GitHub Actions pour CI/CD
- [ ] **Mettre en place un outil de gestion de projet** (Jira, Trello, ou GitHub Projects)
- [ ] **Créer un planning de projet** (diagramme de Gantt)
- [ ] **Documenter la méthodologie Agile** utilisée (Scrum/Kanban)
- [ ] **Créer des comptes-rendus de réunion** (même fictifs si projet solo)
- [ ] **Documenter les sprints** (backlog, sprint review, rétrospective)
- [ ] **Utiliser les conventions de commit** (Conventional Commits)
- [ ] **Créer un tableau Kanban** documenté avec captures d'écran
- [ ] **Rédiger les spécifications techniques** détaillées

### CP7 - Développer une application sécurisée
- [x] Authentification JWT/sessions avec cookies sécurisés (SameSite, HttpOnly)
- [x] Hashage bcrypt des mots de passe
- [x] CORS configuré
- [x] 6 rôles avec contrôle d'accès (Admin, Dev, Comptable, Social, Auditeur, Client)
- [x] Nettoyage automatique des sessions expirées
- [x] **Documenter la politique de sécurité** (dossier section 8 — OWASP Top 10)
- [ ] **Ajouter la protection CSRF** explicite
- [ ] **Ajouter le rate limiting** sur les endpoints d'auth
- [x] **Implémenter la validation des entrées** systématique (UUID regex, filepath.Base, requêtes paramétrées)
- [ ] **Ajouter des headers de sécurité** (CSP, X-Frame-Options, HSTS)
- [x] **Documenter la veille sécurité** (dossier sections 8.5 et 11)
- [x] **Corriger le typo CORS** backend (`prepord` → `preprod`)
- [ ] **Ajouter des tests de sécurité** (OWASP ZAP ou similaire)
- [x] **Documenter la gestion des secrets** (variables d'environnement, pas de secrets en dur — JWT externalisés)
- [ ] **Ajouter le logging de sécurité** (tentatives de connexion échouées, actions admin)

### CP8 - Développer des composants d'accès aux données
- [x] Repository pattern en Go
- [x] SQLAlchemy ORM en Python
- [x] Requêtes paramétrées (protection injection SQL)
- [x] Connection pooling
- [ ] **Documenter les patterns d'accès aux données** utilisés
- [ ] **Ajouter un système de cache** (Redis) si pertinent
- [ ] **Documenter les requêtes SQL complexes** avec explications
- [ ] **Ajouter des index de performance** documentés
- [ ] **Implémenter la pagination** sur les endpoints de liste

---

## AT3 - Préparer le déploiement d'une application sécurisée

### CP9 - Préparer et exécuter les plans de tests
- [x] Tests unitaires Go (11 fichiers) avec testify + sqlmock
- [x] CI qui exécute les tests Go
- [x] **Créer un plan de tests** (dossier section 9.1 — stratégie et couverture)
- [x] **Ajouter des tests unitaires Python** (84 tests pytest — 7 fichiers)
- [x] **Augmenter les tests frontend** (29 tests Vitest — 4 fichiers)
- [ ] **Ajouter des tests E2E** (Cypress ou Playwright)
- [x] **Documenter les résultats des tests** (dossier sections 9.6 et annexe C)
- [ ] **Ajouter le rapport de couverture** dans la CI (go test -cover, pytest-cov)
- [ ] **Créer des jeux de données de test** documentés
- [ ] **Documenter les tests manuels** effectués (captures d'écran)

### CP10 - Préparer et exécuter le déploiement d'une application
- [x] Dockerfiles multi-stage pour les 3 services
- [x] Manifestes Kubernetes (16 fichiers)
- [x] GitHub Actions CI/CD
- [x] Traefik IngressRoute
- [x] Persistent Volume Claims
- [ ] **Documenter la procédure de déploiement** complète (step by step)
- [ ] **Créer un docker-compose.yml** pour le développement local
- [ ] **Documenter l'architecture d'infrastructure** (schéma réseau, K8s cluster)
- [ ] **Ajouter des scripts de déploiement** documentés
- [ ] **Documenter la stratégie de rollback**
- [ ] **Mettre en place le monitoring** (Prometheus/Grafana ou équivalent)
- [ ] **Documenter les environnements** (dev, preprod, prod)

### CP11 - Gérer les versions d'une application
- [x] Git avec GitHub
- [x] CI/CD automatisé
- [ ] **Documenter la stratégie de branching** (Git Flow, GitHub Flow, etc.)
- [ ] **Mettre en place le versioning sémantique** (SemVer)
- [ ] **Ajouter un CHANGELOG.md**
- [ ] **Documenter la politique de release**
- [ ] **Ajouter des tags Git** pour les versions
- [ ] **Documenter la gestion des branches** (feature, develop, release, hotfix)

---

## Compétences transversales

### CT1 - Communiquer en situation professionnelle
- [ ] **Préparer le diaporama** de présentation (40 min)
- [ ] **Préparer les réponses** aux questions types de l'entretien technique
- [ ] **Préparer le questionnaire anglais** (vocabulaire technique)
- [ ] **Rédiger le dossier de projet** (40-60 pages + annexes)

### CT2 - Utiliser l'anglais dans son activité professionnelle
- [ ] **Documenter les termes techniques en anglais** (glossaire)
- [ ] **Préparer le questionnaire professionnel en anglais** (30 min)
- [x] Code source principalement en anglais (noms de variables, fonctions)

### CT3 - Actualiser et partager ses compétences
- [ ] **Documenter la veille technologique** (outils, sources, résultats)
- [ ] **Documenter les formations/certifications** suivies
- [ ] **Préparer un portfolio** de compétences

---

## Documents à produire pour le dossier

### Obligatoires (référentiel REAC)
1. [ ] **Cahier des charges** (contexte, besoins, contraintes, livrables)
2. [ ] **Spécifications fonctionnelles** (user stories, cas d'utilisation)
3. [ ] **Spécifications techniques** (architecture, choix technologiques justifiés)
4. [ ] **Maquettes/Wireframes** (UI/UX design)
5. [ ] **MCD / MLD / MPD** (modélisation données)
6. [ ] **Diagrammes UML** (classes, séquence, cas d'utilisation, déploiement)
7. [ ] **Plan de tests** + résultats
8. [ ] **Documentation sécurité** (OWASP, RGPD, veille)
9. [ ] **Documentation déploiement** (CI/CD, Docker, K8s)
10. [ ] **Dossier de projet** complet (40-60 pages)
11. [ ] **Diaporama** de présentation
12. [ ] **Annexes** (code source pertinent, captures d'écran, résultats de tests)

### Recommandés (pour le dossier)
- [ ] Glossaire technique
- [ ] Bibliographie / sources de veille
- [ ] Tableau de bord du projet (Kanban, Gantt)
- [ ] Captures d'écran de l'application
- [ ] Extraits de code commentés

---

## Priorités

### Haute priorité (indispensable pour le dossier)
1. ~~Rédiger le dossier de projet~~ ✅ Rédigé (doc/dossier_projet.md)
2. ~~Créer les maquettes~~ ✅ Wireframes ASCII intégrés (section 4.2)
3. ~~Créer MCD/MLD/MPD~~ ✅ Modélisés (sections 4.3 + diagrammes.md)
4. ~~Créer les diagrammes UML~~ ✅ 11 diagrammes Mermaid (doc/diagrammes.md)
5. ~~Rédiger le cahier des charges~~ ✅ Rédigé (section 2)
6. ~~Documenter la sécurité (OWASP Top 10)~~ ✅ (section 8)
7. ~~Créer le plan de tests~~ ✅ (section 9)
8. Préparer le diaporama

### Moyenne priorité (améliore le dossier)
9. ~~Ajouter tests Python (pytest)~~ ✅ 84 tests
10. ~~Ajouter tests frontend~~ ✅ 29 tests
11. Créer docker-compose.yml pour dev local
12. ~~Documenter la CI/CD~~ ✅ (section 10.3 + annexe D)
13. ~~Documenter la veille technologique~~ ✅ (section 11)
14. Ajouter linters/formatters

### Basse priorité (bonus)
15. Tests E2E (Cypress)
16. Monitoring (Prometheus/Grafana)
17. Cache Redis
18. Rate limiting
19. CHANGELOG.md + SemVer

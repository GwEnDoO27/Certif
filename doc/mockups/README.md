# Maquettes UI — Portail Cabinet Martini

> Date : 2026-05-22 — Mockups haute fidélité des 5 pages de l'application.
> Couvre la compétence **REAC TP CDA · CP2** (« Créer des maquettes / wireframes »).

## Vue d'ensemble

Cinq pages composent l'application :

| # | Page       | Route                | Composant React                                    | Rôle métier |
|---|------------|----------------------|----------------------------------------------------|-------------|
| 1 | Login      | `/`                  | `frontend/src/components/Auth/Login.jsx`           | Authentification publique |
| 2 | Home       | `/home`              | `frontend/src/components/Landing/Home.jsx`         | Tableau de bord post-login |
| 3 | Admin      | `/admin`             | `frontend/src/components/Admin/Admin.jsx`          | Console d'administration (rôle Admin) |
| 4 | Convert    | `/facture-mb/home`   | `frontend/src/components/pages/Convert/Convert_main.jsx` | Conversion EDI → XLSX (rôle Comptable) |
| 5 | 404        | `*` (fallback)       | `frontend/src/utils/NotFound.jsx`                  | Page d'erreur |

## Progression du design en 4 stades

Le dossier documente la démarche complète, du découpage fonctionnel au pixel-perfect :

| Stade | Fidélité | Fichier | Objet de validation |
|-------|----------|---------|---------------------|
| **0. Zoning** | conceptuelle | [`00-zoning.html`](./00-zoning.html) — planche des 5 pages | Découpage en zones fonctionnelles (Navigation, Identité, Action, Saisie, Auxiliaire…) |
| **1. Wireframe** | basse | [`00-wireframes.html`](./00-wireframes.html) — planche des 5 pages | Structure, parcours, hiérarchie d'information |
| **2. Maquette** | moyenne (abstraite) | [`00-maquettes.html`](./00-maquettes.html) — planche des 5 pages | Grille, rythme visuel, espacements, hiérarchie typographique (sans contenu réel) |
| **3. Mockup HD** | haute | 5 fichiers individuels (voir ci-dessous) | UI finale, composants pixel-perfect, dark + light |

### Mockups haute fidélité (stade 3)

Chaque mockup HD est autonome (Tailwind via CDN, icônes Lucide en SVG inline) — il peut être ouvert directement dans un navigateur ou imprimé.

| Fichier                                | Aperçu |
|----------------------------------------|--------|
| [`01-login.html`](./01-login.html)     | Page de connexion — light + dark side-by-side |
| [`02-home.html`](./02-home.html)       | Tableau de bord — widgets, sélecteur d'apps, fil d'actualités |
| [`03-admin.html`](./03-admin.html)     | Console admin — onglets, stats, CRUD utilisateurs, panel temps réel |
| [`04-convert.html`](./04-convert.html) | Transformation factures MB — stepper, codes, drop zone, conversion |
| [`05-notfound.html`](./05-notfound.html) | 404 — état actuel + proposition d'évolution alignée à la charte |

## Démarche

1. **Analyse du code existant** — lecture systématique de chaque composant JSX pour identifier la structure, les composants UI, les états et les flux.
2. **Stade 0 — Zoning** — découpage de chaque page en zones fonctionnelles colorées (Navigation, Identité, Contenu, Action, Saisie, Auxiliaire, Feedback, Méta). Chaque couleur = un rôle UX, pas un choix esthétique. Permet de valider l'architecture de l'information avant tout dessin.
3. **Stade 1 — Wireframes** — production de boîtes grises + libellés pour figer la structure et le parcours, sans distraction visuelle. Annotations numérotées du flux utilisateur sur chaque page.
4. **Stade 2 — Maquettes (abstraites)** — barres grises + placeholders, une seule couleur d'accent (primary). Aucun texte réel, aucune icône. Permet de valider la **grille**, le **rythme**, les **espacements** et la **hiérarchie typographique par la taille seule** — sans confusion possible avec le rendu final.
5. **Stade 3 — Mockups HD** — reproduction fidèle du rendu final pour chaque page : couleurs, espacements, icônes (Lucide), animations Framer Motion documentées en note. Side-by-side light/dark pour démontrer le support `ThemeContext` (stratégie Tailwind `darkMode: 'class'`).
6. **Annotations** — chaque livrable se termine par un bloc explicatif qui explicite les choix UX/UI et le mapping vers le code source.

## Système de design (synthèse)

### Palette

| Token              | Hex        | Usage |
|--------------------|------------|-------|
| `primary`          | `#6366f1`  | Indigo — couleur de marque, CTA, accents système |
| `primary-hover`    | `#4f46e5`  | État hover des CTA primaires |
| `blue-500/600`     | `#3b82f6` / `#2563eb` | Accent métier (Convert, Excel/factures) |
| `green-500/emerald-600` | `#22c55e` / `#059669` | Action de traitement / succès |
| `slate-50…950`     | gris froid | Backgrounds et textes (light/dark) |
| Accents catalogue  | indigo, rose, violet, emeraude, ambre, bleu, rouge, cyan | Couleur attribuée par index aux cartes du sélecteur d'applications |

### Typographie

- Famille : `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto…`
- Lissage : `antialiased`
- Titres : `font-bold` + `tracking-tight` (`letter-spacing: -0.02em`)
- Monospace : pour l'horloge live (`ClockWidget`)

### Composants récurrents

- **Glassmorphism** — `bg-white/60` ou `bg-slate-900/55` + `backdrop-blur-20px` + bordure semi-translucide. Utilisé : Login, widgets Home, header sticky.
- **Cartes** — `rounded-2xl` (16-24 px), `border-slate-200` (light) / `border-slate-700` (dark), `shadow-sm` → `shadow-md` au hover.
- **Boutons CTA** — gradient diagonal, ombre colorée correspondante (`shadow-primary/20`), micro-interaction `hover:-translate-y-0.5`.
- **Inputs** — `rounded-xl`, icône Lucide en `absolute left-4`, focus ring `focus:ring-primary/20`.
- **Badges** — pilule `rounded-full`, fond léger (`bg-color-50`) + texte foncé (`text-color-700`).

### Iconographie

`lucide-react` exclusivement (cohérence visuelle). Icônes utilisées par page documentées dans chaque mockup.

### Animations

`framer-motion` pour les apparitions (`opacity 0→1`, `y 20→0`), `motion.div` avec `initial / animate / transition`. Keyframes Tailwind custom : `fade-in`, `slide-up`, `pulse-slow`.

## Décisions de design notables

### Choix d'accent par page

| Page    | Accent dominant | Justification |
|---------|-----------------|---------------|
| Login   | Indigo (primary) | Identité de marque, sobriété formulaire |
| Home    | Indigo + 8 accents catalogue | Diversité visuelle des outils, mémorisation |
| Admin   | Indigo + couleurs sémantiques (bleu/vert/orange/jaune par rôle) | Distinction immédiate des rôles |
| Convert | Bleu + vert | Bleu = Excel/factures (métier comptable), vert = action de traitement |
| 404     | Gradient indigo → rose | Cohérence avec le Login, ton chaleureux pour erreur |

### Cas particulier : la page 404

Le composant actuel (`utils/NotFound.jsx`) est minimaliste (12 lignes). Le mockup propose une évolution alignée à la charte glassmorphism du reste du portail, avec :

- Typographie « 404 » géante avec gradient bicolore
- Badge d'alerte flottant
- Doubles CTA (retour accueil + page précédente)
- Lien de support

C'est une **proposition argumentée** — utile pour démontrer la démarche UX dans le dossier REAC : analyse de l'existant → constat de cohérence → proposition.

## Reproductibilité

Les livrables peuvent être régénérés en relisant les composants source à la date du commit. Pour une mise à jour future :

1. Identifier les changements visuels dans le code React.
2. Mettre à jour le bloc HTML correspondant dans `doc/mockups/` (généralement seul le mockup HD nécessite mise à jour ; les wireframes et maquettes restent stables tant que la structure ne change pas).
3. Pour les mockups HD : vérifier la cohérence light/dark.
4. Mettre à jour la section « Décisions notables » si un nouveau pattern apparaît.

## Pour le dossier REAC

Cette progression à 4 stades démontre concrètement la démarche UX/UI :

- **Zoning** prouve la réflexion **fonctionnelle** préalable (architecture de l'information)
- **Wireframes** prouvent la réflexion **structurelle** (parcours utilisateur, hiérarchie de contenu)
- **Maquettes abstraites** valident la **grille et le rythme visuel** (espacements, hiérarchie typographique)
- **Mockups HD** valident le **rendu final** et la cohérence dark/light

Couplée aux captures HTML de production dans [`doc/html_figma/`](../html_figma/), la chaîne documentaire est complète : analyse fonctionnelle → maquettage → rendu final.

## Voir aussi

- [`doc/html_figma/`](../html_figma/) — captures DOM réelles (post-build, via puppeteer) pour import Figma via le plugin html.to.design
- [`doc/diagrammes.md`](../diagrammes.md) — diagrammes UML (composants frontend en section 8)
- [`doc/TODO_CDA.md`](../TODO_CDA.md) — référentiel REAC, section **AT1 / CP2**

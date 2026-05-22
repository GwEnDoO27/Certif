# Pages HTML pour import Figma

Captures du DOM rendu (production build + puppeteer + mocks API) prêtes à importer dans Figma via le plugin **html.to.design**.

| Fichier        | Route source           | Composant React                      | État capturé |
|---------------|------------------------|--------------------------------------|--------------|
| `login.html`  | `/`                    | `Auth/Login.jsx`                     | Public, formulaire vide |
| `home.html`   | `/home`                | `Landing/Home.jsx`                   | Authentifié, widget actualités rempli |
| `admin.html`  | `/admin`               | `Admin/Admin.jsx`                    | Authentifié + admin, liste 2 utilisateurs mockés |
| `convert.html`| `/facture-mb/home`     | `pages/Convert/Convert_main.jsx`     | Authentifié, codes comptables mockés |
| `404.html`    | `/route-inexistante`   | `utils/NotFound.jsx`                 | Page d'erreur |

## Procédé de génération

Le script `frontend/extract-html.mjs` :
1. Lance Chrome headless (puppeteer)
2. Intercepte les requêtes API (`localhost:800x` + domaines de prod) et renvoie un mock JSON cohérent
3. Injecte un cookie `userId` factice via `evaluateOnNewDocument` pour passer `AuthenticationWrapper`
4. Pour chaque route : `goto` → attente `networkidle0` → 1,5s buffer → capture du DOM cloné

## Comment régénérer

```bash
cd frontend
npm run build
npx vite preview --port 4173 --host 127.0.0.1 &
PUPPETEER_CACHE_DIR=/tmp/puppeteer-cache node extract-html.mjs
```

## Import dans Figma

1. Installer le plugin **html.to.design** depuis la Community.
2. Ouvrir un fichier Figma, lancer le plugin.
3. Onglet « Upload HTML file » → choisir un fichier `.html` du dossier.
4. Le plugin convertit le DOM + CSS en frame Figma (composants, autolayout).
5. Répéter pour chaque page.

> **Note** : le plugin gratuit limite à quelques imports/jour. Les frames produites sont éditables (textes, couleurs, classes Tailwind converties en styles Figma natifs).

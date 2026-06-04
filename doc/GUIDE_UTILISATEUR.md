# Guide utilisateur — Plateforme & Outil de traitement des tirages de caisse

> Ce guide s'adresse aux utilisateurs métier (rôle **Comptable**) de la plateforme.
> Pour l'administration des comptes et du catalogue, voir la *Notice Administration* (`frontend/NOTICE_ADMIN.md`).

---

## 1. Se connecter

1. Ouvrez la plateforme dans un navigateur récent (Chrome, Firefox, Edge ou Safari).
2. Sur la page d'accueil, cliquez sur **Connexion**.
3. Saisissez votre **e-mail** et votre **mot de passe**, puis validez.
4. Après authentification, vous arrivez sur votre **catalogue d'applications** : seules les applications qui vous ont été attribuées y figurent.

> 🔒 En cas d'identifiants incorrects, un message générique « identifiants invalides » s'affiche (sécurité anti-énumération). Après plusieurs tentatives échouées, l'accès est temporairement limité.

Pour vous déconnecter, utilisez l'icône **🚪** en haut à droite. Votre session expire automatiquement après 24 h d'inactivité.

---

## 2. Ouvrir l'outil de traitement des tirages de caisse

Depuis le catalogue, cliquez sur la vignette **Tirages Caisse**.

L'écran de l'outil se compose de trois zones :

| Zone | Rôle |
|---|---|
| **Paramétrage des codes** | Définir/réviser vos codes comptables avant traitement |
| **Dépôt des fichiers** | Importer les tirages de caisse `.EDI` / `.txt` |
| **Résultat** | Télécharger le fichier Excel généré |

---

## 3. Paramétrer ses codes comptables (à faire une fois par client)

Le traitement applique **vos** codes comptables aux données de caisse. Ils sont enregistrés en base et **réutilisés automatiquement** lors des traitements suivants — pas besoin de les ressaisir.

Trois familles de codes sont configurables :

| Famille | À quoi ça sert | Exemple |
|---|---|---|
| **Codes comptables** | Associer chaque catégorie de caisse à un compte | `001 SURGELE` → `601100` |
| **Codes généraux / auxiliaires** | Comptes généraux et leurs auxiliaires | `Code General 401000` → `401000` / `401LR` |
| **Journal** | Code du journal comptable | `Journal` → `VNT` |

**Procédure :**

1. Dans la zone **Paramétrage des codes**, modifiez la valeur en face de chaque libellé.
2. Laissez vide un champ que vous ne souhaitez pas modifier (les valeurs vides sont ignorées).
3. Cliquez sur **Enregistrer** : vos codes sont sauvegardés et appliqués aux prochains traitements.

> 💡 Au premier usage, un jeu de codes par défaut est proposé. Adaptez-le à votre dossier, puis enregistrez.

---

## 4. Préparer et importer les fichiers

1. **Organisez vos fichiers par restaurant** : un dossier (ou un lot) par établissement. C'est ce regroupement qui détermine la feuille correspondante dans l'Excel final.
2. Dans la zone **Dépôt des fichiers**, glissez-déposez vos fichiers `.EDI` / `.txt`, ou cliquez pour les sélectionner.
3. Vous pouvez déposer **plusieurs fichiers / plusieurs restaurants en une seule fois**.
4. Cliquez sur **Lancer le traitement**.

> ⚠️ Seuls les fichiers `.txt` / `.EDI` sont pris en compte ; les autres formats sont ignorés et signalés. Un fichier dont l'en-tête n'est pas reconnu comme EDI est rejeté individuellement, **sans interrompre** le traitement des autres fichiers.

---

## 5. Récupérer le résultat

À la fin du traitement, un fichier Excel (`.xlsx`) est proposé au téléchargement :

- **une feuille (onglet) par restaurant** ;
- chaque ligne reprend les données de caisse avec les **codes comptables que vous avez paramétrés** ;
- le fichier est directement importable dans votre logiciel comptable.

> 🧹 Les fichiers déposés et générés sont **automatiquement supprimés du serveur** quelques minutes après le traitement (conformité RGPD). Pensez à télécharger votre résultat.

---

## 6. Configuration McDonald's (cas particulier)

Pour les dossiers McDonald's, une configuration de **fascicule** propre à chaque établissement peut être enregistrée par un administrateur. Elle ajuste le traitement aux spécificités de ces tickets. Adressez-vous à votre administrateur pour la mise en place.

---

## 7. Préférences

- **Thème clair / sombre** : icône **🌙 / ☀️** en haut à droite. Votre choix est mémorisé d'une session à l'autre.
- **Profil** : icône **👤** pour consulter vos informations.
- **Présence en temps réel** : le bandeau « Utilisateurs connectés » indique en direct quels collègues sont en ligne.

---

## 8. Problèmes fréquents

| Symptôme | Cause probable | Solution |
|---|---|---|
| « Aucun fichier valide » | Fichiers au mauvais format | Vérifiez l'extension `.EDI` / `.txt` |
| Mauvais code comptable dans l'Excel | Mapping non configuré pour ce dossier | Revoyez le **Paramétrage des codes** (§ 3) |
| Une catégorie n'est pas reconnue | Code manquant dans votre mapping | Ajoutez le code correspondant et relancez |
| Déconnexion inattendue | Session expirée (24 h) | Reconnectez-vous |
| Téléchargement impossible après un délai | Fichiers nettoyés automatiquement | Relancez le traitement |

Pour toute anomalie persistante, contactez votre administrateur en précisant l'heure du traitement (les actions sont journalisées côté serveur).

# Dictionnaire de données

**Projet :** Plateforme intranet — Cabinet Martini
**Auteur :** Bénard Gwendal
**Version :** 2026-08-28 — calée sur le schéma réellement déployé

> **Source de vérité de ce document — le code, pas le dossier :**
> `backend/internal/db/postgres.go` → `InitSchema`, et les migrations
> `001_fix_anomalies.sql`, `002_add_fascicule_pk.sql`, `003_alignement_conceptuel.sql`,
> `004_cascade_suppression_utilisateur.sql`, complétées par les modèles SQLAlchemy
> `api/schemas/model.py`.
>
> **Périmètre : 9 entités, 42 données.** La table `fascicule_mcdo` existe encore en base
> mais est **hors périmètre présenté** depuis le 22/08 — voir § 3.4.
>
> **Documents dérivés :** ce dictionnaire est en amont de tout le reste. `doc/Mcd.png`
> (MCD), `doc/MLD.png` (MLD), `doc/MPD_capture.png` (MPD) et `doc/schemas/MCD_MLD_MPD.md`
> en découlent — et non l'inverse.

---

## 1. Méthode

Le dictionnaire de données est le **premier livrable de la modélisation**, avant le MCD. Il
répond à une seule question : *de quelles informations l'application a-t-elle besoin, et
qu'est-ce qui justifie chacune ?* Il se construit en trois temps, et c'est ce découpage qui
lui donne sa valeur :

1. **Recensement** — lister **toutes** les données manipulées, sans structure et sans
   arbitrage, en partant des écrans, des formulaires et des règles de gestion. À ce stade
   on accepte les doublons et les approximations. *(§ 2)*
2. **Épuration** — éliminer les **synonymes** (deux noms pour la même donnée), lever les
   **polysèmes** (un nom pour deux données différentes), isoler les **données calculées**
   (déductibles d'autres données) et écarter ce qui ne doit pas être persisté. *(§ 3)*
3. **Regroupement** — rattacher chaque donnée épurée à une entité, ce qui produit
   directement les entités du MCD. *(§ 4)*

**Colonnes du dictionnaire :**

| Colonne | Contenu |
|---|---|
| **Code** | Nom technique de la donnée, tel qu'il existe en base |
| **Désignation** | Libellé métier — ce que la donnée signifie pour l'utilisateur |
| **Type** | `A` alphabétique · `N` numérique · `AN` alphanumérique · `D` date/heure · `B` booléen · `J` structure JSON |
| **Entité** | Entité de rattachement après regroupement |
| **Contrainte** | La contrainte d'intégrité telle qu'elle est déclarée en base, et rien d'autre. Les règles de gestion qui s'appuient dessus sont regroupées au § 5, les points d'attention au § 6 |

---

## 2. Recensement — dictionnaire brut

**42 données**, par ordre alphabétique de code. Les codes apparaissant dans plusieurs
entités sont qualifiés entre parenthèses : ce sont les **polysèmes**, traités au § 3.2.

| # | Code | Désignation | Type | Entité | Contrainte |
|---|------|-------------|:----:|--------|-----------------|
| 1 | `admin` | Indicateur de privilège administrateur | B | `users` | `NOT NULL` |
| 2 | `api_name` | Service ou fonctionnalité concerné par l'événement | AN | `events` | Nullable |
| 3 | `application_id` | Référence de l'application concernée | N | `user_application_permissions` | `NOT NULL`, FK → `applications(id)` |
| 4 | `base_url` | URL d'accès de l'application | AN | `applications` | `NOT NULL` |
| 5 | `can_access` | Droit d'accès effectif de l'utilisateur à l'application | B | `user_application_permissions` | `DEFAULT FALSE` |
| 6 | `code_map` | Table de correspondance des codes comptables | J | `user_code_maps` | `NOT NULL`, `DEFAULT '{}'` |
| 7 | `code_map_gen_aux` | Table de correspondance des codes auxiliaires généraux | J | `user_code_maps_gen_aux` | `NOT NULL` |
| 8 | `conn_time` | Horodatage de début de session applicative | AN | `events` | `NOT NULL` |
| 9 | `created_at` *(application_groups)* | Date de création du groupe | D | `application_groups` | `DEFAULT CURRENT_TIMESTAMP` |
| 10 | `created_at` *(events)* | Date d'enregistrement de l'événement | D | `events` | `TIMESTAMPTZ DEFAULT NOW()` |
| 11 | `created_at` *(sessions)* | Date d'ouverture de la session | D | `sessions` | `NOT NULL` |
| 12 | `day` | Jour de l'événement, clé d'agrégation | AN | `events` | `NOT NULL` |
| 13 | `deco_time` | Horodatage de fin de session applicative | AN | `events` | `NOT NULL` |
| 14 | `email` | Adresse électronique, identifiant de connexion | AN | `users` | `UNIQUE NOT NULL` |
| 15 | `entreprise` | Société de rattachement de l'utilisateur | AN | `users` | Nullable |
| 16 | `expires_at` | Date d'expiration de la session | D | `sessions` | `NOT NULL` |
| 17 | `groups` | Groupe de rattachement de l'application | AN | `applications` | Nullable, FK → `application_groups(name)` `ON UPDATE CASCADE` |
| 18 | `icon_path` | Chemin de l'icône affichée au catalogue | AN | `applications` | Nullable |
| 19 | `id` *(application_groups)* | Identifiant technique du groupe | N | `application_groups` | `SERIAL PRIMARY KEY` |
| 20 | `id` *(applications)* | Identifiant technique de l'application | N | `applications` | `SERIAL PRIMARY KEY` |
| 21 | `id` *(code_journal)* | Identifiant technique du paramétrage | N | `code_journal` | `SERIAL PRIMARY KEY` |
| 22 | `id` *(events)* | Identifiant technique de l'événement | N | `events` | `SERIAL PRIMARY KEY` |
| 23 | `id` *(sessions)* | **Jeton de session** | AN | `sessions` | `PRIMARY KEY` |
| 24 | `id` *(user_application_permissions)* | Identifiant technique de la permission | N | `user_application_permissions` | `SERIAL PRIMARY KEY` |
| 25 | `id` *(user_code_maps)* | Identifiant technique du paramétrage | N | `user_code_maps` | `SERIAL PRIMARY KEY` |
| 26 | `id` *(user_code_maps_gen_aux)* | Identifiant technique du paramétrage | N | `user_code_maps_gen_aux` | `SERIAL PRIMARY KEY` |
| 27 | `id` *(users)* | Identifiant technique de l'utilisateur | N | `users` | `SERIAL PRIMARY KEY` |
| 28 | `journal_map` | Table de correspondance des journaux comptables | J | `code_journal` | `NOT NULL` |
| 29 | `last_seen` *(sessions)* | Dernière activité observée **sur cette session** | D | `sessions` | Nullable |
| 30 | `last_seen` *(users)* | Dernière activité observée **du compte** | D | `users` | `DEFAULT CURRENT_TIMESTAMP` |
| 31 | `name` *(application_groups)* | Libellé du groupe d'applications | AN | `application_groups` | `UNIQUE NOT NULL` |
| 32 | `name` *(applications)* | Nom de l'application affiché au catalogue | AN | `applications` | `NOT NULL` |
| 33 | `noms` | *(hors périmètre — § 3.4)* | AN | `fascicule_mcdo` | `UNIQUE` |
| 34 | `password` | Empreinte bcrypt du mot de passe | AN | `users` | `NOT NULL` |
| 35 | `role` | Rôle métier de l'utilisateur | A | `users` | `DEFAULT 'user'` |
| 36 | `uid` *(events)* | Auteur de l'événement | AN | `events` | `NOT NULL`, FK → `users(uid)` `ON DELETE CASCADE` |
| 37 | `uid` *(users)* | **Identifiant métier stable** de l'utilisateur | AN | `users` | `UNIQUE NOT NULL` |
| 38 | `user_id` *(code_journal)* | Propriétaire du paramétrage | N | `code_journal` | `NOT NULL`, `UNIQUE`, FK → `users(id)` `ON DELETE CASCADE` |
| 39 | `user_id` *(sessions)* | Titulaire de la session | AN | `sessions` | `NOT NULL`, FK → `users(uid)` `ON DELETE CASCADE` |
| 40 | `user_id` *(user_application_permissions)* | Utilisateur détenteur du droit | AN | `user_application_permissions` | `NOT NULL`, FK → `users(uid)` `ON DELETE CASCADE` |
| 41 | `user_id` *(user_code_maps)* | Propriétaire du paramétrage | N | `user_code_maps` | `NOT NULL`, `UNIQUE`, FK → `users(id)` `ON DELETE CASCADE` |
| 42 | `user_id` *(user_code_maps_gen_aux)* | Propriétaire du paramétrage | N | `user_code_maps_gen_aux` | `NOT NULL`, `UNIQUE`, FK → `users(id)` `ON DELETE CASCADE` |

**Trois de ces données sont calculées** — `expires_at`, `users.last_seen` et `events.day` :
elles sont déductibles d'autres données, et pourtant persistées. Chacune est une
dénormalisation assumée, justifiée au § 3.3.

---

## 3. Épuration

### 3.1 Synonymes — un même concept sous plusieurs noms

| Concept unique | Noms rencontrés | Décision |
|---|---|---|
| **Identifiant métier de l'utilisateur** | `users.uid`, `sessions.user_id`, `user_application_permissions.user_id`, `events.uid` | **Une seule donnée**, référencée quatre fois. Le nom varie selon le rôle joué : `uid` quand elle identifie, `user_id` quand elle référence. Retenue une fois, en `users.uid` |
| **Date de dernière activité** | `users.last_seen`, `sessions.last_seen` | **Ce ne sont pas des synonymes** — voir § 3.2 |

### 3.2 Polysèmes — un même nom pour des données différentes

C'est le point le plus important de l'épuration, et celui que le jury vérifie.

| Code ambigu | Sens 1 | Sens 2 | Levée de l'ambiguïté |
|---|---|---|---|
| `id` | Clé de substitution entière, sans signification métier (8 entités) | **Le jeton de session lui-même** dans `sessions` — une donnée métier sensible | Qualification par l'entité. Le cas de `sessions` est documenté au § 6.3 : c'est un choix, pas une inattention |
| `last_seen` | Dans `users` : dernière activité **du compte**, tous postes confondus — donnée **calculée** | Dans `sessions` : dernière activité **de cette connexion** — donnée élémentaire | Deux données distinctes, l'une dérivée de l'autre. Conservées toutes les deux |
| `name` | Dans `applications` : nom d'une application | Dans `application_groups` : libellé d'un groupe, et **cible d'une clé étrangère** | Deux données distinctes. Celle de `application_groups` porte une contrainte `UNIQUE` que l'autre n'a pas |
| `user_id` | Dans `sessions` et `user_application_permissions` : **texte**, référence `users(uid)` | Dans les trois tables de mapping : **entier**, référence `users(id)` | ⚠️ **Polysème réel et assumé** : même nom, deux types, deux cibles. Cause et arbitrage au § 6.2 |
| `created_at` | Date d'ouverture (`sessions`), de création (`application_groups`) | Date d'enregistrement (`events`) — **la seule en `TIMESTAMPTZ`** | Trois données distinctes ; seule celle d'`events` porte un fuseau |

### 3.3 Données calculées — persistées malgré tout

Une donnée calculée ne devrait pas être stockée : elle est déductible, donc redondante, donc
susceptible de diverger. Les trois exceptions retenues sont des **dénormalisations
assumées**, chacune pour une raison précise.

| Donnée | Formule | Pourquoi elle est stockée |
|---|---|---|
| `sessions.expires_at` | `created_at + 24 h` (**RG03**) | La durée de vie doit rester celle qui était en vigueur **au moment de la création**. Recalculer à la lecture ferait varier rétroactivement toutes les sessions à chaque changement de politique. **La date figée est la règle appliquée, pas la règle courante.** |
| `users.last_seen` | `MAX(sessions.last_seen, sessions.created_at)` du titulaire | La liste des utilisateurs de l'administration affiche cette date **pour chaque ligne**. Sans la colonne, il faudrait une sous-requête d'agrégation par utilisateur à chaque affichage. `InitSchema` amorce la colonne par ce calcul exact lors de la migration |
| `events.day` | Partie date de `conn_time`, format `YYYY-MM-DD` | Clé d'agrégation des statistiques. Le filtrage se fait par `day >= $1 AND day <= $2` — **et cette comparaison de chaînes ne fonctionne que parce que le format ISO 8601 est lexicographiquement ordonné.** Fragilité documentée au § 6.1 |

### 3.4 Données écartées du périmètre

| Donnée | Motif |
|---|---|
| `fascicule_mcdo.noms`, `fascicule_mcdo.config` | **Retirées du périmètre le 22/08**, en même temps que le besoin fonctionnel correspondant. La table subsiste en base et le service Go `Macdos` existe encore, mais **plus aucune interface ne les appelle** : elles sont un reliquat de la première version autonome de l'outil. Volontairement non supprimées (la migration 003 le précise), volontairement non présentées |
| Mot de passe en clair | **N'existe à aucun moment en persistance — RG02.** Reçu dans le corps d'une requête HTTPS, comparé par `bcrypt.CompareHashAndPassword`, jamais écrit ni journalisé |
| Jeton de session complet dans les journaux | Exclu de la journalisation par principe |

---

## 4. Regroupement par entité

Le dictionnaire épuré se regroupe en **9 entités**, qui sont exactement celles du MCD — à une
près, expliquée juste après.

| # | Entité | Données | Rôle |
|---|--------|:-------:|------|
| 1 | `users` | 9 | Comptes, identité, rôle, privilège |
| 2 | `sessions` | 5 | Authentification par jeton opaque |
| 3 | `applications` | 5 | Catalogue des outils du portail |
| 4 | `application_groups` | 3 | Classement des applications |
| 5 | `user_application_permissions` | 4 | **Attribution d'une application à un utilisateur** |
| 6 | `events` | 7 | Journal d'usage, source de l'analytique |
| 7 | `user_code_maps` | 3 | Paramétrage des codes comptables |
| 8 | `user_code_maps_gen_aux` | 3 | Paramétrage des codes auxiliaires généraux |
| 9 | `code_journal` | 3 | Paramétrage des journaux comptables |

> **Le point à savoir expliquer : 9 tables en base, mais 8 entités au MCD.**
> `user_application_permissions` **n'est pas une entité conceptuelle** : c'est la
> traduction, au niveau logique, de l'association *accéder* `(0,n)–(0,n)` entre `users`
> et `applications`, qui porte la propriété `can_access`. Elle **naît au passage MCD → MLD**.
> Savoir énoncer cet écart prouve que le MCD n'a pas été redessiné après coup à partir de la base.

---

## 5. Règles de gestion portées par les données

| Règle | Données concernées | Portée par |
|---|---|---|
| **RG01** — un email identifie un utilisateur de façon unique | `users.email` | Contrainte `UNIQUE` en base |
| **RG02** — mot de passe jamais stocké ni journalisé en clair | `users.password` | Empreinte bcrypt (coût 10), sel intégré. **Aucune donnée en clair au dictionnaire** |
| **RG03** — session expirée 24 h après création | `sessions.created_at`, `sessions.expires_at` | Donnée calculée à la création, **vérifiée côté serveur** à chaque requête |
| **RG04** — un utilisateur ne voit que ses applications attribuées | `user_application_permissions.can_access` | Association *accéder* + `UNIQUE(user_id, application_id)` |
| **RG05** — seul un Admin gère comptes et applications | `users.admin` | Vérification **en base** par `AdminMiddleware`, jamais côté client |
| **RG06** — droit à l'oubli : la suppression cascade | Toutes les FK vers `users` | **6 FK en `ON DELETE CASCADE`** après la migration 004 (§ 6.6) |
| **RG07** — les événements d'audit survivent à la suppression | `events.uid` | ⚠️ **Non tenue aujourd'hui** — `events.uid` est en `ON DELETE CASCADE` (§ 6.7) |
| **RG08** — fichiers déposés éphémères | *(hors base)* | Répertoire temporaire par UUID, purge à +5 min. **Aucun fichier n'est persisté en base** |
| **RG09** — toute action administrative sensible est journalisée | `events.*` | Écriture d'un événement horodaté |

**Contraintes d'intégrité transversales :**

- **Unicité** — `users.email`, `users.username`, `users.uid`, `application_groups.name`,
  `fascicule_mcdo.noms`, le couple `(user_id, application_id)`, et `user_id` sur chacune des
  trois tables de mapping (migration 003 : *un seul paramétrage de chaque type par utilisateur*).
- **Référentielle** — 8 clés étrangères, dont 6 vers `users` et toutes les 6 en cascade.
  `applications.groups → application_groups(name)` en `ON UPDATE CASCADE` : renommer un groupe
  se propage aux applications qui le portent.
- **Domaine** — `role` est une liste fermée de 6 valeurs, contrainte **applicative** et non
  déclarée en base (§ 6.5).
- **Temporel** — tous les horodatages sont en **UTC**, convertis en `Europe/Paris` à l'affichage.
  Seule `events.created_at` porte le fuseau (`TIMESTAMPTZ`).

---

## 6. Points d'attention assumés

> Un dictionnaire honnête documente aussi ce qui n'est pas idéal. Ces sept points sont
> **connus, justifiés ou inscrits au backlog** — les découvrir soi-même vaut mieux que se
> les faire trouver.

### 6.1 Les horodatages d'`events` sont stockés en texte
`conn_time`, `deco_time` et `day` sont en `TEXT`, pas en `TIMESTAMP`/`DATE`. **Conséquence
réelle :** aucune arithmétique de date en SQL, et un filtrage par comparaison de chaînes —
`day >= $1 AND day <= $2` — qui **ne fonctionne que grâce à l'ordre lexicographique du format
ISO 8601**. Un format d'écriture différent casserait silencieusement l'agrégation.
**Correctif identifié :** typage en `DATE` et `TIMESTAMPTZ`, migration additive.

### 6.2 La double identité `id` / `uid`, et le polysème `user_id`
`users` porte **deux** identifiants : `id` (`SERIAL`, clé de substitution) et `uid` (UUID
texte, identifiant métier stable). **C'est délibéré :** `uid` est le seul identifiant exposé
au client, ce qui évite de divulguer un compteur — le nombre d'utilisateurs et l'ordre des
inscriptions ne fuitent pas. **Le prix à payer est réel :** le backend Go référence `users(uid)`,
l'API Python `users(id)`. D'où un même nom `user_id` portant **deux types et deux cibles**
selon la table. C'est le coût de deux services développés sur des conventions différentes
autour d'une base partagée ; la convergence sur `uid` seul est un chantier de refonte, pas
une migration additive.

### 6.3 Le jeton de session est la clé primaire
`sessions.id` **est** la valeur du cookie. Il n'y a pas de colonne `token` séparée : le
lookup du middleware d'authentification, qui s'exécute à **chaque requête**, est une lecture
directe par l'index de clé primaire — le chemin d'accès le plus court possible sur le chemin
le plus chaud de l'application.

### 6.4 Les colonnes `JSON` ne violent pas la 1NF
`code_map`, `code_map_gen_aux` et `journal_map` sont des structures **opaques pour la base** :
jamais indexées, jamais jointes, **lues et écrites en bloc**. La première forme normale porte
sur ce que la base doit manipuler comme des valeurs — ici, la valeur atomique **est** le
document. C'est le pattern documentaire couvert en SQL, et c'est l'argument qui justifie
l'absence de moteur NoSQL au projet.

### 6.5 `role` a une valeur par défaut hors liste
La colonne est déclarée `DEFAULT 'user'`, or `'user'` **ne fait pas partie des six rôles**
(`Admin`, `Dev`, `Comptable`, `Social`, `Auditeur`, `Client`). En pratique le formulaire
d'administration impose toujours un rôle, donc le défaut n'est jamais atteint — mais **la
base autorise un état que le métier ne connaît pas**. Correctif : `CHECK` sur la liste fermée,
ou passage à un type énuméré.

### 6.6 Le droit à l'oubli est désormais porté par le schéma
La migration **004** a reposé en `ON DELETE CASCADE` les deux dernières FK qui ne l'étaient
pas (`sessions.user_id` et `user_application_permissions.user_id`). **Les six clés étrangères
vers `users` sont maintenant en cascade.** Conséquence directe sur le code : `DeleteUser`
n'enchaîne plus six `DELETE` dans une transaction, **un seul `DELETE FROM users WHERE uid = $1`
suffit** — le droit à l'oubli est passé d'une convention de code à une garantie de la base.

### 6.7 ⚠️ RG07 est contredite par le schéma
La règle dit que *« les événements d'audit survivent à la suppression du compte »*, mais
`events.uid` est en `ON DELETE CASCADE` depuis la migration 001 : **les événements sont
supprimés avec le compte.** Les deux exigences sont réelles et opposées — traçabilité contre
droit à l'oubli — et **la bonne réponse n'est pas de choisir, c'est d'anonymiser** :
`ON DELETE SET NULL` sur `events.uid`, ou remplacement de l'identifiant par un pseudonyme non
réversible. **On conserve le fait, on efface la personne.** À trancher avant l'oral.

---

## 7. Correspondance des types

| Type dictionnaire | PostgreSQL | Go | Python / SQLAlchemy |
|---|---|---|---|
| `N` numérique (clé) | `SERIAL` / `INTEGER` | `int` | `Integer` |
| `AN` alphanumérique | `TEXT` | `string` | `String` |
| `A` alphabétique (liste fermée) | `TEXT` | `string` | `String` |
| `B` booléen | `BOOLEAN` | `bool` | `Boolean` |
| `D` date/heure | `TIMESTAMP` (naïf, UTC) · `TIMESTAMPTZ` (`events.created_at`) | `time.Time` | `DateTime` |
| `J` structure | `JSON` | `[]byte` / `string` | `JSON` |

> **Note sur les longueurs.** Le schéma n'emploie que `TEXT`, jamais `VARCHAR(n)` : PostgreSQL
> ne tire aucun gain de performance d'une limite déclarée, et une limite en base est coûteuse
> à faire évoluer. **Les longueurs maximales sont donc des contraintes fonctionnelles**,
> vérifiées à la saisie et non déclarées en base — sauf `uid` (36 caractères, longueur d'un
> UUID) et `password` (60, longueur d'une empreinte bcrypt), qui sont **structurellement fixes**.

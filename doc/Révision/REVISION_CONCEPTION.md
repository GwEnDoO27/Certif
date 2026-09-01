# Révision ciblée — Conception

**Point faible identifié.** Ce document ne résume pas : il explique. Puis il fait travailler.
Sources : `Fichier Final/A Envoyer/Certif corrigé.docx` (chapitre *Conception*) et `doc/schemas/`.
**Calé sur l'exposé :** `doc/SCRIPT_ORAL_CDA.md`, § 3.3. Ce § a été **volontairement allégé à l'oral** — tu n'y prononces plus « cardinalité », « troisième forme normale », « atomicité », « clé étrangère », « `ON DELETE CASCADE` » ni « index secondaire ». **C'est exactement pour ça que ce document existe** : tout ce vocabulaire retiré du discours est celui sur lequel on t'interrogera.

> **Comment l'utiliser.** Lis la partie 1 lentement, une seule fois — c'est de la théorie, elle ne s'apprend pas par cœur, elle se comprend. Puis passe à la partie 2, qui applique cette théorie à ton modèle : c'est celle que tu dois maîtriser, parce que c'est celle sur laquelle on t'interrogera. Fais les exercices de la partie 4 **à froid, sur papier**, avant de lire le corrigé.
> Si tu n'as qu'une heure : parties 2 et 5.

---

## Partie 0 — Pourquoi c'est le bloc le plus payant

La conception couvre trois compétences du référentiel à elle seule : **analyser les besoins et maquetter**, **définir l'architecture logicielle**, **concevoir et mettre en place une base de données relationnelle**.

Mais surtout, c'est le seul endroit de la soutenance où un jury peut **vérifier que tu comprends au lieu de vérifier que tu as fait**. Sur le déploiement, on te croit sur parole : tu dis que ton pipeline tourne, personne ne va le lancer. Sur un MCD, on te montre ton propre schéma et on te demande pourquoi la clé est de ce côté-là. Impossible de bluffer.

C'est aussi pour ça que c'est rattrapable en quelques heures : le corpus théorique est petit et fermé. Cardinalités, règles de passage, formes normales, quatre diagrammes UML. C'est tout. Il n'y a pas de fond sans limite comme en sécurité.

**Le piège du candidat faible en conception** n'est pas de ne pas savoir : c'est de réciter des définitions correctes sans pouvoir les appliquer à son propre schéma. Un jury repère ça en une question. La parade est en partie 2.

### Ce que tu dis à l'oral, et ce qu'on te demandera derrière

| Ce que tu dis en § 3.3 | La question qui vient derrière | Où réviser |
|---|---|---|
| « des utilisateurs, des applications, des sessions, des paramétrages » | Donnez-moi les cardinalités de chaque association, minimum **et** maximum | 1.2 et E2 |
| « les deux côtés sont au pluriel, on appelle ça plusieurs à plusieurs » | Traduisez-la en tables. Qu'est-ce qui garantit qu'un couple n'apparaît pas deux fois ? | 1.3, E5, et 2.2 |
| « on crée une troisième table, qui ne contient que des couples » | Quelle est sa clé primaire ? Pourquoi pas un `id` technique seul ? | 1.3 et corrigé E5 |
| « neuf tables, avec les types PostgreSQL et les contraintes » | Votre schéma est-il normalisé ? Jusqu'à quelle forme ? | 1.4 et question 4 |
| « les mappings stockés en JSON plutôt qu'éclatés en tables » | Ça ne viole pas la 1NF ? | 1.4 et 2.2 |
| « le groupe d'une application, stocké en texte simple, un raccourci assumé » | Assumé jusqu'à quand ? Qu'est-ce qui casse le jour où on renomme un groupe ? | 2.2 et 2.3 a) |
| « la base efface automatiquement tout ce qui lui appartient » | Montrez-moi sur quelles clés étrangères. Et qu'est-ce qui **n'est pas** effacé ? | 2.3 d) 🔴 |
| « ce schéma pourrait décrire un classeur papier » | Alors pourquoi voit-on des clés étrangères sur votre MCD ? | 1.1 et mémo n° 1 |

**La ligne la plus dangereuse est l'avant-dernière** : c'est la seule où ta phrase d'exposé est plus forte que ce que ton code garantit. Voir 2.3 d).

---

## Partie 1 — Les fondamentaux, expliqués

### 1.1 Merise : pourquoi trois niveaux et pas un seul

Merise sépare la modélisation en trois niveaux parce qu'ils répondent à **trois questions différentes**, et qu'on ne peut pas y répondre en même temps sans se tromper.

| Niveau | Question | Vocabulaire | Ce qu'on ignore volontairement |
|---|---|---|---|
| **MCD** — conceptuel | *De quoi parle-t-on ?* | Entités, propriétés, associations, cardinalités | Tout ce qui est technique : SGBD, types, clés étrangères, performance |
| **MLD** — logique | *Comment le range-t-on en tables ?* | Relations, clés primaires, clés étrangères | Le SGBD précis, les types exacts, les index |
| **MPD** — physique | *Comment on l'écrit pour PostgreSQL ?* | `CREATE TABLE`, types, contraintes, index, `ON DELETE` | Plus rien — c'est le code |

**L'erreur classique**, et celle qui trahit le plus vite : parler de clés étrangères dans le MCD. Une clé étrangère n'existe pas au niveau conceptuel. Au MCD, il y a une **association** ; la clé étrangère est le **résultat** de sa traduction en MLD. Si tu dessines une FK dans un MCD, tu as sauté un niveau.

**Ce qu'il faut savoir dire :** *« Le MCD décrit le métier indépendamment de toute technologie — je pourrais l'implémenter en PostgreSQL, en Oracle ou sur papier. Le MLD applique des règles de passage mécaniques. Le MPD est la traduction dans le dialecte SQL de PostgreSQL, avec les types et les contraintes réelles. »*

---

### 1.2 Les cardinalités — le point où tout le monde se trompe

Une cardinalité s'écrit **(min, max)** et se lit **depuis une occurrence de l'entité vers l'association**.

La formule qui marche à tous les coups, à te répéter mentalement :

> **« Pour UN [entité], combien de [association] au minimum, et au maximum ? »**

Les quatre valeurs possibles :

| Notation | Lecture |
|---|---|
| **(0,1)** | Pour un X, zéro ou une occurrence — participation facultative, non répétable |
| **(1,1)** | Pour un X, exactement une — participation obligatoire, non répétable |
| **(0,n)** | Pour un X, zéro à plusieurs — facultative, répétable |
| **(1,n)** | Pour un X, au moins une — obligatoire, répétable |

**Le piège n° 1 — le côté où on écrit la cardinalité.** En **Merise**, la cardinalité se place **du côté de l'entité qu'elle décrit**. En **UML**, la multiplicité se place **à l'autre bout**, du côté opposé. Les deux notations disent la même chose mais s'écrivent en miroir.

Si un jury te montre ton MCD et ton diagramme de classes et te demande pourquoi les chiffres ne sont pas au même endroit, c'est **cette** réponse qu'il attend. C'est une question de connaisseur, et y répondre juste vaut très cher.

**Le piège n° 2 — confondre le minimum avec « ça existe forcément ».** Le minimum décrit une contrainte d'**intégrité**, pas une observation. `(1,n)` signifie qu'une occurrence sans association est **interdite** par le modèle, pas simplement qu'on n'en a pas encore vu.

**Le piège n° 3 — croire que « obligatoire » vaut pour toute l'association.** C'est faux : **l'obligation est directionnelle**. Une association porte *deux* minimums, qui répondent à deux questions distinctes :

```
Utilisateur ──(0,n)── ouvrir ──(1,1)── Session
      │                            │
   « une session est-elle       « un utilisateur est-il
     obligatoire pour un          obligatoire pour une
     utilisateur ? » → NON        session ? » → OUI
```

**Le test qui tranche à tous les coups :** prends une ligne réelle et demande-toi si elle peut exister seule.
- *Une ligne `users` sans aucune `sessions` ?* Oui — compte créé par l'admin et jamais utilisé (RG05), utilisateur déconnecté, ou session purgée par la goroutine des 6 h. → minimum **0** côté Utilisateur.
- *Une ligne `sessions` sans `users` ?* Jamais. → minimum **1** côté Session.

**Le repère SQL, à sortir si on te pousse :**
> Un minimum à 1 **du côté où se trouve la clé étrangère**, c'est le `NOT NULL` sur cette clé. Chez moi la FK est dans `sessions` et elle est `NOT NULL` : c'est exactement le `1` de mon `(1,1)`.
> Et le corollaire : **un minimum à 1 de l'autre côté n'a aucune traduction SQL simple** — aucune contrainte ne permet d'exiger « tout utilisateur a au moins une session », il faudrait un déclencheur. C'est une raison de plus pour que le `(0,n)` soit le bon choix, et pas seulement le choix commode.

**Exemple sur ton modèle, à savoir dérouler :**
> Entre `users` et `sessions` : un utilisateur ouvre de **(0,n)** sessions — il peut n'en avoir aucune, il peut en avoir plusieurs. Une session appartient à **(1,1)** utilisateur — elle en a forcément un, et un seul. C'est donc une association **un-à-plusieurs**.
> **Ce que `(1,n)` interdirait :** créer un compte avant sa première connexion, se déconnecter, et laisser la purge des sessions expirées s'exécuter. L'application deviendrait invalide au regard de son propre modèle.

---

### 1.3 Les règles de passage MCD → MLD

Elles sont **mécaniques**. Trois cas, c'est tout.

**Cas 1 — association un-à-plusieurs** *(un côté à (1,1) ou (0,1), l'autre à (0,n) ou (1,n))*
La clé primaire du côté **« 1 »** migre comme clé étrangère du côté **« n »**.

> `users (0,n) ——ouvre—— (1,1) sessions` devient `sessions(id, **user_id → users**, created_at, expires_at)`.
> **Le moyen mnémotechnique :** la clé descend toujours du côté où il y en a beaucoup. Une session ne peut pointer que vers un utilisateur, donc elle peut porter la référence. L'inverse serait impossible : il faudrait mettre plusieurs identifiants de session dans une colonne d'`users`, ce qui violerait la 1NF.

**Cas 2 — association plusieurs-à-plusieurs** *(les deux côtés à (0,n) ou (1,n))*
L'association devient **une table à part entière**, dont la clé primaire est le couple des deux clés étrangères. Les éventuelles propriétés portées par l'association deviennent ses colonnes.

> `users (0,n) ——accède—— (0,n) applications`, avec la propriété `can_access`, devient
> `user_application_permissions(user_id → users, application_id → applications, can_access)`.

**Cas 3 — association un-à-un** *(les deux côtés à (0,1) ou (1,1))*
Fusion des deux entités en une seule table, ou migration de la clé du côté à participation obligatoire. À justifier au cas par cas — c'est le cas le plus rare, et souvent le signe qu'on aurait dû faire une seule entité.

---

### 1.4 La normalisation, avec un contre-exemple de ton métier

Les formes normales servent à **une seule chose** : éliminer les redondances qui produisent des anomalies. Trois anomalies, toujours les mêmes :

- **anomalie d'insertion** — on ne peut pas enregistrer une information sans en inventer une autre ;
- **anomalie de mise à jour** — une même donnée existe à plusieurs endroits, on en oublie un, la base devient incohérente ;
- **anomalie de suppression** — on supprime une ligne et on perd au passage une information sans rapport.

Partons d'une table volontairement mal conçue, tirée de ton domaine :

```
TIRAGE_BRUT
─────────────────────────────────────────────────────────────────────────
num_tirage │ date  │ restaurant  │ ville  │ codes_ventes    │ libelle_compte
   1       │ 31/01 │ McDo Rouen  │ Rouen  │ 707100, 707200  │ Ventes marchandises
   2       │ 28/02 │ McDo Rouen  │ Rouen  │ 707100          │ Ventes marchandises
   3       │ 31/01 │ McDo Elbeuf │ Elbeuf │ 707100, 707300  │ Ventes marchandises
```

**Passage en 1NF — atomicité.**
`codes_ventes` contient **plusieurs valeurs dans une seule cellule**. C'est le défaut le plus visible : impossible de chercher un code sans faire du texte, impossible de compter, impossible de poser une contrainte. On éclate en une ligne par code :

```
TIRAGE_LIGNE(num_tirage, code_vente, date, restaurant, ville, libelle_compte)
```
La clé primaire devient le couple **(num_tirage, code_vente)** — c'est ce qui rend le passage en 2NF nécessaire, et c'est logique : tant que la clé est simple, la 2NF est automatiquement respectée.

**Passage en 2NF — pas de dépendance partielle.**
La clé est composée. Or `date`, `restaurant` et `ville` ne dépendent que de `num_tirage`, **pas du code de vente**. C'est une dépendance **partielle** : un attribut non-clé qui dépend d'une partie seulement de la clé. On sépare :

```
TIRAGE(num_tirage, date, restaurant, ville)
LIGNE_TIRAGE(num_tirage, code_vente, libelle_compte)
```

**Passage en 3NF — pas de dépendance transitive.**
Dans `TIRAGE`, `ville` ne dépend pas de `num_tirage` : elle dépend de `restaurant`, qui dépend de `num_tirage`. Chaîne `num_tirage → restaurant → ville` : c'est une dépendance **transitive**. Même chose pour `libelle_compte`, qui dépend de `code_vente`. On sort ces attributs dans leurs propres entités :

```
TIRAGE(num_tirage, date, #restaurant_id)
RESTAURANT(restaurant_id, nom, ville)
LIGNE_TIRAGE(#num_tirage, #code_vente, montant)
COMPTE(code_vente, libelle_compte)
```

**Ce que ça a réparé, concrètement — c'est ça qu'il faut savoir dire :**
avant, changer la ville d'un restaurant obligeait à modifier toutes ses lignes de tirage, avec le risque d'en oublier ; et supprimer le dernier tirage d'un restaurant faisait disparaître le restaurant lui-même. Après, chaque fait est stocké une fois et une seule.

**La formule à retenir**, dite par Kent : *« chaque attribut non-clé dépend de la clé, de toute la clé, et rien que de la clé. »* La clé → 1NF. Toute la clé → 2NF. Rien que la clé → 3NF.

---

### 1.5 UML : ce qu'on te demandera vraiment

**Diagramme de cas d'utilisation.** Vue fonctionnelle : qui fait quoi. Trois relations à distinguer :
- **`include`** — le cas inclus est **toujours** exécuté, il est factorisé parce que plusieurs cas s'en servent. *« Consulter le catalogue » inclut « être authentifié ».*
- **`extend`** — le cas étendu est **optionnel**, exécuté sous condition. *« Créer un utilisateur » peut être étendu par « attribuer des applications ».*
- **généralisation d'acteurs** — un acteur hérite des cas d'un autre. *Chez toi, l'Admin peut être vu comme une généralisation de l'utilisateur : il fait tout ce que fait un utilisateur, plus l'administration.*

Le sens de la flèche : elle part **du cas qui inclut** vers le cas inclus, et **du cas qui étend** vers le cas étendu. C'est contre-intuitif pour `extend` — la flèche va de l'optionnel vers le principal.

**Diagramme de séquence.** Vue dynamique, chronologique.
- La **ligne de vie** est la ligne verticale : la période d'existence du participant. Le temps descend.
- La **barre d'activation** (le rectangle sur la ligne) : la période où le participant exécute quelque chose.
- **Message synchrone** : flèche pleine, l'appelant **attend** la réponse. **Message asynchrone** : flèche fine ouverte, l'appelant continue. **Retour** : flèche pointillée.
- **Fragments** : `alt` (alternative, un si/sinon), `loop` (boucle), `opt` (optionnel), `par` (parallèle).

Sur ton diagramme d'authentification, tu as un fragment `alt` : mot de passe correct / mot de passe incorrect. Sache le nommer — dire « alt » plutôt que « la boîte avec les deux cas » fait la différence.

**Diagramme de classes.** Vue statique.
- **Visibilités** : `+` public, `-` privé, `#` protégé, `~` paquetage.
- **Association** : lien simple entre deux classes.
- **Agrégation** (losange **vide**) : « fait partie de », mais les deux vivent indépendamment. On supprime le tout, la partie survit.
- **Composition** (losange **plein**) : le composant **meurt avec** le composite. Une session n'existe pas sans son utilisateur.
- **Héritage** : triangle vide, « est un ».
- **Réalisation** (implémentation d'une interface) : triangle vide, trait pointillé.

**Le moyen de ne jamais confondre agrégation et composition :** pose-toi la question de la suppression. *Si je supprime le tout, la partie a-t-elle encore un sens ?* Oui → agrégation. Non → composition.

---

## Partie 2 — Ton modèle, décortiqué

C'est **la** partie à maîtriser. Le jury n'interrogera pas sur la théorie dans l'abstrait : il ouvrira ton MCD.

### 2.1 Les entités et leurs associations

> 📌 **Le MCD a été repris.** La version à présenter est `doc/MCD_corrige.png` — noms métier, sans clés étrangères au conceptuel, association Application ↔ Groupe rétablie, `(0,1)` sur les paramétrages, `fascicule_mcdo` retirée. Les notes de reprise et le point à trancher sont dans `doc/MCD_corrige.md`. Le tableau ci-dessous conserve les noms de tables, parce que c'est le vocabulaire du MLD et du MPD.

| Association | Cardinalités | Type | Traduction en MLD |
|---|---|---|---|
| Utilisateur **ouvre** Session | utilisateur (0,n) — session (1,1) | un-à-plusieurs | `sessions.user_id` → `users.uid` |
| Utilisateur **accède à** Application | utilisateur (0,n) — application (0,n) | **plusieurs-à-plusieurs** | table `user_application_permissions` |
| Application **appartient à** Groupe | application (0,1) — groupe (0,n) | un-à-plusieurs | `applications.groups` — **référence faible, sans FK** |
| Utilisateur **génère** Événement | utilisateur (0,n) — événement (1,1) | un-à-plusieurs | `events.uid` → `users.uid`, `ON DELETE CASCADE` |
| Utilisateur **paramètre** chaque mapping | utilisateur **(0,1)** — mapping (1,1) | un-à-un côté métier | `user_code_maps.user_id` → `users.id`, `CASCADE` |

> ⚠️ La dernière ligne porte un **écart volontaire** : le MCD affiche `(0,1)` parce que le métier veut un seul paramétrage par utilisateur, alors que le schéma autorise `(0,n)` faute de `UNIQUE(user_id)`. Voir 2.3.a.

### 2.2 Les six décisions que tu dois pouvoir défendre

**1. Pourquoi `users` a-t-il deux identifiants, `id` et `uid` ?**
> `id SERIAL` est ma **clé de substitution** : un entier auto-incrémenté, efficace pour les jointures internes, et c'est lui que référencent les clés étrangères posées côté SQLAlchemy dans l'API Python. `uid TEXT UNIQUE` est mon **identifiant métier** : une valeur stable générée côté Go, exposée au client, et c'est lui que référencent les clés étrangères côté Go.
> **Si on te demande si c'est un défaut**, sois honnête : *« c'est un héritage de la construction progressive du projet — l'outil de conversion et sa persistance existaient avant la plateforme. Dans une refonte, j'unifierais sur un seul identifiant. »*

**2. Pourquoi la clé primaire de `sessions` est-elle le jeton lui-même ?**
> Parce que la seule requête que je fais sur cette table est *« ce jeton existe-t-il et est-il encore valide ? »*, exécutée par le middleware **à chaque requête authentifiée**. En faisant du jeton la clé primaire, ce lookup passe directement par l'index de clé primaire. Ajouter une colonne `id` séparée aurait ajouté un index et une indirection sans rien apporter.

**3. Pourquoi `applications.groups` n'a-t-il pas de clé étrangère ?**
> C'est une **dénormalisation assumée**, une référence faible : je stocke le libellé du groupe en texte libre plutôt qu'une clé vers `application_groups`.
> **Le coût que j'accepte :** rien ne garantit que le libellé corresponde à un groupe existant, et renommer un groupe n'est pas propagé.
> **Ce que ça m'apporte :** la lecture du catalogue ne fait pas de jointure, et le nombre de groupes est minuscule et stable.
> **Ce que je ferais si le besoin évoluait :** poser la clé étrangère, dès que les groupes deviendraient administrables par un utilisateur.

**4. Pourquoi des colonnes `JSON` pour les mappings comptables ?**
> Parce que ce sont des **structures opaques pour la base** : leur schéma varie d'un client à l'autre, la base ne les indexe jamais, ne les joint jamais, n'y fait jamais de recherche — elle les lit en bloc et les rend à l'API Python, qui les interprète.
> **Sur la 1NF :** la première forme normale porte sur les attributs que la base doit manipuler comme des valeurs. Un document opaque n'en est pas un. C'est aussi pourquoi je n'ai créé aucun index secondaire dessus.
> **La limite que je reconnais :** le jour où j'aurais besoin de requêter *à l'intérieur* de ces structures, ce choix deviendrait mauvais — il faudrait alors soit les normaliser, soit passer en `JSONB` avec un index GIN.

**5. Pourquoi `ON DELETE CASCADE`, et pas une suppression applicative ?**
> Parce que le droit à l'oubli est une **exigence métier**, et qu'une garantie portée par le schéma est plus fiable qu'une garantie portée par du code. Si je supprimais les données filles depuis l'application, il suffirait d'un chemin de suppression oublié pour laisser des données personnelles orphelines. La base, elle, ne peut pas oublier.

**6. Pourquoi pas de NoSQL ?**
> Voir la fiche générale, partie 4 — les quatre arguments : données relationnelles, besoins transactionnels, volumétrie, semi-structuré déjà couvert en SQL.

### 2.3 Les quatre faiblesses de ton modèle — connais-les avant qu'on te les montre

Ce sont de vraies questions qu'un jury à l'aise en base de données peut poser. Les découvrir en direct serait déstabilisant ; les avoir préparées est un atout.

**a) Rien n'empêche un utilisateur d'avoir deux mappings de codes.**
`user_code_maps` a pour seule clé un `id SERIAL`, et **aucune contrainte d'unicité sur `user_id`**. Le modèle autorise donc `(0,n)` mappings par utilisateur, alors que le métier en veut manifestement **un seul**.
> **Réponse préparée :** *« vous avez raison, la contrainte métier n'est pas portée par le schéma : c'est l'application qui garantit qu'il n'y a qu'un mapping par utilisateur. Le correctif propre est un `UNIQUE(user_id)` sur les trois tables de mapping. C'est exactement le genre d'écart que je viens de vous décrire sur `applications.groups` : une règle qui vit dans le code alors qu'elle devrait vivre dans la base. »*
> C'est une excellente réponse, parce qu'elle montre que tu sais **où** doit vivre une contrainte.

**b) `fascicule_mcdo` n'apparaît plus au MCD, mais la table existe toujours.**
Elle a été retirée du MCD corrigé — elle y flottait sans aucune association. Mais **la table reste au MPD et dans le code**, et la fonctionnalité correspond à **BF05** de ton cahier des charges. C'est donc un écart MCD/MPD que tu dois assumer explicitement.
> **Réponse préparée :** *« c'est une table de configuration technique, pas une entité du modèle métier du portail : elle n'a aucune association, elle est lue en bloc par l'outil de conversion. Je l'ai donc écartée du conceptuel et documentée au physique. C'est la table la plus ancienne du projet, héritée de l'outil autonome, où la configuration était globale et pas rattachée à un utilisateur. Proprement, elle devrait être rattachée soit à l'utilisateur, soit à une entité Restaurant qui n'existe pas encore dans mon modèle. »*
> Les trois options possibles et leur coût sont détaillés dans `doc/MCD_corrige.md` — **tranche avant l'oral.**

**c) Il n'y a pas d'entité `Restaurant`.**
Alors que le restaurant est le pivot du métier — les tirages sont par restaurant, l'Excel a une feuille par restaurant, les codes comptables sont propres à chaque client.
> **Réponse préparée :** *« parce que les tirages ne sont pas persistés : ils sont traités en flux et les fichiers sont supprimés au bout de cinq minutes. Le restaurant n'existe que le temps du traitement, il n'a donc pas besoin d'être une entité. Le jour où l'on voudrait historiser les tirages ou produire des statistiques par restaurant, il faudrait créer cette entité — c'est la première évolution que je ferais sur ce modèle. »*
> Cette réponse est forte : elle montre que l'absence d'une entité est un **choix de périmètre**, pas un oubli.

**d) 🔴 Ta phrase d'exposé sur le droit à l'oubli est plus forte que ton schéma.**
En § 3.3 tu dis : *« le droit à l'oubli n'est pas écrit dans mon code, il est garanti par la structure de la base elle-même »*. Vérifie avant de la prononcer, parce qu'elle est **à moitié fausse** :
- `ON DELETE CASCADE` réel sur `events.uid`, `user_code_maps.user_id`, `user_code_maps_gen_aux.user_id`, `code_journal.user_id` ;
- **mais `sessions.user_id` et `user_application_permissions.user_id` ont une FK sans cascade** — sans action explicite, la suppression du compte **échouerait** (comportement par défaut : `NO ACTION`). C'est `DeleteUser` qui supprime ces lignes, explicitement, dans une transaction de six ordres avec rollback.

> **Reformulation à adopter :** *« la suppression est atomique : une transaction supprime les droits, les sessions et les paramétrages, puis le compte. Le schéma et le code se couvrent mutuellement — les cascades garantissent qu'aucune ligne ne survit à son propriétaire, et là où la cascade n'est pas posée, la clé étrangère fait échouer la suppression plutôt que de laisser des orphelins. »* C'est plus juste **et** plus solide que la formule absolue.

**Et le piège dans le piège :** ta règle de gestion **RG07** dit que « les événements d'audit survivent à la suppression du compte », alors que `events.uid` est justement en `ON DELETE CASCADE`. **La règle et le schéma se contredisent.**
> **Réponse préparée :** *« vous avez raison, et c'est la règle qui a raison sur le code : un journal d'audit ne doit pas disparaître avec son sujet. Le correctif est un `ON DELETE SET NULL` avec conservation d'un identifiant pseudonymisé — la traçabilité est préservée sans conserver de donnée personnelle, donc sans conflit avec le droit à l'oubli. »*
> **Tranche avant l'oral :** soit tu corriges le schéma, soit tu reformules RG07. Les deux se défendent ; l'incohérence, non.

---

## Partie 3 — Les questions de conception que le jury pose vraiment

1. Expliquez-moi votre MCD. *(Ne récite pas les tables : raconte le métier. « Un utilisateur accède à des applications selon des droits explicites ; il ouvre des sessions ; son activité génère des événements. »)*
2. Montrez-moi une association plusieurs-à-plusieurs et sa traduction.
3. Pourquoi cette clé étrangère est-elle de ce côté-là ?
4. Votre schéma est-il normalisé ? Jusqu'à quelle forme, et comment le savez-vous ?
5. Où avez-vous dénormalisé, et pourquoi l'assumez-vous ?
6. Qu'est-ce qui se passe en base quand un utilisateur est supprimé ?
7. Quels index avez-vous, et pourquoi pas davantage ?
8. Comment feriez-vous évoluer ce schéma pour [ajouter une fonctionnalité] ?
9. Différence entre `include` et `extend` ?
10. Sur votre diagramme de séquence, que signifie ce cadre `alt` ?
11. Pourquoi une interface entre le Service et le Repository ?
12. Si je vous demande d'ajouter l'historisation des tirages, que changez-vous dans votre modèle ?
13. *(§ 3.3)* Vous dites que votre MCD « pourrait décrire un classeur papier ». Alors pourquoi y voit-on des identifiants techniques ? *(Réponse : un MCD ne porte ni clé étrangère ni clé technique — s'il en reste sur ta planche, c'est un mélange de niveaux, et c'est exactement le reproche fait à l'entité « Permission des applications ». Assume ou corrige, ne bricole pas.)*
14. *(§ 3.3)* Vous annoncez **neuf tables** et votre MCD compte **huit entités**. D'où vient la différence ? *(La table de jonction : au conceptuel c'est une **association**, elle ne devient une table qu'au passage MLD. Savoir dire ça, c'est prouver qu'on a compris le passage.)*
15. *(§ 3.3)* Vos mappings sont en JSON parce que « la base ne fait jamais de recherche dedans ». Et le jour où il faut chercher dedans ? *(Deux sorties : un index **GIN** sur la colonne `jsonb`, ou l'éclatement en table si la donnée devient interrogeable et jointe. Le critère de bascule, c'est le moment où la base doit manipuler ces valeurs **une par une** au lieu de les lire en bloc.)*
16. *(§ 3.3)* Qu'est-ce que la suppression d'un compte **n'efface pas** ? *(voir 2.3 d\) — question la plus dangereuse du bloc)*
17. *(§ 3.4)* Votre diagramme de séquence de l'authentification : à quel moment exact la session est-elle créée, et pourquoi pas avant ? *(Après la comparaison bcrypt, jamais avant : créer la session d'abord reviendrait à matérialiser un accès pour une identité non vérifiée, et à offrir une surface d'écriture en base à un attaquant non authentifié.)*

**La question 8 et la question 12 sont les plus dangereuses**, parce qu'on ne peut pas les préparer par cœur : ce sont des questions de conception **en direct**. La méthode pour y répondre sans paniquer :

> 1. **Reformule** pour gagner cinq secondes et vérifier que tu as compris.
> 2. **Nomme les entités** en jeu et dis si elles existent déjà.
> 3. **Détermine la cardinalité** à voix haute, avec la formule : *« pour un tirage, combien de restaurants ? Un seul. Pour un restaurant, combien de tirages ? Plusieurs. Donc un-à-plusieurs. »*
> 4. **Applique la règle de passage** : la clé descend du côté « n ».
> 5. **Mentionne l'impact** : index, cascade, migration.

Dérouler ces cinq étapes à voix haute, même lentement, vaut infiniment mieux qu'une réponse rapide et fausse. Le jury note la **méthode**, pas la vitesse.

---

## Partie 4 — Exercices

> À faire **sur papier, sans regarder le corrigé**. Compte 45 minutes pour l'ensemble.

### Niveau 1 — Lire

**E1.** Traduis en français ces trois cardinalités Merise :
`CLIENT (1,n) —— passe —— (1,1) COMMANDE`

**E2.** Dans ton modèle, quelle est la cardinalité entre `users` et `sessions`, de chaque côté ? Justifie chaque minimum.

**E3.** En UML, où place-t-on la multiplicité par rapport à Merise ? Pourquoi cette différence est-elle une question piège ?

**E4.** Losange plein ou losange vide entre `users` et `sessions` ? Justifie en une phrase.

### Niveau 2 — Traduire

**E5.** Traduis en MLD, en notant les clés primaires et étrangères :
`ETUDIANT (0,n) —— suit —— (1,n) COURS`, l'association portant une propriété `note`.

**E6.** Même exercice avec :
`SALARIE (1,1) —— appartient —— (0,n) SERVICE`

**E7.** Sur ton propre modèle : écris le MLD complet de l'association entre `users` et `applications`, en incluant la contrainte qui empêche les doublons.

### Niveau 3 — Normaliser

**E8.** Voici une table extraite d'un système comptable. Donne la forme normale atteinte, puis normalise-la jusqu'en 3NF en nommant chaque anomalie corrigée.

```
ECRITURE
──────────────────────────────────────────────────────────────────────────────
num_piece │ date  │ code_journal │ libelle_journal │ comptes           │ montant
   A-102  │ 31/01 │ VE           │ Journal ventes  │ 707100 ; 445710   │ 1284.50
   A-103  │ 31/01 │ VE           │ Journal ventes  │ 707200            │  412.90
   A-104  │ 02/02 │ AC           │ Journal achats  │ 601000 ; 445660   │  873.20
```

**E9.** Ta table `user_code_maps` stocke un mapping en JSON. Quelqu'un te dit : *« ce n'est pas en 1NF »*. Rédige ta réponse en trois phrases, puis indique dans quel cas cette personne aurait raison.

### Niveau 4 — Trouver l'erreur

**E10.** Ce fragment de MCD contient **deux** erreurs de méthode. Trouve-les.

```
   UTILISATEUR                          APPLICATION
   ─────────────                        ────────────
   id_utilisateur                       id_application
   email                                nom
   id_application  ←── FK               base_url
                        (0,n) —— accède —— (0,n)
```

**E11.** Un candidat écrit : *« mon schéma est en 3NF, donc il est aussi en 2NF et en 1NF »*. Est-ce correct ? Et la réciproque ?

**E12.** Un candidat justifie une table de jonction en disant : *« j'ai mis une table intermédiaire pour améliorer les performances »*. Qu'est-ce qui cloche dans cette justification ?

### Niveau 5 — Concevoir en direct

**E13.** Le cabinet veut désormais **historiser les tirages de caisse** : conserver, pour chaque traitement, le restaurant, la date, les montants ventilés par compte, et l'utilisateur qui a lancé le traitement. Déroule les cinq étapes de la méthode : entités, cardinalités, MLD, index, impact sur l'existant.

**E14.** On te demande d'ajouter la notion de **client** (le restaurant appartient à un client, un client peut avoir plusieurs restaurants), et de rendre les codes comptables propres au **client** plutôt qu'à l'utilisateur. Que devient `user_code_maps` ?

---

## Partie 5 — Corrigé

**E1.** Un client passe **au moins une** commande et peut en passer plusieurs. Une commande est passée par **exactement un** client. Association un-à-plusieurs. *(Note : le `(1,n)` côté client est discutable — il interdit d'enregistrer un client avant sa première commande. En pratique on met souvent `(0,n)`. Savoir soulever ce point vaut des points.)*

**E2.** `users (0,n)` : un utilisateur peut n'avoir aucune session ouverte — c'est le cas dès qu'il est déconnecté — et il peut en avoir plusieurs, s'il se connecte depuis deux navigateurs. `sessions (1,1)` : une session appartient forcément à un utilisateur et à un seul ; une session orpheline n'a aucun sens, et la clé étrangère `NOT NULL` l'interdit.

**E3.** En Merise, la cardinalité est **du côté de l'entité qu'elle décrit** ; en UML, la multiplicité est **à l'autre bout**, du côté opposé. C'est une question piège parce que les deux notations expriment la même contrainte mais s'écrivent en miroir : un candidat qui n'a pas compris lira un de ses deux diagrammes à l'envers.

**E4.** **Losange plein — composition.** Une session n'a aucune existence sans son utilisateur ; si l'utilisateur disparaît, la session n'a plus de sens, et c'est d'ailleurs ce que traduit mon `ON DELETE CASCADE`.

**E5.** Association plusieurs-à-plusieurs → table de jonction portant la propriété :
```
ETUDIANT(num_etudiant, nom, ...)
COURS(code_cours, intitule, ...)
INSCRIPTION(#num_etudiant, #code_cours, note)
        clé primaire = (num_etudiant, code_cours)
```

**E6.** Association un-à-plusieurs → la clé descend du côté « n », c'est-à-dire côté salarié :
```
SERVICE(code_service, libelle)
SALARIE(matricule, nom, #code_service NOT NULL)
```
Le `NOT NULL` traduit le minimum à 1 : un salarié appartient obligatoirement à un service.

**E7.**
```
users(id, uid UNIQUE, email UNIQUE, username UNIQUE, password, admin, role, entreprise, last_seen)
applications(id, name, base_url, icon_path, groups)
user_application_permissions(id, #user_id → users(uid), #application_id → applications(id), can_access,
                             UNIQUE(user_id, application_id))
```
La contrainte `UNIQUE(user_id, application_id)` est ce qui empêche deux droits contradictoires sur le même couple. La clé primaire `id` est une clé de substitution ; la clé candidate naturelle serait le couple lui-même.

**E8.** La table est **en 0NF** : `comptes` est multivalué.

*1NF* — éclatement du multivalué, une ligne par compte. Clé = (num_piece, compte). Anomalie corrigée : impossibilité de rechercher ou de contraindre un compte.

*2NF* — `date`, `code_journal` et `libelle_journal` ne dépendent que de `num_piece`, pas du compte. Dépendance partielle. On sépare l'en-tête des lignes :
```
PIECE(num_piece, date, #code_journal)
LIGNE(#num_piece, #compte, montant)
```
Anomalie corrigée : la date était répétée sur chaque ligne, avec un risque d'incohérence.

*3NF* — `libelle_journal` dépend de `code_journal`, pas de `num_piece` : dépendance transitive. On sort le journal :
```
JOURNAL(code_journal, libelle_journal)
PIECE(num_piece, date, #code_journal)
LIGNE(#num_piece, #compte, montant)
```
Anomalie corrigée : renommer un journal se faisait en autant d'endroits qu'il y avait de pièces ; et supprimer la dernière pièce d'un journal faisait disparaître le journal.

**E9.** *« Non, parce que la première forme normale porte sur les attributs que la base doit manipuler comme des valeurs. Ce champ est une structure opaque pour PostgreSQL : elle n'est jamais indexée, jamais jointe, jamais filtrée — elle est lue en bloc et interprétée par l'API Python. C'est le pattern documentaire, assumé, dans un moteur relationnel. »*
**Cette personne aurait raison** si je devais un jour requêter à l'intérieur de la structure — chercher tous les utilisateurs ayant mappé le compte 707100, par exemple. À ce moment-là, il faudrait soit normaliser en une table `mapping(user_id, code_source, code_cible)`, soit passer en `JSONB` avec un index GIN.

**E10.** Erreur 1 : **une clé étrangère apparaît dans un MCD**. `id_application` n'a rien à faire dans l'entité UTILISATEUR au niveau conceptuel — c'est un objet du MLD. Erreur 2 : cette FK est de toute façon **incompatible avec les cardinalités** affichées : une association (0,n)—(0,n) ne se traduit jamais par une clé étrangère, mais par une table de jonction.

**E11.** **Oui, c'est correct** : les formes normales sont emboîtées, la 3NF implique la 2NF qui implique la 1NF. **La réciproque est fausse** : être en 1NF n'apprend rien sur la 2NF. Une seule direction.

**E12.** Une table de jonction n'est **pas** une décision de performance — c'est la **seule traduction possible** d'une association plusieurs-à-plusieurs dans un modèle relationnel. Justifier par la performance révèle qu'on a appliqué une recette sans comprendre la règle. La bonne justification est : *« parce qu'un utilisateur accède à plusieurs applications et qu'une application est accessible à plusieurs utilisateurs, et qu'on ne peut pas stocker plusieurs références dans une colonne sans violer la 1NF. »*

**E13.**
1. *Entités* — `RESTAURANT` (n'existe pas), `TIRAGE` (n'existe pas), `LIGNE_TIRAGE` (n'existe pas), `users` (existe).
2. *Cardinalités* — pour un tirage, un seul restaurant ; pour un restaurant, plusieurs tirages → un-à-plusieurs. Pour un tirage, un seul utilisateur déclencheur ; pour un utilisateur, plusieurs tirages → un-à-plusieurs. Pour un tirage, plusieurs lignes ; pour une ligne, un seul tirage → un-à-plusieurs, et **composition** : la ligne n'existe pas sans son tirage.
3. *MLD* —
```
RESTAURANT(id, nom, ville)
TIRAGE(id, date_traitement, #restaurant_id, #user_uid → users(uid))
LIGNE_TIRAGE(id, #tirage_id ON DELETE CASCADE, compte, montant)
```
4. *Index* — sur `TIRAGE(restaurant_id, date_traitement)`, parce que la requête attendue est « les tirages d'un restaurant sur une période ». C'est le premier index secondaire justifié de mon modèle.
5. *Impact* — aucune table existante n'est modifiée, uniquement des ajouts : la migration est **additive et compatible N-1**, conforme à ma stratégie de rollback. Et cela remet en cause ma règle RG08 sur la suppression des fichiers à cinq minutes : les fichiers resteraient éphémères, mais leur **contenu** deviendrait persistant, ce qui a une conséquence RGPD à documenter.

*(Ce dernier point — relier un changement de modèle à une règle de gestion et au RGPD — est ce qui distingue une bonne réponse d'une excellente.)*

**E14.**
```
CLIENT(id, raison_sociale)
RESTAURANT(id, nom, ville, #client_id)
CODE_MAP(id, #client_id UNIQUE, mapping JSON)
```
`user_code_maps` **disparaît en tant que telle** : le mapping cesse d'être une propriété de l'utilisateur pour devenir une propriété du client. C'est un déplacement de la clé étrangère, pas une simple copie.
**Le point à mentionner :** il faut une migration de données, pas seulement de schéma — il faut décider à quel client rattacher les mappings existants, et ce n'est pas déductible automatiquement. C'est typiquement le genre de migration qui exige une reprise manuelle.

---

## Partie 6 — Mémo de la veille

À relire dix minutes avant d'entrer.

1. **Trois niveaux** : MCD = le métier, MLD = les tables, MPD = le SQL de PostgreSQL. **Jamais de clé étrangère dans un MCD.**
2. **Cardinalité** : *« pour UN X, combien de Y, minimum et maximum ? »* Merise écrit le chiffre du côté de l'entité décrite ; UML à l'autre bout.
3. **Règles de passage** : 1:N → la clé descend côté « n ». N:N → table de jonction. 1:1 → fusion ou clé côté obligatoire.
4. **Formes normales** : la clé, toute la clé, rien que la clé. Emboîtées, dans un seul sens.
5. **Mon schéma** : **9 tables au MPD, 8 entités au MCD** — la différence, c'est la table de jonction, qui n'existe qu'au niveau logique. 3NF, deux dénormalisations assumées : `applications.groups` et les colonnes `JSON`.
6. **Composition vs agrégation** : si je supprime le tout, la partie a-t-elle encore un sens ?
7. **Mes cascades** portent le droit à l'oubli : une garantie de schéma vaut mieux qu'une garantie de code.
8. **Mes quatre faiblesses connues** : pas de `UNIQUE(user_id)` sur les mappings (posé par la migration 003), `fascicule_mcdo` présente au MPD mais absente du MCD, pas d'entité `Restaurant`, et **la cascade qui ne couvre pas tout** — `sessions` et `user_application_permissions` sont supprimées par transaction, pas par le schéma, et RG07 contredit la cascade sur `events`. Pour chacune, j'ai une réponse.
   ⚠️ **Ne dis pas** « le droit à l'oubli n'est pas écrit dans mon code » : dis « la suppression est atomique, schéma et transaction se couvrent mutuellement ».
9. **Question de conception en direct** : entités → cardinalités à voix haute → règle de passage → index → impact. Lentement.
10. **Si je ne sais pas** : je le dis, et je raisonne à voix haute. Le jury note la méthode, pas la vitesse.

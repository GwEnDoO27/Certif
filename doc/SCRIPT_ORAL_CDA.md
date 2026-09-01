# Script de soutenance — TP CDA

**Candidat :** Bénard Gwendal — Zone01 Normandie / Cabinet Martini
**Durée cible de l'exposé :** environ 46 minutes
**Source de vérité :** `Fichier Final/A Envoyer/Certif corrigé.docx` — la version remise au jury. Tout ce script est calé dessus.

> **Comment lire ce script.**
> `[ÉCRAN]` = ce que tu affiches à ce moment-là. `⏱` = minutage cumulé indicatif.
> Le texte en prose est **ce que tu dis** — écrit pour être parlé, pas lu. Ne l'apprends pas mot pour mot : retiens l'enchaînement des idées et les chiffres. Une soutenance récitée s'entend.
> **Le ton à viser : une présentation de projet en réunion de travail, pas une plaidoirie d'examen.** Tu expliques ce que tu as construit et pourquoi, à des gens qui s'y connaissent — tu ne t'adresses pas à un jury qui va te noter. Rien dans ce que tu dis à voix haute ne devrait mentionner l'évaluation, le référentiel, ou anticiper une question qu'« on » pourrait te poser.
> Les encadrés `⚠️` sont des rappels à toi-même, à ne pas prononcer.
> Un guide de coupe pour tenir en 35 minutes est donné à la fin.

---

## 0. Ouverture — 1 min 30 ⏱ 0:00 → 1:30

`[ÉCRAN] Page de titre : nom, titre du projet, Cabinet Martini, Zone01 Normandie`

Bonjour, je m'appelle Gwendal Bénard. Le projet que je vais vous présenter est celui que j'ai mené en alternance au Cabinet Martini, un cabinet d'expertise comptable à Rouen : la mise en place d'une plateforme regroupant les outils développés pour les collaborateurs et les clients du cabinet.

Je vais vous le présenter dans l'ordre où je l'ai vécu : d'abord le problème posé, puis l'analyse et la conception, les choix techniques, la réalisation, la sécurité, les tests, la mise en production, et enfin le bilan.

Ça dure environ quarante-cinq minutes. Gardez vos questions pour la fin si possible, mais arrêtez-moi si un point n'est pas clair.

> ⚠️ Respire. Regarde les trois membres du jury, pas l'écran. Ton nom et le nom du projet doivent être dits lentement.

---

## 1. Le contexte et le problème — 4 min ⏱ 1:30 → 5:30

`[ÉCRAN] Logo du cabinet + les 3 pôles + le chiffre 40 collaborateurs`

Le Cabinet Martini est un cabinet d'expertise comptable basé à Rouen. Il officie majoritairement en Normandie et a des clients dans toute la France. Il compte une quarantaine d'employés répartis en trois pôles : la comptabilité, qui rassemble la majorité des effectifs, le social, et le juridique.

Le souhait du cabinet, au départ, était de mettre en place des outils internes répondant à des problématiques propres à chaque pôle. Cette idée a ensuite évolué vers un portail centralisé, donnant accès à chaque outil, avec la possibilité d'en mettre certains à disposition des clients.

Le projet n'est pas parti d'un cahier des charges. Il est parti d'une observation.

Parmi les clients du cabinet, il y a des restaurants — notamment des franchises McDonald's. Chaque mois, ces restaurants transmettent leurs tirages de caisse sous forme de fichiers `.EDI` : un format texte brut produit par les caisses. Les comptables les traitaient **à la main**, restaurant par restaurant.

`[ÉCRAN] Capture d'un fichier .EDI brut à gauche, l'Excel attendu à droite`

Concrètement : ouvrir chaque fichier, lire les lignes, retrouver à quel compte comptable correspond chaque type de vente, ressaisir les montants dans un tableur. Avec une difficulté supplémentaire — **les codes comptables sont propres à chaque client**. Le même type de vente ne va pas sur le même compte selon le restaurant. À chaque traitement, le comptable devait se souvenir de la bonne correspondance ou aller la rechercher. Long, répétitif, et par nature exposé à l'erreur de saisie.

`[ÉCRAN] Les difficultés identifiées]`

En creusant la situation avec eux, plusieurs difficultés concrètes sont apparues, et ce sont elles qui ont structuré tout le projet : le traitement manuel et chronophage des tirages de caisse ; des codes comptables propres à chaque client, à ressaisir à chaque fois ; une multiplication d'outils non centralisés, sans point d'accès unique ; l'absence de gestion unifiée des droits d'accès ; et un manque de visibilité sur l'utilisation réelle des outils.

Les deux premières ont donné le **premier logiciel** : un outil qui automatise la conversion des tirages de caisse. Il récupère les fichiers issus des caisses, leur applique les transformations comptables paramétrées, et restitue un fichier Excel exploitable.

Les autres ont fait émerger le vrai besoin, celui qui est devenu le projet : **une plateforme** capable d'héberger cet outil et tous les futurs outils du cabinet derrière un accès unique et sécurisé, avec une gestion des droits par rôle et un suivi de l'activité.

Le besoin a donc émergé en deux temps, et le projet a évolué d'un outil vers une infrastructure. C'est cette évolution qui en fait un projet de conception, et pas seulement de développement.

> ⚠️ C'est le passage le plus important de l'exposé. L'auditoire doit comprendre **pourquoi** la plateforme existe. Prends le temps : si le problème n'est pas clair, tout le reste sonnera comme une démonstration technique gratuite.

---

## 2. Le cadrage et l'organisation — 5 min ⏱ 5:30 → 10:30

### 2.1 Les objectifs et le périmètre — 2 min

`[ÉCRAN] Les objectifs]`

Avec le cabinet, on a fixé plusieurs objectifs : créer des applications métier spécialisées, gérer les utilisateurs et leurs accès selon leur rôle, assurer un suivi de l'activité via un tableau de bord, permettre une communication entre les utilisateurs connectés, et garantir la sécurité des données ainsi que la conformité au RGPD.

Ça s'est traduit en **douze besoins fonctionnels** priorisés — quatre pour l'outil métier, huit pour la plateforme — et en **cinq besoins non fonctionnels** : un temps de réponse inférieur à deux secondes sur les opérations courantes, la conformité OWASP et RGPD, une disponibilité de 99,5 % hors maintenance, une architecture permettant le scaling horizontal, et une maintenabilité assurée par du code documenté en couches.

`[ÉCRAN] Le tableau des BF`

J'ai aussi formalisé **neuf règles de gestion** — les règles métier, indépendantes de la technique. Par exemple : une session expire au bout de 24 heures ; un utilisateur ne voit que les applications qui lui sont explicitement attribuées, il n'y a pas d'accès par défaut ; les fichiers déposés pour traitement sont supprimés au plus tard cinq minutes après. Ces règles vivent dans la couche métier du code, j'y reviens plus loin.

### 2.2 Les contraintes — 1 min

`[ÉCRAN] Contraintes techniques / organisationnelles`

Sur le plan technique, il n'y avait qu'**une seule contrainte d'infrastructure imposée** : un serveur vierge, sur lequel il fallait provisionner et configurer l'intégralité de l'environnement — système, sécurité, reverse proxy, base de données, orchestration. Tout le reste relève de mes propres décisions d'architecture.

Deux contraintes venaient du métier : le format d'entrée `.EDI`, imposé par les caisses, et le format de sortie Excel, attendu par les comptables. Non négociables. À quoi s'ajoutait un accès en HTTPS et la compatibilité avec les navigateurs modernes.

Sur le plan organisationnel : le projet a été mené **seul**, trois jours par semaine, sur environ six mois.

### 2.3 Comment le travail s'est organisé — 2 min

`[ÉCRAN] Frise des 6 itérations`

Un rythme à temps partiel, en solo, rend certains cadres de travail peu adaptés. Un fonctionnement pensé pour une équipe, avec des rituels quotidiens et des points de fin de cycle collectifs, perd son sens dès qu'il n'y a plus qu'une seule personne pour les tenir.

Le suivi s'est donc fait de façon simple : un carnet papier faisant office de tableau de bord, les tâches listées par itération, la tâche en cours marquée, les terminées rayées, les reports d'une session à l'autre recopiés explicitement — relu en début de session pour recharger le contexte après plusieurs jours d'interruption. Une seule tâche ouverte à la fois, parce qu'avec des sessions espacées de plusieurs jours, un chantier à moitié terminé se perd facilement. Et une règle simple pour clore une tâche : le code écrit, testé, passé au lint, et commité selon les conventions du projet.

Le tout organisé en six itérations, chacune se terminant par une démonstration au cabinet et un point sur ce qui avait fonctionné ou pas.

`[ÉCRAN] Les 6 itérations et leurs durées`

Le séquencement a suivi la logique de valeur. D'abord le logiciel de tirages de caisse — la priorité explicite des collaborateurs — livré en autonome pour apporter de la valeur au plus vite. Ensuite la plateforme, développée en parallèle des retours sur l'outil. Enfin le déploiement.

Au total, six itérations : dix-sept jours, dix-sept, treize, dix, onze et vingt — **quatre-vingt-huit jours effectifs**.

Un point à retenir sur cette organisation : les utilisateurs étaient dans le bureau d'à côté. L'itération 2 existe uniquement parce que les comptables, en utilisant l'outil, ont fait remonter qu'il les rendait dépendants de moi. J'y reviens dans la partie réalisation.

`[ÉCRAN] Exemples de commits + schéma de branching`

Côté outillage : GitHub pour le versioning, GitHub Actions pour la CI/CD, Figma pour le maquettage.

Deux conventions ont été posées. D'abord les **Conventional Commits**, au format type, portée, description — ça rend l'historique lisible et filtrable, et permet de déduire automatiquement le type de release : un `feat` donne une version mineure, un `fix` un correctif, un *breaking change* une version majeure.

Ensuite une stratégie de branches : **GitHub Flow**. Une seule branche permanente, `main`, toujours déployable. Toute modification passe par une branche éphémère préfixée `feature/`, `fix/`, `chore/` ou `docs/`. Et une pull request, même seul — pas comme un rituel de revue, mais pour déclencher la CI : tests et lint obligatoires avant le merge. Puis un squash & merge, pour garder un historique linéaire où un commit correspond à une fonctionnalité.

GitHub Flow a été préféré à Git Flow, avec ses branches `develop`, `release` et `hotfix`, parce qu'il n'y a qu'un développeur, un déploiement continu vers la préproduction après chaque merge, et aucune version à maintenir en parallèle.

---

## 3. La conception — 8 min 30 ⏱ 10:30 → 19:00

### 3.1 Les acteurs et les cas d'utilisation — 1 min 30

`[ÉCRAN] Diagramme de cas d'utilisation`

La première étape a été d'identifier les acteurs. Il y en a six, qui correspondent aux six rôles de la plateforme : Admin, Dev, Comptable, Social, Auditeur et Client.

L'idée directrice est simple : **un utilisateur ne voit que ce à quoi il a droit**. Un comptable voit les outils de comptabilité, un utilisateur du pôle social les outils de paie, un client externe uniquement ce qu'on lui a explicitement attribué. Seul un administrateur accède à l'administration.

Sur ce diagramme, il y a les cas d'utilisation communs — se connecter, consulter son catalogue — et les cas réservés, en particulier tout le bloc d'administration : créer un utilisateur, attribuer des applications, consulter les statistiques.

### 3.2 Le maquettage — 2 min

`[ÉCRAN] Les 3 stades côte à côte : zoning → wireframe → maquette abstraite`

Avant de coder, cinq écrans ont été maquettés : la connexion, l'accueil avec le catalogue, l'administration, l'outil de tirages de caisse et la page d'erreur.

Mais ils ne l'ont pas été d'un seul coup. Le travail a été découpé en **trois stades de fidélité croissante**, et chaque stade sert à valider **une seule chose**. C'est ce découpage qui a rendu le maquettage utile plutôt que décoratif.

`[ÉCRAN] Le zoning — planche des 5 pages, zones colorées`

**Le premier stade, c'est le zoning.** Chaque page est découpée en zones fonctionnelles — navigation, identité, contenu, action, saisie, auxiliaire, feedback. Chaque couleur correspond à un **rôle**, pas à un choix esthétique : à ce stade, aucune décision visuelle n'est prise. On valide uniquement l'architecture de l'information — est-ce que l'utilisateur trouvera ce qu'il cherche là où il le cherche ?

`[ÉCRAN] Les wireframes — boîtes grises + parcours annoté`

**Le deuxième, les wireframes.** Des boîtes grises et des libellés, rien d'autre. On y fige la structure et le parcours, avec le flux utilisateur annoté par des numéros sur chaque page. L'absence de couleur est délibérée : tant qu'il y a du visuel, on discute du visuel — et on ne regarde plus le parcours.

`[ÉCRAN] Les maquettes abstraites — grille et rythme, un seul accent`

**Le troisième, les maquettes abstraites.** Des barres grises, une seule couleur d'accent, aucun texte réel, aucune icône. Ça paraît contre-intuitif pour un dernier stade, mais c'est justement le plus utile : sans contenu lisible, on ne peut valider que la **grille**, le **rythme**, les **espacements** et la hiérarchie typographique — celle qui doit fonctionner par la taille seule. Si la hiérarchie tient sans mots, elle tiendra avec.

Chaque planche se termine par un bloc d'annotations qui explicite les choix et fait le lien vers le composant React correspondant.

`[ÉCRAN] Principes UX + RGAA`

Sur les principes retenus : une navigation qui tient en un coup d'œil, un retour visuel systématique sur chaque action — un traitement de fichier prend quelques secondes, l'utilisateur doit savoir qu'il se passe quelque chose — et une interface responsive, mobile, tablette, desktop.

Sur l'accessibilité, le travail s'appuie sur le **RGAA 4**, la déclinaison française des WCAG : contrastes suffisants, navigation possible au clavier, textes alternatifs, labels de formulaires. C'est un axe où les bases sont posées, mais où il reste du travail — c'est documenté comme tel plutôt que présenté comme terminé.

> ⚠️ **Trois stades, pas quatre.** Les mockups haute fidélité existent bien dans `doc/mockups/` (fichiers `01-` à `05-`), mais tu ne les présentes pas comme un stade de la démarche — les écrans finis sont montrés juste après, en §3.2 bis. Le message qui compte : **chaque stade valide une chose et une seule**, et retirer de l'information à chaque étape est un choix, pas une limite.

### 3.3 La modélisation des données — 3 min 30

`[ÉCRAN] Dictionnaire de données — extrait`

Avant de dessiner quoi que ce soit, j'ai fait la liste de tout ce que l'application doit stocker : chaque information, son type, et la règle métier qui la justifie. C'est le dictionnaire de données. Tous les schémas qui suivent en découlent.

Ensuite j'ai suivi la méthode Merise, qui découpe la modélisation en trois étapes. Le principe : on ne se pose qu'une question à la fois.

`[ÉCRAN] MCD`

**La première, c'est le métier.** De quoi parle-t-on, et qu'est-ce qui est relié à quoi ? Ici : des utilisateurs, des applications, des sessions, des paramétrages comptables.

Le cœur du modèle, c'est le lien entre utilisateurs et applications. Un utilisateur a accès à plusieurs applications, et une application est accessible à plusieurs utilisateurs. Les deux côtés sont au pluriel — en modélisation on appelle ça une relation « plusieurs à plusieurs ».

À ce stade, aucune décision technique : ce schéma pourrait aussi bien décrire un classeur papier.

`[ÉCRAN] MLD`

**La deuxième étape, c'est le rangement en tables.** Et c'est là que la relation « plusieurs à plusieurs » pose un problème concret : on ne peut pas mettre plusieurs applications dans une seule case d'une ligne utilisateur.

La solution est mécanique : on crée **une troisième table**, qui ne contient que des couples. Un utilisateur, une application, et le droit associé. Une ligne par droit accordé.

Et c'est cette table qui porte une règle centrale du projet : **pas d'accès par défaut**. Si la ligne n'existe pas, l'application n'apparaît même pas dans le catalogue de l'utilisateur.

`[ÉCRAN] MPD`

**La troisième étape, c'est le SQL réel** : neuf tables, avec les types PostgreSQL et les contraintes.

Deux choix méritent un mot. D'abord les mappings de codes comptables, stockés en JSON plutôt qu'éclatés en tables : ils changent d'un client à l'autre, la base ne fait jamais de recherche dedans, elle les lit d'un bloc. Ensuite le groupe d'une application, stocké en texte simple — un raccourci assumé, pour éviter une jointure sur une donnée qui ne bouge quasiment jamais.

Un dernier point, qui relie la technique au droit. Quand un compte est supprimé, la base efface automatiquement tout ce qui lui appartient : ses sessions, ses droits, ses paramétrages, son historique. Le droit à l'oubli du RGPD n'est pas écrit dans mon code — il est garanti par la structure de la base elle-même. Ce qui le rend impossible à oublier.

> ⚠️ Bloc allégé. Le vocabulaire technique — cardinalités, troisième forme normale, atomicité, clé étrangère, `ON DELETE CASCADE`, index secondaires — n'est plus prononcé, mais tu dois le maîtriser : c'est exactement là-dessus qu'on t'interrogera. Tout est dans `REVISION_CONCEPTION.md`.

### 3.4 Les diagrammes dynamiques — 1 min 30

`[ÉCRAN] Diagramme de séquence de l'authentification`

Trois diagrammes de séquence complètent le dossier de conception, sur les flux critiques : l'authentification, la conversion d'un fichier EDI, et la connexion WebSocket.

Celui de l'authentification : le client envoie ses identifiants. Le handler valide la forme de la requête. Le service demande au repository l'utilisateur correspondant à l'email. Il compare le mot de passe fourni au hash bcrypt stocké. Si la comparaison réussit, il crée une session en base avec sa date d'expiration. Puis le handler pose le cookie et répond.

`[ÉCRAN] Diagramme de classes`

Et un diagramme de classes, qui illustre la couche métier du backend Go selon Clean Architecture. On y lit les trois couches : les handlers, les services — `AuthService`, `AdminService`, `AnalyseService`, `OnlineUserManager` — et les repositories.

Le point central, ce sont les **interfaces**. `AdminService` dépend de l'interface `AdminRep`, pas d'une implémentation concrète. En production, l'implémentation est une structure branchée sur PostgreSQL ; en test, un mock renvoie des valeurs déterministes sans aucune entrée-sortie.

---

## 4. Les choix techniques et l'architecture — 7 min ⏱ 19:00 → 26:00

### 4.1 L'architecture globale — 2 min

`[ÉCRAN] Schéma d'architecture globale`

Voici l'architecture. Un utilisateur arrive en HTTPS sur Traefik, qui joue le rôle de reverse proxy et de point d'entrée. Traefik route vers trois services : un frontend React servi statiquement par Nginx, un backend écrit en Go, et une API Python. Les deux back-ends partagent une base PostgreSQL.

Pourquoi trois services, et surtout pourquoi **deux** back-ends dans deux langages différents ? Le principe suivi est : **chaque service fait ce que son langage fait le mieux.**

Le backend Go porte le cœur transactionnel : l'authentification, les sessions, l'administration, le WebSocket. Go excelle sur la concurrence grâce aux goroutines, et offre des temps de réponse stables sous charge — exactement ce qu'exigent un middleware de session sollicité à chaque requête et un hub WebSocket qui maintient des dizaines de connexions ouvertes en permanence.

L'API Python porte le traitement des tirages de caisse : le parsing EDI, le mapping comptable, la génération de l'Excel. L'écosystème Python sur la donnée tabulaire — pandas, xlsxwriter — est sans rival, et les bibliothèques Go ne sont pas encore assez matures de leur côté pour traiter correctement certains cas complexes.

`[ÉCRAN] Le compromis, écrit noir sur blanc`

Ce choix a un prix, qui est assumé : deux back-ends à déployer, à monitorer et à maintenir. Et une cohérence de données à gérer au niveau applicatif, puisque les deux services partagent la même base plutôt que d'en avoir une chacun — ce qui simplifie la cohérence, au prix d'un couplage par le schéma.

À l'échelle de ce projet, le solde reste favorable : chaque service reste petit, testable isolément, et déployable indépendamment. Un correctif sur l'outil de conversion ne redéploie pas le service d'authentification.

### 4.2 Les choix de technologies — 2 min

`[ÉCRAN] Tableau comparatif — une ligne par techno`

Les autres choix, plus rapidement, mais tous ont été arbitrés.

**React**, pour la richesse de son écosystème et la réutilisabilité par composants. **Vite** plutôt que Create React App, qui est déprécié : le rechargement à chaud est quasi instantané. **Tailwind**, dont l'approche utility-first évite le CSS mort en production.

**PostgreSQL** plutôt que MySQL ou MongoDB. Deux raisons : le support JSON natif — dont l'usage vient d'être détaillé — et l'intégrité référentielle, dont dépend directement le droit à l'oubli.

Sur la base de données, un point mérite d'être détaillé : aucun moteur NoSQL n'a été utilisé à côté de PostgreSQL, et ce n'est pas un oubli — c'est un arbitrage.

**Première raison : mes données sont faites de liens.** Un utilisateur, ses applications, ses droits — tout est relié, et la base doit garantir ces liens. Si je supprime un compte, ses droits et ses sessions doivent disparaître avec lui. PostgreSQL le fait tout seul ; avec une base documentaire, j'aurais dû le reprogrammer.

**Deuxième raison : la taille.** Quelques dizaines d'utilisateurs internes. MongoDB est fait pour encaisser des millions d'écritures réparties sur plusieurs serveurs — à mon échelle, ça n'apporterait rien.

**Troisième raison : le besoin souple existe, mais je le couvre déjà.** Les mappings de codes changent d'un client à l'autre, donc je les stocke en JSON. PostgreSQL sait le faire nativement. J'obtiens la souplesse d'une base documentaire sans avoir un second moteur à sauvegarder, surveiller et mettre à jour.

Là où le NoSQL deviendrait pertinent, c'est identifié : **Redis**, pour externaliser les sessions et les compteurs de limitation de débit, dès que le backend passera en plusieurs instances — un état partagé en mémoire ne scale pas horizontalement.

### 4.3 L'architecture en couches — 3 min

`[ÉCRAN] Schéma Handler → Service → Repository`

Sur l'organisation interne du code : côté Go, il y a plusieurs domaines métier — authentification, administration, applications, analyse, WebSocket — et chacun répète strictement le même triptyque `handler.go`, `service.go`, `repository.go`.

> ⚠️ Il existe un sixième dossier, `Macdos`, mais la fonctionnalité correspondante n'est plus au périmètre depuis le retrait de BF05. Ne le cite pas spontanément. Si on te demande pourquoi il est là : *« c'est un service hérité de l'outil autonome, qui n'a plus d'interface pour l'appeler — je l'ai sorti du périmètre annoncé plutôt que de le présenter comme livré. »*

Le **Handler** ne connaît que le HTTP : il parse la requête, valide les entrées, retourne la réponse. Il ne sait pas ce qu'est une table. Le **Service** porte la logique métier — c'est là que vivent les règles de gestion — et il est indépendant du transport HTTP. Le **Repository** est la seule couche qui parle à PostgreSQL.

Le point clé, c'est que le Service ne dépend pas d'un Repository concret : il dépend d'une **interface**. Concrètement, ça répond à trois besoins.

`[ÉCRAN] Les 3 bénéfices`

Tester sans base de données : en test, un mock remplace l'interface Repository, les tests d'authentification tournent en millisecondes, sans PostgreSQL. Changer de source de données : passer de PostgreSQL à une autre base n'impacterait que la couche Repository. Isoler les règles métier : les neuf règles de gestion vivent dans le Service, pas éparpillées dans les handlers HTTP.

Cette régularité a aussi un bénéfice humain : un développeur qui comprend un des six services les comprend tous. Ajouter un domaine, c'est appliquer un patron connu.

`[ÉCRAN] Les 3 subrouters`

Dernier point d'architecture, qui est aussi un point de sécurité : le routage est découpé en **trois sous-routeurs**. Le premier est public — connexion et déconnexion, sans aucun middleware d'authentification. Le deuxième regroupe les routes authentifiées, protégées par un middleware qui vérifie la session. Le troisième regroupe les routes d'administration, protégées par ce même middleware plus un second qui vérifie le statut d'administrateur.

L'intérêt de ce découpage : il rend l'oubli difficile. Impossible d'ajouter une route d'administration sans la placer dans le sous-routeur qui porte déjà les deux protections.

Sur la documentation d'API : côté Python, FastAPI génère automatiquement une spécification **OpenAPI 3.0** à partir des annotations de type, exposée en Swagger interactif, régénérée à chaque démarrage du service — la source unique de vérité, c'est le code, aucune dérive ne peut s'installer entre le code et sa documentation. Côté Go, la documentation est maintenue manuellement.

---

## 5. La réalisation — 7 min ⏱ 26:00 → 33:00

> ⚠️ Ne fais pas le tour de toutes les fonctionnalités. Deux modules suffisent — ils portent à eux seuls le métier, la concurrence et la sécurité.

`[ÉCRAN] Vue d'ensemble des modules, puis démo ou captures`

La réalisation a été organisée par module fonctionnel vertical plutôt que par couche technique : chaque module suit le même schéma — besoin, interface, backend, persistance, flux complet, extrait de code.

Deux modules, choisis parce qu'ils illustrent des problèmes techniques différents : le métier et le parsing d'abord, puis la concurrence et le contrôle d'accès.

### 5.1 Le traitement des tirages de caisse — 3 min

`[ÉCRAN] L'outil de conversion, en usage`

L'outil qui est à l'origine de tout, d'abord.

Le comptable dépose ses fichiers `.EDI` — plusieurs d'un coup, il n'a plus à les traiter un par un. Il lance le traitement. Il récupère un fichier Excel avec une feuille par restaurant.

`[ÉCRAN] Le flux, étape par étape`

Ce qui se passe derrière : l'API Python reçoit la requête et valide d'abord le format de l'identifiant utilisateur avec une expression régulière stricte d'UUID — rien n'est fait avant cette validation, j'y reviens dans la partie sécurité. Elle crée ensuite un répertoire de travail isolé pour cet utilisateur et y sauvegarde les fichiers. Puis elle boucle sur chaque fichier : parsing ligne à ligne pour en extraire les valeurs, détermination facture ou avoir — ce qui change le sens comptable de l'écriture —, et recherche **en base** du mapping de codes propre à cet utilisateur.

C'est exactement ce que l'itération 2 a changé. Au départ, ces codes étaient dans un fichier de configuration modifié manuellement. En utilisant l'outil, les comptables ont fait remonter que ça les rendait dépendants — chacun voulait retrouver ses propres codes. Ils ont été déplacés en base, par utilisateur, dans des colonnes JSON, avec une interface pour les gérer. Les comptables sont devenus autonomes sur ce point.

Enfin, l'API génère l'Excel et renvoie un lien de téléchargement. Un thread de nettoyage supprime les fichiers temporaires cinq minutes après — ces fichiers contiennent des données comptables de clients, ils n'ont aucune raison de rester sur le serveur.

`[ÉCRAN] Le fichier EDI d'origine et l'Excel produit`

Une difficulté à mentionner : les fichiers EDI réels présentaient des **encodages variables** — de l'ISO-8859-1 et de l'UTF-8 — et des segments optionnels. Il a fallu rendre le parsing tolérant à ces variations sans masquer les vraies erreurs de format, un équilibre plus subtil qu'il n'y paraît. Ce qui en ressort : confronter le code à de vrais jeux de données anonymisés, et non à des cas idéaux, fait émerger des bugs qu'on n'anticipe jamais sur le papier.

### 5.2 L'administration — 4 min

`[ÉCRAN] Le panneau d'administration`

Deuxième module : l'administration. C'est le poste de pilotage du portail, réservé au rôle Admin.

**Le premier volet, c'est la gestion des comptes.** Créer un utilisateur, modifier son rôle, le supprimer. À la création, le mot de passe est haché avant d'être enregistré — il n'existe jamais en clair, même dans les journaux.

**Le deuxième, c'est le catalogue d'applications.** L'administrateur ajoute une application au portail en renseignant son nom, son adresse, son icône et son groupe — comptabilité ou social. C'est ce qui permet d'intégrer un nouvel outil sans redéployer le portail : on l'ajoute par l'interface, il apparaît dans le catalogue.

**Le troisième, et c'est le cœur du système, c'est l'attribution des droits.** L'administrateur coche, utilisateur par utilisateur, les applications auxquelles il a accès. C'est là qu'est alimentée la table de couples dont je parlais en conception. Sans cochage, pas d'accès : l'application n'apparaît pas.

`[ÉCRAN] Le tableau de bord analytique`

**Le quatrième volet, c'est le tableau de bord.** Il répond directement au manque de visibilité identifié au départ : personne au cabinet ne savait quels outils servaient vraiment.

Chaque connexion et chaque ouverture d'application enregistre un événement en base. Le tableau de bord les agrège et affiche trois choses.

D'abord **les connexions dans le temps**, jour par jour, ce qui montre si le portail est réellement adopté ou seulement installé.

Ensuite **l'usage par application** : quels outils sont ouverts, et lesquels ne le sont jamais. C'est l'information la plus utile pour le cabinet — elle dit où investir, et ce qu'on peut arrêter de maintenir.

Et enfin **les heures de pointe**, qui indiquent quand une intervention de maintenance dérangerait le moins de monde.

`[ÉCRAN] Le bandeau de présence`

Un dernier élément dans ce panneau : **la liste des collègues connectés en ce moment**, mise à jour en direct. Techniquement, c'est du WebSocket — une connexion qui reste ouverte, où le serveur pousse l'information au lieu que le navigateur la redemande en boucle.

C'est ce module qui m'a valu le bug le plus intéressant du projet : plusieurs connexions simultanées écrivaient dans la même liste en mémoire, ce qui provoquait un comportement imprévisible. Invisible en développement, il ne se serait manifesté qu'en production sous charge. Il a été trouvé par l'outil de détection intégré à Go et corrigé par un verrou. J'y reviens volontiers si ça vous intéresse.

`[ÉCRAN] Le contrôle d'accès admin`

Pour finir sur ce module, un point de sécurité.

Au moment où j'ai passé l'application au crible de l'**OWASP Top 10**, risque par risque, je me suis arrêté sur la première catégorie : le contrôle d'accès. Et je suis allé vérifier comment le mien était réellement appliqué.

Le constat : la vérification du rôle administrateur se faisait **côté navigateur**. Visuellement, tout était correct — l'interface n'apparaissait pas pour un non-administrateur. Mais le code du navigateur tourne sur la machine de l'utilisateur : il suffisait d'appeler l'API directement, sans passer par l'interface, pour contourner la vérification.

C'est le type même de faille qu'on ne voit pas en testant l'application normalement, parce que rien ne dysfonctionne. Je l'ai corrigée en déplaçant le contrôle côté serveur : le statut d'administrateur est désormais vérifié **en base à chaque requête**, et l'interface ne sert plus qu'au confort d'affichage.

C'est ce passage en revue qui a ancré un réflexe pour le reste du projet : **ne jamais faire confiance au client**.

Même logique pour le catalogue : le filtrage est fait en base. Le navigateur ne reçoit jamais la liste complète des applications pour en cacher une partie — il reçoit uniquement celles auxquelles l'utilisateur a droit.

> ⚠️ Le WebSocket est devenu anecdotique, c'est voulu : la présence temps réel est un détail du panneau, pas un module. Mais garde la version complète en tête — goroutines, data race, `go test -race`, `sync.RWMutex`, verrou en lecture parallélisable. La phrase « j'y reviens volontiers » est une invitation : il y a de bonnes chances qu'on la saisisse.

---

## 6. La sécurité — 5 min ⏱ 33:00 → 38:00

`[ÉCRAN] Les axes de sécurité`

La sécurité a été traitée comme un axe transversal, pris en compte dès la conception — *security by design* — plutôt que comme une couche ajoutée à la fin. À l'itération 5, il est d'ailleurs apparu que certaines mesures — l'externalisation des secrets, le paramétrage des requêtes SQL — auraient dû être intégrées dès les premières itérations plutôt qu'ajoutées après coup.

### 6.1 L'authentification — 1 min 30

Les mots de passe ne sont jamais stockés. Ce qui est enregistré, c'est une empreinte calculée par **bcrypt** — impossible à inverser. Et bcrypt est **volontairement lent** : c'est ce qui rend une attaque par essais massifs impraticable, là où un algorithme rapide se casse en quelques heures sur une carte graphique.

Pour les sessions, j'ai pris le contre-pied de ce qui se fait souvent. Beaucoup utilisent des jetons JWT, qui contiennent eux-mêmes l'information et évitent d'interroger la base. C'est efficace, mais ça a un défaut : **une fois émis, un JWT reste valide jusqu'à son expiration. On ne peut pas le rappeler.**

Or dans un cabinet, on peut avoir besoin de couper l'accès à quelqu'un immédiatement. J'ai donc gardé des sessions classiques : un jeton sans signification stocké en base, vérifié à chaque requête. Pour couper un accès, il suffit de supprimer la ligne — la requête suivante est refusée.

Ça coûte une lecture en base par requête. À l'échelle de quarante personnes, c'est indolore. J'ai échangé de la performance dont je n'ai pas besoin contre du contrôle dont j'ai besoin.

Les sessions expirent au bout de vingt-quatre heures, et un nettoyage automatique passe toutes les six heures.

### 6.2 Le contrôle d'accès — 1 min

`[ÉCRAN] Les 3 niveaux de vérification`

Les droits sont vérifiés à **trois endroits**, et c'est volontaire.

Le navigateur masque ce à quoi l'utilisateur n'a pas droit — mais ce n'est **pas** une sécurité, seulement du confort d'affichage. La vraie barrière est côté serveur : à chaque requête, on vérifie en base que la session est valide, puis que l'utilisateur a bien le rôle requis. Et l'API de traitement de fichiers refait sa propre vérification avant de toucher au moindre fichier.

Trois barrières indépendantes : si l'une tombe, les autres tiennent.

### 6.3 Les menaces analysées — 2 min

`[ÉCRAN] Extrait du tableau STRIDE`

Plutôt que de me contenter de cocher les cases de l'OWASP Top 10 — que j'ai bien sûr passé en revue, risque par risque —, j'ai conduit une analyse de menaces par surface d'exposition, en m'inspirant du modèle **STRIDE**. En voici trois exemples.

**Sur l'authentification.** La menace principale, c'est l'usurpation par force brute : bcrypt, lent par conception, est déjà une défense, complétée par une limitation de débit en **token bucket** — cinq essais, puis un jeton régénéré toutes les trente secondes. J'ai aussi traité une menace plus subtile : **l'énumération de comptes**. Si mon message d'erreur distinguait « email inconnu » de « mot de passe incorrect », un attaquant pourrait cartographier les comptes existants. Le message d'erreur est donc **générique et unique**, quelle que soit la cause de l'échec. Sur le déni de service : comme bcrypt est coûteux en CPU, un attaquant pourrait saturer le serveur en le sollicitant — d'où une réponse **429 renvoyée avant tout calcul bcrypt**.

**Sur le traitement de fichiers.** La menace, c'est le **path traversal** : forger un identifiant permettant de sortir du répertoire de travail et lire ou écrire ailleurs sur le serveur. C'est pour ça que la validation par expression régulière UUID intervient **avant toute construction de chemin**. Et côté Go, sur les noms de fichiers uploadés, je supprime toute composante de chemin avec `filepath.Base`. Le nettoyage automatique à cinq minutes répond, lui, au risque de saturation du disque par upload massif.

**Sur le WebSocket.** La menace s'appelle le **Cross-Site WebSocket Hijacking**. Le point piégeux, c'est que le handshake WebSocket **n'est pas soumis à la politique de même origine** du navigateur : un site malveillant peut ouvrir une connexion vers mon serveur en réutilisant le cookie de la victime. La parade est une **liste blanche d'origines, évaluée à chaque tentative d'upgrade** : toute connexion dont l'en-tête `Origin` n'y figure pas est rejetée.

> ⚠️ Bloc volontairement technique, contrairement au reste du script. C'est ici que le vocabulaire précis sert : il montre que l'analyse a été menée, pas récitée.

### 6.4 Ce qui reste à faire — 30 s

`[ÉCRAN] Les points identifiés`

Plusieurs points restent ouverts. La limite du nombre de tentatives de connexion est définie mais pas encore active en production. Les en-têtes de sécurité du navigateur sont spécifiés, il reste à les déployer. L'enregistrement des tentatives de connexion échouées et une politique de mot de passe plus stricte sont à faire.

Ce sont des points identifiés et classés par priorité, pas des angles morts.

> ⚠️ Ce passage vaut la peine d'être dit : ces points seront de toute façon visibles en creusant le dossier. Les nommer soi-même change la perception. **Ne le supprime pas pour gagner du temps.**

---

## 7. Les tests — 1 min 30 ⏱ 38:00 → 39:30

`[ÉCRAN] Pyramide des tests + les chiffres`

Sur les tests, j'ai suivi la logique classique : beaucoup de petits tests rapides qui vérifient une fonction isolée, et moins de tests qui font travailler plusieurs morceaux ensemble.

Aujourd'hui, à chaque envoi de code, la chaîne d'intégration lance automatiquement **84 tests côté API Python**, **29 côté interface**, et les tests du backend Go — dont un mode spécial qui détecte les problèmes de concurrence.

Ces tests tournent **sans base de données à installer** : l'application bascule sur une base légère en mémoire le temps des tests. C'est ce qui permet de les exécuter n'importe où, y compris sur le serveur d'intégration.

Il manque un étage : les tests qui simulent un utilisateur dans un vrai navigateur, du clic jusqu'au résultat. L'outil est choisi, les scénarios sont écrits, le déclencheur automatique est prêt — **mais ces tests ne sont pas encore développés.** Je ne les présente pas comme livrés.

En complément, je repasse manuellement les parcours principaux avant chaque mise en production, avec de vrais fichiers de caisse anonymisés.

> ⚠️ Bloc simplifié. Ce que tu ne dis plus mais dois savoir : `testify` et `sqlmock`, `go test -race`, le remplacement de `psycopg2` au niveau de `sys.modules`, SQLite en mémoire, Playwright et ses quatre arguments contre Cypress. Et le chiffre réel : 72 des 84 tests Python passent aujourd'hui — vérifie avant de citer 84.

---

## 8. Le déploiement — 4 min ⏱ 39:30 → 43:30

`[ÉCRAN] Schéma d'infrastructure`

Dernier volet technique : la mise en production. C'est la partie qui a demandé le plus de montée en compétence, en partant de zéro connaissance sur le sujet, avec un serveur vierge et sans aide extérieure.

### 8.1 La conteneurisation — 1 min

Chaque service est conteneurisé avec Docker, en **build multi-étapes** : une première étape fait la compilation, avec tous les outils nécessaires ; une seconde ne récupère que l'artefact produit et le place dans une image minimale. Pour le frontend, compilation avec Node puis copie du résultat statique dans une image Nginx. Pour le backend, compilation avec l'image Go puis copie du seul binaire dans une image Alpine.

Le gain est double : des images beaucoup plus légères, donc des déploiements plus rapides ; et surtout une **surface d'attaque réduite**, puisque l'image finale ne contient ni compilateur, ni code source, ni outillage.

### 8.2 L'orchestration — 1 min 30

`[ÉCRAN] Les objets Kubernetes`

L'orchestration est assurée par **K3s**, une distribution allégée de Kubernetes adaptée à un serveur unique : l'API Kubernetes complète, sans le coût opérationnel d'un cluster complet.

Chaque service a son **Deployment**, qui gère les réplicas et permet les mises à jour progressives ; son **Service** en ClusterIP pour la communication interne ; et sa route d'entrée via une **IngressRoute Traefik**, qui fait office de reverse proxy et gère la terminaison HTTPS.

Les fichiers uploadés sont stockés sur des **volumes persistants** : un conteneur est éphémère par nature, et sans ça les fichiers disparaîtraient au premier redémarrage.

### 8.3 La chaîne CI/CD et l'exploitation — 1 min 30

`[ÉCRAN] Le pipeline`

La chaîne d'intégration et de déploiement continus tourne sur GitHub Actions. À chaque push sur `main` : les tests unitaires Go s'exécutent, l'image Docker est construite et poussée vers le registre, puis le cluster est mis à jour par connexion SSH et redéploiement progressif.

Le déploiement se fait en **mise à jour progressive** : les nouveaux conteneurs démarrent, on attend qu'ils soient prêts, et seulement ensuite les anciens sont retirés. Pas de coupure de service.

`[ÉCRAN] Rollback`

Le retour arrière a été prévu, parce qu'un déploiement rate toujours un jour. Quatre déclencheurs sont définis : une régression fonctionnelle détectée en production, un pic d'erreurs serveur au-delà du seuil d'alerte, une latence dégradée, ou l'échec d'une migration critique.

Kubernetes conserve l'historique des ReplicaSets : une seule commande ramène la version précédente, sans perte de données.

Une distinction importante : ça, c'est le rollback **applicatif**. Si le problème vient d'une migration de base de données, c'est un tout autre sujet — le code revient en arrière, mais les données non. D'où un choix de conception fait en amont : les migrations de schéma sont toujours **additives et compatibles avec la version précédente** — des colonnes nullables sont ajoutées, jamais supprimées directement. Ça permet de revenir à la version applicative précédente sans rollback du schéma, et toute suppression de colonne est différée d'au moins deux releases. En dernier recours, il reste la restauration depuis la sauvegarde quotidienne PostgreSQL.

Trois environnements : développement en local, préproduction, production. Le frontend sait à quelle API parler grâce à un fichier de configuration avec un aiguillage par environnement.

---

## 9. Les améliorations — 2 min ⏱ 43:30 → 45:30

`[ÉCRAN] Les améliorations, en deux colonnes`

Le projet est fonctionnel, déployé et utilisé. Je l'envisage comme une base évolutive plutôt que comme un produit fini, et j'ai classé ce qui reste à faire en **deux natures**, parce qu'elles ne se décident pas de la même façon.

**La première, c'est ce que j'appelle la dette assumée** : des choses identifiées, documentées, volontairement reportées. Elles ne rendent pas le produit plus riche — elles le rendent plus solide. Quatre points, dans cet ordre de priorité.

D'abord **fermer les points de sécurité** : rendre effective la limite de tentatives de connexion, déployer les en-têtes de sécurité du navigateur, et ajouter un jeton anti-CSRF sur les formulaires. C'est ce qui réduit le plus de risque pour le moins d'effort, donc c'est en premier.

Ensuite **terminer les tests de bout en bout** — l'étage qui manque aujourd'hui, celui qui simule un utilisateur dans un vrai navigateur.

Puis **introduire Redis**, pour sortir les sessions de la mémoire du serveur. C'est le prérequis technique si le portail devait tourner sur plusieurs instances.

Et enfin **le monitoring**, avec Prometheus et Grafana, pour ne plus découvrir un incident parce qu'un utilisateur appelle.

`[ÉCRAN] La colonne « nouvelle valeur »`

**La seconde nature, c'est la nouvelle valeur** : des notifications, un export de rapports en PDF, un tableau de bord personnalisable. Ce sont de vraies fonctionnalités, mais je ne les engage que si le besoin se confirme auprès des pôles. Les inscrire au dossier ne suffit pas à les justifier.

Et côté métier, la suite est surtout d'y ajouter de nouveaux outils. C'était le but de la centralisation dès le départ : chaque nouvel outil coûte désormais beaucoup moins cher à mettre à disposition, parce que l'authentification, les droits et le déploiement existent déjà.

**Ce que je retiens de cette liste, c'est la façon de la trier** : on ne fait pas tout, on fait ce qui réduit le plus de risque pour le moins d'effort.

---

## 10. Conclusion — 30 s ⏱ 45:30 → 46:00

`[ÉCRAN] Page de synthèse`

Ce projet est parti de comptables qui ressaisissaient des tickets de caisse à la main. Il a abouti à une plateforme conçue, développée, testée, déployée, et utilisée tous les jours au cabinet.

Merci de votre attention.

---

## Guide de coupe — pour tenir en 35 minutes

Si le temps imparti est plus court, coupe **dans cet ordre** :

| Priorité | Section | Gain |
|---|---|---|
| 1 | §4.2 Choix de technos — ne garder que PostgreSQL + l'argument NoSQL en une phrase | ~1 min 30 |
| 2 | §5.1 — supprimer le paragraphe sur les encodages EDI | ~40 s |
| 3 | §8.1 Conteneurisation — condenser en 30 s | ~30 s |
| 4 | §2.1 Objectifs — ne garder que les BF/BNF en chiffres, sans détail | ~1 min |
| 5 | §3.2 Maquettage — ne garder que **zoning** et **maquette abstraite**, les deux stades les moins évidents | ~40 s |
| 6 | §9 — ne garder que la colonne « dette assumée », sans la nouvelle valeur | ~45 s |
| 7 | §2.3 — condenser l'organisation en 3-4 phrases | ~1 min |
| 8 | §3.3 MLD — fusionner l'explication MLD directement dans le MPD | ~1 min |

**Ne coupe jamais :** la partie 1 (le problème), la §3.3 (modélisation des données — c'est le bloc le plus technique et le plus noté), la §4.3 (architecture en couches), la §5.2 (l'erreur de contrôle d'accès), la §6 (sécurité, surtout le 6.4) et la §9 sur les améliorations.

---

## Notes de préparation

**Avant la répétition**
- [ ] Construire le support visuel en suivant les repères `[ÉCRAN]` — environ 27 à 30 vues
- [ ] Vérifier que chaque `[ÉCRAN]` correspond à un visuel existant (`doc/schemas/`, `doc/mockups/`, `Mcd.png`, `MLD.png`, `UML.png`, le dictionnaire de données, ou les images du docx)
- [ ] Préparer le fichier `.EDI` d'exemple et l'Excel produit, imprimés, à montrer si on le demande
- [ ] Décider démo live ou captures — si c'est live, avoir **impérativement** un plan B en captures

**Pendant les répétitions**
- [ ] Chronométrer chaque partie séparément et noter les dérives
- [ ] Répéter à voix haute au moins deux fois en entier — la lecture silencieuse ment sur la durée
- [ ] Faire une répétition devant quelqu'un de non technique : s'il comprend la partie 1, elle est bonne
- [ ] Se réécouter une fois pour traquer les tics de langage qui trahissent une présentation d'examen plutôt qu'une présentation de projet : « j'anticipe votre question », « je veux vous montrer que… », « je préfère vous le dire plutôt que… ». Aucun de ces tours ne devrait apparaître.
- [ ] Répéter spécifiquement §3.3 (modélisation, la partie la plus dense) et §5.2 (l'erreur de contrôle d'accès) — ce sont les passages où l'on est tenté de bafouiller, et ce sont les plus payants

**Déjà corrigé dans le docx**
- [x] ~~Capture `CheckOrigin` en dur avec la coquille `cabinet-matini.fr`~~ — **18/08**, remplacée par une phrase renvoyant à l'annexe. Le script §6.3 est calé dessus.
- [x] ~~« Temps de développement estimé : » vide~~ — **22/08**, renseigné à **600 h**.
- [x] ~~BF05 « Configurer les fascicules McDonald's » sans réalisation~~ — **22/08**, retiré du tableau des besoins. Il ne reste plus que **12 BF**, renumérotés.
- [x] ~~`fascicule_mcdo` présentée comme « quatrième table » de l'outil de tirages~~ — **22/08**, § 7.4 repris : l'outil n'utilise que ses trois tables de mapping, et le volet configuration décrit les vraies routes de l'API Python.
- [x] ~~Entité `fascicule_mcdo` dans le dictionnaire de données~~ — **22/08**, retirée.
- [x] ~~Les deux images du § 7.4 montraient encore du code `fascicule_mcdo`~~ — **22/08**, remplacées : le flux « Comptable → GET /codes » et l'extrait `code_comptas()`. Vérifié dans le fichier.
- [x] ~~« ACID » retiré du dossier~~ — **suppression volontaire**, confirmée le 23/08. Le § 4.2 du script ne le cite plus : PostgreSQL y est justifié par le JSON natif et l'intégrité référentielle.
  ⚠️ Garde tout de même la définition en tête — « que veut dire ACID ? » reste une question de jury possible même si le mot n'est plus écrit. Voir `REVISION_CONCEPTION.md`, question 36.

**Reste à corriger avant impression**
- [ ] **BF05 (ex-BF06) « Authentification sécurisée (JWT) »** contredit toujours la réalisation (« pas de JWT côté client ») — et ce script défend explicitement la session serveur contre le JWT. **Priorité 1.**
- [ ] **Tous les renvois BF du chapitre Réalisation sont faux**, et la renumérotation les a décalés d'un cran de plus. Voir le tableau ci-dessous.
- [ ] **§ 7.4, phrase cassée** : « deux volets indissociables : le traitement des fichiers (conversion EDI → Excel) **et la façon dont les tickets sont convertis** ». Le second volet n'est plus nommé. Remplacer par « …et **le paramétrage des codes comptables (BF03, § 7.4.7), qui pilote** la façon dont les tickets… ».
- [ ] **§ 7.4, « et BF08 — configuration associée »** subsiste. BF08 est désormais « Attribution des applications par utilisateur ». Écrire simplement « (BF01 à BF04) ».
- [ ] **US19 « Configurer les fascicules McDonald's »** existe encore dans les user stories, et le **Périmètre fonctionnel** annonce toujours « Gestion de configurations : exemple de configuration pour un McDonald's ». À retirer aussi, sinon BF05 revient par la fenêtre.
- [ ] **Dates** : page de garde « Novembre 2024 - Septembre 2026 » vs « environ 6 mois (novembre 2024 - avril 2025) ». Le script dit « environ six mois ».
- [ ] **`/sys/register`** dans le tableau de rate limiting, et « l'utilisateur doit pouvoir s'inscrire » : l'inscription n'existe pas.
- [ ] **A10 SSRF marqué « non implémenté »** → « N/A / sans objet ».
- [ ] **« Cypress/Playwright »** en améliorations vs « Playwright plutôt que Cypress » au chapitre Tests.
- [ ] Coquilles : « **OSWAP** Top 10 » → OWASP ; « **thread** modeling » → threat modeling ; titre « **Planning et sprints** » → « Planning et itérations ».
- [ ] Coquilles introduites le 22/08 : « l'**outils** sollicite » → outil ; « sont **rattaché**  » → rattachées ; « user_**codes**_maps (code_**maps**) » → `user_code_maps (code_map)` ; « (**code_gen_aux**) » → `code_map_gen_aux` ; « POST **/ codes** » → `/codes` ; « **coté** API Python » → côté ; « fichier de **configurations** » → configuration ; « sans **migrations** de schéma » → migration ; « là **ou** elle a du sens » → où ; « handlers **http** » → HTTP ; « nommage )**.**Une migration » → espace manquante.

**Renvois BF du chapitre Réalisation — table de correction après renumérotation**

| Chapitre | Écrit aujourd'hui | Doit devenir |
|---|---|---|
| Authentification et session | « épic 1 (BF01) » | **BF05** |
| Panneau d'administration | « épic 2 (BF02) » | **BF06** |
| Tableau de bord analytique | « épic 2, BF05 / BF10 » | **BF09** |
| WebSocket — présence temps réel | « épic 4 (BF06) » | **BF10** |
| Outil de tirages de caisse | « BF01 à BF04, et BF08 » | **BF01 à BF04** |
| Volet configuration | « (BF03) » | **BF03** ✓ *déjà juste* |
| Thème (Dark mode) | « BF07 » | **BF11** |

*Rappel de la nouvelle numérotation : BF01–BF04 outil de caisse · BF05 authentification · BF06 rôles · BF07 catalogue · BF08 attribution · BF09 analytics · BF10 WebSocket · BF11 mode sombre · BF12 responsive.*

**À vérifier dans le code, pas dans le dossier**
- [ ] **La présence temps réel fonctionne-t-elle réellement sur `logiciel.cabinet-martini.fr` ?** L'allowlist WebSocket ne contient pas ce domaine (voir l'encadré Écarts ci-dessous). Si l'application tourne encore sur `preprod.azert.fr`, tout va bien ; sinon la fonctionnalité est cassée en production, et son échec est silencieux — le handshake est simplement refusé, sans erreur visible. **Vérifie-le avant l'oral** : si c'est confirmé cassé, ça peut s'ajouter à la liste des points ouverts du §6.4 ; si ça marche, n'en parle pas spontanément.

> ### ⚠️ Écarts entre le dossier et le code réel — à connaître, pas à réciter
> Ce script suit le dossier remis. Mais si une question descend au niveau de l'implémentation, il faut savoir où ça ne colle pas :
> - **Cookies.** Le dossier annonce un cookie de session `HttpOnly`, `Secure`, `SameSite=Strict`. Le code pose **deux** cookies (`sessionId`, `userId`), en `SameSite=Lax`, `Secure` conditionnel, **sans `HttpOnly`**.
> - **WebSocket.** Le tableau STRIDE annonce un `AuthMiddleware` avant l'upgrade ; le code monte `/ws` avec **seulement** la validation d'`Origin`. Le script ne revendique que la validation d'`Origin` — c'est volontaire, reste sur ce terrain.
> - **Routes.** Le dossier écrit `sys/ws` et `/sys/health` ; les routes réelles sont `/ws` et `/health`.
> - **Domaine de production absent de l'allowlist WebSocket.** La capture d'annexe montre le vrai code : `allowedOrigins` contient `https://preprod.azert.fr`, `localhost:3000` et `127.0.0.1:3000` — **pas `logiciel.cabinet-martini.fr`**. Comme `CheckOrigin` retourne `allowedOrigins[origin]`, une clé absente vaut `false` : le handshake est refusé depuis la production, et la liste étant en dur, aucune variable d'environnement ne peut le corriger (contrairement au CORS HTTP, configurable par `CORS_ORIGIN`).
>   Ce n'est **pas une erreur du dossier** — le corps du texte ne nomme aucun domaine —, mais l'annexe la photographie. Détection très improbable : il faudrait rapprocher cette capture du tableau Environnements situé bien plus loin.
>   **Si le sujet arrive, ne pas bricoler une réponse** : *« vous avez raison, c'est un défaut de configuration réel : l'allowlist WebSocket est en dur et n'a pas suivi le passage en production. Le correctif est de la rendre configurable par variable d'environnement, sur le modèle de ce qui est déjà fait pour le CORS HTTP. »* C'est une bonne réponse — elle montre une relecture réelle du code.
>
> Sur les autres points : *« le dossier décrit la cible spécifiée ; sur ce point précis l'implémentation actuelle est à X, et le correctif est identifié. »* Mieux vaut ça qu'une affirmation indéfendable.

**Le jour J**
- [ ] Arriver avec le dossier imprimé, marque-pages sur : dictionnaire de données, MCD, MLD, MPD, diagramme de classes, séquence auth, tableau OWASP, tableau STRIDE
- [ ] Avoir trois questions prêtes à poser en fin d'entretien
- [ ] Boire de l'eau avant, pas pendant

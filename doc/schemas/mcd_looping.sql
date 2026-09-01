-- =====================================================================
-- Portail Cabinet Martini — source d'import Looping
-- Régénère MCD, MLD et MPD de façon cohérente.
--
-- Remplace : doc/schemas/mcd.txt
-- Cible    : Looping (import « Générer un MCD depuis un script SQL »)
--
-- Conventions imposées par l'import Looping :
--   * clauses FOREIGN KEY explicites (pas de REFERENCES en ligne)
--   * TIMESTAMP simple (TIMESTAMPTZ n'est pas reconnu)
--   * aucun INSERT de seed, aucune fonction, aucun index secondaire
--   * ordre de déclaration = ordre de résolution des clés étrangères
--
-- ---------------------------------------------------------------------
-- ÉCARTS VOLONTAIRES AVEC LE SCHÉMA DE PRODUCTION (3)
--
--   1. FOREIGN KEY sur applications.groups -> application_groups(name)
--      Matérialise l'association Application <-> Groupe, absente de
--      l'ancien MCD parce que la référence était faible (TEXT sans FK).
--
--   2. UNIQUE (user_id) sur les trois tables de paramétrage comptable
--      Traduit la règle métier « un seul paramétrage par utilisateur ».
--      Sans cette contrainte, Looping génère (0,n) au lieu de (0,1).
--
--   3. fascicule_mcdo absente
--      Entité isolée, sans aucune association. Retirée du conceptuel.
--      /!\ La table existe toujours en base et sert BF05 : ne jamais
--          la supprimer côté production. Voir doc/MCD_corrige.md.
--
--   Les écarts 1 et 2 sont rattrapables en base :
--   backend/internal/db/migrations/003_alignement_conceptuel.sql
-- =====================================================================


-- 1. Groupes d'applications -------------------------------------------
--    `name` est UNIQUE : c'est l'identifiant naturel au conceptuel.
CREATE TABLE application_groups (
    id          SERIAL      PRIMARY KEY,
    name        TEXT        UNIQUE NOT NULL,
    created_at  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);


-- 2. Utilisateurs ------------------------------------------------------
--    Double identifiant assumé : `id` sert les FK côté SQLAlchemy,
--    `uid` sert les FK côté Go et l'exposition au client.
CREATE TABLE users (
    id          SERIAL      PRIMARY KEY,
    uid         TEXT        UNIQUE NOT NULL,
    email       TEXT        UNIQUE NOT NULL,
    username    TEXT        UNIQUE NOT NULL,
    password    TEXT        NOT NULL,
    admin       BOOLEAN     NOT NULL,
    role        TEXT        DEFAULT 'user',
    entreprise  TEXT,
    last_seen   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);


-- 3. Applications ------------------------------------------------------
--    `groups` porte le libellé du groupe. La FK vers application_groups(name)
--    transforme l'ancienne référence faible en association réelle.
--    Colonne nullable => cardinalité (0,1) côté Application.
CREATE TABLE applications (
    id          SERIAL      PRIMARY KEY,
    name        TEXT        NOT NULL,
    base_url    TEXT        NOT NULL,
    icon_path   TEXT,
    groups      TEXT,
    FOREIGN KEY (groups) REFERENCES application_groups(name)
);


-- 4. Sessions ----------------------------------------------------------
--    Le jeton de session est lui-même la clé primaire : le middleware
--    d'authentification n'interroge cette table que par le jeton.
CREATE TABLE sessions (
    id          TEXT        PRIMARY KEY,
    user_id     TEXT        NOT NULL,
    created_at  TIMESTAMP   NOT NULL,
    expires_at  TIMESTAMP   NOT NULL,
    last_seen   TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(uid)
);


-- 5. Permissions utilisateur <-> application ---------------------------
--    Table de jonction N:N portant l'attribut `can_access`.
CREATE TABLE user_application_permissions (
    id              SERIAL      PRIMARY KEY,
    user_id         TEXT        NOT NULL,
    application_id  INTEGER     NOT NULL,
    can_access      BOOLEAN     DEFAULT FALSE,
    FOREIGN KEY (user_id)        REFERENCES users(uid),
    FOREIGN KEY (application_id) REFERENCES applications(id),
    UNIQUE (user_id, application_id)
);


-- 6. Événements d'analyse ----------------------------------------------
--    created_at est TIMESTAMPTZ en production (TIMESTAMP ici pour Looping).
CREATE TABLE events (
    id          SERIAL      PRIMARY KEY,
    api_name    TEXT,
    uid         TEXT        NOT NULL,
    conn_time   TEXT        NOT NULL,
    deco_time   TEXT        NOT NULL,
    day         TEXT        NOT NULL,
    created_at  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE
);


-- 7. Paramétrage comptable, par utilisateur ----------------------------
--    UNIQUE (user_id) => cardinalité (0,1) côté Utilisateur.
--    ON DELETE CASCADE => droit à l'oubli porté par le schéma.
CREATE TABLE user_code_maps (
    id          SERIAL      PRIMARY KEY,
    user_id     INTEGER     NOT NULL UNIQUE,
    code_map    JSON        NOT NULL DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE user_code_maps_gen_aux (
    id                  SERIAL      PRIMARY KEY,
    user_id             INTEGER     NOT NULL UNIQUE,
    code_map_gen_aux    JSON        NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE code_journal (
    id          SERIAL      PRIMARY KEY,
    user_id     INTEGER     NOT NULL UNIQUE,
    journal_map JSON        NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

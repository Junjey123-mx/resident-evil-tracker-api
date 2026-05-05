-- =============================================================================
-- Resident Evil Franchise Tracker — Official Database Schema
-- Engine: PostgreSQL
-- Scope: structural contract only; no seed data, no triggers, no functions
-- =============================================================================


-- -----------------------------------------------------------------------------
-- TABLE: series
-- Central table. Every other table references this one.
-- Represents one entry in the Resident Evil franchise archive.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS series (
    id                      SERIAL          PRIMARY KEY,

    -- Core identity
    title                   VARCHAR(255)    NOT NULL,
    alias_title             VARCHAR(255),
    release_year            SMALLINT        NOT NULL
                                CHECK (release_year BETWEEN 1996 AND 2026),
    main_protagonist        VARCHAR(100)    NOT NULL,
    original_platform       VARCHAR(100)    NOT NULL,
    registered_platforms    TEXT,           -- comma-separated or JSON string
    chronology_order        SMALLINT        NOT NULL
                                CHECK (chronology_order > 0),
    chronology_era          VARCHAR(100),

    -- Narrative & editorial
    description             TEXT            NOT NULL,
    category                VARCHAR(20)     NOT NULL
                                CHECK (category IN (
                                    'main_series', 'remake', 'prequel',
                                    'spin_off', 'expansion'
                                )),
    status                  VARCHAR(20)     NOT NULL
                                CHECK (status IN (
                                    'registered', 'pending', 'archived'
                                )),
    threat_level            VARCHAR(10)     NOT NULL
                                CHECK (threat_level IN (
                                    'low', 'medium', 'high', 'critical'
                                )),
    umbrella_classification VARCHAR(100),
    threat_type             VARCHAR(100),
    main_locations          TEXT,           -- comma-separated or JSON string

    -- Production metadata
    director                VARCHAR(100),
    developer               VARCHAR(100),
    genre                   VARCHAR(100),
    engine                  VARCHAR(100),

    -- Gameplay
    players                 SMALLINT        CHECK (players >= 1),
    estimated_duration      SMALLINT,       -- in minutes
    survival_index          SMALLINT        CHECK (survival_index BETWEEN 0 AND 100),

    -- Cover image (managed via Cloudinary)
    cover_image_url         TEXT,
    cover_image_public_id   TEXT,

    -- Audit timestamps
    created_at              TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);


-- -----------------------------------------------------------------------------
-- TABLE: ratings
-- Optional 1-to-1 personal rating per series entry.
-- Cascades on deletion so orphan ratings are never left behind.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ratings (
    id          SERIAL          PRIMARY KEY,

    -- One rating per game, enforced at DB level
    series_id   INTEGER         NOT NULL UNIQUE,

    score       NUMERIC(3, 1)   NOT NULL
                    CHECK (score BETWEEN 1 AND 10),
    review      VARCHAR(500),

    created_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_ratings_series
        FOREIGN KEY (series_id)
        REFERENCES series (id)
        ON DELETE CASCADE
);


-- -----------------------------------------------------------------------------
-- TABLE: activity_logs
-- Append-only audit trail for all user actions.
-- series_id is nullable so log entries survive series deletion (SET NULL).
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS activity_logs (
    id              SERIAL          PRIMARY KEY,

    -- Nullable FK: log survives even when the related series is deleted
    series_id       INTEGER,

    action          VARCHAR(30)     NOT NULL
                        CHECK (action IN (
                            'game_created',
                            'game_updated',
                            'game_deleted',
                            'rating_created',
                            'rating_updated',
                            'rating_deleted',
                            'cover_uploaded',
                            'cover_updated',
                            'archive_sync'
                        )),
    message         TEXT            NOT NULL,
    previous_value  TEXT,
    new_value       TEXT,

    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_activity_logs_series
        FOREIGN KEY (series_id)
        REFERENCES series (id)
        ON DELETE SET NULL
);


-- =============================================================================
-- INDEXES
-- Covers the most common query patterns expected in the application.
-- =============================================================================

-- series
CREATE INDEX IF NOT EXISTS idx_series_title
    ON series (title);

CREATE INDEX IF NOT EXISTS idx_series_release_year
    ON series (release_year);

CREATE INDEX IF NOT EXISTS idx_series_chronology_order
    ON series (chronology_order);

CREATE INDEX IF NOT EXISTS idx_series_category
    ON series (category);

CREATE INDEX IF NOT EXISTS idx_series_status
    ON series (status);

CREATE INDEX IF NOT EXISTS idx_series_threat_level
    ON series (threat_level);

CREATE INDEX IF NOT EXISTS idx_series_created_at
    ON series (created_at);

-- ratings
CREATE INDEX IF NOT EXISTS idx_ratings_series_id
    ON ratings (series_id);

CREATE INDEX IF NOT EXISTS idx_ratings_score
    ON ratings (score);

-- activity_logs
CREATE INDEX IF NOT EXISTS idx_activity_logs_series_id
    ON activity_logs (series_id);

CREATE INDEX IF NOT EXISTS idx_activity_logs_action
    ON activity_logs (action);

CREATE INDEX IF NOT EXISTS idx_activity_logs_created_at
    ON activity_logs (created_at);



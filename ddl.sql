CREATE TABLE data (
    dates DATE,
    ids TEXT PRIMARY KEY,
    names TEXT,
    monthly_listeners INTEGER,
    popularity INTEGER,
    followers INTEGER,
    genres JSONB,
    first_release CHAR(4),
    last_release CHAR(4),
    num_releases INTEGER,
    num_tracks INTEGER,
    playlists_found TEXT,
    feat_track_ids JSONB
);

CREATE TABLE data_reject (
    dates DATE,
    ids TEXT,
    names TEXT,
    monthly_listeners INTEGER,
    popularity INTEGER,
    followers INTEGER,
    genres JSONB,
    first_release CHAR(4),
    last_release CHAR(4),
    num_releases INTEGER,
    num_tracks INTEGER,
    playlists_found TEXT,
    feat_track_ids JSONB
);

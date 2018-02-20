CREATE USER narrative PASSWORD 'narrative1';
CREATE DATABASE narrative;
\c narrative;

CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE users (    
  id    TEXT          NOT NULL
);

CREATE TABLE clicks (
  time        TIMESTAMPTZ   NOT NULL,
  user_id     TEXT          NOT NULL
);
SELECT create_hypertable('clicks', 'time');

CREATE TABLE impressions (
  time        TIMESTAMPTZ   NOT NULL,
  user_id     TEXT          NOT NULL
);
SELECT create_hypertable('impressions', 'time');

GRANT ALL PRIVILEGES ON TABLE users TO narrative;
GRANT ALL PRIVILEGES ON TABLE clicks TO narrative;
GRANT ALL PRIVILEGES ON TABLE impressions TO narrative;

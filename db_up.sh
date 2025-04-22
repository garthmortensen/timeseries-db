#!/bin/bash
# db_up.sh

# exit on error
set -e

cat <<'EOF'
        _ _
      _| | |_       _ _ ___
     | . | . |     | | | . |
     |___|___|_____|___|  _|
             |_____|   |_|
EOF

echo "\nsetting up postgres container..."
docker compose up --detach

echo "waiting for container to start..."
until docker exec timeseries_db pg_isready --username=timeseriesuser --dbname=timeseriesdb; do
  sleep 2
done

# Optional: Only include if you have a seed.sql file
# echo "running seed/dml..."
# docker exec -i timeseries_db psql --username=timeseriesuser --dbname=timeseriesdb < seed.sql

echo "verifying database setup..."
docker exec -i timeseries_db psql --username=timeseriesuser --dbname=timeseriesdb -c "select count(*) from pipeline_runs;"

echo "database successfully set up!"

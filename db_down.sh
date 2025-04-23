#!/bin/bash
# db_down.sh

# exit on error
set -e

cat <<'EOF'
        _ _           _
      _| | |_       _| |___ _ _ _ ___
     | . | . |     | . | . | | | |   |
     |___|___|_____|___|___|_____|_|_|
             |_____|
EOF

echo "\ntearing down postgres container..."

# prod
# removing --volumes flag maintains persistence
# docker compose down

# dev
# Add --volumes back in when remaking db
docker compose down --volumes

echo "database successfully torn down!"

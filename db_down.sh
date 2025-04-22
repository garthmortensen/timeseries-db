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

docker compose down  # removing --volumes flag maintains persistence

echo "database successfully torn down!"

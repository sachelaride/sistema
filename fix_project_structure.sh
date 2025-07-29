#!/bin/bash

# Navigate to project root
cd /home/sachelaride/sistema_clinicas

# Remove extra directories
rm -rf sistema_clinicas/migrations
rm -rf sistema_clinicas/__pycache__
rm -rf clinica/__pycache__
rm -rf clinica/migrations/__pycache__
rm -rf clinica/templates/templates

# Ensure clinica/migrations/__init__.py exists
mkdir -p clinica/migrations
touch clinica/migrations/__init__.py

# Ensure management command structure
mkdir -p clinica/management/commands
touch clinica/management/__init__.py
touch clinica/management/commands/__init__.py

# Fix permissions
sudo chown -R sachelaride:sachelaride /home/sachelaride/sistema_clinicas
chmod -R 775 /home/sachelaride/sistema_clinicas

echo "Project structure corrected. Verify with 'tree /home/sachelaride/sistema_clinicas -L 2'"

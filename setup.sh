#!/bin/bash

echo "🔧 Mise à jour du système..."
apt update && apt upgrade -y
apt install -y nano git npm python3-pip curl wget unzip

echo "🐍 Installation des dépendances Python..."
pip install --upgrade pip
pip install -r /mnt/ASTRO/requirements.txt

echo "✅ Installation terminée !"

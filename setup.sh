#!/bin/bash

echo "🔧 Mise à jour du système..."
apt update && apt upgrade -y
apt install -y nano git npm python3-pip curl wget unzip

# Installation de tree pour voir la structure des fichiers
apt update && apt install -y tree


echo "🐍 Installation des dépendances Python..."
pip install --upgrade pip
pip install -r /mnt/ASTRO/requirements.txt

echo "✅ Installation terminée !"


#!/bin/bash

echo "🚀 Démarrage d'Astro..."

# 📌 Création du dossier de logs si inexistant
mkdir -p /mnt/user/ASTRO/logs

# 📌 Vérification et lancement de Redis
echo "📌 Vérification et lancement de Redis..."
docker exec astro_env bash -c "redis-cli ping" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "✅ Redis non détecté, lancement..."
    docker exec astro_env bash -c "redis-server --daemonize yes"
else
    echo "✅ Redis déjà en cours d'exécution"
fi

# 📌 Vérification et lancement de FastAPI
echo "📌 Lancement de FastAPI..."
docker exec astro_env bash -c "cd /mnt/ASTRO/backend && uvicorn main:app --host 0.0.0.0 --port 8100 --reload" > /mnt/user/ASTRO/logs/fastapi.log 2>&1 &

# 📌 Vérification et lancement du frontend Vite
echo "📌 Vérification et lancement du frontend Vite..."
docker exec astro_env bash -c "cd /mnt/ASTRO/astro-frontend && npm run dev -- --host 0.0.0.0" > /mnt/user/ASTRO/logs/vite.log 2>&1 &

# 📌 Attente du lancement de FastAPI avant de tester
echo "📌 Attente de FastAPI..."
sleep 5

# 📌 Test du serveur FastAPI
echo "📌 Test de FastAPI..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8100/ping)
if [ "$STATUS" -eq 200 ]; then
    echo "✅ FastAPI est en ligne !"
else
    echo "❌ FastAPI ne répond pas ! Vérifie les logs : /mnt/user/ASTRO/logs/fastapi.log"
fi

echo "✅ Tout est lancé ! 🚀"

# 📌 Afficher les logs en temps réel
echo "📌 Logs de FastAPI :"
tail -f /mnt/user/ASTRO/logs/fastapi.log &

echo "📌 Logs de Vite :"
tail -f /mnt/user/ASTRO/logs/vite.log &

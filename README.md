<<<<<<< HEAD
# ASTRO
Mon projet Astro
=======
# Documentation du projet ASTRO

## 1. Mise en place de l'environnement

### Pré-requis :
- Unraid installé et configuré avec Docker.
- Node.js et npm installés sur Unraid.

### Étapes d'installation :

1. **Cloner le dépôt Git** sur Unraid :
   ```bash
   git clone <repository_url> /mnt/user/ASTRO

Construire l'image Docker pour l'environnement :

bash
Copier
docker build -t astro_env_image .
Créer un conteneur Docker en utilisant l'image astro_env_image :

bash
Copier
docker run -dit --network host --name astro_env -v /mnt/user/ASTRO:/mnt/ASTRO astro_env_image
Accéder au conteneur et lancer Vite :

bash
Copier
docker exec -it astro_env sh
cd /mnt/ASTRO/astro-frontend
npm install
npm run dev -- --host

Construire l'image Docker pour l'environnement :

bash
Copier
docker build -t astro_env_image .
Créer un conteneur Docker en utilisant l'image astro_env_image :

bash
Copier
docker run -dit --network host --name astro_env -v /mnt/user/ASTRO:/mnt/ASTRO astro_env_image
Accéder au conteneur et lancer Vite :

bash
Copier
docker exec -it astro_env sh
cd /mnt/ASTRO/astro-frontend
npm install
npm run dev -- --host

>>>>>>> 496c02d (Suppression des fichiers et dossiers redondants)

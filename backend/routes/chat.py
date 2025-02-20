import os
import openai
import sqlite3
import redis
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# ✅ Charger les variables d'environnement depuis `/mnt/ASTRO/.env`
load_dotenv('/mnt/ASTRO/.env')
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

DB_PATH = "/mnt/ASTRO/astro_memory.db"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

class ChatRequest(BaseModel):
    user: str
    message: str

def init_db():
    """Créer la base de données et les tables si elles n'existent pas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table des messages normaux (historique de chat)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 📌 Nouvelle table pour stocker la mémoire permanente
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permanent_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def save_permanent_memory(user, key, value):
    """Ajoute ou met à jour une information permanente pour un utilisateur"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO permanent_memory (user, key, value) 
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    ''', (user, key, value))

    conn.commit()
    conn.close()

def get_permanent_memory(user):
    """Récupère toutes les informations permanentes d’un utilisateur"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT key, value FROM permanent_memory WHERE user = ?', (user,))
    memories = cursor.fetchall()
    
    conn.close()
    
    return {mem[0]: mem[1] for mem in memories}  # 🔹 Retourne un dictionnaire clé/valeur

def get_permanent_memory(user):
    """Récupère toutes les informations permanentes d’un utilisateur"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT key, value FROM permanent_memory WHERE user = ?', (user,))
    memories = cursor.fetchall()
    
    conn.close()
    
    return {mem[0]: mem[1] for mem in memories}  # 🔹 Retourne un dictionnaire clé/valeur

def delete_permanent_memory(user, key):
    """Supprime une information spécifique de la mémoire permanente et purge la mémoire courte"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Supprimer l'information en mémoire permanente (SQLite)
    cursor.execute('DELETE FROM permanent_memory WHERE user = ? AND key = ?', (user, key))
    conn.commit()
    conn.close()

    # Supprimer aussi la mémoire courte (Redis)
    redis_client.delete(f"chat_history:{user}")

def save_message(user, message, response):
    """Enregistrer un échange utilisateur dans la mémoire longue durée"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_memory (user, message, response) VALUES (?, ?, ?)", (user, message, response))
    conn.commit()
    conn.close()

def get_last_messages(user, limit=5):
    """Récupérer les derniers messages depuis SQLite (mémoire longue)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT message, response FROM chat_memory WHERE user = ? ORDER BY timestamp DESC LIMIT ?", (user, limit))
    messages = cursor.fetchall()
    conn.close()

    # Construction de l'historique en sens chronologique (du plus ancien au plus récent)
    messages = messages[::-1]
    
    history = []
    for msg in messages:
        history.append({"role": "user", "content": msg[0]})
        history.append({"role": "assistant", "content": msg[1]})
    return history

def store_short_term_memory(user, message, response):
    """Stocker les échanges courts en Redis"""
    key = f"chat_history:{user}"
    redis_client.rpush(key, message)
    redis_client.rpush(key, response)
    redis_client.ltrim(key, -70, -1)  # Conserver seulement les 70 derniers éléments

def get_short_term_memory(user):
    """Récupérer les derniers échanges depuis Redis (mémoire courte)"""
    key = f"chat_history:{user}"
    messages = redis_client.lrange(key, 0, -1)

    # On parcourt par pas de 2 : [user_message, assistant_reply, user_message, assistant_reply, ...]
    history = []
    for i in range(0, len(messages), 2):
        user_msg = messages[i]
        assistant_msg = messages[i+1] if i+1 < len(messages) else ""
        history.append({"role": "user", "content": user_msg})
        history.append({"role": "assistant", "content": assistant_msg})
    return history

init_db()

@router.post("/")
async def chat_with_openai(request: ChatRequest):
    """
    Envoie un message à OpenAI et retourne la réponse du modèle GPT-4o 
    avec gestion de la mémoire courte (Redis), longue (SQLite) et permanente.
    """
    try:
        # ✅ Récupération de l'historique court + long
        short_term = get_short_term_memory(request.user)
        long_term = get_last_messages(request.user)
        history = short_term + long_term

        # ✅ Récupération de la mémoire permanente
        permanent_memory = get_permanent_memory(request.user)
        if permanent_memory:
            memory_string = "\n".join([f"{key}: {value}" for key, value in permanent_memory.items()])
            history.insert(0, {"role": "system", "content": f"Informations mémorisées :\n{memory_string}"})

        # ✅ Vérification des commandes utilisateur pour mémoire permanente
        if request.message.lower().startswith("mémorise ") or request.message.lower().startswith("souviens-toi "):
            parts = request.message.split(" ", 2)
            if len(parts) >= 3:
                key, value = parts[1], parts[2]
                save_permanent_memory(request.user, key, value)
                return {"response": f"✅ C'est noté ! Je me souviendrai que {key} est {value}."}
            else:
                return {"response": "❌ Format incorrect. Exemple : 'Mémorise prénom Paul'."}

        if request.message.lower().startswith("oublie "):
            key = request.message.split(" ", 1)[1]
            delete_permanent_memory(request.user, key)
            return {"response": f"✅ J'ai oublié {key}."}

        # ✅ Ajout du nouveau message
        history.append({"role": "user", "content": request.message})

        # ✅ Appel OpenAI (inchangé)
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=history,
            temperature=0.5
        )

        if not response.choices or not response.choices[0].message:
            raise HTTPException(status_code=500, detail="Réponse vide de l'API OpenAI.")

        reply = response.choices[0].message.content.strip()

        # ✅ Sauvegarde mémoire
        store_short_term_memory(request.user, request.message, reply)
        save_message(request.user, request.message, reply)

        return {"response": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur OpenAI: {str(e)}")

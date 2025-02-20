import React, { useState } from "react";

function App() {
  const [inputValue, setInputValue] = useState("");
  const [response, setResponse] = useState("");

async function sendMessage() {
  try {
    const res = await fetch("/api/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: inputValue }), // Envoie la commande tapée par l'utilisateur
    });

    if (!res.ok) {
      throw new Error("Erreur réseau");
    }

    const data = await res.json();
    setResponse(data.response); // On affiche la réponse du backend
  } catch (error) {
    console.error("Erreur lors de la connexion au serveur:", error);
    setResponse("Erreur de connexion au serveur");
  }
}

  return (
    <div style={{ padding: "1rem" }}>
      <h1>Astro Assistant - TEST</h1>
      <label>
        Ton message :
        <input
          type="text"
          placeholder="Écris ici"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          style={{ marginLeft: "0.5rem" }}
        />
      </label>
      <div style={{ marginTop: "1rem" }}>
        <button onClick={sendMessage}>Envoyer</button>
      </div>
      <p style={{ marginTop: "1rem" }}>
        <strong>Réponse :</strong> {response}
      </p>
    </div>
  );
}

export default App;

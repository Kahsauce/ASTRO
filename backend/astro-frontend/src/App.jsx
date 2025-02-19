import React, { useState } from "react";

function App() {
    const [message, setMessage] = useState("");
    const [response, setResponse] = useState("");

    const sendMessage = async () => {
        try {
	    const res = await fetch("https://astro.doctoral.fr/api/message", {  // Ajout de /api/
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            });

            if (!res.ok) {
                throw new Error(`Erreur réseau: ${res.statusText}`);
            }

            const data = await res.json();
            setResponse(data.response);
        } catch (error) {
            console.error("Erreur :", error);
            setResponse("Erreur lors de la connexion au serveur");
        }
    };

    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1>Astro Assistant - TEST</h1>
            <input 
                type="text" 
                value={message} 
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Écris un message"
            />
            <button onClick={sendMessage}>Envoyer</button>
            {response && <p>Réponse : {response}</p>}
        </div>
    );
}

export default App;

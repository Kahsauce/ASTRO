import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App"; // ⬅️ Assure-toi que `App.jsx` est bien importé !

ReactDOM.createRoot(document.getElementById("app")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

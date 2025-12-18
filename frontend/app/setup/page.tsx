// app/setup/page.tsx
"use client";
import axios from "axios";

export default function SetupPage() {
  const crearAdmin = async () => {
    try {
      // Registramos al administrador de soporte
      await axios.post("/api/auth/register", {
        email: "admin@soporte.com", // Puedes cambiar esto
        password: "admin123",        // Puedes cambiar esto
        role: "soporte"
      });
      alert("✅ Usuario de Soporte creado con éxito. Ahora borra este archivo.");
    } catch (error) {
      alert("❌ Error: El usuario ya existe o la base de datos no está lista.");
    }
  };

  return (
    <div className="p-20 text-center">
      <button 
        onClick={crearAdmin}
        className="bg-indigo-600 text-white p-4 rounded-xl font-bold"
      >
        Click aquí para crear Usuario Soporte Inicial
      </button>
    </div>
  );
}
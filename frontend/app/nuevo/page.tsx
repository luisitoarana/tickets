// app/nuevo/page.tsx
"use client";
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Link from "next/link";

const API_URL = "/api";


export default function NuevoTicket() {
  const router = useRouter();
  const [form, setForm] = useState({ asunto: "", mensajeInicial: "" });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await axios.post("/api/tickets", {
        asunto: form.asunto,
        mensaje_inicial: form.mensajeInicial,
      });

      router.push("/");
    } catch (error) {
      console.error(error);
      alert("Error creando ticket");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      {/* Fondo decorativo */}
      <div className="absolute inset-0 bg-slate-50 z-0">
         <div className="absolute inset-y-0 left-0 w-1/2 bg-gray-100 skew-x-12 transform origin-bottom-left opacity-30"></div>
      </div>

      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg z-10 overflow-hidden">
        <div className="bg-indigo-600 px-8 py-6">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Crear Nuevo Ticket
          </h2>
          <p className="text-indigo-200 text-sm mt-1">Completa la información para abrir una incidencia.</p>
        </div>
        
        <form onSubmit={handleSubmit} className="p-8 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Asunto</label>
            <input
              type="text"
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none text-gray-800 placeholder-gray-400 bg-gray-50 focus:bg-white"
              placeholder="Ej: Error en el servidor de correos"
              value={form.asunto}
              onChange={(e) => setForm({ ...form, asunto: e.target.value })}
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Mensaje Inicial</label>
            <textarea
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none h-40 resize-none text-gray-800 placeholder-gray-400 bg-gray-50 focus:bg-white"
              placeholder="Describe detalladamente el problema..."
              value={form.mensajeInicial}
              onChange={(e) => setForm({ ...form, mensajeInicial: e.target.value })}
              required
            ></textarea>
          </div>

          <div className="pt-4 flex flex-col gap-3">
            <button
              type="submit"
              disabled={loading}
              className={`w-full flex items-center justify-center py-3.5 px-4 rounded-lg text-white font-semibold shadow-md transition-all duration-200 
                ${loading ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 hover:shadow-lg hover:-translate-y-0.5'}`}
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Enviando...
                </>
              ) : 'Crear Ticket'}
            </button>
            
            <Link 
              href="/" 
              className="w-full text-center py-3 px-4 rounded-lg text-gray-600 bg-white border border-gray-200 hover:bg-gray-50 font-medium transition-colors"
            >
              Cancelar
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
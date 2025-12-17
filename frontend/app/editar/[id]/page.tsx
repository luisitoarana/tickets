// app/editar/[id]/page.tsx
"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";

const API_URL = "/api";


interface TicketData {
  id: number;
  asunto: string;
  mensaje_inicial: string;
  estado: string;
  fecha: string;
}

export default function EditarTicket() {
  const router = useRouter();
  const params = useParams();
  const ticketId = params.id as string;

  const [form, setForm] = useState<TicketData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const cargarTicket = async () => {
      try {
        const res = await axios.get(
          `/api/tickets/${ticketId}`
        );
        setForm(res.data);
      } catch {
        alert("Error cargando ticket");
        router.push("/");
      } finally {
        setLoading(false);
      }
    };

    if (ticketId && ticketId !== "[id]") {
      cargarTicket();
    }
  }, [ticketId, router]);

  const handleSubmit = async () => {
    if (!form) return;
    setSaving(true);

    try {
      await axios.put(`/api/tickets/${ticketId}`, {
        asunto: form.asunto,
        mensaje_inicial: form.mensaje_inicial,
      });
      router.push("/");
    } catch {
      alert("Error actualizando ticket");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-indigo-600 font-semibold flex items-center gap-2">
          <svg className="animate-spin h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Cargando datos...
        </div>
      </div>
    );
  }

  if (!form) return null;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center pt-20 p-4">
      {/* Elemento de diseño de fondo */}
      <div className="absolute top-0 left-0 right-0 h-64 bg-indigo-600 transform -skew-y-2 origin-top-left -z-10"></div>

      <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg overflow-hidden relative">
        <div className="bg-white px-8 py-6 border-b border-gray-100">
           <div className="flex justify-between items-center">
             <div>
                <h2 className="text-2xl font-bold text-gray-800">Editar Ticket</h2>
                <p className="text-gray-500 text-sm">ID #{form.id}</p>
             </div>
             <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                form.estado === 'Abierto' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
             }`}>
               {form.estado}
             </span>
           </div>
        </div>

        <form className="p-8 space-y-6">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">Asunto</label>
            <div className="relative">
              <input
                type="text"
                className="w-full pl-4 pr-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all text-gray-800"
                value={form.asunto}
                onChange={(e) => setForm({ ...form, asunto: e.target.value })}
                required
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">Mensaje Inicial</label>
            <textarea
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all h-32 resize-none text-gray-800"
              value={form.mensaje_inicial}
              onChange={(e) => setForm({ ...form, mensaje_inicial: e.target.value })}
              required
            ></textarea>
          </div>

          <div className="pt-4 space-y-3">
            <button
              type="button"
              onClick={handleSubmit}
              disabled={saving}
              className={`w-full flex justify-center items-center py-3 px-4 rounded-lg text-white font-bold text-lg shadow-md transition-all 
                ${saving ? 'bg-emerald-400 cursor-not-allowed' : 'bg-emerald-500 hover:bg-emerald-600 hover:shadow-lg hover:-translate-y-0.5'}`}
            >
              {saving ? 'Guardando...' : 'Guardar Cambios'}
            </button>

            <button
              type="button"
              onClick={() => router.push('/')}
              className="w-full py-3 px-4 rounded-lg text-gray-600 font-semibold bg-gray-100 hover:bg-gray-200 transition-colors"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
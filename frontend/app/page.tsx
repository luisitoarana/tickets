"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import Link from "next/link";
import { useRouter } from "next/navigation";

interface Ticket {
  id: number;
  asunto: string;
  estado: string;
  fecha: string;
}

interface UserSession {
  userId: number;
  email: string;
  role: string;
}

export default function Home() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<UserSession | null>(null);
  const router = useRouter();

  useEffect(() => {
    const loggedUser = localStorage.getItem("user");
    if (!loggedUser) {
      router.push("/login");
    } else {
      const userData = JSON.parse(loggedUser);
      setUser(userData);
      cargarTickets();
    }
  }, [router]);

  const cargarTickets = async () => {
    try {
      setLoading(true);
      const res = await axios.get("/api/tickets");
      setTickets(res.data);
    } catch (error) {
      console.error("Error conectando al API:", error);
    } finally {
      setLoading(false);
    }
  };

  const eliminarTicket = async (ticketId: number) => {
    if (!confirm(`¿Estás seguro de eliminar el ticket #${ticketId}?`)) return;

    try {
      await axios.delete(`/api/tickets/${ticketId}`);
      setTickets(tickets.filter((t) => t.id !== ticketId));
    } catch (error) {
      console.error(error);
      alert("Error al eliminar ticket");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    router.push("/login");
  };

  return (
    <div className="min-h-screen bg-slate-50 relative overflow-hidden">
      {/* Fondo decorativo */}
      <div className="absolute top-0 left-0 w-full h-64 bg-gradient-to-r from-indigo-700 to-blue-600 transform -skew-y-3 origin-top-left -z-10 shadow-lg"></div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-20">
        
        {/* Barra Superior de Usuario */}
        <div className="flex justify-end mb-4 text-white">
          {user && (
            <div className="flex items-center gap-4 bg-black/20 px-4 py-2 rounded-full backdrop-blur-sm border border-white/10">
              <span className="text-sm">
                Conectado: <strong className="text-indigo-200">{user.email}</strong> 
                <span className="ml-2 px-2 py-0.5 bg-white/20 rounded text-[10px] uppercase tracking-wider font-black">
                  {user.role}
                </span>
              </span>
              <button 
                onClick={handleLogout}
                className="bg-red-500/80 hover:bg-red-600 px-3 py-1 rounded-lg text-xs font-bold transition-all shadow-sm active:scale-95"
              >
                Cerrar Sesión
              </button>
            </div>
          )}
        </div>

        {/* Encabezado Principal */}
        <div className="md:flex md:items-center md:justify-between mb-10">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tight text-white drop-shadow-md">
              Soporte Técnico
            </h1>
            <p className="mt-2 text-indigo-100 text-lg">Panel de control de incidencias.</p>
          </div>
          <div className="mt-4 md:mt-0">
            <Link
              href="/nuevo"
              className="inline-flex items-center px-6 py-3 border border-transparent shadow-lg text-base font-medium rounded-full text-indigo-600 bg-white hover:bg-indigo-50 transition-all duration-200 transform hover:scale-105 active:scale-95"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Nuevo Ticket
            </Link>
          </div>
        </div>

        {/* Contenedor de la Tabla */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
          {loading ? (
            <div className="p-20 text-center text-gray-500 animate-pulse font-medium">
              Cargando tickets...
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">ID</th>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Asunto</th>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Estado</th>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Fecha</th>
                    <th className="px-6 py-4 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Acciones</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {tickets.map((t) => (
                    <tr key={t.id} className="hover:bg-indigo-50/30 transition-colors duration-150">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">#{t.id}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-semibold text-gray-900">{t.asunto}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full border ${
                          t.estado === 'Abierto' 
                            ? 'bg-emerald-100 text-emerald-800 border-emerald-200' 
                            : 'bg-amber-100 text-amber-800 border-amber-200'
                        }`}>
                          {t.estado}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(t.fecha).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <div className="flex justify-end gap-3">
                          <Link
                            href={`/editar/${t.id}`}
                            className="text-indigo-600 hover:text-indigo-900 p-2 hover:bg-indigo-100 rounded-full transition-colors"
                            title="Editar"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                            </svg>
                          </Link>

                          {/* 🟢 El botón de eliminar solo se renderiza si el rol es soporte */}
                          {user?.role === "soporte" && (
                            <button
                              onClick={() => eliminarTicket(t.id)}
                              className="text-red-600 hover:text-red-900 p-2 hover:bg-red-100 rounded-full transition-colors active:scale-90"
                              title="Eliminar"
                            >
                              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 000-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                              </svg>
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                  {tickets.length === 0 && !loading && (
                    <tr>
                      <td colSpan={5} className="px-6 py-12 text-center text-gray-400 font-medium">
                        No hay tickets registrados
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
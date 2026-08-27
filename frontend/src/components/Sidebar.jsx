import { Link, useLocation, useNavigate } from "react-router-dom";

export default function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const menu = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: "🏠",
    },
    {
      name: "Memories",
      path: "/dashboard",
      icon: "🧠",
    },
    {
      name: "Settings",
      path: "/settings",
      icon: "⚙️",
    },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 min-h-screen text-white flex flex-col">

      <div className="p-6 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-cyan-400">
          🧠 AI Memory
        </h1>

        <p className="text-slate-400 text-sm mt-2">
          Personal Knowledge Base
        </p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {menu.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className={`flex items-center gap-3 p-3 rounded-lg transition ${
              location.pathname === item.path
                ? "bg-cyan-500 text-white"
                : "hover:bg-slate-800 text-slate-300"
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span>{item.name}</span>
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <button
          onClick={logout}
          className="w-full bg-red-500 hover:bg-red-600 transition rounded-lg py-3 font-semibold"
        >
          Logout
        </button>
      </div>

    </aside>
  );
}
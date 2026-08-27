import { useState } from "react";

export default function Navbar({ onSearch, onAdd }) {
  const [search, setSearch] = useState("");

  const handleSearch = () => {
    onSearch(search);
  };

  return (
    <header className="bg-slate-900 border-b border-slate-800 p-5 flex items-center justify-between">
      <div>
        <h2 className="text-2xl font-bold text-white">
          Dashboard
        </h2>

        <p className="text-slate-400 text-sm">
          Welcome to your AI Memory Platform
        </p>
      </div>

      <div className="flex items-center gap-4">

        <input
          type="text"
          placeholder="Search memories..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSearch();
          }}
          className="bg-slate-800 text-white px-4 py-2 rounded-lg w-72 border border-slate-700 focus:outline-none focus:border-cyan-500"
        />

        <button
          onClick={handleSearch}
          className="bg-green-500 hover:bg-green-600 px-5 py-2 rounded-lg text-white"
        >
          Search
        </button>

        <button
          onClick={onAdd}
          className="bg-cyan-500 hover:bg-cyan-600 px-5 py-2 rounded-lg text-white font-semibold"
        >
          + Add Memory
        </button>

      </div>
    </header>
  );
}
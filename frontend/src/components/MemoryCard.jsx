export default function MemoryCard({
  memory,
  onEdit,
  onDelete,
}) {
  const formatDate = (date) => {
    if (!date) return "";

    return new Date(date).toLocaleString();
  };

  return (
    <div className="bg-slate-900 rounded-xl border border-slate-800 shadow-lg hover:shadow-cyan-500/10 transition-all duration-300">

      <div className="p-5">

        <div className="flex items-center justify-between">

          <h2 className="text-lg font-bold text-cyan-400">
            Memory #{memory.id}
          </h2>

          <span className="text-xs text-slate-500">
            {formatDate(memory.created_at)}
          </span>

        </div>

        <p className="text-slate-300 mt-4 whitespace-pre-wrap break-words">
          {memory.content}
        </p>

      </div>

      <div className="border-t border-slate-800 px-5 py-4 flex justify-end gap-3">

        <button
          onClick={() => onEdit(memory)}
          className="px-4 py-2 rounded-lg bg-yellow-500 hover:bg-yellow-600 text-white font-medium transition"
        >
          ✏ Edit
        </button>

        <button
          onClick={() => onDelete(memory.id)}
          className="px-4 py-2 rounded-lg bg-red-500 hover:bg-red-600 text-white font-medium transition"
        >
          🗑 Delete
        </button>

      </div>

    </div>
  );
}
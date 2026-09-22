export default function MemoryCard({
  memory,
  onEdit,
  onDelete,
}) {
  const formatDate = (date) => {
    if (!date) return "";
    return new Date(date).toLocaleString();
  };

  const API_BASE_URL =
    import.meta.env.VITE_API_URL
      ? import.meta.env.VITE_API_URL.replace("/api", "")
      : "https://ai-memory-backend-8319.onrender.com";

  const getMediaUrl = (url) => {
    if (!url) return null;
    if (url.startsWith("http://") || url.startsWith("https://") || url.startsWith("data:")) {
      return url;
    }
    return `${API_BASE_URL}${url}`;
  };

  const isPdf =
    memory.image_url &&
    (memory.image_url.toLowerCase().endsWith(".pdf") ||
      memory.image_url.includes("application/pdf"));

  return (
    <div className="bg-slate-900 rounded-xl border border-slate-800 shadow-lg hover:shadow-cyan-500/10 transition-all duration-300 flex flex-col justify-between">

      <div className="p-5">

        <div className="flex items-center justify-between">

          <h2 className="text-lg font-bold text-cyan-400">
            Memory #{memory.id}
          </h2>

          <span className="text-xs text-slate-500">
            {formatDate(memory.created_at)}
          </span>

        </div>

        <p className="text-slate-300 mt-4 whitespace-pre-wrap break-words leading-relaxed">
          {memory.content}
        </p>

        {/* ATTACHED PDF OR PHOTO */}
        {memory.image_url && (
          <div className="mt-4">
            {isPdf ? (
              <a
                href={getMediaUrl(memory.image_url)}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3.5 bg-red-950/40 hover:bg-red-950/70 border border-red-800/60 hover:border-red-500 rounded-xl text-white group transition duration-200"
              >
                <div className="w-10 h-10 rounded-lg bg-red-600/20 border border-red-500/40 flex items-center justify-center text-xl group-hover:scale-110 transition-transform">
                  📄
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-sm truncate text-red-200">
                    {memory.image_name || "Attached PDF Document"}
                  </p>
                  <span className="text-xs text-red-400 font-medium flex items-center gap-1 mt-0.5">
                    Click to Open & View Entire PDF ↗
                  </span>
                </div>
              </a>
            ) : (
              <div className="rounded-xl overflow-hidden border border-slate-700 bg-slate-950 max-h-48 flex items-center justify-center">
                <img
                  src={getMediaUrl(memory.image_url)}
                  alt={memory.image_name || "Memory attachment"}
                  className="max-h-48 w-auto object-contain cursor-pointer hover:opacity-90 transition"
                  onClick={() => window.open(getMediaUrl(memory.image_url), "_blank")}
                />
              </div>
            )}
          </div>
        )}

      </div>

      <div className="border-t border-slate-800 px-5 py-4 flex justify-end gap-3">

        <button
          onClick={() => onEdit(memory)}
          className="px-4 py-2 rounded-lg bg-yellow-500 hover:bg-yellow-600 text-white font-medium transition text-sm"
        >
          ✏ Edit
        </button>

        <button
          onClick={() => onDelete(memory.id)}
          className="px-4 py-2 rounded-lg bg-red-500 hover:bg-red-600 text-white font-medium transition text-sm"
        >
          🗑 Delete
        </button>

      </div>

    </div>
  );
}
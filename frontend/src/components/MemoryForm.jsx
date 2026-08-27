import { useState } from "react";
import { createMemory } from "../services/memoryService";

export default function MemoryForm({ onMemoryCreated }) {
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);
  const [imageName, setImageName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!content.trim() && !image) {
      setError("Please enter a memory or select an image.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const newMemory = await createMemory(
        content,
        image,
        imageName
      );

      setContent("");
      setImage(null);
      setImageName("");

      // Reset file input
      const fileInput = document.getElementById("memory-image");
      if (fileInput) {
        fileInput.value = "";
      }

      if (onMemoryCreated) {
        onMemoryCreated(newMemory);
      }

    } catch (error) {
      console.error("Memory creation failed:", error);

      setError(
        error?.response?.data?.detail ||
        "Failed to create memory."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        backgroundColor: "#1e293b",
        padding: "20px",
        borderRadius: "12px",
        marginBottom: "20px",
        color: "white",
      }}
    >
      <h3
        style={{
          marginTop: 0,
          color: "#22d3ee",
        }}
      >
        🧠 Save a Memory
      </h3>

      <form onSubmit={handleSubmit}>

        {/* Memory text */}
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write your memory..."
          rows={4}
          style={{
            width: "100%",
            boxSizing: "border-box",
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #475569",
            backgroundColor: "#0f172a",
            color: "white",
            resize: "vertical",
            fontSize: "15px",
            marginBottom: "15px",
          }}
        />

        {/* Image */}
        <label
          htmlFor="memory-image"
          style={{
            display: "block",
            marginBottom: "8px",
            fontWeight: "bold",
          }}
        >
          📷 Select Photo
        </label>

        <input
          id="memory-image"
          type="file"
          accept="image/*"
          onChange={(e) => {
            const file = e.target.files[0];

            setImage(file || null);

            if (file && !imageName) {
              setImageName(file.name);
            }
          }}
          style={{
            width: "100%",
            marginBottom: "15px",
          }}
        />

        {/* Image name */}
        <input
          type="text"
          value={imageName}
          onChange={(e) => setImageName(e.target.value)}
          placeholder="Photo name"
          style={{
            width: "100%",
            boxSizing: "border-box",
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #475569",
            backgroundColor: "#0f172a",
            color: "white",
            fontSize: "15px",
            marginBottom: "15px",
          }}
        />

        {/* Preview */}
        {image && (
          <div style={{ marginBottom: "15px" }}>
            <img
              src={URL.createObjectURL(image)}
              alt="Preview"
              style={{
                maxWidth: "250px",
                maxHeight: "200px",
                borderRadius: "8px",
                objectFit: "cover",
              }}
            />
          </div>
        )}

        {/* Error */}
        {error && (
          <p
            style={{
              color: "#f87171",
              marginBottom: "15px",
            }}
          >
            {error}
          </p>
        )}

        {/* Save */}
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "12px 25px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: loading ? "#64748b" : "#06b6d4",
            color: "white",
            fontWeight: "bold",
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Saving..." : "Save Memory"}
        </button>
      </form>
    </div>
  );
}
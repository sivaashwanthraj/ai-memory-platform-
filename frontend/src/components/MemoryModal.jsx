import { useEffect, useState } from "react";


export default function MemoryModal({
  isOpen,
  onClose,
  onSave,
  editingMemory,
}) {

  const [content, setContent] = useState("");
  const [photo, setPhoto] = useState(null);
  const [photoName, setPhotoName] = useState("");


  // =========================================================
  // LOAD EDITING MEMORY
  // =========================================================

  useEffect(() => {

    if (editingMemory) {

      setContent(
        editingMemory.content || ""
      );

      setPhoto(null);

      setPhotoName(
        editingMemory.image_name || ""
      );

    } else {

      setContent("");

      setPhoto(null);

      setPhotoName("");

    }

  }, [editingMemory, isOpen]);


  if (!isOpen) {
    return null;
  }


  // =========================================================
  // SELECT PHOTO
  // =========================================================

  function handlePhotoChange(e) {

    const selectedFile =
      e.target.files?.[0] || null;

    setPhoto(selectedFile);

    if (selectedFile && !photoName.trim()) {
      const cleanName = selectedFile.name.replace(/\.[^/.]+$/, "");
      setPhotoName(cleanName);
    }

    console.log(
      "Selected file:",
      selectedFile
    );
  }


  // =========================================================
  // SUBMIT
  // =========================================================

  function handleSubmit(e) {

    e.preventDefault();


    // -------------------------------------------------------
    // TEXT MEMORY
    // -------------------------------------------------------

    if (
      !content.trim() &&
      !photo &&
      !editingMemory?.image_url
    ) {

      alert(
        "Please enter a memory or select a photo."
      );

      return;
    }


    // -------------------------------------------------------
    // PHOTO NAME
    // -------------------------------------------------------

    if (
      photo &&
      !photoName.trim()
    ) {

      alert(
        "Please enter a photo name."
      );

      return;
    }


    console.log(
      "Saving memory..."
    );

    console.log(
      "Content:",
      content
    );

    console.log(
      "Photo:",
      photo
    );

    console.log(
      "Photo name:",
      photoName
    );


    // -------------------------------------------------------
    // SEND TO DASHBOARD
    // -------------------------------------------------------

    onSave(
      content.trim(),
      photo,
      photoName.trim()
    );


    // -------------------------------------------------------
    // RESET
    // -------------------------------------------------------

    setContent("");
    setPhoto(null);
    setPhotoName("");
  }


  // =========================================================
  // CANCEL
  // =========================================================

  function handleClose() {

    setContent("");
    setPhoto(null);
    setPhotoName("");

    onClose();
  }


  // =========================================================
  // UI
  // =========================================================

  return (

    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">


      <div className="bg-slate-900 rounded-xl shadow-2xl w-full max-w-lg p-6">


        {/* =================================================
            TITLE
        ================================================= */}

        <h2 className="text-2xl font-bold text-cyan-400 mb-6">

          {editingMemory
            ? "Edit Memory"
            : "Add Memory"}

        </h2>


        <form onSubmit={handleSubmit}>


          {/* =================================================
              MEMORY TEXT
          ================================================= */}

          <label className="block text-white mb-2">

            Memory

          </label>


          <textarea
            rows={6}
            placeholder="Write your memory..."
            value={content}
            onChange={(e) =>
              setContent(e.target.value)
            }
            className="w-full bg-slate-800 border border-slate-700 rounded-lg p-4 text-white resize-none focus:outline-none focus:border-cyan-500"
          />


          {/* =================================================
              PHOTO OR DOCUMENT
          ================================================= */}

          {!editingMemory && (

            <>

              <label className="block text-white mt-5 mb-2">

                📷 Photo or 📄 Document (PDF)

              </label>


              <input
                type="file"
                accept="image/jpeg,image/png,image/jpg,image/webp,application/pdf,.pdf"
                onChange={handlePhotoChange}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-white file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-cyan-600 file:text-white hover:file:bg-cyan-500 cursor-pointer"
              />


              {/* SELECTED FILE */}

              {photo && (

                <div className="mt-2 flex items-center gap-2">

                  <span className="text-xl">
                    {photo.name.toLowerCase().endsWith(".pdf") ? "📄" : "🖼️"}
                  </span>

                  <p className="text-green-400 text-sm font-medium truncate">
                    ✓ Selected: {photo.name}
                  </p>

                </div>

              )}


              {/* =================================================
                  PHOTO OR DOCUMENT NAME
              ================================================= */}

              <label className="block text-white mt-5 mb-2">

                Name / Title

              </label>


              <input
                type="text"
                placeholder="Example: Internship Offer Letter or College ID"
                value={photoName}
                onChange={(e) =>
                  setPhotoName(e.target.value)
                }
                className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-cyan-500"
              />

            </>

          )}


          {/* =================================================
              BUTTONS
          ================================================= */}

          <div className="flex justify-end gap-3 mt-6">


            {/* CANCEL */}

            <button
              type="button"
              onClick={handleClose}
              className="px-5 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-white"
            >
              Cancel
            </button>


            {/* SAVE */}

            <button
              type="submit"
              className="px-5 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-600 text-white font-semibold"
            >

              {editingMemory
                ? "Update"
                : "Save"}

            </button>


          </div>


        </form>


      </div>

    </div>
  );
}
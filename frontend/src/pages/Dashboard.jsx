import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import MemoryCard from "../components/MemoryCard";
import MemoryModal from "../components/MemoryModal";

import {
  getMemories,
  createMemory,
  updateMemory,
  deleteMemory,
  searchMemories,
} from "../services/memoryService";


export default function Dashboard() {

  const navigate = useNavigate();

  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(true);

  const [modalOpen, setModalOpen] = useState(false);
  const [editingMemory, setEditingMemory] = useState(null);


  // =========================================================
  // LOAD MEMORIES
  // =========================================================

  useEffect(() => {
    loadMemories();
  }, []);


  async function loadMemories() {

    try {

      setLoading(true);

      const data = await getMemories();

      setMemories(data);

    } catch (error) {

      console.error(
        "Failed to load memories:",
        error
      );

      alert("Failed to load memories");

    } finally {

      setLoading(false);

    }
  }


  // =========================================================
  // SEARCH
  // =========================================================

  async function handleSearch(query) {

    try {

      if (!query.trim()) {

        await loadMemories();

        return;
      }

      setLoading(true);

      const results =
        await searchMemories(query);

      setMemories(results);

    } catch (error) {

      console.error(
        "Search failed:",
        error
      );

      alert("Search failed");

    } finally {

      setLoading(false);

    }
  }


  // =========================================================
  // OPEN ADD MODAL
  // =========================================================

  function openAddModal() {

    setEditingMemory(null);

    setModalOpen(true);
  }


  // =========================================================
  // OPEN EDIT MODAL
  // =========================================================

  function openEditModal(memory) {

    setEditingMemory(memory);

    setModalOpen(true);
  }


  // =========================================================
  // SAVE MEMORY
  // =========================================================

  async function handleSave(
    content,
    photo,
    photoName
  ) {

    try {

      console.log(
        "========== SAVE MEMORY =========="
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
        "Photo Name:",
        photoName
      );


      // -----------------------------------------------------
      // EDIT EXISTING MEMORY
      // -----------------------------------------------------

      if (editingMemory) {

        await updateMemory(
          editingMemory.id,
          content
        );

      }

      // -----------------------------------------------------
      // CREATE NEW MEMORY
      // -----------------------------------------------------

      else {

        await createMemory(
          content,
          photo,
          photoName
        );

      }


      // -----------------------------------------------------
      // Close modal
      // -----------------------------------------------------

      setModalOpen(false);

      setEditingMemory(null);


      // -----------------------------------------------------
      // Reload memories
      // -----------------------------------------------------

      await loadMemories();

    } catch (error) {

      console.error(
        "Failed to save memory:",
        error
      );

      console.error(
        "Response:",
        error.response
      );

      alert(
        error.response?.data?.detail ||
        "Failed to save memory"
      );
    }
  }


  // =========================================================
  // DELETE MEMORY
  // =========================================================

  async function handleDelete(id) {

    const ok = window.confirm(
      "Delete this memory?"
    );

    if (!ok) return;


    try {

      await deleteMemory(id);

      await loadMemories();

    } catch (error) {

      console.error(
        "Delete failed:",
        error
      );

      alert("Delete failed");
    }
  }


  // =========================================================
  // CLOSE MODAL
  // =========================================================

  function closeModal() {

    setModalOpen(false);

    setEditingMemory(null);
  }


  // =========================================================
  // UI
  // =========================================================

  return (

    <div className="flex min-h-screen bg-slate-950">

      {/* =====================================================
          SIDEBAR
      ===================================================== */}

      <Sidebar />


      <div className="flex-1 flex flex-col">


        {/* ===================================================
            NAVBAR
        =================================================== */}

        <Navbar
          onSearch={handleSearch}
          onAdd={openAddModal}
        />


        {/* ===================================================
            MAIN CONTENT
        =================================================== */}

        <div className="p-8">


          {/* =================================================
              HEADER
          ================================================= */}

          <div className="flex justify-between items-center mb-8">

            <h1 className="text-3xl font-bold text-white">
              My Memories
            </h1>


            <div className="flex gap-3">


              {/* CHATBOT BUTTON */}

              <button
                onClick={() =>
                  navigate("/chatbot")
                }
                className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg text-white font-semibold"
              >
                🤖 Chatbot
              </button>


              {/* ADD MEMORY BUTTON */}

              <button
                onClick={openAddModal}
                className="bg-cyan-500 hover:bg-cyan-600 px-6 py-3 rounded-lg text-white font-semibold"
              >
                + Add Memory
              </button>


            </div>

          </div>


          {/* =================================================
              LOADING
          ================================================= */}

          {loading ? (

            <div className="text-center text-slate-400 text-lg">
              Loading memories...
            </div>

          )


          /* =================================================
             EMPTY
          ================================================= */

          : memories.length === 0 ? (

            <div className="text-center text-slate-500 text-lg">
              No memories found.
            </div>

          )


          /* =================================================
             MEMORY CARDS
          ================================================= */

          : (

            <div className="grid gap-6">

              {memories.map((memory) => (

                <MemoryCard
                  key={memory.id}
                  memory={memory}
                  onEdit={openEditModal}
                  onDelete={handleDelete}
                />

              ))}

            </div>

          )}


        </div>


      </div>


      {/* =====================================================
          MEMORY MODAL
      ===================================================== */}

      <MemoryModal
        isOpen={modalOpen}
        onClose={closeModal}
        onSave={handleSave}
        editingMemory={editingMemory}
      />


    </div>
  );
}
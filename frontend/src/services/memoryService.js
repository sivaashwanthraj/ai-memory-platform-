import api from "./api";


// =========================================================
// GET ALL MEMORIES
// =========================================================

export const getMemories = async () => {
  console.log("Loading memories...");

  try {
    const response = await api.get("/memories/");

    console.log(
      "GET Success:",
      response.data
    );

    return response.data;

  } catch (error) {
    console.error(
      "GET Error:",
      error
    );

    console.error(
      "Response:",
      error.response?.data
    );

    throw error;
  }
};


// =========================================================
// GET ONE MEMORY
// =========================================================

export const getMemory = async (id) => {
  try {
    const response = await api.get(
      `/memories/${id}`
    );

    return response.data;

  } catch (error) {
    console.error(
      "GET ONE MEMORY Error:",
      error
    );

    throw error;
  }
};


// =========================================================
// CREATE MEMORY
//
// Supports:
// 1. Text only
// 2. Photo only
// 3. Text + Photo
// =========================================================

export const createMemory = async (
  content = "",
  photo = null,
  photoName = ""
) => {

  console.log(
    "========================================"
  );

  console.log(
    "CREATE MEMORY"
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

  console.log(
    "========================================"
  );


  // =======================================================
  // CREATE FORMDATA
  // =======================================================

  const formData = new FormData();


  // -------------------------------------------------------
  // Add memory content
  // -------------------------------------------------------

  formData.append(
    "content",
    content || ""
  );


  // -------------------------------------------------------
  // Add photo name
  // -------------------------------------------------------

  formData.append(
    "image_name",
    photoName || ""
  );


  // -------------------------------------------------------
  // Add photo if selected
  // -------------------------------------------------------

  if (photo) {

    console.log(
      "Photo selected:"
    );

    console.log(
      photo.name
    );

    formData.append(
      "image",
      photo
    );
  }


  // =======================================================
  // DEBUG
  // =======================================================

  console.log(
    "FormData content:",
    formData.get("content")
  );

  console.log(
    "FormData image_name:",
    formData.get("image_name")
  );

  console.log(
    "FormData image:",
    formData.get("image")
  );


  // =======================================================
  // SEND TO BACKEND
  //
  // IMPORTANT:
  //
  // DO NOT USE:
  // /memories/photo
  //
  // USE:
  // /memories/
  //
  // =======================================================

  try {

    console.log(
      "Sending POST request..."
    );

    console.log(
      "Endpoint: /memories/"
    );


    const response = await api.post(
      "/memories/",
      formData
    );


    console.log(
      "CREATE MEMORY SUCCESS:"
    );

    console.log(
      response.data
    );


    return response.data;

  } catch (error) {

    console.error(
      "CREATE MEMORY ERROR:",
      error
    );

    console.error(
      "Status:",
      error.response?.status
    );

    console.error(
      "Server response:",
      error.response?.data
    );

    throw error;
  }
};


// =========================================================
// UPDATE MEMORY
// =========================================================

export const updateMemory = async (
  id,
  content
) => {

  try {

    const response = await api.put(
      `/memories/${id}`,
      {
        content: content,
      }
    );

    console.log(
      "UPDATE SUCCESS:",
      response.data
    );

    return response.data;

  } catch (error) {

    console.error(
      "Update error:",
      error
    );

    console.error(
      "Response:",
      error.response?.data
    );

    throw error;
  }
};


// =========================================================
// DELETE MEMORY
// =========================================================

export const deleteMemory = async (
  id
) => {

  try {

    const response = await api.delete(
      `/memories/${id}`
    );

    console.log(
      "DELETE SUCCESS"
    );

    return response.data;

  } catch (error) {

    console.error(
      "Delete error:",
      error
    );

    console.error(
      "Response:",
      error.response?.data
    );

    throw error;
  }
};


// =========================================================
// SEARCH MEMORIES
// =========================================================

export const searchMemories = async (
  query,
  limit = 5
) => {

  try {

    const response = await api.post(
      "/memories/search",
      {
        query: query,
        limit: limit,
      }
    );

    console.log(
      "SEARCH SUCCESS:",
      response.data
    );

    return response.data;

  } catch (error) {

    console.error(
      "Search error:",
      error
    );

    console.error(
      "Response:",
      error.response?.data
    );

    throw error;
  }
};
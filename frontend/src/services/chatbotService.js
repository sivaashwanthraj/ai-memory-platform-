// ============================================================
// FILE:
// frontend/src/services/chatbotService.js
// ============================================================

import api from "./api";


// ============================================================
// SEND MESSAGE TO CHATBOT
// ============================================================

export const sendMessage = async (message) => {

  try {

    console.log("==============================");
    console.log("CHATBOT SERVICE");
    console.log("MESSAGE:", message);
    console.log("==============================");


    // --------------------------------------------------------
    // Send request to FastAPI
    //
    // Frontend:
    // http://localhost:5173
    //
    // Backend:
    // http://127.0.0.1:8000
    //
    // api.js should contain the backend base URL.
    // --------------------------------------------------------

    const response = await api.post(
      "/chatbot/",
      {
        message: message,
      }
    );


    // --------------------------------------------------------
    // Log backend response
    // --------------------------------------------------------

    console.log(
      "CHATBOT API RESPONSE:",
      response.data
    );


    // --------------------------------------------------------
    // Return only the backend data
    // --------------------------------------------------------

    return response.data;

  } catch (error) {

    console.error(
      "CHATBOT SERVICE ERROR:",
      error
    );


    console.error(
      "CHATBOT BACKEND ERROR:",
      error.response?.data
    );


    throw error;

  }

};


// ============================================================
// OPTIONAL ALIAS
// ============================================================
// If another component imports `chatbot` instead of
// `sendMessage`, this will also work.
// ============================================================

export const chatbot = sendMessage;
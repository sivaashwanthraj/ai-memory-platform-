// ============================================================
// FILE:
// frontend/src/pages/Chatbot.jsx
// ============================================================

import React, { useEffect, useRef, useState } from "react";

import { sendMessage } from "../services/chatbotService";


// ============================================================
// FASTAPI BACKEND URL
// ============================================================

const API_BASE_URL = import.meta.env.VITE_API_URL
  ? import.meta.env.VITE_API_URL.replace(/\/api\/?$/, "")
  : "https://ai-memory-backend-8319.onrender.com";


// ============================================================
// CHATBOT COMPONENT
// ============================================================

export default function Chatbot() {

  // ----------------------------------------------------------
  // STATES
  // ----------------------------------------------------------

  const [messages, setMessages] = useState([]);

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);


  // ----------------------------------------------------------
  // REF
  // ----------------------------------------------------------

  const messagesEndRef = useRef(null);


  // ==========================================================
  // AUTO SCROLL TO BOTTOM
  // ==========================================================

  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages]);


  // ==========================================================
  // CONVERT BACKEND IMAGE PATH TO FULL URL
  // ==========================================================

  const getImageUrl = (imageUrl) => {

    if (!imageUrl) {
      return null;
    }


    // If backend already gives full URL
    if (
      imageUrl.startsWith("http://") ||
      imageUrl.startsWith("https://")
    ) {

      return imageUrl;

    }


    // Backend gives:
    // /uploads/memories/example.png
    //
    // Convert to:
    // http://127.0.0.1:8000/uploads/memories/example.png

    return `${API_BASE_URL}${imageUrl}`;

  };


  // ==========================================================
  // OPEN IMAGE IN NEW TAB
  // ==========================================================

  const openImage = (imageUrl) => {

    const fullUrl = getImageUrl(imageUrl);

    if (!fullUrl) {
      return;
    }

    console.log(
      "OPENING IMAGE:",
      fullUrl
    );

    window.open(
      fullUrl,
      "_blank",
      "noopener,noreferrer"
    );

  };


  // ==========================================================
  // SEND MESSAGE
  // ==========================================================

  const handleSend = async () => {

    const text = input.trim();


    // Don't send empty message
    if (!text) {
      return;
    }


    // Don't send while loading
    if (loading) {
      return;
    }


    // --------------------------------------------------------
    // ADD USER MESSAGE
    // --------------------------------------------------------

    const userMessage = {

      id: Date.now(),

      type: "user",

      text: text,

    };


    setMessages((previousMessages) => [

      ...previousMessages,

      userMessage,

    ]);


    // Clear input

    setInput("");


    // Start loading

    setLoading(true);


    try {

      console.log(
        "=============================="
      );

      console.log(
        "CHATBOT REQUEST"
      );

      console.log(
        "MESSAGE:",
        text
      );

      console.log(
        "=============================="
      );


      // ------------------------------------------------------
      // CALL FASTAPI
      // ------------------------------------------------------

      const response = await sendMessage(text);


      console.log(
        "CHATBOT API RESPONSE:",
        response
      );


      // ------------------------------------------------------
      // GET ANSWER
      // ------------------------------------------------------

      const answer =
        response?.answer ||
        "I don't know because it isn't in my memory.";


      // ------------------------------------------------------
      // GET IMAGE URL
      // ------------------------------------------------------

      const imageUrl =
        response?.image_url || null;


      // ------------------------------------------------------
      // GET IMAGE NAME
      // ------------------------------------------------------

      const imageName =
        response?.image_name || null;


      console.log(
        "IMAGE URL FROM BACKEND:",
        imageUrl
      );


      console.log(
        "FULL IMAGE URL:",
        getImageUrl(imageUrl)
      );


      // ------------------------------------------------------
      // ADD AI MESSAGE
      // ------------------------------------------------------

      const aiMessage = {

        id: Date.now() + 1,

        type: "ai",

        text: answer,

        image_url: imageUrl,

        image_name: imageName,

      };


      setMessages((previousMessages) => [

        ...previousMessages,

        aiMessage,

      ]);

    } catch (error) {

      console.error(
        "CHATBOT ERROR:",
        error
      );


      console.error(
        "CHATBOT ERROR RESPONSE:",
        error?.response?.data
      );


      // ------------------------------------------------------
      // SHOW ERROR IN CHAT
      // ------------------------------------------------------

      const errorMessage = {

        id: Date.now() + 1,

        type: "ai",

        text:
          "Sorry, something went wrong while contacting the server.",

        image_url: null,

        image_name: null,

      };


      setMessages((previousMessages) => [

        ...previousMessages,

        errorMessage,

      ]);

    } finally {

      setLoading(false);

    }

  };


  // ==========================================================
  // ENTER KEY
  // ==========================================================

  const handleKeyDown = (event) => {

    if (event.key === "Enter") {

      event.preventDefault();

      handleSend();

    }

  };


  // ==========================================================
  // UI
  // ==========================================================

  return (

    <div className="min-h-screen bg-slate-950 text-white px-4 py-8">


      {/* ================================================== */}
      {/* MAIN CONTAINER */}
      {/* ================================================== */}

      <div className="max-w-5xl mx-auto">


        {/* ================================================== */}
        {/* HEADER */}
        {/* ================================================== */}

        <div className="text-center mb-8">

          <h1 className="text-3xl font-bold text-cyan-400">

            🤖 AI Memory Chatbot

          </h1>

          <p className="text-slate-400 mt-2">

            Ask questions about your saved memories

          </p>

        </div>


        {/* ================================================== */}
        {/* CHAT BOX */}
        {/* ================================================== */}

        <div
          className="
            bg-slate-900
            border
            border-slate-700
            rounded-2xl
            p-5
            min-h-[500px]
            max-h-[650px]
            overflow-y-auto
            shadow-2xl
          "
        >


          {/* ================================================= */}
          {/* EMPTY CHAT */}
          {/* ================================================= */}

          {messages.length === 0 && (

            <div
              className="
                min-h-[450px]
                flex
                items-center
                justify-center
              "
            >

              <div className="text-center">

                <div className="text-5xl mb-4">

                  🧠

                </div>

                <p className="text-slate-400 text-lg">

                  Ask something about your memories...

                </p>

              </div>

            </div>

          )}


          {/* ================================================= */}
          {/* MESSAGES */}
          {/* ================================================= */}

          {messages.map((message) => (

            <div
              key={message.id}
              className="mb-6"
            >


              {/* ================================================= */}
              {/* USER MESSAGE */}
              {/* ================================================= */}

              {message.type === "user" && (

                <div className="flex justify-end">

                  <div
                    className="
                      max-w-[80%]
                      bg-cyan-600
                      rounded-2xl
                      rounded-br-sm
                      px-5
                      py-4
                    "
                  >

                    <div
                      className="
                        text-sm
                        font-semibold
                        text-cyan-100
                        mb-2
                      "
                    >

                      You

                    </div>


                    <div className="text-white">

                      {message.text}

                    </div>

                  </div>

                </div>

              )}


              {/* ================================================= */}
              {/* AI MESSAGE */}
              {/* ================================================= */}

              {message.type === "ai" && (

                <div className="flex justify-start">

                  <div
                    className="
                      max-w-[90%]
                      bg-slate-700
                      rounded-2xl
                      rounded-bl-sm
                      px-5
                      py-4
                    "
                  >


                    {/* ----------------------------------------- */}
                    {/* AI LABEL */}
                    {/* ----------------------------------------- */}

                    <div
                      className="
                        text-sm
                        font-semibold
                        text-cyan-300
                        mb-2
                      "
                    >

                      AI

                    </div>


                    {/* ----------------------------------------- */}
                    {/* ANSWER */}
                    {/* ----------------------------------------- */}

                    <div
                      className="
                        text-white
                        text-base
                        leading-relaxed
                      "
                    >

                      {message.text}

                    </div>


                    {/* ================================================= */}
                    {/* IMAGE */}
                    {/* ================================================= */}

                    {message.image_url && (

                      <div className="mt-5">


                        {/* --------------------------------------------- */}
                        {/* IMAGE NAME */}
                        {/* --------------------------------------------- */}

                        {message.image_name && (

                          <div
                            className="
                              flex
                              items-center
                              gap-2
                              text-cyan-300
                              font-semibold
                              mb-3
                            "
                          >

                            <span className="text-xl">

                              🖼️

                            </span>

                            <span>

                              {message.image_name}

                            </span>

                          </div>

                        )}


                        {/* --------------------------------------------- */}
                        {/* IMAGE CONTAINER */}
                        {/* --------------------------------------------- */}

                        <div
                          className="
                            inline-block
                            bg-slate-800
                            p-2
                            rounded-xl
                            border
                            border-slate-600
                          "
                        >


                          {/* ------------------------------------------- */}
                          {/* MEMORY IMAGE */}
                          {/* ------------------------------------------- */}

                          <img

                            src={getImageUrl(
                              message.image_url
                            )}

                            alt={
                              message.image_name ||
                              "Memory"
                            }


                            // -----------------------------------------
                            // CLICK IMAGE
                            // -----------------------------------------

                            onClick={() => {

                              openImage(
                                message.image_url
                              );

                            }}


                            // -----------------------------------------
                            // IMAGE LOADED
                            // -----------------------------------------

                            onLoad={() => {

                              console.log(
                                "IMAGE LOADED SUCCESSFULLY:"
                              );

                              console.log(
                                getImageUrl(
                                  message.image_url
                                )
                              );

                            }}


                            // -----------------------------------------
                            // IMAGE ERROR
                            // -----------------------------------------

                            onError={(event) => {

                              console.error(
                                "IMAGE COULD NOT BE LOADED:"
                              );

                              console.error(
                                getImageUrl(
                                  message.image_url
                                )
                              );

                              console.error(
                                event.currentTarget
                              );

                            }}


                            className="
                              block
                              w-auto
                              max-w-full
                              max-h-[500px]
                              h-auto
                              rounded-lg
                              object-contain
                              cursor-pointer
                              hover:opacity-90
                              transition
                            "

                          />

                        </div>


                        {/* --------------------------------------------- */}
                        {/* CLICK MESSAGE */}
                        {/* --------------------------------------------- */}

                        <p
                          className="
                            text-xs
                            text-slate-400
                            mt-2
                          "
                        >

                          Click the image to open it in full size.

                        </p>

                      </div>

                    )}

                  </div>

                </div>

              )}

            </div>

          ))}


          {/* ================================================= */}
          {/* LOADING */}
          {/* ================================================= */}

          {loading && (

            <div className="flex justify-start mb-4">

              <div
                className="
                  bg-slate-700
                  rounded-2xl
                  px-5
                  py-4
                  text-slate-300
                "
              >

                <span>

                  AI is thinking...

                </span>

              </div>

            </div>

          )}


          {/* ================================================= */}
          {/* SCROLL TARGET */}
          {/* ================================================= */}

          <div ref={messagesEndRef} />

        </div>


        {/* ================================================== */}
        {/* INPUT AREA */}
        {/* ================================================== */}

        <div
          className="
            mt-5
            flex
            gap-3
          "
        >


          {/* ================================================= */}
          {/* INPUT */}
          {/* ================================================= */}

          <input

            type="text"

            value={input}

            onChange={(event) => {

              setInput(
                event.target.value
              );

            }}

            onKeyDown={handleKeyDown}

            disabled={loading}

            placeholder="Ask something..."

            autoComplete="off"

            className="
              flex-1
              px-5
              py-4
              rounded-xl
              bg-slate-800
              border
              border-slate-600
              text-white
              placeholder-slate-500
              focus:outline-none
              focus:border-cyan-400
              focus:ring-1
              focus:ring-cyan-400
              disabled:opacity-50
            "

          />


          {/* ================================================= */}
          {/* SEND BUTTON */}
          {/* ================================================= */}

          <button

            type="button"

            onClick={handleSend}

            disabled={
              loading ||
              !input.trim()
            }

            className="
              px-7
              py-4
              rounded-xl
              bg-cyan-500
              hover:bg-cyan-600
              text-white
              font-bold
              transition
              disabled:opacity-50
              disabled:cursor-not-allowed
            "

          >

            {loading
              ? "Sending..."
              : "Send"}

          </button>

        </div>


      </div>

    </div>

  );

}
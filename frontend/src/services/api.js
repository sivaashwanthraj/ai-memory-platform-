// ============================================================
// FILE:
// frontend/src/services/api.js
// ============================================================

import axios from "axios";


// ============================================================
// AXIOS INSTANCE
// ============================================================

const api = axios.create({

  baseURL:
    import.meta.env.VITE_API_URL ||
    "https://ai-memory-backend-8319.onrender.com/api",

  // IMPORTANT:
  // DO NOT set Content-Type here.
  //
  // Axios will automatically use:
  //
  // application/json
  //
  // for normal JSON requests and:
  //
  // multipart/form-data
  //
  // for FormData requests.
  //
});


// ============================================================
// ADD JWT TOKEN TO REQUESTS
// ============================================================

api.interceptors.request.use(

  (config) => {

    const token =
      localStorage.getItem("token");

    if (token) {

      config.headers.Authorization =
        `Bearer ${token}`;

    }

    return config;

  },

  (error) => {

    return Promise.reject(error);

  }

);


// ============================================================
// RESPONSE INTERCEPTOR
// ============================================================

api.interceptors.response.use(

  (response) => {

    return response;

  },

  (error) => {

    console.error(
      "API ERROR:",
      error.response?.status
    );

    console.error(
      "API URL:",
      error.config?.url
    );

    console.error(
      "API RESPONSE:",
      error.response?.data
    );

    return Promise.reject(error);

  }

);


// ============================================================
// EXPORT
// ============================================================

export default api;
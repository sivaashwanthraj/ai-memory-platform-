import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";

import { AuthContext } from "../context/AuthContext";
import { login as loginUser } from "../services/authService";

export default function Login() {
  const navigate = useNavigate();

  const { login } = useContext(AuthContext);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  // =========================================================
  // LOGIN
  // =========================================================

  const handleSubmit = async (e) => {
    e.preventDefault();

    // -------------------------------------------------------
    // Validate email
    // -------------------------------------------------------

    if (!email.trim()) {
      alert("Please enter your email.");
      return;
    }

    // -------------------------------------------------------
    // Validate password
    // -------------------------------------------------------

    if (!password.trim()) {
      alert("Please enter your password.");
      return;
    }

    try {
      setLoading(true);

      console.log("==============================");
      console.log("LOGIN START");
      console.log("==============================");

      console.log("EMAIL:", email);

      // -----------------------------------------------------
      // Call backend login
      // -----------------------------------------------------

      const response = await loginUser(
        email,
        password
      );

      console.log(
        "LOGIN RESPONSE:",
        response
      );

      // -----------------------------------------------------
      // Check access token
      // -----------------------------------------------------

      if (!response.access_token) {
        throw new Error(
          "Access token was not returned by the server."
        );
      }

      // -----------------------------------------------------
      // Save JWT token
      // -----------------------------------------------------

      localStorage.setItem(
        "token",
        response.access_token
      );

      console.log(
        "TOKEN SAVED"
      );

      // -----------------------------------------------------
      // Get current logged-in user
      // -----------------------------------------------------

      const userResponse =
        await fetch(
          "http://127.0.0.1:8000/api/auth/me",
          {
            method: "GET",

            headers: {
              Authorization:
                `Bearer ${response.access_token}`,

              "Content-Type":
                "application/json",
            },
          }
        );

      console.log(
        "CURRENT USER STATUS:",
        userResponse.status
      );

      // -----------------------------------------------------
      // Check current user response
      // -----------------------------------------------------

      if (!userResponse.ok) {
        throw new Error(
          "Unable to get current user."
        );
      }

      // -----------------------------------------------------
      // Convert response to JSON
      // -----------------------------------------------------

      const userData =
        await userResponse.json();

      console.log(
        "CURRENT USER:",
        userData
      );

      // -----------------------------------------------------
      // Update AuthContext
      // -----------------------------------------------------

      login(
        response.access_token,
        userData
      );

      console.log(
        "AUTH CONTEXT UPDATED"
      );

      // -----------------------------------------------------
      // Navigate to dashboard
      // -----------------------------------------------------

      console.log(
        "NAVIGATING TO DASHBOARD..."
      );

      navigate("/dashboard");

    } catch (error) {

      // =====================================================
      // ERROR HANDLING
      // =====================================================

      console.error(
        "=============================="
      );

      console.error(
        "LOGIN ERROR"
      );

      console.error(
        "=============================="
      );

      console.error(
        "ERROR:",
        error
      );

      console.error(
        "STATUS:",
        error.response?.status
      );

      console.error(
        "BACKEND RESPONSE:",
        error.response?.data
      );

      // -----------------------------------------------------
      // Remove invalid token
      // -----------------------------------------------------

      localStorage.removeItem(
        "token"
      );

      // -----------------------------------------------------
      // Get backend error
      // -----------------------------------------------------

      const detail =
        error.response?.data?.detail;

      // =====================================================
      // FASTAPI 422 VALIDATION ERROR
      // =====================================================

      if (Array.isArray(detail)) {

        const messages =
          detail.map((item) => {

            const field =
              Array.isArray(item.loc)
                ? item.loc.join(" → ")
                : "field";

            return `${field}: ${item.msg}`;
          });

        alert(
          messages.join("\n")
        );

      }

      // =====================================================
      // NORMAL BACKEND ERROR
      // =====================================================

      else if (
        typeof detail === "string"
      ) {

        alert(detail);

      }

      // =====================================================
      // OBJECT ERROR
      // =====================================================

      else if (detail) {

        alert(
          JSON.stringify(
            detail,
            null,
            2
          )
        );

      }

      // =====================================================
      // JAVASCRIPT ERROR
      // =====================================================

      else if (
        error.message
      ) {

        alert(
          error.message
        );

      }

      // =====================================================
      // UNKNOWN ERROR
      // =====================================================

      else {

        alert(
          "Login failed. Please check your email and password."
        );

      }

    } finally {

      // -----------------------------------------------------
      // Stop loading
      // -----------------------------------------------------

      setLoading(false);
    }
  };


  // =========================================================
  // UI
  // =========================================================

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4">

      <div className="w-full max-w-md">

        {/* ================================================= */}
        {/* LOGIN CARD */}
        {/* ================================================= */}

        <div className="bg-slate-800 rounded-2xl shadow-2xl p-8">

          {/* =============================================== */}
          {/* TITLE */}
          {/* =============================================== */}

          <div className="text-center mb-8">

            <div className="text-5xl mb-4">
              🧠
            </div>

            <h1 className="text-3xl font-bold text-white">
              AI Memory Platform
            </h1>

            <p className="text-slate-400 mt-2">
              Sign in to your account
            </p>

          </div>


          {/* =============================================== */}
          {/* LOGIN FORM */}
          {/* =============================================== */}

          <form
            onSubmit={handleSubmit}
            className="space-y-6"
          >

            {/* ============================================= */}
            {/* EMAIL */}
            {/* ============================================= */}

            <div>

              <label className="block text-white font-medium mb-2">
                Email
              </label>

              <input
                type="email"
                value={email}
                placeholder="Enter your email"

                onChange={(e) =>
                  setEmail(e.target.value)
                }

                disabled={loading}

                autoComplete="email"

                className="
                  w-full
                  px-4
                  py-3
                  rounded-lg
                  bg-slate-700
                  border
                  border-slate-600
                  text-white
                  placeholder-slate-400
                  focus:outline-none
                  focus:border-cyan-400
                  focus:ring-1
                  focus:ring-cyan-400
                  disabled:opacity-50
                "
              />

            </div>


            {/* ============================================= */}
            {/* PASSWORD */}
            {/* ============================================= */}

            <div>

              <label className="block text-white font-medium mb-2">
                Password
              </label>

              <input
                type="password"
                value={password}
                placeholder="Enter your password"

                onChange={(e) =>
                  setPassword(e.target.value)
                }

                disabled={loading}

                autoComplete="current-password"

                className="
                  w-full
                  px-4
                  py-3
                  rounded-lg
                  bg-slate-700
                  border
                  border-slate-600
                  text-white
                  placeholder-slate-400
                  focus:outline-none
                  focus:border-cyan-400
                  focus:ring-1
                  focus:ring-cyan-400
                  disabled:opacity-50
                "
              />

            </div>


            {/* ============================================= */}
            {/* SIGN IN BUTTON */}
            {/* ============================================= */}

            <button
              type="submit"
              disabled={loading}

              className="
                w-full
                py-3
                rounded-lg
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
                ? "Signing In..."
                : "Sign In"}

            </button>

          </form>


          {/* =============================================== */}
          {/* REGISTER */}
          {/* =============================================== */}

          <div className="text-center mt-6">

            <p className="text-slate-400">

              Don't have an account?{" "}

              <button
                type="button"

                onClick={() =>
                  navigate("/register")
                }

                className="
                  text-cyan-400
                  hover:text-cyan-300
                  font-semibold
                "
              >
                Register
              </button>

            </p>

          </div>

        </div>

      </div>

    </div>
  );
}
import { createContext, useState, useEffect } from "react";
import * as authService from "../services/authService";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {

  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // =========================================================
  // CHECK EXISTING LOGIN
  // =========================================================

  useEffect(() => {

    const loadUser = async () => {

      const token =
        localStorage.getItem("token");

      // No token = not logged in
      if (!token) {

        setUser(null);
        setLoading(false);

        return;
      }

      try {

        console.log(
          "Checking existing login..."
        );

        const response =
          await authService.getCurrentUser();

        console.log(
          "Current user:",
          response.data
        );

        setUser(
          response.data
        );

      } catch (error) {

        console.error(
          "AUTH CHECK ERROR:",
          error
        );

        localStorage.removeItem(
          "token"
        );

        setUser(null);

      } finally {

        setLoading(false);

      }
    };

    loadUser();

  }, []);


  // =========================================================
  // LOGIN
  // =========================================================

  const login = (
    token,
    userData
  ) => {

    console.log(
      "Saving login..."
    );

    localStorage.setItem(
      "token",
      token
    );

    setUser(
      userData
    );
  };


  // =========================================================
  // LOGOUT
  // =========================================================

  const logout = () => {

    console.log(
      "Logging out..."
    );

    localStorage.removeItem(
      "token"
    );

    setUser(null);
  };


  // =========================================================
  // LOADING SCREEN
  // =========================================================

  if (loading) {

    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950">

        <div className="text-center">

          <div className="text-5xl mb-4">
            🧠
          </div>

          <h1 className="text-2xl font-bold text-white">
            AI Memory Platform
          </h1>

          <p className="text-slate-400 mt-2">
            Loading...
          </p>

        </div>

      </div>
    );
  }


  // =========================================================
  // PROVIDER
  // =========================================================

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
import { Navigate, Outlet } from "react-router-dom";
import { useContext } from "react";

import { AuthContext } from "../context/AuthContext";

export default function ProtectedRoute() {

  const { user, loading } =
    useContext(AuthContext);

  // ---------------------------------------------------------
  // Still checking authentication
  // ---------------------------------------------------------

  if (loading) {

    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950">

        <div className="text-white text-xl">
          Checking authentication...
        </div>

      </div>
    );
  }


  // ---------------------------------------------------------
  // Not logged in
  // ---------------------------------------------------------

  if (!user) {

    console.log(
      "ProtectedRoute: user not logged in"
    );

    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }


  // ---------------------------------------------------------
  // Logged in
  // ---------------------------------------------------------

  console.log(
    "ProtectedRoute: user authenticated"
  );

  return <Outlet />;
}
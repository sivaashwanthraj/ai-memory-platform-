import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "../pages/Login";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import MemoryDetails from "../pages/MemoryDetails";
import Chatbot from "../pages/Chatbot";

import ProtectedRoute from "./ProtectedRoute";


export default function AppRoutes() {

  return (

    <BrowserRouter>

      <Routes>

        {/* ================================================= */}
        {/* PUBLIC ROUTES */}
        {/* ================================================= */}

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />


        {/* ================================================= */}
        {/* PROTECTED ROUTES */}
        {/* ================================================= */}

        <Route element={<ProtectedRoute />}>

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          <Route
            path="/chatbot"
            element={<Chatbot />}
          />

          <Route
            path="/memory/:id"
            element={<MemoryDetails />}
          />

        </Route>


        {/* ================================================= */}
        {/* ROOT */}
        {/* ================================================= */}

        <Route
          path="/"
          element={
            <Navigate
              to="/login"
              replace
            />
          }
        />


        {/* ================================================= */}
        {/* UNKNOWN PAGE */}
        {/* ================================================= */}

        <Route
          path="*"
          element={
            <Navigate
              to="/login"
              replace
            />
          }
        />

      </Routes>

    </BrowserRouter>
  );
}
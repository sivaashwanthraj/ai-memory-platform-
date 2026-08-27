import api from "./api";

// =========================================================
// LOGIN
// =========================================================

export const login = async (email, password) => {

  const formData =
    new URLSearchParams();

  formData.append(
    "username",
    email.trim()
  );

  formData.append(
    "password",
    password
  );

  console.log(
    "LOGIN EMAIL:",
    email
  );

  console.log(
    "LOGIN FORM DATA:",
    formData.toString()
  );

  const response =
    await api.post(
      "/auth/login",
      formData,
      {
        headers: {
          "Content-Type":
            "application/x-www-form-urlencoded",
        },
      }
    );

  console.log(
    "LOGIN API RESPONSE:",
    response.data
  );

  return response.data;
};


// =========================================================
// REGISTER
// =========================================================

export const register = async (
  userData
) => {

  const response =
    await api.post(
      "/auth/register",
      userData
    );

  return response.data;
};


// =========================================================
// CURRENT USER
// =========================================================

export const getCurrentUser = async () => {

  const response =
    await api.get(
      "/auth/me"
    );

  return response;
};


// =========================================================
// LOGOUT
// =========================================================

export const logout = () => {

  localStorage.removeItem(
    "token"
  );
};
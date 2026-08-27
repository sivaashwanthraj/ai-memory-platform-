# AI Memory Platform - Deployment & Run Guide

## 🚀 Option 1: Easiest 1-Click Launch (Local)
Since you already have **PostgreSQL**, **Node.js**, **Python 3.11**, and **Ollama (`qwen3:4b`)** installed:

1. Simply double-click **`start.bat`** in `D:\AI-Memory-Platform`.
2. This will automatically:
   - Check and start Ollama in the background.
   - Start the FastAPI Backend on `http://127.0.0.1:8000`.
   - Start the Vite React Frontend on `http://localhost:5173`.
   - Open `http://localhost:5173` in your default browser.

---

## 🌐 Option 2: Cloud Deployment (Web Hosting)

### 1. Frontend (Vercel / Netlify - Free)
1. Push your `frontend` directory to a GitHub repository.
2. Go to [Vercel](https://vercel.com) or [Netlify](https://netlify.com) and click **Add New Project**.
3. Set the Root Directory to `frontend`.
4. Add the Environment Variable:
   - `VITE_API_URL`: Your deployed backend URL (e.g. `https://your-backend.onrender.com/api`).
5. Click **Deploy**.

### 2. Backend (Render / Railway / VPS)
1. **Database**: Use a free managed PostgreSQL instance from [Neon.tech](https://neon.tech) or [Supabase](https://supabase.com).
2. Set the Environment Variables:
   - `DATABASE_URL`: Your PostgreSQL connection string.
   - `SECRET_KEY`: A secure random string for JWT.
   - `BACKEND_CORS_ORIGINS`: `["https://your-frontend.vercel.app"]`
3. Start command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

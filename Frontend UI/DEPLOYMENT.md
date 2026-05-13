# 🚀 Cloud Deployment Guide: Retail Intelligence Pro

This guide explains how to deploy your full-stack retail application to the web for free using **Vercel** and **Render**.

## 1. Push Code to GitHub
Deployment services work best when linked to a GitHub repository.
1. Create a new repository on GitHub.
2. Initialize git in your local project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for deployment"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

## 2. Deploy the Backend (FastAPI) to Render
1. Create a free account on [Render.com](https://render.com/).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository.
4. Set the following:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Render will give you a URL like `https://retail-api.onrender.com`. **Copy this URL.**

## 3. Deploy the Frontend (React) to Vercel
1. Create a free account on [Vercel.com](https://vercel.com/).
2. Click **Add New** -> **Project**.
3. Import your GitHub repository.
4. In **Framework Preset**, select **Vite**.
5. In **Root Directory**, select `frontend`.
6. **IMPORTANT**: In Environment Variables, add:
   - `VITE_API_URL` = (Your Render Backend URL from Step 2)
7. Click **Deploy**.

## 4. Final Connection
Update your `frontend/src/App.jsx` to use the environment variable for API calls instead of `localhost:8000`:
```javascript
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
// Update axios calls: await axios.get(`${API_BASE}/api/summary`);
```

---
*Your Retail Intelligence Pro Suite will now be live at your-project.vercel.app!*

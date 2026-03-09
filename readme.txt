# Flask + Playwright on Render.com (Free Tier)

## Project Structure
```
.
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker config with Playwright + Chromium
├── render.yaml         # Render.com deployment config
└── .dockerignore
```

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Health check |
| GET | `/download-quotation` | Downloads the PDF via Playwright |

---

## Deploy to Render.com (Free)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2 — Create Web Service on Render
1. Go to [https://render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Runtime**: `Docker`
   - **Plan**: `Free`
   - **Dockerfile Path**: `./Dockerfile`
5. Click **"Create Web Service"**

Render will auto-detect `render.yaml` and apply the settings.

---

## Local Development

```bash
# Build Docker image
docker build -t flask-playwright .

# Run container
docker run -p 5000:5000 flask-playwright

# Test
curl http://localhost:5000/
curl http://localhost:5000/download-quotation --output quotation.pdf
```

---

## Notes on Free Tier Limits
- **512 MB RAM** — Chromium is heavy; `--workers 1` in Gunicorn keeps memory low
- **Spins down after 15 min inactivity** — first request after sleep takes ~30s
- **No persistent disk** — files are handled in-memory (already done ✅)
- **750 free hours/month** — enough for one always-on service
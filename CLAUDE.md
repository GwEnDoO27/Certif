# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack enterprise intranet/portal platform with three components:
- **frontend/** — React 19 + Vite SPA (port 3000)
- **api/** — Python FastAPI service for file processing and utilities (port 8001)
- **backend/** — Go service handling auth, user management, analytics, WebSocket (port 8002)
- **Shared DB:** PostgreSQL (env vars: `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`)

## Commands

### Frontend
```bash
cd frontend
npm install
npm run dev       # Dev server on port 3000
npm run build     # Production build → dist/
npm run preview   # Preview production build
```

### Python API
```bash
cd api
pip install -r requirements.txt
python run.py     # Uvicorn on port 8001 with hot reload
```

### Go Backend
```bash
cd backend
go mod download
go run ./cmd/main.go        # Run server on port 8002
go build -o main ./cmd      # Build binary
go test ./...               # Run all tests
go test ./path/to/package   # Run single package tests
```

## Architecture

### Request Flow
```
Frontend (React) ──axios──► Go Backend (port 8002)   ─── PostgreSQL
                 ──axios──► Python API (port 8001)    ─── PostgreSQL
                 ──ws──────► Go Backend (WebSocket)
```

The Go backend handles all primary business logic (auth, users, apps catalog, analytics). The Python API handles file-heavy operations (Excel/PDF conversion, data merging, code mappings).

### Frontend Structure (`frontend/src/`)
- **App.jsx** — Root router; all pages are lazy-loaded via `React.lazy()`
- **Landing/** — Auth pages (login, register, password reset)
- **Admin/** — Admin dashboard (user management, app catalog, analytics)
- **pages/** — 22 specialized tool pages (accounting, HR, audit utilities)
- **components/** — Shared UI components
- **hooks/** — Custom hooks: `useWebSocket`, `useAnalytics`, `useScrollPosition`
- **services/** — Axios-based API call abstractions per domain
- **context/** — React Context providers (ThemeContext, config)

### Go Backend Structure (`backend/`)
- **cmd/main.go** — Entry point; initializes DB, registers all service routes
- **auth/** — JWT authentication and session management
- **admin/** — User CRUD, role management
- **applications/** — App catalog service
- **analyse/** — Analytics and event tracking
- **websocket/** — Real-time user presence
- Pattern: Handler → Service → Repository for each domain

### Python API Structure (`api/`)
- **main.py** — FastAPI app setup with CORS middleware
- **routers.py** — All route definitions (~500 lines)
- **db/** — SQLAlchemy models and database connection
- **utils/** — `format.py`, `convert.py`, `searching.py`, `sort.py`

## Roles & Access Control
Six user roles: `Admin`, `Dev`, `Comptable`, `Social`, `Auditeur`, `Client`. Admin panel documentation is in `frontend/NOTICE_ADMIN.md`.

## Deployment
- Dockerfiles in each component directory
- Kubernetes manifests in `api/k8s/` and `backend/k8s/`
- File uploads are persisted to `/app/uploads` via a PVC in K8s
- CORS is configured for `https://preprod.azert.fr`

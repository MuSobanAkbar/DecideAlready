# DecideAlready V1 (26th September 2026)

A button that picks a film, so you stop scrolling.

**Live:** https://decidealready.onrender.com/
*(first load after inactivity takes ~30s to wake.)*

## What it does

Click the button, get a random film from TMDB's popular catalogue. That's it.

## How it works

Browser → React frontend → FastAPI backend → TMDB API

The backend picks a random page (1–500) from TMDB's `/discover/movie` endpoint, takes one film from the twenty returned, and sends back clean JSON. FastAPI also serves the compiled frontend, so one service handles both the page and the API.

**Why a backend at all:** TMDB's API key would be visible to anyone opening DevTools if the browser called it directly. The backend keeps it server-side.

## Stack

| Layer | Tech |
|---|---|
| Frontend | React + TypeScript (Vite) |
| Backend | Python + FastAPI |
| Container | Docker (multi-stage: Node builds → Python runtime) |
| CI | GitHub Actions — builds the image on every push |
| Hosting | Render |




Film data from [TMDB](https://www.themoviedb.org/). This product uses the TMDB API but is not endorsed or certified by TMDB.

# To add/change for V2
[] 
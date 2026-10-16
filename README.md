# DecideAlready

I made this to solve an issue me and my friend face. So basically, whenever finding a movie, the issue arises that it's hard to find a specific movie that's good. And when you do find a movie online, spoilers come along with it, so what I've done is that I've created a spin the wheel for movies. It also solves the issue of spoilers.
It's essentially:
A button that picks a film, so you stop scrolling. Then it tells you what the film is about, without spoiling it.

**Live:** https://decidealready.onrender.com/
*(It runs on Render's free tier, so the first load after a quiet spell takes about 30 seconds to wake up.)*

I built this for me and a friend. We watch films together and can never decide what to put on, so now a button decides for us.

---

## What it does

1. Click **Pick a film**.
2. You get a random popular film: poster, title and year on a card.
3. An AI writes a short, spoiler-free teaser, and it types itself out while you watch.
4. TMDB's full synopsis is there too, blurred like a spoiler tag. Click it only if you don't mind knowing.

---

## How it works

```
Browser ──► React (Vite) ──► FastAPI ──► TMDB API   (films, posters, synopses)
                                     └──► Groq LLM   (spoiler-free teaser)
```

**`GET /api/random`** picks a random page (1–500) from TMDB's `/discover/movie` endpoint, takes one film from the twenty returned, and sends back clean JSON.

**`GET /api/overview/{movie_id}`** writes the teaser. It follows the same six steps every time:

1. **Check** the cache. If this film's teaser was already written, return it instantly.
2. **Fetch** the film's synopsis from TMDB.
3. **Prompt**: build the instructions for the AI.
4. **Ask** the LLM.
5. **Catch** failures and turn them into clear status codes (502, 503, 504).
6. **Save** the answer in the cache, then send it back.

FastAPI also serves the compiled frontend, so one service handles both the page and the API.

**Why a backend at all:** if the browser called TMDB directly, the API key would be visible to anyone who opens DevTools. The backend keeps every key server-side.

**Why the browser only sends an id:** you can't trust what a browser sends. If the overview route accepted text, anyone could make my server send *their* text to the AI and burn through my free tokens. So the browser sends a film id, and the server looks up the real synopsis itself.

---

## Stack

| Layer | Tech |
|---|---|
| Frontend | React 19 + TypeScript (Vite), Tailwind CSS v4, shadcn/ui |
| Backend | Python + FastAPI |
| AI | Groq (`openai/gpt-oss-120b`), behind a small adapter in `backend/llm.py` |
| Data | TMDB API |
| Tests | pytest (backend), Vitest + React Testing Library (frontend) |
| Quality | ruff, ESLint, `tsc --noEmit` |
| Container | Docker, multi-stage (Node builds the frontend, Python runs the app) |
| CI | GitHub Actions |
| Hosting | Render (auto-deploys from `main`) |

---

## Run it locally

You'll need Node 22, Python 3.12, a [TMDB API key](https://www.themoviedb.org/settings/api) and a [Groq API key](https://console.groq.com/keys).

**1. Add your keys** to `backend/.env`:

```
TMDB_API_KEY=your_tmdb_key
GROQ_API_KEY=your_groq_key
```

**2. Install everything:**

```bash
cd backend
pip install -r requirements.txt
cd ../frontend
npm install
```

**3. Start both servers with one command** (from `frontend/`):

```bash
npm run dev:all
```

Open http://localhost:5173. Saving a file updates the page straight away.

**Or run it the way Render does**, in Docker:

```bash
docker compose up --build
```

---

## Tests

```bash
cd backend && pytest -v       # backend: TMDB and the LLM are faked, nothing real is called
cd frontend && npm test       # frontend: click the button, check a film appears
```

Tests never call real services. TMDB and Groq are swapped for fakes, so the tests run in a second, don't need API keys, and still pass when TMDB is down.

---

## Checkpoints

### v1: the button (26 Sep 2026)

- A button that picks a random film from TMDB
- FastAPI backend that keeps the TMDB key hidden
- Docker image, GitHub Actions CI, deployed on Render

### v1.1: the safety net

- `/api/health` endpoint, so Render (and I) can check the server is alive
- pytest tests for the backend, with TMDB faked using `MagicMock` (a stand-in object that pretends to be whatever the test needs)
- Vitest + React Testing Library test: click the button, a title appears
- ESLint and TypeScript checks in CI
- Branch protection on `main`: every change goes through an Issue, a branch and a PR

### v2: it looks like an app now (2 Oct 2026)

| Issue | What | Status |
|---|---|---|
| #15 | Tailwind CSS v4 + shadcn/ui setup | ✅ Done |
| #16 | Film card with poster, title and year | ✅ Done |
| #17 | Skeleton while loading, friendly error state | ✅ Done |

### v3: the spoiler-free AI teaser (Oct 2026, in progress)

| Issue | What | Status |
|---|---|---|
| #18 | `backend/llm.py` adapter: timeout, retries, its own error types, answer checks, logging, 5 tests | ✅ Live |
| #19 | `GET /api/overview/{movie_id}`: prompt, cache, 502/503/504 errors | ✅ Live |
| #20 | `OverviewBox` on the card, typewriter effect, blurred TMDB synopsis | ✅ Done |
| #21 | pytest tests for the overview route (TMDB and LLM faked, including a cache hit) | ⬜ Next |
| #22 | 20-case spoiler eval, with the score in this README | ⬜ To do |

**Spoiler eval score:** *coming with #22.*

---

## Things that broke (and what they taught me)

Most of what I learned on this project came from things going wrong.

- **Tailwind wouldn't work with shadcn.** The project was set up for Tailwind v3, and shadcn expects v4. Fixing it meant adding the `@` path alias, upgrading to v4 and re-running the shadcn setup. *Lesson: set up Tailwind v4 and the alias first, then shadcn.*
- **The frontend got HTML instead of JSON.** In dev mode, Vite answered `/api/random` with the web page because nothing told it to forward API calls to FastAPI. *Lesson: add a Vite proxy for `/api`.*
- **CI found three hidden bugs the first time it ran pytest.** Wrong import paths, a missing TMDB key and a wrong `@patch` path. All of them had been hiding because the tests had only ever run on my laptop. *Lesson: run tests on a clean machine.*
- **"Merged" didn't mean "deployed."** Render kept serving a weeks-old version because new deploys were crashing on startup with `No module named 'llm'`. Uvicorn was starting from the wrong folder. Fixed with `--app-dir backend`. *Lesson: CI checked that the image builds, not that it starts. Always check the live site after a merge.*
- **The live AI route returned 500.** `KeyError: 'GROQ_API_KEY'`. The key lived in my `.env`, and Render never sees that file. *Lesson: every secret needs to be set in the host's environment too.*

---

## What's next

**Small fixes (to open as issues):**

- CI smoke test: actually start the Docker container in CI and check `/api/health`, so a startup crash can't reach `main` again
- `/api/random` returns `"Unknown"` for a missing poster or date, which breaks the poster fallback and the year badge. It should return `null`. It should also return a 502 when TMDB fails, instead of crashing
- Dockerfile: move to `node:22-alpine` and tighten `.dockerignore`
- Run the Vitest frontend tests in CI too

**Bigger plans:**

- **v4: sign in and "don't repeat."** Supabase Auth (magic-link email) and Postgres, so the button never suggests a film you've already marked as seen. FastAPI verifies the login token, and row-level security keeps each person's list private.
- **v5: polish.** Dependabot, structured logging, a Playwright end-to-end test, a CHANGELOG and releases.
- **v6: production hardening.** Rate limiting on the AI route, security headers, request IDs, Sentry, and LLM tracing with Langfuse.

---

## Known limitations

- **Cold starts:** Render's free tier sleeps after 15 minutes without traffic, so the first visit afterwards takes about 30 seconds.
- **The cache forgets:** teasers are cached in memory, so the cache empties whenever Render restarts or sleeps. v4 moves it into Postgres.
- **AI rate limits:** Groq's free tier allows about 8,000 tokens a minute. The cache helps a lot, but a burst of new films can hit the limit, and you'll see a friendly "try again shortly" message.

---

## Credits

Film data from [TMDB](https://www.themoviedb.org/). This product uses the TMDB API but is not endorsed or certified by TMDB.

Spoiler-free teasers are generated by an open-weight model served by [Groq](https://groq.com/).
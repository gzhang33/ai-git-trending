# Repository Guidelines

## Project Structure & Module Organization
- `backend/` contains the Flask service; core logic sits in `backend/app/*.py` (scraper, analyzer, summarizer). `router.py` exposes REST endpoints, and `config/settings.py` stores schedule and token defaults.
- `frontend/` houses the Vue 3 + Vite SPA. Views live in `frontend/src/views`, reusable UI in `frontend/src/components`, and API helpers in `frontend/src/api/reports.ts`.
- `images/` caches generated artwork, `output/` keeps markdown and JSON consumed by the UI, and `docker-compose.yml` wires both services.

## Build, Test & Development Commands
- Backend: `python -m venv .venv && .venv\\Scripts\\activate`, `pip install -r backend/requirements.txt`; `python app.py --mode full` runs the scheduled scrape plus API, `python app.py --mode web --debug --port 5001` is best for endpoint iterations, and `python seed_database.py` refreshes local records.
- Frontend: from `frontend/`, run `npm install`; `npm run dev` (http://localhost:5173) starts Vite, `npm run build` produces the production bundle, `npm run preview` smoke-tests the output, and `npm run lint` / `npm run type-check` gate formatting and types.
- Stack: `docker compose up --build` launches both services via the provided Dockerfiles and shared `.env`.

## Coding Style & Naming Conventions
- Python: follow PEP 8 with 4-space indents, snake_case functions, PascalCase classes, and uppercase config constants; order imports stdlib → third-party → local.
- Vue + TS: prefer `<script setup lang="ts">`; name components in PascalCase `.vue` files and utilities in camelCase `.ts` modules; Prettier (no semicolons, single quotes, width 100) and ESLint run with `npm run lint`.
- Tailwind drives styling—extend `tailwind.config.js` tokens instead of inlining colors or spacing.

## Testing Guidelines
- Automated backend tests are not yet committed; add `pytest` modules under `backend/tests/` and rely on `app.test_client()` fixtures instead of real network calls.
- Frontend changes must pass `npm run type-check` and `npm run lint`; add Vitest-style component specs (`ComponentName.spec.ts`) alongside complex widgets and register the script in `package.json` when introduced.
- Capture manual QA steps in PRs (commands like `curl http://localhost:5001/api/reports` plus UI screenshots).

## Commit & Pull Request Guidelines
- Use the repo’s `type: summary` format (e.g., `feat: add trend bucketing`, `fix: 数据筛选逻辑`) in imperative voice; squash noisy WIP commits locally.
- PRs need a short description, motivation, verification checklist, linked issues, and media for UI changes; update `.env.example` whenever configuration shifts.
- Secrets live in `.env` files loaded via `python-dotenv` and Vite; prefix frontend variables with `VITE_` and never commit real tokens.

# Repository Guidelines

## Project Structure & Module Organization
The top-level Python app is the primary runtime. Core areas are `ai/` for orchestration and providers, `api/` for FastAPI routers, `bot/` for Discord bot logic, `core/` for config and workflow runners, `mcp_server/` for MCP tools, `utils/` for shared integrations, `worker/` for automation jobs, and `frontend/` for the static dashboard. Entry points are `main.py` and `launch.sh`. A separate Node/Express app lives in `officialbot_source/` with feature folders such as `controllers/`, `routes/`, `services/`, `models/`, and `dashboard/`.

## Build, Test, and Development Commands
Use the Python virtual environment first: `source venv/bin/activate`.

- `pip install -r requirements.txt` installs the main platform dependencies.
- `playwright install chromium` installs the worker browser dependency.
- `python main.py` runs the FastAPI app and bot bootstrap on port `8001`.
- `python -m worker.main` starts the background automation worker.
- `./launch.sh` starts the API, worker, and static dashboard together.
- `cd officialbot_source && npm install` installs the Node dashboard/backend dependencies.
- `cd officialbot_source && npm run dev` starts the Node app with `nodemon`.
- `cd officialbot_source && npm start` runs the Node app in production mode.

## Coding Style & Naming Conventions
Follow the existing style in each subsystem. Python uses 4-space indentation, `snake_case` for modules/functions, and clear service-style filenames such as `state.py` or `logger.py`. JavaScript in `officialbot_source/` uses CommonJS, 2-space indentation, and feature-aligned names across `routes`, `controllers`, and `services`. Keep modules focused, prefer descriptive names over abbreviations, and avoid mixing Python and Node concerns in the same directory.

## Testing Guidelines
No formal automated suite is configured yet. For Python changes, verify imports and boot locally with `python main.py` or `./launch.sh`, then hit `/health`. For Node changes, run `node --check path/to/file.js`, start `npm run dev`, and manually test the affected route or dashboard flow. Add tests near the touched feature if you introduce a test framework.

## Commit & Pull Request Guidelines
Recent history favors imperative, summary-first subjects such as `docs: update README...`, `Deployment: ...`, and `Implement ...`. Keep commit titles concise and scoped to one change. Pull requests should explain the user-visible effect, list verification steps, reference related issues, and include screenshots for `frontend/` or `officialbot_source/dashboard/` UI changes.

## Security & Configuration Tips
Secrets belong in `.env`, never in source control. Validate permission-sensitive actions on the backend, especially Discord, guild, and Minecraft admin flows. Treat CORS and API keys as production-sensitive settings when editing `main.py`, auth routes, or integration utilities.

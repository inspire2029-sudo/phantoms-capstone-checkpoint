# PHANTOMS AI — Week 2

## Backend Engineering Capstone

A small backend integration project that connects an external API, a SQLite persistence layer, and a Flask webhook into one reproducible workflow.

**Core flow**

`OpenWeather API → SQLite → Webhook → SQLite`

## What I built

- External API client for OpenWeather
- SQLite persistence layer
- Flask webhook receiver
- API → database → webhook pipeline
- Automated tests for project structure and database schema
- Appointment-booking database design
- SQL JOIN and aggregation debugging
- Environment-based configuration for secrets and runtime settings

## Repository structure

```text
phantoms-ai-week2/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   └── store.db              # generated locally, ignored by Git
├── src/
│   ├── api.py                # OpenWeather API client
│   ├── database.py           # SQLite storage layer
│   ├── pipeline.py           # API → DB → webhook pipeline
│   └── webhook.py            # Flask webhook receiver
├── tests/
│   └── test_project.py       # project and database checks
├── .env.example              # local configuration template
├── .gitignore
├── main.py
├── requirements.txt
├── db_design.md
└── debug_solution.sql
```

## Notebooks

### W2D1 — SQL Foundations
`W2D1_SQL_Foundations.ipynb`

Introduces SQLite database creation, table design, inserts, filtering, and sorting.

### W2D3 — Webhooks & Flask
`W2D3_Webhooks_+_Flask_Basics.ipynb`

Builds a Flask webhook endpoint, validates JSON requests, and stores received payloads.

### W2D4 — Automation Pipeline
`W2D4_Automation_Pipeline.ipynb`

Connects the weather API, SQLite logging, webhook delivery, and repeated pipeline execution.

The notebook uses Google Colab Secrets for the API key and webhook URL rather than storing credentials in source code.

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and provide your local values.

Required:

- `OPENWEATHER_API_KEY`
- `WEBHOOK_URL`

Optional:

- `PIPELINE_CYCLES` — default: `3`
- `PIPELINE_INTERVAL` — default: `30` seconds

Real credentials must never be committed.

## Run the webhook

`python -m src.webhook`

Endpoint:

`http://127.0.0.1:5000/webhook`

## Run the pipeline

`python main.py`

Each cycle:

1. Fetches weather data
2. Stores the response in SQLite
3. Sends a JSON payload to the webhook
4. Stores the received payload in SQLite

## Run tests

`pytest -q`

GitHub Actions also runs tests automatically on pushes and pull requests to `main`.

## Database design

`db_design.md` documents:

- Patients
- Doctors
- Appointments
- Appointment status
- Start/end times
- Preserved cancellation history

## SQL debugging

`debug_solution.sql` demonstrates:

1. Keeping a `LEFT JOIN` effective by placing right-table filters in `ON`
2. Grouping by all selected non-aggregated columns
3. `COALESCE` for customers with no completed orders

## Engineering decisions

- Configuration and secrets separated from source
- Generated SQLite ignored by Git
- Context managers for DB cleanup
- UTC timestamps
- Parameterized SQL
- HTTP timeouts
- Runtime configuration validation
- Small, inspectable components
- Automated CI tests

## Security considerations

This is a learning project, not a production webhook service.

The webhook currently accepts JSON without authentication or signature verification. A production implementation should add authentication, request validation, rate limiting, structured logging, and network controls.

Never commit API keys, webhook secrets, `.env` files, or credentials.

## Learning direction

This project is part of my progression from software and backend foundations toward **cybersecurity, AI security, and eventually LLM Red Teaming**.

> Build it. Break it. Understand it. Document it.

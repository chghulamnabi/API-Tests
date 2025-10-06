## API Automation Demo

A production-quality API automation testing template featuring async HTTP client, robust retries, validation with Pydantic, clean configuration, and rich HTML reporting. Uses JSONPlaceholder for demo CRUD endpoints.

### Highlights
- Async `httpx` client with connection pooling and exponential-jitter retries
- Strongly-typed request/response models with `pydantic`
- Environment-driven config via `.env`
- Pytest with `pytest-asyncio` and single-file HTML report via `pytest-html`
- Structured console logs with `rich`

### Quickstart
```bash
make install   # create venv and install deps
make test      # run tests and generate HTML report
make open      # open reports/report.html in browser
```

- HTML report: `reports/report.html`
- Default base URL: `https://jsonplaceholder.typicode.com` (override via `.env`)

### Endpoints Covered
- GET `/posts/{id}`
- POST `/posts`
- PUT `/posts/{id}`
- DELETE `/posts/{id}`

Backed by `https://jsonplaceholder.typicode.com`.

### Configuration
Copy `.env.example` to `.env` to tweak settings:
- `API_BASE_URL` (default JSONPlaceholder)
- `API_CONNECT_TIMEOUT`, `API_READ_TIMEOUT`, `API_WRITE_TIMEOUT`
- `API_POOL_LIMIT`, `API_RETRY_ATTEMPTS`, `API_RETRY_BACKOFF`

### Project Structure
```
src/api_tests/     # reusable client, models, config
  ├─ client.py     # async httpx client with retries
  ├─ config.py     # env-driven settings
  ├─ models.py     # pydantic models for Post
  └─ logging_config.py

tests/
  └─ test_posts.py # GET/POST/PUT/DELETE tests

reports/           # pytest-html output (created on test run)
```

### Make Targets
- `make install`: create `.venv` and install dependencies
- `make test`: run pytest quietly, generate `reports/report.html`
- `make open`: open the latest HTML report
- `make clean`: remove venv and caches

### What makes this world-class
- **Reliability**: retry-on-transient failures with exponential backoff and jitter
- **Correctness**: schema-validated payloads and responses via `pydantic`
- **Performance**: async HTTP client with connection pooling
- **DX**: one-command setup, rich logs, single-file HTML report for easy sharing

Troubleshooting:
- Ensure you run commands from the project root.
- If networking is restricted, GET/POST/PUT/DELETE to the public demo API may fail; try later or point `API_BASE_URL` to a reachable mock server.
# API-Tests

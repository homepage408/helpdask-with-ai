.DEFAULT_GOAL := help
.PHONY: help install dev start test lint lint-fix format format-check typecheck check ci db-migrate db-rollback db-migration db-current clean

# Load environment variables from .env if present
-include .env

# Clean surrounding quotes and set fallback defaults from .env
APP_HOST := $(if $(HOST),$(strip $(subst ",,$(HOST))),0.0.0.0)
APP_PORT := $(if $(PORT),$(strip $(subst ",,$(PORT))),8000)
APP_WORKERS := $(if $(WORKERS),$(strip $(subst ",,$(WORKERS))),4)

help: ## Tampilkan daftar perintah yang tersedia
	@echo "======================================================================="
	@echo " HelpDesk Mini — Management & Development Commands"
	@echo " (Active Config: HOST=$(APP_HOST), PORT=$(APP_PORT), WORKERS=$(APP_WORKERS))"
	@echo "======================================================================="
	@grep -h -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo "======================================================================="

## Setup & Dependency
install: ## Install dan sinkronisasi seluruh dependensi via uv
	uv sync

## Development & Execution
dev: ## Jalankan FastAPI server dalam mode development (auto-reload)
	uv run uvicorn app.main:app --reload --host $(APP_HOST) --port $(APP_PORT)

start: ## Jalankan FastAPI server dalam mode production (multi-workers)
	uv run uvicorn app.main:app --host $(APP_HOST) --port $(APP_PORT) --workers $(APP_WORKERS)

## Testing & Quality Assurance
test: ## Jalankan automated test suite via pytest
	uv run pytest -v

lint: ## Periksa kode menggunakan Ruff linter
	uv run ruff check .

lint-fix: ## Perbaiki otomatis isu linter yang fixable menggunakan Ruff
	uv run ruff check --fix .

format: ## Format kode sumber menggunakan Ruff formatter
	uv run ruff format .

format-check: ## Periksa konsistensi formatting kode sumber tanpa mengubah file
	uv run ruff format . --check

typecheck: ## Jalankan static type checker menggunakan mypy (strict mode)
	uv run mypy app tests

check: format-check lint typecheck ## Jalankan format-check, lint, dan typecheck sekaligus

ci: check test ## Jalankan seluruh pengecekan mutu kode dan automated tests

## Database & Migrations (Alembic)
db-migrate: ## Jalankan seluruh migrasi database ke versi terbaru (head)
	uv run alembic upgrade head

db-rollback: ## Kembalikan satu revisi migrasi ke belakang (-1)
	uv run alembic downgrade -1

db-migration: ## Buat revisi migrasi baru (gunakan: make db-migration name="deskripsi_migrasi")
	@if [ -z "$(name)" ]; then \
		echo "ERROR: Masukkan nama migrasi. Contoh: make db-migration name=\"create_users_table\""; \
		exit 1; \
	fi
	uv run alembic revision --autogenerate -m "$(name)"

db-current: ## Tampilkan versi revisi migrasi database saat ini
	uv run alembic current

## Maintenance
clean: ## Bersihkan file cache bytecode, pytest, mypy, dan ruff
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "Cache berhasil dibersihkan."

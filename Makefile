.PHONY: test test-backend test-mobile check migrate up

test: test-backend test-mobile

test-backend:
	cd backend && .venv/bin/python -m pytest

test-mobile:
	cd mobile && npm test -- --watchAll=false

check:
	cd backend && .venv/bin/python manage.py check

migrate:
	cd backend && .venv/bin/python manage.py migrate

up:
	docker compose up --build

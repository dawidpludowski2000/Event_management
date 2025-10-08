# ------- Docker compose wrappers -------
DC := docker compose

.PHONY: up down restart logs be-logs fe-logs be-sh fe-sh redis-sh \
        lint format test cov migrate mm csu

up:
	$(DC) up -d

down:
	$(DC) down

restart:
	$(DC) restart

logs:
	$(DC) logs -f

be-logs:
	$(DC) logs -f backend

fe-logs:
	$(DC) logs -f frontend

be-sh:
	$(DC) exec backend sh

fe-sh:
	$(DC) exec frontend sh

redis-sh:
	$(DC) exec redis sh

# ------- Backend quality & tests -------
lint:
	$(DC) exec backend ruff check .
	$(DC) exec backend black --check .
	$(DC) exec backend isort --check-only .

format:
	$(DC) exec backend ruff check . --fix
	$(DC) exec backend black .
	$(DC) exec backend isort .

test:
	$(DC) exec -e DJANGO_SECRET_KEY=test -e DEBUG=False -e ALLOWED_HOSTS=localhost backend pytest -q

cov:
	$(DC) exec -e DJANGO_SECRET_KEY=test -e DEBUG=False -e ALLOWED_HOSTS=localhost backend pytest -q --cov=. --cov-report=term-missing

# ------- Django helpers -------
migrate:
	$(DC) exec backend python manage.py migrate

mm:
	$(DC) exec backend python manage.py makemigrations

csu:
	$(DC) exec backend python manage.py createsuperuser

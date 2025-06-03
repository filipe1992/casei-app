.PHONY: up down clean clean-pyc clean-volume help db-revision db-upgrade db-downgrade

help:
	@echo "Comandos disponíveis:"
	@echo "  make up              - Inicia os containers Docker"
	@echo "  make down            - Para e remove os containers Docker"
	@echo "  make clean           - Remove containers, volumes e arquivos __pycache__"
	@echo "  make clean-pyc       - Remove arquivos Python compilados"
	@echo "  make clean-volume    - Remove volumes Docker"
	@echo "  make db-revision     - Cria uma nova revisão do banco de dados"
	@echo "  make db-upgrade      - Aplica todas as migrações pendentes"
	@echo "  make db-downgrade    - Reverte a última migração"

up:
	docker-compose up -d

down:
	docker-compose down

clean-pyc:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

clean-volume:
	docker volume rm $$(docker volume ls -q) 2>/dev/null || true

clean: down clean-pyc clean-volume

# Comandos do banco de dados
db-revision:
	cd backend/fastapi && POSTGRES_SERVER=localhost alembic revision --autogenerate -m "$(shell read -p 'Digite o nome da migração: ' name; echo $$name)"

db-upgrade:
	cd backend/fastapi && POSTGRES_SERVER=localhost alembic upgrade head

db-downgrade:
	cd backend/fastapi && POSTGRES_SERVER=localhost alembic downgrade -1 
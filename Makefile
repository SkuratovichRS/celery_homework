celery_run:
	celery -A app.celery_scripts.celery_app worker --pool=solo --loglevel=info

app_build:
	docker build -t app:latest .

up_test_db:
	docker compose up -d rabbitmq mongo redis

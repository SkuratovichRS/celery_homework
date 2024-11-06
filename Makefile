celery_run:
	celery -A app.celery_scripts.celery_app worker --pool=solo --loglevel=info

app_build:
	docker build -t app:latest .



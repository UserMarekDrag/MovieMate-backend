.PHONY: lint
lint:
	export DJANGO_SETTINGS_MODULE=moviemate.settings; \
	pylint --load-plugins pylint_django --rcfile=.pylintrc movie_api/ moviemate/ user_api/ scraper/

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: migrations
migrations:
	python manage.py makemigrations

.PHONY: run-server
run-server:
	python manage.py runserver

.PHONY: shell
shell:
	python manage.py shell

.PHONY: superuser
superuser:
	python manage.py createsuperuser

.PHONY: test
test:
	python manage.py test

.PHONY: install
install:
	pip install -r requirements.txt

postgres:
	until pg_isready -h db -p 5432; do \
		echo "Waiting for PostgreSQL..."; \
		sleep 2; \
	done
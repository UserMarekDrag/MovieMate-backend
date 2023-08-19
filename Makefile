.PHONY: lint
lint:
	pylint $(find . -name "*.py")

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

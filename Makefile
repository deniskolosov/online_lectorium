up_build:
	sudo docker-compose -f production.yml up --build

down:
	sudo docker-compose -f production.yml down

django_shell:
	sudo docker-compose -f production.yml run --rm django python manage.py shell

django_logs:
	sudo docker-compose -f production.yml logs -f django

front_logs:
	sudo docker-compose -f production.yml logs -f frontend

logs:
	sudo docker-compose -f production.yml logs -f

migrate:
	sudo docker-compose -f production.yml run --rm django python manage.py migrate

all:
	down up_build

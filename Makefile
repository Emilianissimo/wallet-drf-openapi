start:
	docker-compose up -d
up:
	docker-compose up
down:
	docker-compose down
stop:
	docker-compose stop
build:
	docker-compose build
migrate:
	docker exec -it web_wallet_python alembic upgrade head
rollback:
	docker exec -it web_wallet_python alembic downgrade -2
reset: down start rollback migrate stop up
test:
	python3 web_wallet/manage.py test application

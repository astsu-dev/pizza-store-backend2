fmt:
	isort pizza_store tests
	black pizza_store tests
migration:
	docker exec -it pizza-store-backend-db-1 edgedb -I local_dev migration create
migrate:
	docker exec -it pizza-store-backend-db-1 edgedb -I local_dev migrate
dbshell:
	docker exec -it pizza-store-backend-db-1 edgedb -I local_dev
dbtypes:
	docker exec -it pizza-store-backend-db-1 edgedb -I local_dev list types
dev:
	uvicorn --host 127.0.0.1 --port 8000 --reload --factory "pizza_store.adapters.app.app:create_app" 

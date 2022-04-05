fmt:
	isort pizza_store
	black pizza_store
migration:
	docker exec -it pizza-store-backend-db-1 edgedb -I local_dev migration create
migrate:
	docker exec -it pizza-store-backend-db-1 edgedb -I local_dev migrate
dbshell:
	docker exec -it pizza-store-backend-db-1 edgedb -I local_dev
dbtypes:
	docker exec -it pizza-store-backend-db-1 edgedb -I local_dev list types


import edgedb

client = edgedb.asyncio_client.create_async_client(
    user="edgedb",
    host="localhost",
    port=5656,
    database="edgedb",
    tls_security="insecure",
)

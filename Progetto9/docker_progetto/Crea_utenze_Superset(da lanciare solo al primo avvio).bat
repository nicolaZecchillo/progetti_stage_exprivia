docker exec -it superset_progetto superset fab create-admin --username progetto --firstname progetto --lastname progetto --email progetto@progetto.com --password progetto
docker exec -it superset_progetto superset db upgrade
docker exec -it superset_progetto superset init
pause
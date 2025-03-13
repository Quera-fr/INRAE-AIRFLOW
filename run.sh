docker build -t airflow-server .

docker run -p 8050:8080 \
 -v "$(pwd):/root/airflow" \
 -it airflow-server

docker build -t airflow-server .

docker run -p 8080:8080 \
 -v "C:/Users/Quera/Desktop/INRAE-Airflow:/root/airflow" \
 -it airflow-server
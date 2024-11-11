cd ./dashboard_app

docker build -t flask-app .

docker tag flask-app:latest

docker push flask-app:latest

pause
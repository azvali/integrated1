cd ./dashboard_app

docker build -t flask-app .

docker tag flask-app:latest chrisstefaniak/pkinglot-analyzer:latest

docker push chrisstefaniak/pkinglot-analyzer:latest

pause
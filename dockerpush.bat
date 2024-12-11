cd ./dashboard_app

docker build --no-cache -t flask-app .

docker tag flask-app:latest chrisstefaniak/pkinglot-analyzer2:1.0.13

docker push chrisstefaniak/pkinglot-analyzer2:1.0.13

pause
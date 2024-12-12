# Parking Lot Analyzer

A system to gather images of parking lots, interperet their availability, and display the results onto a web application running in the cloud

## HOW TO RUN WEBAPP

Run by creating the following resources:

    - Firestore Database
    - Kubernetes Autopilot Cluster
    - Service Account with "Datastore Owner," "Datastore User," "Editor" and "Viewer" roles
    - Google Bucket

Connect to the GCP cluster and execute the following:

1. Clone this repository

2. Install NGINX ingress from the "ingress-nginx" Helm repo

3. Create a key and download the JSON for the service account that was created earlier

4. Upload the JSON file to the cloud shell file system and run the following command:

       kubectl create secret generic firestore-credentials \
  --from-file=key.json=/path/to/service-account-key.json

5. Install the Helm chart included in this GitHub repo

6. Execute "kubectl get svc" and navigate to the external IP provided by the ingress controller

## HOW TO RUN CAMERA APPLICATION

1. Clone the repository onto a raspberry pi

2. Install the necessary libraries, such as PiCam

3. Fill in the host variable with the correct host IP provided by NGINX ingress

4. Provide an API key for the OpenAI API through an enviornment variable

5. Configure a camera onto the raspberry pi and aim it at a parking lot

6. Run the application and the image along with the interperated availability will be displayed on the webapp

## WEB APP ARCHITECTURE (FLASK PROJECT)

Our web app can be defined by multiple different endpoints

1. / root directory - This serves the web page. It fetches the current parking lot, the availability of that parking lot, and the history of the parking lot's availability and displays them on the page

2.  /submit endpoint - This handles the incoming requests from raspberry pi cameras. It takes the UUID created by the raspberry pi and stores it in a hash map so if there are multiple raspberry pi's, they can be distinguished. The image and the description are temporarily saved so that they can be puled by the root directory endpoint. Finally, the data that was recieived from the pi is sent to the Firestore database 

3.  /get-entities - This endpoint served as a test endpoint, but there is a function that is related to it that processes the data from the database and prepares it to be displayed on the web page.

## PI APPLICATION ARCHITECTURE

The application that runs on the raspberry pi contains a two seperate API calls that translate and send the parking lot observation

1. The application makes a request to the GPT API to interperet the parking lot's avaliability

2. Once the request returns the interpertation, it is then sent to the flask application

## KUBERNETES ARCHITECTURE

Our Kubernetes platform consists of the Helm chart for the main project and the Helm chart for NGINX ingress

The main project Helm chart builds one deployment that has the Kubernetes secret mounted onto it as a volume. This deployment also has a service which is used in the ingress file to expose the endpoints of the flask application. 

## MONITORING SCRIPT

We included a monitoring script to track HTTP requests from the flask application. The only line that needs to be configured is the access log line, which needs to be updated if the pod name is different from what is there. 

The script is outputted to a log file in the project folder, but a cron job can also be set up to backup the log files to a Google Bucket:

    crontab -e
    
    0 0 * * * gsutil cp /home/<USERNAME>/integrated1/http_monitoring/webserver_monitor.log gs://<BUCKET-NAME>/webserver_monitor_$(date +\%Y\%m\%d\%H\%M\%S).log >>           /tmp/cron_output.log 2>&1
    
    service cron status
    
    service cron start

These commands will ensure that the monitoring logs will be backed up in the bucket

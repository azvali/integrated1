# Integrated Computing Systems Project

Run by navigating to the "dashboard_app" directory and running "python app.py"

To run on GCP:

1. Run a Unbuntu VM instance

2. SSH and run "sudo git clone https://github.com/azvali/integrated1"

3. Run "sudo add-apt-repository universe" and "sudo apt update"

4. Run "sudo apt install python3-pip" and "pip install flask"

5. Run "sudo apt install nginx"

6. Run "sudo nano /etc/nginx/sites-available/flask-app" and paste the following into the file:

    server {
        listen 80;
        server_name 127.0.0.1;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

7. Create the symbolic link by executing "sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled" and do "sudo systemctl restart nginx"

8. Install gunicorn with "sudo pip3 install gunicorn"

9. Finally, run the command "gunicorn --workers 3 --bind 127.0.0.1:8000 app:app"

10. Access it through the external IP provided by the VM
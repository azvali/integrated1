
#!/bin/bash
 
### TO RUN SCRIPT IN GOOGLE CLOUD ###

# run "sudo nano webserver_monitor.sh" to create a new file
# copy and paste the script below
# run "sudo chmod +x webserver_monitor.sh" to make the script executable
# run "sudo ./webserver_monitor.sh" to run the script
# navigate to /var/log/webserver_monitor.log to see the log file
# execute "cat /var/log/webserver_monitor.log" to view the log file

# Log file to store resource and web server usage
LOG_FILE="/var/log/webserver_monitor.log"

log_resource_usage() {
    echo "-----------------------------------" >> $LOG_FILE
    echo "Timestamp: $(date)" >> $LOG_FILE

    echo "NGINX Metrics:" >> $LOG_FILE


    access_log="/var/log/nginx/access.log"
    if [ -f "$access_log" ]; then
        # Count total requests
        total_requests=$(grep -c "^" $access_log)
        echo "Total HTTP requests: $total_requests" >> $LOG_FILE

        # Count response status codes
        status_200=$(grep " 200 " $access_log | wc -l)
        status_400=$(grep " 400 " $access_log | wc -l)
        status_404=$(grep " 404 " $access_log | wc -l)
        status_500=$(grep " 500 " $access_log | wc -l)

        echo "Status 200 (OK): $status_200" >> $LOG_FILE
        echo "Status 400 (Bad Request): $status_400" >> $LOG_FILE
        echo "Status 404 (Not Found): $status_404" >> $LOG_FILE
        echo "Status 500 (Internal Server Error): $status_500" >> $LOG_FILE
    else
        echo "Nginx access log not found!" >> $LOG_FILE
    fi
        echo "-----------------------------------" >> $LOG_FILE
}

while true
do
    log_resource_usage
    sleep 5
done



#!/bin/bash

# Log file to store resource and web server usage
LOG_FILE="./http_monitoring/webserver_monitor.log"

log_resource_usage() {
    echo "-----------------------------------" >> $LOG_FILE
    echo "Timestamp: $(date)" >> $LOG_FILE

    echo "NGINX Metrics:" >> $LOG_FILE

    # If pod is updated, may need to update the pod name
    access_log=$(kubectl logs pkinglot-analyzer-deployment-57b4b88f7d-krcmn -c my-container-name --tail=1000)

    if [ -n "$access_log" ]; then
        total_requests=$(echo "$access_log" | grep -c "^")
        echo "Total HTTP requests: $total_requests" >> $LOG_FILE

        submit_requests=$(echo "$access_log" | grep "/submit" | wc -l)
        echo "Total /submit requests: $submit_requests" >> $LOG_FILE

        status_200=$(echo "$access_log" | grep " 200 " | wc -l)
        status_400=$(echo "$access_log" | grep " 400 " | wc -l)
        status_404=$(echo "$access_log" | grep " 404 " | wc -l)
        status_500=$(echo "$access_log" | grep " 500 " | wc -l)

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
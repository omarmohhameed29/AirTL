# Apache Airflow ETL Project

## Overview

This project demonstrates an ETL (Extract, Transform, Load) pipeline using Apache Airflow. It includes the following components:

- **XComs**: For inter-task communication and data exchange.
- **Group Tasks**: To manage and execute tasks in parallel.
- **PostgreSQL Connection**: For database interaction.
- **Data Scraping from API**: To extract data from a specified API.
- **Data Transformation**: To process and transform the scraped data.
- **Data Loading into PostgreSQL**: To load the transformed data into a PostgreSQL database.
- **Email Notifications**: To notify users of task success or failure.

## Project Structure

- `dags/ETL.py`: The main Airflow DAG file defining the ETL workflow.
- `plugins/fotmob_scrapper.py`: Custom plugin for data scraping from the API.
- `plugins/mail_utel.py`: For Mail Notification.
- `plugins/create_table.sql`: Create Tables in PostgreSQL.

## ETL PipeLine



## Setup

### Prerequisites

- Docker
- Docker Compose

### Configuration

1. **Update the Airflow Configuration**

   Ensure you have the following settings configured in your `docker-compose.yml` file:

   ```yaml
   smtp:
     image: maildev/maildev
     ports:
       - "25:25"
       - "80:80"
     environment:
       - MAILDEV_SMTP_PORT=25
       - MAILDEV_WEB_PORT=80
2. **Set Up Airflow**
    Create a .env file with the necessary environment variables for PostgreSQL:
    ```.env
    POSTGRES_HOST=airflow
    POSTGRES_USER=airflow
    POSTGRES_PASSWORD=ariflow
    POSTGRES_DB=airflow

    ```
    Start Airflow using Docker Compose:
    ```yaml
    docker-compose up -d
    ```

3. **Configure Email**

    ```yaml
    smtp:
    host: smtp.gmail.com
    port: 587
    user: your-email@gmail.com
    password: your-email-password
    tls: true
    email_backend: airflow.utils.email.send_email_smtp
    ```

4. **Usage**
    Access Airflow Dashboard: Navigate to http://localhost:8080 in your browser.

    Trigger the DAG: Manually trigger the ETL DAG from the Airflow UI or wait for the scheduled interval.
    
    Check Logs: Review task logs from the Airflow UI for debugging and verification.

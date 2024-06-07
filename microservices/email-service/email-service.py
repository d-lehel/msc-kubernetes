from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from kafka import KafkaConsumer
import json

# Initialize FastAPI app
app = FastAPI()

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['microservice1']
email_logs_collection = db['email_logs']

# Initialize Kafka consumer
consumer = KafkaConsumer('user-notifications', bootstrap_servers='localhost:9092', group_id='notification-consumer')

# Function to consume messages from Kafka topic (user-notifications)
def consume_user_notifications():
    for message in consumer:
        notification = json.loads(message.value.decode('utf-8'))
        log_email(notification['user_email'], notification['message'])

# Function to log the email content into the database
def log_email(user_email, message):
    # Save email log to MongoDB
    email_log = {'user_email': user_email, 'message': message, 'status': 'sent'}
    email_logs_collection.insert_one(email_log)

# Start consuming user notifications
consume_user_notifications()

# Endpoint to read email logs from the database
@app.get('/email_logs')
def get_email_logs():
    email_logs = list(email_logs_collection.find())
    return email_logs

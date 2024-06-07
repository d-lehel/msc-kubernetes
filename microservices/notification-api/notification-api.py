from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
# from kafka import KafkaConsumer, KafkaProducer
import json
import os

# Initialize FastAPI app
app = FastAPI()

# Initialize MongoDB client
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client['microservice1']
notifications_collection = db['notifications']

# Initialize Kafka consumer and producer
kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
# consumer = KafkaConsumer('user-registration', bootstrap_servers=kafka_bootstrap_servers, group_id='notification-group')
# producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Notification model
class Notification(BaseModel):
    user_email: str
    message: str

# Endpoint to read notifications from the database
@app.get('/notifications')
def get_notifications():
    notifications = list(notifications_collection.find())
    return notifications

# # Function to process incoming user registration events
# def process_user_registration_event(email, username):
#     # Create notification message
#     message = f'New user registered with email: {email} and username: {username}'
    
#     # Save notification to MongoDB
#     notification = {'user_email': email, 'username': username, 'message': message}
#     notifications_collection.insert_one(notification)
    
#     # Produce message to Kafka topic (user-notifications)
#     producer.send('user-notifications', value=json.dumps(notification).encode('utf-8'))

# # Function to consume messages from Kafka topic (user-registration)
# def consume_user_registration_events():
#     for message in consumer:
#         event_data = json.loads(message.value.decode('utf-8'))
#         process_user_registration_event(event_data['email'], event_data['username'])

# # Start consuming user registration events
# consume_user_registration_events()

# Test endpoint to return a message
@app.get('/test2')
def test_endpoint():
    return {'message': 'This is a test endpoint'}

# Test routes
@app.get('/mongo-url2')
async def get_mongo_url():
    return {"mongo_url": mongo_url}

@app.get('/db-connection2')
async def test_route():
    try:
        client.server_info()
        return {"message": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

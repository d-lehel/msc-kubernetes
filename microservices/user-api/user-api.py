from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from kafka import KafkaProducer
import bcrypt
import os

# Initialize FastAPI app
app = FastAPI()

# Initialize MongoDB client
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client['microservice1']
users_collection = db['users']

# Initialize Kafka producer
# producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Pydantic model for user registration request
class UserRegistrationRequest(BaseModel):
    email: str
    password: str

# Register endpoint - Produces a message to Kafka upon user registration
@app.post('/register')
def register_user(user: UserRegistrationRequest):
    email = user.email
    password = user.password
    
    # Hash the password before saving it to the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Save user to MongoDB
    users_collection.insert_one({'email': email, 'password': hashed_password})
    
    # Produce message to Kafka topic with email and username
    message = {'email': email, 'username': username}
    producer.send('user-registration', value=json.dumps(message).encode('utf-8'))
    
    return {'message': 'User registered successfully'}

# Get users endpoint - Reads users from the database
@app.get('/users')
def get_users():
    users = [{'email': user['email']} for user in users_collection.find()]
    return users

# Test endpoint to return a message
@app.get('/test')
def test_endpoint():
    return {'message': 'This is a test endpoint'}

# Test routes
@app.get('/mongo-url')
async def get_mongo_url():
    return {"mongo_url": mongo_url}

@app.get('/db-connection')
async def test_route():
    try:
        client.server_info()
        return {"message": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
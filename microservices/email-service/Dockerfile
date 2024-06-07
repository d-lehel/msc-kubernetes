# use official python image to run the application
FROM python:3.9-slim

# set working directory
WORKDIR /app

# install fastapi required extensions
RUN pip install --no-cache-dir fastapi uvicorn pymongo kafka-python pydantic bcrypt

# copy the application into the container
COPY email-service.py .

# set the port
EXPOSE 80

# command to run fastapi app using uvicorn
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","80"]
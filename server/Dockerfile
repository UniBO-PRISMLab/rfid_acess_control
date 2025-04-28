FROM python

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code into the container
COPY . /app/

# Expose the port your Flask app will run on
EXPOSE 5000

# Define the command to run your app
CMD ["python", "server.py"]

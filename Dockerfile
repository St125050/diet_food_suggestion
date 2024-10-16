# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container at /app
COPY app.py .
COPY combined_diets.csv .
COPY decision_tree_model.pkl .
COPY index.html .
COPY script.js .
COPY style.css .

# Set environment variable for Flask (or another web framework if applicable)
ENV FLASK_APP=app.py

# Make port 80 available to the world outside this container
EXPOSE 80

# Use a lighter WSGI server like Gunicorn for production
RUN pip install gunicorn

# Run the app using Gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]

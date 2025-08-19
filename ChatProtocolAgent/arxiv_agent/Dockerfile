FROM python:3.12.4
# Set the working directory
WORKDIR /app
# Copy requirements.txt to the container
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application code to the container
COPY . .
EXPOSE 8002
# Command to run the application
CMD ["python3", "arxiv_agent.py"]

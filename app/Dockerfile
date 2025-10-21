FROM python:3.14-alpine3.21

WORKDIR /app

# Copy and install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and README file
COPY app/src/ .
COPY README.md .

# Run the application on container start
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0"]
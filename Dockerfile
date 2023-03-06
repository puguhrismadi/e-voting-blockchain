FROM python:3.9-alpine

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=3333
ENV SERVICE_PORT=4444

# Install system dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install service Flask==1.1 gunicorn==20.1.0 Jinja2==2.11.3 MarkupSafe==2.1.2

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application files to container
COPY ./app /app

# Expose ports
EXPOSE $FLASK_RUN_PORT
EXPOSE $SERVICE_PORT

# Run the application
CMD ["sh", "-c", "gunicorn --workers=2 --bind=0.0.0.0:$FLASK_RUN_PORT --log-level=debug app:app --timeout 300 & gunicorn --workers=2 --bind=0.0.0.0:$SERVICE_PORT --log-level=debug service:app --timeout 300"]

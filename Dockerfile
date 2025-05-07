# Step 1: Build stage with Python and Gunicorn
FROM python:3.13.3-slim as base

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    nginx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Ensure gunicorn is installed if not already in requirements.txt
RUN python3 -m pip install gunicorn

# Copy the entire project to /app
COPY . /app/

# Set working directory to where manage.py is located
WORKDIR /app/mysite

# Run migrations and collect static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Set Django settings module
ENV DJANGO_SETTINGS_MODULE=mysite.settings

# Copy Nginx config to the correct path
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Step 2: Run Gunicorn and Nginx together
CMD ["sh", "-c", "gunicorn --chdir /app mysite.wsgi:application --bind 0.0.0.0:8000 & nginx -g 'daemon off;'"]

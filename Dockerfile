# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Stage 2: Run
FROM python:3.11-slim
WORKDIR /usr/src/app

# Copy only necessary files from the build stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .

# Install Gunicorn
RUN pip install --no-cache-dir gunicorn

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "blog_project.wsgi:application"]

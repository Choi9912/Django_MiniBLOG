FROM python:3.11
WORKDIR /usr/src/app

# Install packages
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
RUN pip install gunicorn

# Copy all src files
COPY . .

# Run the application on port 8000
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "blog_project.wsgi:application"]
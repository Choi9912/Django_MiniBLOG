# ./Dockerfile 
FROM python:3.11
WORKDIR /usr/src/app

## Install packages
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
RUN pip install gunicorn

## Copy all src files
COPY . .

## Run the application on the port 8080
EXPOSE 8000

# gunicorn 배포 명령어
# CMD ["gunicorn", "--bind", "허용하는 IP:열어줄 포트", "project.wsgi:application"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "blog_project.wsgi:application"]
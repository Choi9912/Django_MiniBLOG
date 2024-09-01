FROM python:3.11-slim

# 패키지 설치
RUN apt-get update && apt-get install -y git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# requirements.txt 파일 복사
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir daphne

# 나머지 소스 코드 복사
COPY . .

# 서버 실행 명령어 (Daphne 사용)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "blog_project.asgi:application"]
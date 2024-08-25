"""
Django settings for blog_project project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
load_dotenv()

# 다른 설정들...

# SECRET_KEY를 환경 변수에서 가져옴
SECRET_KEY = os.getenv("SECRET_KEY")

# SECRET_KEY가 없으면 오류 발생
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Django application")


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        return error_msg


SECRET_KEY = get_env_variable("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.naver",
    "bootstrap4",
    "blog",
    "widget_tweaks",
    "imagekit",
    "django_summernote",
]

SUMMERNOTE_CONFIG = {
    "summernote": {
        "width": "100%",
        "height": "480",
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "blog_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 다음 설정 추가:
SITE_ID = 1

# Allauth 설정
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
# 중간 확인 페이지 건너뛰기 설정
SOCIALACCOUNT_LOGIN_ON_GET = True

# 이메일 인증 건너뛰기 설정 (선택사항)
SOCIALACCOUNT_AUTO_SIGNUP = False  # 소셜 계정으로 로그인 시 자동으로 회원가입을 진행합
SOCIALACCOUNT_EMAIL_REQUIRED = False  # 소셜 계정에서 이메일을 필수로 요구하지 않습니다.
ACCOUNT_EMAIL_REQUIRED = True  #  일반 계정에서도 이메일을 필수로 요구하지 않습니다.
ACCOUNT_USERNAME_REQUIRED = True  # 사용자 이름을 필수로 요구하지 않습니다.
SOCIALACCOUNT_QUERY_EMAIL = False  # 소셜 제공자에게 이메일 정보를 요청하지 않습니다

# 이메일 설정 (개발 환경에서는 콘솔에 출력)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "blog_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# collectstatic으로 생성된 폴더
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = "/static/"
STATIC_ROOT = "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = "media"

MODEL_DIR = os.path.join(BASE_DIR, "models")

SUMMERNOTE_CONFIG = {
    "iframe": True,
    "summernote": {
        "width": "100%",
        "height": "480",
        "toolbar": [
            ["style", ["style"]],
            ["font", ["bold", "underline", "clear"]],
            ["color", ["color"]],
            ["para", ["ul", "ol", "paragraph"]],
            ["table", ["table"]],
            ["insert", ["link", "picture", "video"]],
            ["view", ["fullscreen", "codeview", "help"]],
        ],
    },
}

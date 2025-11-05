# Django settings with fake secrets

# Security keys
SECRET_KEY = 'django-insecure-very-long-secret-key-here-123456'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'myPassword123!',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# API Keys
STRIPE_SECRET_KEY = 'sk_live_51ABC123xyz789fakekey789'
AWS_ACCESS_KEY_ID = 'AKIAJEXAMPLE1234567'
AWS_SECRET_ACCESS_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'

# OAuth
OAUTH_TOKEN = 'ghp_abc123def456ghi789jkl012mno345pqr678stu'

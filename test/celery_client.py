from celery_worker import send_email

send_email.apply_async(['w'], countdown=8400)
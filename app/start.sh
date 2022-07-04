python manage.py migrate
gunicorn TheCompound.wsgi:application --bind 0.0.0.0:8000

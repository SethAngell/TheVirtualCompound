python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py rename_app landing_page profile
python manage.py migrate
gunicorn TheCompound.wsgi:application --bind 0.0.0.0:8000

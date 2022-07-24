web: gunicorn Ecodig.wsgi --log-file -

web: python manage.py collectstatic --no-input; gunicorn Ecodig.wsgi --log-file - --log-level debug
web: python texting_wall/manage.py collectstatic --noinput; gunicorn texting_wall.wsgi -b 0.0.0.0:$PORT
worker: python manage.py listen_for_tweets

mkdir -p "logs"
nohup gunicorn -c gunicorn_config.py app:flask_app &
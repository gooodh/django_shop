#!/bin/bash
python /shop/myshop/manage.py runserver  --insecure 0.0.0.0:8000
cd myshop
celery -A myshop worker -l info

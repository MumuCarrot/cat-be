## Getting Started

To start application in dev mode, run the following commands in the project directory:

```bash
pip install django python-dotenv django-cors-headers psycopg2-binary
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data.json
python manage.py runserver
```

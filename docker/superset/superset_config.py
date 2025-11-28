import os
SESSION_COOKIE_NAME = "superset_session"
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@postgres:5432/superset_db'
SECRET_KEY = 'tajni_kljuc112233'
WTF_CSRF_ENABLED = True
ROW_LIMIT = 5000
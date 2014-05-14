
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "d72a6ae3-c112-4895-9330-4b8d992a65af24acfea6-171b-4e48-bde7-3c5d444d43bb06e12232-3fbe-43e9-9cb7-a103fac641eb"
NEVERCACHE_KEY = "c295e15f-11bb-405b-b615-8650cba75ffa318d3523-5d4c-474a-b26f-ae61879e8eef11c6a159-c2fd-4cda-869c-4f94dd27a331"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

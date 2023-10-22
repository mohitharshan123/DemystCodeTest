#!/bin/sh

if [ "$1" = "test" ]; then
    # Run the tests
    python manage.py test accounting/
else
    python manage.py makemigrations
    python manage.py migrate

    # Seed business data
    python manage.py seed_business_data

    # Start the Django development server
    python manage.py runserver 0.0.0.0:8000
fi

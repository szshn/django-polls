============
django-polls
============

django-polls is a Django app to conduct web-based polls. For each
question, visitors can choose between a fixed number of answers.

This app was developed following `Writing your first Django app tutorial <https://docs.djangoproject.com/en/5.2/intro/tutorial01/>`_ 
by `Django <https://github.com/django/django>`_.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_polls",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("polls/", include("django_polls.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a poll.

5. Visit the ``/polls/`` URL to participate in the poll.

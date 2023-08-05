=====
django-wenzhi
=====

django-wenzhi project is demo application for codingsoho

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "wenzhi" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'wenzhi',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^wenzhi/', include('wenzhi.urls')),

3. Run `python manage.py migrate` to create the wenzhi models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a models if needed (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/wenzhi/ to participate in the poll.
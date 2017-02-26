# A Django Bundle

This bundle contains a Django deployment:

- One [Django charm](http://jujucharms.com/precise/django-python)
- One [Gunicorn charm](http://jujucharms.com/precise/gunicorn)
- One [PostgreSQL charm](http://jujucharms.com/precise/postgresql)

To deploy this bundle:

    juju-quickstart bundle:django/example-single

Note that this bundle will just deploy a rough equivalent of a 
[Django Creating a Project](https://docs.djangoproject.com/en/1.5/intro/tutorial01/#creating-a-project), for more configuration options see the [Django charm's](http://jujucharms.com/precise/django-python) README.


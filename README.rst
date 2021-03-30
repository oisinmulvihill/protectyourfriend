Protect Your Friend
===================

Protect your cherished pet against the unforseen medical expenses.

.. contents::

I use make, docker, docker-compose, python3 and virtualenvwrappers to manage
the project.

Development
-----------

To set up the code for development you can do::

    mkvirtualenv --clear -p python3 protectyourfriend
    make install

To run the service locally in the dev environment do::

    # activate the env
    workon protectyourfriend

    # Start postgresql and other dependant services.
    make up

    # Create/migrate the DB schema ready for use:
    make migrate

    # If you want to load some initial policy and breed fixtures you can:
    make migrate

    # Create a super user to login to the admin system:
    make superadmin

    # run the webapp
    make run

If you go to https://localhost:8000/ you the site root and call to action.

You can log into the admin system to edit the policy and breed information
here http://localhost:8000/admin.


Testing
-------

With docker compose running postgres in one window, you can run the tests as
follows::

    # activate the env
    workon protectyourfriend

    # Run basic model and view tests
    make test


Release
-------

*Note*: this is more for example. The build system would handle all the
releases to actual production/staging/development. Once CI env is configured,
it would simply call::

    # rerun the tests to be sure:
    make test docker_build docker_release

If all tests passed then the image would be deployed to prod/dev/stage docker
repository.

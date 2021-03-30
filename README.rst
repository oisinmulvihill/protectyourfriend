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

*Note*: this is more for example purposes as

If all the tests pass then you can do a release to the AWS ECR repository by
doing::

    # rerun the tests to be sure:
    make test docker_build docker_release

You will need to have logged-in to AWS and recovered the credentials to allow
docker to push. The protectyourfriend_terraform README shows how to do this.

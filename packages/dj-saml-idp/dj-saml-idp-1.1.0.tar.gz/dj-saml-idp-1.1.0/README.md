# dj-saml-idp

This started as a fork of `novapost/django-saml2-idp`, distributed
independently as `dj-saml-idp`.

The original project is at https://github.com/guitarmanvt/django-saml2-idp

`dj-saml-idp` implements the Identity Provider (IDP) side of the SAML 2.0
protocol and makes user authentication available to external applications.

This package only supports Django 1.9+. At this time, it's only been tested
with Django 1.9 & 1.11

# Development And Testing 

The package uses a Docker container to support both development and
tests. The container creates virtual environments for different
Python versions as below:

* Python 2.7 in `/venv27`
* Python 3.7 in `/venv37`

These environments may be used for development and interactive testing.

To build and run the container, to get a bash prompt:
```bash
docker build -t dj-saml-idp:latest .
docker-compose run --service-ports test
```

To support use of IDEs (such as PyCharm) for development, the container
can also run SSHD; run the command `docker/run_sshd.sh` at a bash prompt
in the container. In the commands above, the --service-ports option is
only needed if you intend to run sshd in the container.

The test runner is `pytest`. For release tests, we use `tox` to run
the tests against different versions of Python and Django. The tests
can be run inside the Docker container using `tox`:

```bash
$ . /venv37/bin/activate
$ tox
```

# Release

First of all, create a new version of the package. We use `bumpversion`_ to
handle updating all version strings, committing the changes and creating a
new git tag automatically. To bump the package version use the following
command with whichever part of the semantic version you'd like to update::

`$ bumpversion (major|minor|patch)`

for instance for a *minor* update, use (which should be the most common case)::

`$ bumpversion minor`

You need the PyPI credentials for the `mobify` account to be able to release
a new version and the build script is expecting it defined as an environment
variable:

`$ export PYPI_PASSWORD=supersecretpassword`

Releasing a new version to PyPI is very simple. The first thing you need to do
is make sure that all the test are passing and that the version in
`saml2idp/__init__.py` is the one that you'd like to create on PyPI.

With that done, all you need to do is run the following commands::

`$ make release`

This will cleanup the `build/` and `dist/` directories, build a source package
and a Python wheel. Both will then be uploaded to PyPI.

# License

Distributed under the `MIT License`.

.. _`novapost/django-saml2-idp`: https://github.com/novapost/django-saml2-idp
.. _`MIT License`: https://github.com/mobify/dj-saml-idp/blob/master/LICENSE
.. _`wheel`: http://wheel.readthedocs.org/en/latest/
.. _`bumpversion`: https://github.com/peritus/bumpversion

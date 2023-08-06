# Vote4Film

Simplify film selection for regular film nights. Participants can:

- Add films
- Vote for films
- Declare absences
- See the schedule which takes into account votes and absences

Admins can set the schedule of film nights.

This is a simple WSGI Web Application.

## Development

1. `poetry install` to set-up the virtualenv (one-off)
2. `poetry run ./src/vote4film/manage.py migrate` to set-up the local DB (one-off)
3. `poetry run ./src/vote4film/manage.py runserver_plus`
4. `make check` and `make test` before committing

### Publishing

This application will be published on PyPi.

1. Ensure you have configured Poetry repositories including `TestPyPi` (one-off)
2. `poetry publish --build -r testpypi` to upload to the test repository
3. `poetry publish --build` to release

## Deployment

Unfortunately, I will not provide any guidance here.

## Changelog

### v1.03 - 2019/11/12

- Fix config sub-directory used in XDG config home

### v1.02 - 2019/11/12

- Load configuration from XDG config home

### v1.0.1 - 2019/11/10

- First release of Vote4Film.

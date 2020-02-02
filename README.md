# Fixer App

## About
The aim of this application is to ingest currency exchange data provided from the Fixer API and provide an API for retriving exchange rate for a given date.

## Getting Started

### Assumptions and understanding of the problem

- This project was developed in a machine using macOS Catalina
- These instructions assume you are working on a unix based system.
- Since I used a free membership for interacting with fixer.io API, The key `base` is NOT used on retrieving currencies and it will be limited to `EUR` with as many `symbols` as specified later on. The opposite will get you a `105` error code. For more information read the [documentation](https://fixer.io/documentation) 
- To reduce scope I will assume a lot of happy paths and not handle all possible erros with the Fixer API or what users can do with the API
- The API will only return a map of rates for an specif date or if not specified the latest available
- Since the API required is too small, the application will be done with Flask
- The script mentioned in the pdf was not accessible :(

### Requirements

Make sure that you have the following installed on your machine:

- Python 3.8.1 (version in `.python-version` file)
- I strongly recommend that you setup a virtual environment for this project
- Postgres is used as DB, in case you are using MacOS > 10, make sure that you have the correct openssl flags exported in your terminal, otherwise you will run into trouble with the binaries for `psycopg2`. For example:
```bash
export CPPFLAGS="-I/usr/local/opt/openssl@1.1/include"
export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib"
```
- Docker will be running all dependencies from the project including the DB. For Mac user please read [documentation](https://docs.docker.com/docker-for-mac/)

#### Installing python

You can use your system python, but if you want to use multiple python versions on your machine, use [pyenv](https://github.com/pyenv/pyenv). If you are using it, the python version will be detected automatically inside the project's folder.

#### Installing dependencies

Like I said before, I strongly recommend using a virtual environment for this project, for this run the following:

```bash
make virtualenv
```

Activate the virtual environment
```bash
. venv/bin/activate
```

Install all the dependencies:
```bash
make install
```

If you want to exit the virtual env:
```bash
deactivate
```

#### Postgres

##### Running the DB
Like I mentioned before the DB will be running in a docker container so the application doesn't need to interact with your system. If you have postgres running locally make sure you change the port in the docker container. Here we will assume that you don't need to:

```bash
docker run --name fixer_test -e POSTGRES_USER=fixer -e POSTGRES_PASSWORD=fixer -e POSTGRES_DB=fixer_test -p 5434:5432 -d postgres:12.1
```

Also I run 2 different docker container at the same time, one for test and one for development. Make sure all your envs are point accordingly
##### Migrate

```bash
make migrate
```

For rollback:
```bash
make rollback
```

No need to migrate test, all this will be taken care for you automatically.

#### Running tests

Is really important at this point that you have a DB running so you can point the test to. The previous point gives you an example of how to do it. Now you need to set up your testing environment.

##### Setup .test.env

Modify the values accordingly
```bash
cp .sample.env .test.env
```

Once this is done and all env variables are changed to the correct values. Run:
```bash
make test
```

If you have reached this point without errors, congratulations you can start the application.


#### Running the app

The app has 2 modes. One serving the API and the otherone ingesting the rates through the fixer API.

For running the app:
```bash
python app.py api
```

For ingesting rates:
```bash
python app.py ingest
```

Anything else will show you an error message.

## Missings

The application was done with the minimum so it could be done during the time expected. As a consequence the app can be productionasible but is missing a few things to do so:
- I would have added static analysers like pylint, but I run out of time. Probably I will have some erros with docstring and a few things like that are easy to fix.
- Requires better error handling, at the moment just prints in screen some errors.
- Ideally we would have alerting.
- It has no monitoring (essential from every perspective)
- CI (Ideally we would have a pipeline where everything is automated)
- Missing more types of tests. At the moment it only has unit tests, but ideally it would have ac ceptance, system integration, performance tests etc. But given the time and that the fixer api key used is personal what was written is limited.
- The application needs a refactor in few areas, like the handling of the test DB, or even the APIcould be improved, but again it was done with the minimum.
- Define a deployment strategy (Docker, Kubernetis, etc)

Said this, this would be the minimum to start using it in production. But also is likely that since a lot of assumptions were made and was done a minimalistic version, the application would have to go first through a few changes to cope with the client needs.

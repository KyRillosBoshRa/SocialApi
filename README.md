# SocialApi

this is a social media api project.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

```
fastapi
postgresql
requirements.txt
```

### Installing

A step by step series of examples that tell you how to get a development env running

first you need to make your version of dot_env file then rename it to .env.

then:

```
pip install pipenv
pipenv shell
pipenv install -r requirements.txt
uvicorn app.main:app --reload # to run the app
```
to test your api you can run:

```
pytest --asyncio-mode=auto -s -v
```

### Using docker

you can ignore the previous steps if you prefer docker and just type:
```
docker-compose up --build -d
```
## Authors

* [KyRillosBoshRa](https://github.com/KyRillosBoshRa)

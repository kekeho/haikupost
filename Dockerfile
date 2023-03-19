FROM python:3.10-slim

RUN mkdir /code
RUN mkdir /vol


RUN pip install pipenv

WORKDIR /code
COPY ./Pipfile /code
RUN python -m pipenv install

COPY ./ /code
CMD ["pipenv", "run", "start"]

FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/source; mkdir -p /code/new; mkdir -p /code/data
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY *.py /code/
RUN sed -i "s/SA/Docker/g" /code/imhash.py
COPY config.ini /code/config.ini
CMD [ "python", "/code/imhash.py" ]
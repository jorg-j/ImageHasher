FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/source; mkdir -p /code/new; mkdir -p /code/data
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY *.py /code/
COPY config.ini /code/config.ini
RUN sed -i "s/Default/temp/g" /code/config.ini; sed -i "s/Docker/Default/g" /code/config.ini
CMD [ "python", "/code/imhash.py" ]
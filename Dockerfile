# image based on
FROM python:3.7.3

# define working directory
WORKDIR /app

# copy my_app files to workdir
COPY . /app/

# install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

# which file to execute
CMD python main.py

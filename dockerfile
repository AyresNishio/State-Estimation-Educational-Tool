From debian:latest

# set working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y build-essential python3 python3-pip && pip3 install -r requirements.txt && pip install --upgrade numpy

# copy python app to the folder
COPY . /app

# start the server
CMD ["gunicorn", "-b", "0.0.0.0:8050", "main:server"]

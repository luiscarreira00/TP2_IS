FROM python:3.9.15-slim

WORKDIR /usr/src/app

# install nodemon
RUN apt update
RUN apt install curl -y
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash
RUN apt install nodejs
RUN npm install -g npm@9.2.0
RUN npm install -g nodemon

# install pg_config
RUN apt install libpq-dev -y
RUN apt install build-essential -y

# upgrade pip
RUN python -m pip install --upgrade pip

# dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# run the script
CMD (sed -i 's/\r$//' ./run.sh) && (chmod +x ./run.sh) && (./run.sh)

RUN pip install requests
RUN pip install pycountry
RUN pip install geojson
RUN pip install shapely
RUN pip install -U flask-cors
RUN pip install geopy
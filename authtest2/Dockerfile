FROM node:lts-alpine

RUN npm install -g http-server

RUN mkdir /code
WORKDIR /code

COPY package*.json /code/
RUN npm install
COPY . .

# RUN npm run build
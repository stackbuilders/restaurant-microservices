FROM node:18.18.1-alpine3.18

WORKDIR /usr/app

COPY package.json .

RUN yarn install

RUN npm install -g nodemon

COPY . .

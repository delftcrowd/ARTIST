FROM node:19-alpine3.16

ARG default_api_base_url="http://127.0.0.1:8000/api/"
ENV API_BASE_URL=${default_api_base_url}

RUN mkdir application
COPY . /application/
WORKDIR /application

RUN npm install --global serve
RUN npm install
RUN npm run build

EXPOSE 3000

CMD ["serve", "-s", "./dist"]
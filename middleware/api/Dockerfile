FROM node:argon

# Create app directory
RUN mkdir -p /apps/waq/middleware/api
WORKDIR /apps/waq/middleware/api

# Install app dependencies
COPY package.json /apps/waq/middleware/api/
RUN npm install

# Bundle app source
COPY . /apps/waq/middleware/api/

EXPOSE 8080

CMD [ "npm", "start" ]

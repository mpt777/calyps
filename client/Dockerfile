FROM node:22-alpine
WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY . .

# RUN node -r dotenv/config
# RUN npm run build
# CMD ["npm", "run", "start"]
CMD ["npm", "run", "dev"]

# FROM node:20-alpine3.17
# WORKDIR /usr/src/app
# COPY package*.json ./

# RUN npm install
# COPY --chown=node:node . .
# USER node
# CMD ["npm", "run", "dev"]
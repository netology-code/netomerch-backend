# Specify a base image
FROM node:16-alpine

WORKDIR '/app'

# Install some depenendencies
COPY package.json .
COPY package-lock.json .
RUN npm install --silent
RUN npm install react-scripts -g --silent
COPY . .
RUN find . -type f -name "*.js*" -print0 | xargs -0 dos2unix
RUN npm run build

# Uses port which is used by the actual application
EXPOSE 3000

# Default command
CMD ["npm", "run", "start"]

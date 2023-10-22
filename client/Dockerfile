FROM node:18-alpine

WORKDIR /app/client/

COPY package.json tailwind.config.js postcss.config.js /app/client/
RUN yarn install --all
EXPOSE 3000
COPY . /app/client/

CMD ["yarn", "dev"]
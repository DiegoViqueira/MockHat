#!/bin/bash

npm run build:prod

aws s3 sync dist/browser s3://mockhat/ --delete

aws cloudfront create-invalidation --distribution-id ES6J2OY8ZSFMH --paths "/*"

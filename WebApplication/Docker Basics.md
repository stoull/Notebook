# Docker Basics


# nginx示例

```
FROM nginx:1.15.8-alpine
#configuration
copy ./nginx.conf /etc/nginx/nginx.conf
#content, comment out the ones you dont need!
copy ./*.html /usr/share/nginx/html/
#copy ./*.css /usr/share/nginx/html/
#copy ./*.png /usr/share/nginx/html/
#copy ./*.js /usr/share/nginx/html/
```

[How to create a static web server for HTML with NGINX](https://thatdevopsguy.medium.com/how-to-create-a-static-web-server-for-html-with-nginx-99bf8226bce6)

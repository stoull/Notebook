# Gunicorn and Nginx

### what is WSGI

WSGI指定了web服务器和web应用或web框架之间的标准接口，以提高web应用在一系列web服务器间的移植性。

- WSGI是一套接口标准协议/规范；
- 通信（作用）区间是Web服务器和Python Web应用程序之间；
- 目的是制定标准，以保证不同Web服务器可以和不同的web程序之间相互通信

> WSGI: WSGI is an interface. It is just a specification or a set of rules. WSGI is not a software. WSGI is not a library or a framework. WSGI is not something you can install via pip.

## what is gunicorn

- Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX
- gunicorn是Python语言的WSGI HTTP 服务器，即Web Servergatway Intergate
- 与gunicorn类似的库还有uSWGI

### Why needs gunicorn

## Nginx and Gunicorn work together!

`Nginx` is where requests from the internet arrive first. It can handle them very quickly, and is usually configured to only let those requests through, which really need to arrive at your web application.

`Gunicorn` translates requests which it gets from Nginx into a format which your web application can handle, and makes sure that your code is executed when needed.

### Nginx

`Nginx` is a web server and reverse proxy. It’s highly optimized for all the things a web server needs to do. Here are a few things it’s great at:

* Take care of domain name routing (decides where requests should go, or if an error response is in order)
* Serve static files
* Handle lots of requests coming in at once
* Handle slow clients
* Forwards requests which need to be dynamic to Gunicorn
* Terminate SSL (https happens here)
* Save computing resources (CPU and memory) compared to your Python code
* And a lot more, if you configure it to do so (load balancing, caching, …)

Things `Nginx` can’t do for you:

* Running Python web applications for you
* Translate requests to WSGI

### Gunicorn

Once Nginx decides, that a particular request should be passed on to Gunicorn (due to the rules you configured it with), it’s Gunicorn’s time to shine.

Gunicorn is really great at what it does! It’s highly optimized and has a lot of convenient features. Mostly, its jobs consist of:

* Running a pool of worker processes/threads (executing your code!)
* Translates requests coming in from Nginx to be WSGI compatible
* Translate the WSGI responses of your app into proper http responses
* Actually calls your Python code when a request comes in
* Gunicorn can talk to many different web servers

What Gunicorn can’t do for you:

* Not prepared to be front-facing: easy to DOS and overwhelm
* Can’t terminate SSL (no https handling)
* Do the job of a webserver like Nginx, they are better at it

## Use Gunicorn

### Installation

`pip install gunicorn`

Ubuntu: `sudo apt-get install gunicorn`

### Runing

`gunicorn [OPTIONS] [WSGI_APP]`

The only required argument to Gunicorn tells it how to load your Flask application. 

Like:

```
# equivalent to 'from hello import app'
$ gunicorn -w 4 'hello:app'

# equivalent to 'from hello import create_app; create_app()'
$ gunicorn -w 4 'hello:create_app()'
```

Now, create a example app and run with Gunicorn. Paste blow codes, and save as `app.py` file. And run: `gunicorn -w 1 'app:app'`, if everything goes well, you can acess the code in a browser.


```
def app(environ, start_response):
    """Simplest possible application object"""
    data = b'Hello, Gunicorn! Green Unicorn?? \n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])

```

#### More Arguments

```
$ gunicorn -w 4 -b 0.0.0.0 'hello:create_app()'
Listening at: http://0.0.0.0:8000
```

[For more](https://docs.gunicorn.org/en/stable/run.html)

### Deploying Gunicorn

run: `gunicorn -w 2 --forwarded-allow-ips="127.0.0.1" app:app`

then socket to nginx:

```
	upstream app_server {
   	 	# for a TCP configuration
    	server 127.0.0.1:8000 fail_timeout=0;
 	}
 
	location / {
		# checks for static file, if not found proxy to app
      	try_files $uri @proxy_to_app;
	}

	location @proxy_to_app {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Host $http_host;
      # we don't want nginx trying to do something clever with
      # redirects, we set the Host: header above already.
      proxy_redirect off;
      proxy_pass http://127.0.0.1:8000;
    }
```

注意flask程序中的static给nginx用

```
    # path for flask application static files
    location  /static/ {
        alias /home/pi/Documents/Vault/static/;
        autoindex on;
        expires max;
    }
    

	location /media/ {
		root /home/pi/Documents/Vault/media/;
	}
```



[nginx, gunicorn and WSGI](https://medium.com/@HannahMel/nginx-gunicorn-and-wsgi-e1795943536e)

[Gunicorn and Nginx in a Nutshell](https://vsupalov.com/gunicorn-and-nginx/#:~:text=Nginx%20and%20Gunicorn%20work%20together&text=It%20can%20handle%20them%20very,arrive%20at%20your%20web%20application)

[Gunicorn - WSGI server Doc](https://docs.gunicorn.org)

[Deploying Gunicorn](https://docs.gunicorn.org/en/stable/deploy.html)
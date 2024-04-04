# HTTP

## Overview

HTTP is a protocol for fetching resources (e.g. HTML documents).
HTTP is a client-server protocol.
This means that requests are initiated by the recipient (usually a web browser).

Client and servers communicate by exchanging individual messages (instead of data streams).
Clients send requests and servers send responses.

The client is often called the user agent (a tool that acts on behalf of the user).

To display a page, the browser sends a request to fetch the HTML document that represents the page.
It parses the file and makes additionaol requests for scripts, CSS files, images, videos etc.
The browser then combines these resources to present the web page.

HTTP is stateless (no link between two successive requests), but not sessionless (e.g. cookies allow the use of stateful sessions).

## Requests

Example:

```
curl --trace-ascii example.txt http://example.com
```

Look at `example.txt`:

```
GET / HTTP/1.1
Host: example.com
User-Agent: curl/7.81.0
Accept: */*
```

Elements:

- HTTP method (e.g. `GET`, `POST`, ...)
- path of the resource to fetch (here `/`)
- version of the HTTP protocol (here `HTTP/1.1`)
- optional headers
- a body in `POST`

Response:

```
HTTP/1.1 200 OK
Accept-Ranges: bytes
Age: 343881
Cache-Control: max-age=604800
Content-Type: text/html; charset=UTF-8
Date: Sun, 03 Mar 2024 09:05:25 GMT
Etag: "3147526947"
Expires: Sun, 10 Mar 2024 09:05:25 GMT
Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
Server: ECS (nyd/D146)
Vary: Accept-Encoding
X-Cache: HIT
Content-Length: 1256

<!doctype html>
...
</html>
```

Elements:

- version of HTTP protocol
- status code (here `200`)
- status message (here `OK`)
- HTTP headers
- optionally, a body with the fetched resource

Use HTTP via:

- `fetch` API (replaces the `XMLHttpRequest` API)
- server-sent events (create an `EventSource` instance and receive events from the server)

## Resources

Targets of HTTP requests are usually "resources" identified by URI (Uniform Resource Identifiers).
The most common URI is the URL (Uniform Resource Locator).

Syntax of URI:

- protocol/scheme
- authority
- port
- path
- query
- fragment

Data URLs (`data:` scheme) allow you to embed small files inline in documents:

```
data:[$MEDIATYPE][;base64],$DATA
```

## Connection Management

Types:

- short-lived connections
- persistent connection
- HTTP pipelining

## MIME Types

A MIME type (media type) indicates the nature/format of a document/file/byte sequence.
Composed of type and subtype `type/subtype`.

Two classes of types.
**Discrete types** are types that represent a single file or medium.
**Multipart types** are types that represent a document that consists of multiple component parts (each part may have its own MIME type).

Discrete types:

- `application` (binary data that doesn't fall into other types), e.g. `application/octet-stream` for generic binary data or `application/pdf`, `application/zip`, ...
- `audio`, e.g. `audio/mpeg`
- `example`
- `image`, e.g. `image/jpeg` or `image/png`
- `model` for model data for 3D object/scene
- `text` for text-only data including human-readable content, e.g. `text/plain`, `text/html`, `text/css`, `text/javascript` or `text/csv`
- `video`, e.g. `video/mp4`

Multipart types:

- `message`
- `multipart`

## CORS

### Origins

An **origin** of web content is the scheme, hostname and port of the URL used ot acccess it.

Consider the URL `http://example.com/app1/index.html`.
The origin would be `http://example.com` (the port is implicit).

URLs can be **same-origin** or **cross-origin**.

For example the URLs `http://example.com/app1/index.html` and `http://example.com/app2/about.html` are same-origin.

The URLs `http://example.com/app1/index.html` and `https://example.com/app1/index.html` are different origin (different schemas).

The URLs `http://example.com/app1/index.html` and `http://test.com/app1/index.html` are different origin (different hostnames).

The URLs `http://example.com/app1/index.html` and `http://example.com:8080/app1/index.html` are different origin (different ports).

### The Same-Origin Policy

By default browser restrict how a document or a script loaded by one origin can interact with a resource from another origin.
This prevents malicious websites on the internet from running JS in a browser to read data from another service.

### Cross-Origin Requests

CORS allows a _server_ to indicate any origins (domain, scheme, port) other than its own from which a browser should permit loading resources.
CORS relies on "preflight" requests to the server hosting the cross-origin resource in order to check that the server will permit the actual request.

Browser restrict cross-origin HTTP requests initiated from scripts.
For example `fetch` (and `XMLHttpRequest`) follow the same-origin policy.
This means that a web application using those APIs can only request resources from the same origin unless the other origin response includes the right CORS headers.

Go to `https://example.com`, open the console and try making requests.

This request will succeed:

```js
fetch("https://example.com").then(console.log).catch(console.error);
```

This request will fail:

```js
fetch("https://www.google.com").then(console.log).catch(console.error);
```

You won't get specifics on the error, only:

```
TypeError: NetworkError when attempting to fetch resource.
```

> Note a request to `http://example.com` will also fail, but not because of CORS but because of mixed content errors.

CORS requests can be simple or preflighted.
This is based on method, headers and content types.

A request is simple if it meets the following conditions:

- the method is `GET`, `HEAD` or `POST`
- apart from headers automatically set by the user agent, only the `Accept`, `Accept-Language`, `Content-Language`, `Content-Type` and `Range` headers (and other headers like `Origin`) are set
- the `Content-Type` header has one of the values `application/x-www-form-urlencoded`, `multipart/form-data` or `text/plain`

> Note that Safari places additional weird and poorly documented restrictions on the values allowed in `Accept`, `Accept-Language`, `Content-Language`.

You need to set the `Origin` header and the server will set an `access-control-allow-origin` header.

For example this won't lead to the `access-control-allow-origin` header:

```sh
curl -I https://jsonplaceholder.typicode.com/todos/1
```

But this will:

```sh
curl -H "Origin: https://example.com" -I https://jsonplaceholder.typicode.com/todos/1
```

If you look at the output you will see this header:

```
access-control-allow-origin: https://example.com
```

Note that this value will vary depending on the origin.
For example if you run this:

```sh
curl -H "Origin: https://google.com" -H "Content-Type: application/xml" -I https://jsonplaceholder.typicode.com/todos/1
```

You will see this header in the response:

```
access-control-allow-origin: https://google.com
```

Note that the server can also set `access-control-allow-origin: *` which means that the resource can be accessed by any origin.

If a request is not simple, it is preflighted.
For example, let's execute this from `https://example.com`:

```js
fetch("https://jsonplaceholder.typicode.com/posts", {
  method: "POST",
  headers: {
    "Content-Type": "application/xml",
  },
  body: "<thing>Thingy</thing>",
})
  .then(console.log)
  .catch(console.error);
```

In this case the browser will send a preflight request using the `OPTIONS` method.
This will contain the request headers:

```
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type
```

The `Access-Control-Request-Method` header notifies the server as a part of a preflight request that when the actual request is sent, it will do so using the given method (here `POST`).
The `Access-Control-Request-Headers` header notifies the server that when the actual request is sent, it will do so with the given headers.
The server can now determine whether it can accept such a request.

The server will respond to the preflight request and include these response headers:

```
access-control-allow-origin: https://example.com
access-control-allow-methods: GET,HEAD,PUT,PATCH,POST,DELETE
access-control-allow-headers: content-type
```

Once the preflight request is completed, the real request is sent.

TODO: The `Vary` header

## HTTP Authentication

RFC 7235 defines the HTTP authentication framework.

### Basic Authentication

RFC 7617 defines the "Basic" authentication framework.

The idea is super simple - just set an `authorization` header with the value `Basic $BASE_64_ENCODED_VALUE`.
For example `$BASE_64_ENCODED_VALUE` could be `base64encode(username, password)`.

An example follows.

Server:

```js
const express = require("express");
const basicAuth = require("express-basic-auth");
const cors = require("cors");

const app = express();
const port = 3000;

app.use(cors());

// Basic authentication middleware
const myAuthorizer = (username, password) => {
  const userMatches = basicAuth.safeCompare(username, "admin");
  const passwordMatches = basicAuth.safeCompare(password, "password");
  return userMatches & passwordMatches;
};

app.use(basicAuth({ authorizer: myAuthorizer }));

app.get("/", (req, res) => {
  res.send("You are authenticated");
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
```

Client:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Basic Auth Example</title>
  </head>
  <body>
    <h1>HTTP Basic Authentication Example</h1>
    <button id="fetchResource">Fetch Protected Resource</button>
    <script>
      document.getElementById("fetchResource").addEventListener("click", () => {
        const username = "admin";
        const password = "password";
        const headers = new Headers();
        headers.set(
          "Authorization",
          "Basic " + window.btoa(username + ":" + password)
        );

        fetch("http://localhost:3000", { method: "GET", headers: headers })
          .then((response) => {
            if (response.ok) {
              return response.text();
            }
            throw new Error("Network response was not ok.");
          })
          .then((text) => alert(text))
          .catch((error) =>
            console.log(
              "There has been a problem with your fetch operation:",
              error
            )
          );
      });
    </script>
  </body>
</html>
```

### Bearer Authentication

RFC 6750 defines the Bearer Authentication framework.

An example follows.

Server:

```js
const express = require("express");
const app = express();
const cors = require("cors");
const port = 3000;

app.use(cors());

// Middleware to check for Bearer token
const checkAuthToken = (req, res, next) => {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1]; // Extract the token

  if (token == null) return res.sendStatus(401); // If no token is present, unauthorized

  if (token === "YourSecretTokenHere") {
    next(); // Token is valid, proceed to the route
  } else {
    res.sendStatus(403); // Token is not valid, forbidden
  }
};

app.get("/protected", checkAuthToken, (req, res) => {
  res.json({ message: "Welcome to the protected route!" });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
```

Client:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Bearer Auth Example</title>
  </head>
  <body>
    <h1>Bearer Token Authentication Example</h1>
    <button id="fetchProtectedResource">Fetch Protected Resource</button>
    <script>
      document
        .getElementById("fetchProtectedResource")
        .addEventListener("click", () => {
          const token = "YourSecretTokenHere"; // This should be the token you received from authentication
          fetch("http://localhost:3000/protected", {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          })
            .then((response) => {
              if (response.ok) {
                return response.json();
              }
              throw new Error("Network response was not ok.");
            })
            .then((data) => alert(JSON.stringify(data)))
            .catch((error) =>
              console.error("Error fetching protected resource:", error)
            );
        });
    </script>
  </body>
</html>
```

## HTTP Caching

The HTTP cache stores a response associated with a request and reuses the stored response for subsequent requests.

There are two main types of caches: **private caches** and **shared caches**:.
A private cache is tied to a specific client (e.g. a browser cache is a private cache).
If you want to store the response only in a private cache, specify `Cache-Control: private`.

A shared cache is located between client and server and can store response than can be shared among users.
Shared caches are divided into **proxy caches** and **managed caches**.

Even if no `Cache-Control` is given, HTTP is designed to cache as much as possible via **heuristic caching**.
However this was mostly a workaround before `Cache-Control` support became widely adopted, so you should always use `Cache-Control`.

Stored responses have two states: **fresh** and **stale**.
The fresh state indicated that the cached response is valid and can be reused.
The stale state means that the the cached response has expired.

Fresh or stale is determined by the **age** (= time elapsed since response generated) and the `max-age`.
The `max-age=N` response directive indicates that response remains fresh until N seconds after the response is generated.

You can cause the responses to be cached separately via the `Vary` header which causes the cache to be keyed based on a composite of the response URL and the given header(s).

You can perform revalidation of a stale request by using the `If-Modified-Since` request header.
Alternatively, use `ETag`.

### Example

Here is a simple setup.
We have two pages (home and about).

The `app.py` file:

```python
from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.route('/')
def home():
    response = make_response(render_template('home.html'))
    return response

@app.route('/about')
def about():
    response = make_response(render_template('about.html'))
    return response

if __name__ == '__main__':
    app.run(debug=True)
```

Here the `templates/home.html`:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Home Page</title>
  </head>
  <body>
    <h1>Welcome to the Home Page</h1>
    <p>This is the home page of our Flask application.</p>
    <a href="/about">Go to About Page</a>
  </body>
</html>
```

Here the `templates/about.html`:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>About Page</title>
  </head>
  <body>
    <h1>About Us</h1>
    <p>This page gives information about our Flask application.</p>
    <a href="/">Go to Home Page</a>
  </body>
</html>
```

Run the app:

```sh
python app.py
```

If you switch between the pages you will see normal requests (both in the browser network inspector and in Wireshark).

To enable caching we need to set the `Cache-Control` header and specify a `max-age` value.
For example, let's say we want to cache for 5 seconds:

```python
response.headers['Cache-Control'] = 'max-age=5'
```

If you quickly switch between the pages, you will see that the requests are cached.

> Note that you will still see a request/response pair in your browser, however this will not be a real request/response pair (observe this in Wireshark).

Other common `Cache-Control` directives:

- `public` indicates that the response can be cached by any cache
- `private` indicates that response is intended for a single user and must not be stored by shared caches

The `must-revalidate` value ensures that once a cached response becomes stale, it cannot be reused until validated.

### The `no-cache` Value

The `no-cache` value indicates that the response can be stored in a cache but must be validated with the origin server before each reuse.
This is useful if you want to store something in the cache but still validate with the server before every reuse (via a conditional request).

There are two ways to make conditional requests:

- via `If-Modified-Since`
- via `If-None-Match` and ETags

Consider the modified example:

```python
from flask import Flask, request, make_response, send_file
from werkzeug.http import http_date
from os.path import getmtime
from datetime import datetime, timezone
import os

app = Flask(__name__)

# Path to the static resource
resource_file_path = 'resource.txt'

def file_last_modified_time(file_path):
    """Get the last modified time of the file as a datetime object."""
    timestamp = getmtime(file_path)
    return datetime.fromtimestamp(timestamp, timezone.utc)

@app.route('/resource')
def serve_static_resource():
    if not os.path.exists(resource_file_path):
        return make_response('Resource not found.', 404)

    # Get the last modified time of the file
    last_modified = file_last_modified_time(resource_file_path).replace(microsecond=0)

    # Check the 'If-Modified-Since' header in the request
    if_modified_since = request.headers.get('If-Modified-Since')
    if if_modified_since:
        # Parse the If-Modified-Since header to datetime
        if_modified_since_date = datetime.strptime(if_modified_since, '%a, %d %b %Y %H:%M:%S GMT').replace(tzinfo=timezone.utc)

        # Compare if the file was modified since the provided date
        if last_modified <= if_modified_since_date:
            # File hasn't been modified since the date in the 'If-Modified-Since' header
            return make_response('', 304)

    # If the file was modified after the 'If-Modified-Since' date, or if the header is not present,
    # return the file with the Last-Modified header
    with open(resource_file_path, 'r') as file:
      content = file.read()
    response = make_response(content)
    response.last_modified = last_modified
    response.headers['Cache-Control'] = 'max-age=15'
    response.headers['Last-Modified'] = http_date(last_modified.timestamp())
    return response

if __name__ == '__main__':
    app.run(debug=True)
```

Consider this example:

```python
from flask import Flask, request, jsonify, make_response
import hashlib
import os

app = Flask(__name__)

# Path to the file that represents the resource
resource_file_path = 'resource.txt'

def generate_etag(file_path):
    """Generate an ETag by hashing the contents of the given file."""
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read in chunks to avoid large files issues
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

@app.route('/resource')
def get_resource():
    # Ensure the file exists
    if not os.path.exists(resource_file_path):
        return make_response('Resource not found.', 404)

    # Generate the ETag for the current state of the resource file
    etag = generate_etag(resource_file_path)

    # Check if the 'If-None-Match' header in the request matches the ETag
    if request.headers.get('If-None-Match') == etag:
        # If the ETag matches, it means the client already has the latest version of the resource
        return make_response('', 304)
    else:
        # If the ETag doesn't match or is not provided, return the resource content along with the ETag
        with open(resource_file_path, 'r') as file:
            content = file.read()
        response = make_response(content)
        response.headers['ETag'] = etag
        response.headers['Content-Type'] = 'text/plain'  # You might want to adjust the content type
        return response

if __name__ == '__main__':
    app.run(debug=True)
```

Go to `localhost:5000/resource`.
You will see a real request+response.
The response will have this header:

```
ETag: 7b4758d4baa20873585b9597c7cb9ace2d690ab8
```

If you inspect the disk cache, you will see that `localhost:5000/resource` has saved the associated ETag.

Refresh the page and you will see another request containing the following header:

```
If-None-Match: 7b4758d4baa20873585b9597c7cb9ace2d690ab8
```

The server will return a `304`.

Now change the resource.
You will see another request:

```
If-None-Match: 7b4758d4baa20873585b9597c7cb9ace2d690ab8
```

You will see a regular 200 response with a new ETag.
Note that the cache entry will be updated.

### The `no-store` Value

The `no-store` value indicates that any caches of any kind should not store the response.
This is especially useful for sensitive data.

If you set `Cache-Control: no-store` you will see that moving between the "home" and "about" pages always retrieves a new page.

However this is not always a good idea.
Think about whemn we don't want to cache:

- don't want the response stored by anyone other than the specific client, for privacy reasons -> use `Cache-Control: private` here
- want to provide up-to-date information always -> use `Cache-Control: no-cache` here

### Common Caching Patterns

The default is not _don't cache_, but instead _heuristic caching_.

If you want to make sure that the latest versions of resources are always transmitted use `Cache-Control: no-cache`.

If you don't want to share a resource with other users use `Cache-Control: no-cache, private`.

Caching works best for static immutable files whose contents never change.

For resource that do change, it's best practice to change the URL each time the content changes, so that the URL can be cached.
Consider a HTML file contaning some `file.js` and/or `file.css`.
You can't serve with this with a reasonable `max-age` because the JS and CSS versions might change and you will want to serve the new versions.
Therefore it makes sense to send the files with a changing version.

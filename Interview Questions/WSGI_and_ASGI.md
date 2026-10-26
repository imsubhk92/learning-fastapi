## What are WSGI and ASGI?

**WSGI (Web Server Gateway Interface)** and **ASGI (Asynchronous Server Gateway Interface)** are specifications that define how web servers communicate with Python web applications and frameworks.

Think of them as "contracts" or "protocols" that ensure web servers and Python applications can work together seamlessly.

## WSGI (Web Server Gateway Interface)

### Overview

- **Created**: 2003 (PEP 333, updated in PEP 3333)
- **Purpose**: Standardize the interface between web servers and Python web applications
- **Model**: Synchronous, blocking I/O
- **Status**: Mature, widely adopted standard

### How WSGI Works

WSGI defines a simple interface with two sides:

1. **Server side**: Web server that implements WSGI
2. **Application side**: Python application that conforms to WSGI

### WSGI Application Structure

A WSGI application is simply a callable (function or class) that:

- Takes two arguments: `environ` and `start_response`
- Returns an iterable of byte strings

```python
def simple_wsgi_app(environ, start_response):
    """
    environ: dictionary containing CGI-like environment variables
    start_response: callable to initiate the HTTP response
    """
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)

    return [b'Hello, WSGI World!']

# Class-based WSGI application
class WSGIApp:
    def __call__(self, environ, start_response):
        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)

        path = environ.get('PATH_INFO', '/')
        method = environ.get('REQUEST_METHOD', 'GET')

        response = f"""
        <html>
            <body>
                <h1>WSGI Application</h1>
                <p>Path: {path}</p>
                <p>Method: {method}</p>
            </body>
        </html>
        """.encode('utf-8')

        return [response]

app = WSGIApp()
```

### WSGI Servers

Popular WSGI servers include:

- **Gunicorn** - Python WSGI HTTP Server for UNIX
- **uWSGI** - Full-featured application server
- **mod\_wsgi** - Apache module
- **Waitress** - Production-quality pure-Python WSGI server
- **Werkzeug** - Development server (used by Flask)

### WSGI Frameworks

- **Django** - Full-featured web framework
- **Flask** - Lightweight micro-framework
- **Bottle** - Minimalist framework
- **Pyramid** - Flexible framework

### WSGI Example with Flask

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, WSGI with Flask!'

@app.route('/user/<name>')
def user(name):
    return f'Hello, {name}!'

# This is a WSGI application
# Flask automatically creates the WSGI interface

if __name__ == '__main__':
    # Development server
    app.run(debug=True)

    # In production, you'd use a WSGI server:
    # gunicorn app:app
```

## ASGI (Asynchronous Server Gateway Interface)

### Overview

- **Created**: 2016
- **Purpose**: Extend WSGI to support asynchronous Python and handle WebSockets, HTTP/2, etc.
- **Model**: Asynchronous, non-blocking I/O
- **Status**: Modern standard for async Python web applications

### Why ASGI?

WSGI limitations:

- **Synchronous only** - blocking I/O operations
- **HTTP only** - can't handle WebSockets, HTTP/2 server push
- **Request-response cycle** - doesn't support long-lived connections
- **Threading overhead** - each request typically needs a thread

ASGI solutions:

- **Asynchronous** - non-blocking I/O with async/await
- **Protocol agnostic** - HTTP, WebSockets, HTTP/2, etc.
- **Long-lived connections** - persistent connections
- **Better performance** - single-threaded event loop

### ASGI Application Structure

An ASGI application is an async callable that:

- Takes three arguments: `scope`, `receive`, `send`
- Uses async/await syntax

```python
async def simple_asgi_app(scope, receive, send):
    """
    scope: dictionary containing connection info
    receive: async callable to receive messages
    send: async callable to send messages
    """
    if scope['type'] == 'http':
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({
            'type': 'http.response.body',
            'body': b'Hello, ASGI World!',
        })

# Class-based ASGI application
class ASGIApp:
    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            await self.handle_http(scope, receive, send)
        elif scope['type'] == 'websocket':
            await self.handle_websocket(scope, receive, send)

    async def handle_http(self, scope, receive, send):
        path = scope.get('path', '/')
        method = scope.get('method', 'GET')

        response_body = f"""
        <html>
            <body>
                <h1>ASGI Application</h1>
                <p>Path: {path}</p>
                <p>Method: {method}</p>
            </body>
        </html>
        """.encode('utf-8')

        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/html']],
        })
        await send({
            'type': 'http.response.body',
            'body': response_body,
        })

    async def handle_websocket(self, scope, receive, send):
        await send({'type': 'websocket.accept'})

        while True:
            message = await receive()
            if message['type'] == 'websocket.receive':
                await send({
                    'type': 'websocket.send',
                    'text': f"Echo: {message.get('text', '')}"
                })
            elif message['type'] == 'websocket.disconnect':
                break

app = ASGIApp()
```

### ASGI Servers

Popular ASGI servers include:

- **Uvicorn** - Lightning-fast ASGI server
- **Hypercorn** - HTTP/2 and HTTP/3 support
- **Daphne** - HTTP, HTTP/2, and WebSocket protocol server
- **Gunicorn** - With uvicorn worker class

### ASGI Frameworks

- **FastAPI** - Modern, high-performance API framework
- **Starlette** - Lightweight ASGI framework
- **Django** - ASGI support since Django 3.0
- **Quart** - Async version of Flask
- **Sanic** - Async web framework

### ASGI Example with FastAPI

```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import aiofiles

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "ASGI World"}

@app.get("/async-file")
async def read_file():
    # Non-blocking file I/O
    async with aiofiles.open('data.txt', mode='r') as f:
        content = await f.read()
    return {"content": content}

@app.get("/slow-endpoint")
async def slow_endpoint():
    # Non-blocking sleep - other requests can be processed
    await asyncio.sleep(5)
    return {"message": "This took 5 seconds but didn't block other requests"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message was: {data}")

# Run with: uvicorn main:app --reload
```

## Key Differences Comparison

| Aspect | WSGI | ASGI |
| --- | --- | --- |
| **Execution Model** | Synchronous, blocking | Asynchronous, non-blocking |
| **Concurrency** | Threading/multiprocessing | Single-threaded event loop |
| **Protocols** | HTTP only | HTTP, WebSockets, HTTP/2, etc. |
| **Connection Types** | Request-response only | Long-lived connections |
| **I/O Operations** | Blocking | Non-blocking |
| **Memory Usage** | Higher (thread per request) | Lower (shared event loop) |
| **Performance** | Good for CPU-bound tasks | Excellent for I/O-bound tasks |
| **Complexity** | Simpler | More complex |
| **Maturity** | Very mature (20+ years) | Newer (8+ years) |

## Performance Comparison

### WSGI Performance Characteristics

```python
# WSGI - Each request blocks until complete
import time
import requests

def wsgi_blocking_operation():
    # This blocks the entire thread
    time.sleep(1)  # Simulating database query
    return "Data from database"

@app.route('/data')
def get_data():
    result = wsgi_blocking_operation()
    return result

# With 10 concurrent requests:
# - WSGI needs 10 threads
# - Total time: ~1 second (with enough threads)
# - Memory usage: High (thread overhead)
```

### ASGI Performance Characteristics

```python
# ASGI - Concurrent requests don't block each other
import asyncio
import aiohttp

async def asgi_async_operation():
    # This doesn't block the event loop
    await asyncio.sleep(1)  # Simulating async database query
    return "Data from database"

@app.get('/data')
async def get_data():
    result = await asgi_async_operation()
    return result

# With 10 concurrent requests:
# - ASGI uses single event loop
# - Total time: ~1 second (all requests processed concurrently)
# - Memory usage: Low (no thread overhead)
```

## When to Use Each

### Use WSGI When:

- Building traditional web applications
- Working with mature frameworks (Django, Flask)
- CPU-intensive operations
- Simple request-response patterns
- Team familiar with synchronous programming
- Existing infrastructure built around WSGI

### Use ASGI When:

- Building modern APIs or microservices
- Need WebSocket support
- High I/O operations (database, file system, network calls)
- Real-time applications
- Need maximum performance for concurrent requests
- Building new applications from scratch

## Migration Considerations

### WSGI to ASGI Migration

```python
# WSGI Flask app
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'

# Convert to ASGI with Quart
from quart import Quart
app = Quart(__name__)

@app.route('/')
async def hello():
    return 'Hello World'

# Or use ASGI adapter for Flask
from asgiref.wsgi import WsgiToAsgi
from flask import Flask

flask_app = Flask(__name__)
app = WsgiToAsgi(flask_app)
```

### Running Both

```python
# You can run WSGI apps on ASGI servers using adapters
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask

# WSGI Flask app
flask_app = Flask(__name__)

@flask_app.route('/legacy')
def legacy_endpoint():
    return 'This is a legacy WSGI endpoint'

# ASGI FastAPI app
fastapi_app = FastAPI()

@fastapi_app.get('/modern')
async def modern_endpoint():
    return {'message': 'This is a modern ASGI endpoint'}

# Mount WSGI app in ASGI app
fastapi_app.mount('/wsgi', WSGIMiddleware(flask_app))
```

## Conclusion

**WSGI** remains excellent for traditional web applications, especially when working with mature frameworks and teams familiar with synchronous programming.

**ASGI** is the future for high-performance, modern web applications that need to handle many concurrent connections, real-time features, or intensive I/O operations.

Many organizations are gradually migrating from WSGI to ASGI, or using hybrid approaches where both coexist during the transition period.

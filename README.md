## How to use:

Clone the repository in a fresh virtualenv. 

Install dependencies
```
pip install -r requirements.txt
```

Start gRPC server
```
$ python serve.py
```

Start gRPC client (FastAPI web framework)
```
$ uvicorn client:app
```

Use ``curl`` to interact with the client api on address ``http://localhost:8000``
or simply go to ``http://localhost:8000/docs`` and use the FastAPI interactive 
API documentation.
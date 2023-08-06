aioclient
===

Installation
---

```sh
pip install aioclient
```

Usage
---

```python
import aioclient

async def get_example():
    status, headers, body = await aioclient.get('https://www.example.com/')
    print(body)
```

Changelog
---

### v0.1.0

* GET requests return `status, headers, body` tuples


### v0.2.0

* Support OPTIONS, HEAD, POST, PUT, PATCH, and DELETE requests
* Deserialize text/xml responses as XML ElementTree

### v0.2.1

* Fix project description

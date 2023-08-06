# h

An opinionated HTTP client library.

## Getting Started

`python -m pip install h` or `python -m pip install h.ttp`

```python
import h.ttp as http

# Send a single request and wait for a response
resp = http.request("GET", "https://www.example.com")

# Send an async request
resp = await http.async_request("GET", "https://www.example.com")

# Send a group of requests
async with http.session() as session:
    responses = []
    for host in ("example.com", "example.org", "example.nope"):
        responses.append((host, await session.request("GET", f"https://{host}")))
    for host, resp in responses:
        await resp.wait()
        print(host, resp.status_code)

# Also works with synchronous, just remove awaits.
with http.session() as session:
    ...
```

## FAQ

### How can I use HTTP without TLS or disable  certificate verification?

**You can't for non-local hosts.**

90% of all HTTP requests made on the public internet use TLS.
HTTP/3 and (functionally) HTTP/2 are only implemented over TLS.
TLS and certificate verification are the new defaults for the web.

You're allowed to not use TLS with `localhost`, `127.0.0.1`, and `::1`
as well as unix connections using `http+unix`.

### How do I configure read, write, and connection timeouts?

**You can't.** Set timeouts that matter to HTTP client consumers
like 'how long until I give up on this request'?

### How do I configure a specific TLS version / cipher?

**You can't.** TLS 1.2 and TLS 1.3 are the only allowed versions
and AES-GCM / ChaCha20 with strong ephemeral key exchanges
are all that can be configured.

### The server I'm making requests to doesn't conform to HTTP / TLS standards, what can I do?

Contact the server administrator and see if something can be done.

## License

Apache-2.0

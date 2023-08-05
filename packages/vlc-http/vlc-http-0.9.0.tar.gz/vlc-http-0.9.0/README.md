# VLC-HTTP (0.9.0)
An HTTP client for VLC's HTTP server.

## Example Usage
```python
from vlchttp import Client

client = Client('127.0.0.1', 8080, 'password')
status = client.get_status()
print('Running API version %d' % (status['apiversion']))
```
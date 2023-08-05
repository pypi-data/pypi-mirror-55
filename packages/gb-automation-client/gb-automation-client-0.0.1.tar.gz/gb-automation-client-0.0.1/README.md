[GBA getting started](https://docs.gamebench.net/automation-interface-usage/http-api/#getting-started)

Please note this will only work with GBA version v1.5.0 or greater.

### Create a client

```python
import gba
client_factory = gba.ClientFactory()
client = client_factory.create()
```

You can optionally pass a dictionary when creating the client

```python
config = {
    baseUrl: '',
    username: '',
    password: '',
}
client = client_factory.create(config)
```

Alternatively, use env vars for configuration

```
GBA_BASE_URL=
GBA_USERNAME=
GBA_PASSWORD=
```

### List devices

```python
client.list_devices()
```

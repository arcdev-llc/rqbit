# rqbit-container

Docker container for rqbit BitTorrent client with comprehensive environment variable support.

## Quick Start

```bash
docker run -d \
  -p 3030:3030 \
  -p 4240:4240 \
  -v rqbit-db:/home/rqbit/db \
  -v rqbit-cache:/home/rqbit/cache \
  -v rqbit-downloads:/home/rqbit/downloads \
  rqbit
```

## Environment Variables

All rqbit CLI flags can be configured via environment variables. Boolean flags accept: `1`, `true`, `yes`, `on` (case-insensitive).

### Logging

| Variable | Type | Description | CLI Flag | Default |
|----------|------|-------------|----------|---------|
| `RQBIT_LOG_FILE` | string | Log file path | `--log-file` | - |
| `RQBIT_LOG_FILE_RUST_LOG` | string | Rust log filter for file | `--log-file-rust-log` | - |

### HTTP API

| Variable | Type | Description | CLI Flag | Default |
|----------|------|-------------|----------|---------|
| `RQBIT_HTTP_API_LISTEN_ADDR` | string | HTTP API listen address | `--http-api-listen-addr` | `0.0.0.0:3030` |
| `RQBIT_HTTP_API_ALLOW_CREATE` | boolean | Allow creating torrents via API | `--http-api-allow-create` | - |

### Networking

| Variable | Type | Description | CLI Flag | Default |
|----------|------|-------------|----------|---------|
| `RQBIT_LISTEN_PORT` | string | Listen port for peer connections | `--listen-port` | `4240` |
| `RQBIT_LISTEN_IP` | string | Listen IP address | `--listen-ip` | - |
| `RQBIT_BIND_DEVICE` | string | Network device to bind to | `--bind-device` | - |
| `RQBIT_SOCKS_PROXY_URL` | string | SOCKS proxy URL | `--socks-url` | - |
| `RQBIT_TCP_LISTEN_DISABLE` | boolean | Disable TCP listening | `--disable-tcp-listen` | - |
| `RQBIT_TCP_CONNECT_DISABLE` | boolean | Disable TCP connections | `--disable-tcp-connect` | - |
| `RQBIT_EXPERIMENTAL_UTP_LISTEN_ENABLE` | boolean | Enable experimental uTP listening | `--experimental-enable-utp-listen` | - |

### UPNP

| Variable | Type | Description | CLI Flag | Default |
|----------|------|-------------|----------|---------|
| `RQBIT_UPNP_PORT_FORWARD_DISABLE` | boolean | Disable UPNP port forwarding | `--disable-upnp-port-forward` | - |
| `RQBIT_UPNP_SERVER_ENABLE` | boolean | Enable UPNP server | `--enable-upnp-server` | `true` |
| `RQBIT_UPNP_SERVER_FRIENDLY_NAME` | string | UPNP server friendly name | `--upnp-server-friendly-name` | `rqbit-docker` |

### DHT (Distributed Hash Table)

| Variable | Type | Description | CLI Flag |
|----------|------|-------------|----------|
| `RQBIT_DHT_DISABLE` | boolean | Disable DHT | `--disable-dht` |
| `RQBIT_DHT_PERSISTENCE_DISABLE` | boolean | Disable DHT persistence | `--disable-dht-persistence` |
| `RQBIT_DHT_BOOTSTRAP` | string | DHT bootstrap addresses | `--dht-bootstrap-addrs` |

### Peer Connections

| Variable | Type | Description | CLI Flag | Default |
|----------|------|-------------|----------|---------|
| `RQBIT_PEER_CONNECT_TIMEOUT` | string | Peer connection timeout (seconds) | `--peer-connect-timeout` | `10` |
| `RQBIT_PEER_READ_WRITE_TIMEOUT` | string | Peer read/write timeout (seconds) | `--peer-read-write-timeout` | `30` |

### Runtime & Performance

| Variable | Type | Description | CLI Flag | Default |
|----------|------|-------------|----------|---------|
| `RQBIT_SINGLE_THREAD_RUNTIME` | boolean | Use single-threaded runtime | `--single-thread-runtime` | - |
| `RQBIT_RUNTIME_WORKER_THREADS` | string | Number of worker threads | `--worker-threads` | - |
| `RQBIT_RUNTIME_MAX_BLOCKING_THREADS` | string | Max blocking threads | `--max-blocking-threads` | - |
| `RQBIT_DEFER_WRITES_UP_TO` | string | Defer writes up to size | `--defer-writes-up-to` | - |
| `RQBIT_CONCURRENT_INIT_LIMIT` | string | Concurrent initialization limit | `--concurrent-init-limit` | `10` |
| `RQBIT_EXPERIMENTAL_MMAP_STORAGE` | boolean | Enable experimental mmap storage | `--experimental-mmap-storage` | - |

### Trackers

| Variable | Type | Description | CLI Flag | Default |
|----------|------|-------------|----------|---------|
| `RQBIT_TRACKER_REFRESH_INTERVAL` | string | Tracker refresh interval (seconds) | `--tracker-refresh-interval` | `1800` |
| `RQBIT_TRACKERS_DISABLE` | boolean | Disable trackers | `--disable-trackers` | - |
| `RQBIT_TRACKERS_FILENAME` | string | Trackers filename | `--trackers-filename` | - |

### Local Service Discovery

| Variable | Type | Description | CLI Flag |
|----------|------|-------------|----------|
| `RQBIT_LSD_DISABLE` | boolean | Disable Local Service Discovery | `--disable-lsd` |

### Rate Limiting

| Variable | Type | Description | CLI Flag |
|----------|------|-------------|----------|
| `RQBIT_RATELIMIT_DOWNLOAD` | string | Download rate limit | `--ratelimit-download` |
| `RQBIT_RATELIMIT_UPLOAD` | string | Upload rate limit | `--ratelimit-upload` |
| `RQBIT_DISABLE_UPLOAD` | boolean | Disable uploads | `--disable-upload` |

### Blocklist/Allowlist

| Variable | Type | Description | CLI Flag |
|----------|------|-------------|----------|
| `RQBIT_BLOCKLIST_URL` | string | Blocklist URL | `--blocklist-url` |
| `RQBIT_ALLOWLIST_URL` | string | Allowlist URL | `--allowlist-url` |

### File System

| Variable | Type | Description | CLI Flag |
|----------|------|-------------|----------|
| `RQBIT_UMASK` | string | File umask (non-Windows) | `--umask` |

### Server Subcommand

These variables apply when using the `server start` command:

| Variable | Type | Description | CLI Flag |
|----------|------|-------------|----------|
| `RQBIT_SESSION_PERSISTENCE_DISABLE` | boolean | Disable session persistence | `--disable-persistence` |
| `RQBIT_SESSION_PERSISTENCE_LOCATION` | string | Session persistence location | `--persistence-location` |
| `RQBIT_FASTRESUME` | string | Fast resume file | `--fastresume` |
| `RQBIT_WATCH_FOLDER` | string | Watch folder for new torrents | `--watch-folder` |

### Internal

| Variable | Type | Description |
|----------|------|-------------|
| `RQBIT_BINARY` | string | Path to rqbit binary (default: `rqbit`) |

## Volumes

- `/home/rqbit/db` - Database and session data
- `/home/rqbit/cache` - Cache directory
- `/home/rqbit/downloads` - Download directory

## Ports

- `3030` - HTTP API
- `4240` - Peer listening port

## Examples

### Basic usage with custom ports

```bash
docker run -d \
  -p 8080:8080 \
  -p 5000:5000 \
  -e RQBIT_HTTP_API_LISTEN_ADDR=0.0.0.0:8080 \
  -e RQBIT_LISTEN_PORT=5000 \
  -v rqbit-db:/home/rqbit/db \
  -v rqbit-cache:/home/rqbit/cache \
  -v rqbit-downloads:/home/rqbit/downloads \
  rqbit
```

### Disable DHT and enable debug logging

```bash
docker run -d \
  -p 3030:3030 \
  -p 4240:4240 \
  -e RQBIT_DHT_DISABLE=true \
  -e RQBIT_LOG_LEVEL_CONSOLE=debug \
  -v rqbit-db:/home/rqbit/db \
  -v rqbit-cache:/home/rqbit/cache \
  -v rqbit-downloads:/home/rqbit/downloads \
  rqbit
```

### Use SOCKS proxy and watch folder

```bash
docker run -d \
  -p 3030:3030 \
  -p 4240:4240 \
  -e RQBIT_SOCKS_PROXY_URL=socks5://proxy:1080 \
  -e RQBIT_WATCH_FOLDER=/home/rqbit/watch \
  -v rqbit-db:/home/rqbit/db \
  -v rqbit-cache:/home/rqbit/cache \
  -v rqbit-downloads:/home/rqbit/downloads \
  -v /path/to/watch:/home/rqbit/watch \
  rqbit
```

### Rate limited with blocklist

```bash
docker run -d \
  -p 3030:3030 \
  -p 4240:4240 \
  -e RQBIT_RATELIMIT_DOWNLOAD=10MB \
  -e RQBIT_RATELIMIT_UPLOAD=2MB \
  -e RQBIT_BLOCKLIST_URL=https://example.com/blocklist.txt \
  -v rqbit-db:/home/rqbit/db \
  -v rqbit-cache:/home/rqbit/cache \
  -v rqbit-downloads:/home/rqbit/downloads \
  rqbit
```

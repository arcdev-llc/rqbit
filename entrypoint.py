#!/usr/bin/env python3
import os
import sys


def get_env_bool(key, default=None):
    val = os.getenv(key)
    if val is None:
        return default
    return val.lower() in ('1', 'true', 'yes', 'on')


RQBIT_ARG_MAPPING = [
    ('RQBIT_LOG_FILE', '--log-file', None),
    ('RQBIT_LOG_FILE_RUST_LOG', '--log-file-rust-log', None),
    ('RQBIT_TRACKER_REFRESH_INTERVAL', '--tracker-refresh-interval', '1800'),
    ('RQBIT_HTTP_API_LISTEN_ADDR', '--http-api-listen-addr', '0.0.0.0:3030'),
    ('RQBIT_PEER_CONNECT_TIMEOUT', '--peer-connect-timeout', '10'),
    ('RQBIT_PEER_READ_WRITE_TIMEOUT', '--peer-read-write-timeout', '30'),
    ('RQBIT_LISTEN_PORT', '--listen-port', '4240'),
    ('RQBIT_UPNP_SERVER_FRIENDLY_NAME', '--upnp-server-friendly-name', 'rqbit-docker'),
    ('RQBIT_CONCURRENT_INIT_LIMIT', '--concurrent-init-limit', '10'),
    ('RQBIT_DHT_BOOTSTRAP', '--dht-bootstrap-addrs', None),
    ('RQBIT_RUNTIME_WORKER_THREADS', '--worker-threads', None),
    ('RQBIT_LISTEN_IP', '--listen-ip', None),
    ('RQBIT_BIND_DEVICE', '--bind-device', None),
    ('RQBIT_RUNTIME_MAX_BLOCKING_THREADS', '--max-blocking-threads', None),
    ('RQBIT_DEFER_WRITES_UP_TO', '--defer-writes-up-to', None),
    ('RQBIT_SOCKS_PROXY_URL', '--socks-url', None),
    ('RQBIT_UMASK', '--umask', None),
    ('RQBIT_RATELIMIT_DOWNLOAD', '--ratelimit-download', None),
    ('RQBIT_RATELIMIT_UPLOAD', '--ratelimit-upload', None),
    ('RQBIT_BLOCKLIST_URL', '--blocklist-url', None),
    ('RQBIT_ALLOWLIST_URL', '--allowlist-url', None),
    ('RQBIT_TRACKERS_FILENAME', '--trackers-filename', None),
]

RQBIT_FLAG_MAPPING = [
    ('RQBIT_HTTP_API_ALLOW_CREATE', '--http-api-allow-create'),
    ('RQBIT_SINGLE_THREAD_RUNTIME', '--single-thread-runtime'),
    ('RQBIT_DHT_DISABLE', '--disable-dht'),
    ('RQBIT_DHT_PERSISTENCE_DISABLE', '--disable-dht-persistence'),
    ('RQBIT_TCP_LISTEN_DISABLE', '--disable-tcp-listen'),
    ('RQBIT_TCP_CONNECT_DISABLE', '--disable-tcp-connect'),
    ('RQBIT_EXPERIMENTAL_UTP_LISTEN_ENABLE', '--experimental-enable-utp-listen'),
    ('RQBIT_UPNP_PORT_FORWARD_DISABLE', '--disable-upnp-port-forward'),
    ('RQBIT_EXPERIMENTAL_MMAP_STORAGE', '--experimental-mmap-storage'),
    ('RQBIT_DISABLE_UPLOAD', '--disable-upload'),
    ('RQBIT_LSD_DISABLE', '--disable-lsd'),
    ('RQBIT_TRACKERS_DISABLE', '--disable-trackers'),
]

RQBIT_FLAG_WITH_DEFAULT = [
    ('RQBIT_UPNP_SERVER_ENABLE', '--enable-upnp-server', True),
]

SERVER_ARG_MAPPING = [
    ('RQBIT_SESSION_PERSISTENCE_LOCATION', '--persistence-location', None),
    ('RQBIT_FASTRESUME', '--fastresume', None),
    ('RQBIT_WATCH_FOLDER', '--watch-folder', None),
]

SERVER_FLAG_MAPPING = [
    ('RQBIT_SESSION_PERSISTENCE_DISABLE', '--disable-persistence'),
]


def build_args_from_mapping(arg_mapping, flag_mapping, flag_with_default):
    args = []
    
    for env_key, arg_name, default in arg_mapping:
        val = os.getenv(env_key, default)
        if val:
            args.extend([arg_name, val])
    
    for env_key, arg_name in flag_mapping:
        if get_env_bool(env_key):
            args.append(arg_name)
    
    for env_key, arg_name, default in flag_with_default:
        if get_env_bool(env_key, default):
            args.append(arg_name)
    
    return args


def build_rqbit_args():
    return build_args_from_mapping(RQBIT_ARG_MAPPING, RQBIT_FLAG_MAPPING, RQBIT_FLAG_WITH_DEFAULT)


def build_server_args():
    return build_args_from_mapping(SERVER_ARG_MAPPING, SERVER_FLAG_MAPPING, [])

def main():
    cmd = sys.argv[1:] if len(sys.argv) > 1 else ['server', 'start', '/home/rqbit/downloads']
    
    rqbit_args = build_rqbit_args()
    
    full_cmd = ['/usr/local/bin/rqbit'] + rqbit_args
    
    if len(cmd) >= 2 and cmd[0] == 'server' and cmd[1] == 'start':
        server_args = build_server_args()
        full_cmd.extend(cmd[:2])
        full_cmd.extend(server_args)
        if len(cmd) > 2:
            full_cmd.extend(cmd[2:])
    else:
        full_cmd.extend(cmd)
    
    os.execvp('/usr/local/bin/rqbit', full_cmd)

if __name__ == '__main__':
    main()


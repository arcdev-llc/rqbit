#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import NoReturn, Sequence


@dataclass(frozen=True)
class ArgOption:
    env: str
    flag: str
    default: str | None = None


@dataclass(frozen=True)
class BoolFlag:
    env: str
    flag: str
    default: bool | None = None  # None means "only set if env is present"


def _get_env_bool(key: str, default: bool | None = None) -> bool | None:
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ('1', 'true', 'yes', 'on')


def build_args(
    options: Sequence[ArgOption],
    flags: Sequence[BoolFlag],
) -> list[str]:
    args: list[str] = []

    # Environment variables that map to "--flag value" style options
    for opt in options:
        value = os.getenv(opt.env, opt.default)
        if value:
            args.extend([opt.flag, value])

    # Environment variables that map to "--flag" style booleans
    for flg in flags:
        if _get_env_bool(flg.env, flg.default):
            args.append(flg.flag)

    return args


RQBIT_OPTIONS: list[ArgOption] = [
    ArgOption('RQBIT_LOG_FILE', '--log-file'),
    ArgOption('RQBIT_LOG_FILE_RUST_LOG', '--log-file-rust-log'),
    ArgOption('RQBIT_TRACKER_REFRESH_INTERVAL', '--tracker-refresh-interval', '1800'),
    ArgOption('RQBIT_HTTP_API_LISTEN_ADDR', '--http-api-listen-addr', '0.0.0.0:3030'),
    ArgOption('RQBIT_PEER_CONNECT_TIMEOUT', '--peer-connect-timeout', '10'),
    ArgOption('RQBIT_PEER_READ_WRITE_TIMEOUT', '--peer-read-write-timeout', '30'),
    ArgOption('RQBIT_LISTEN_PORT', '--listen-port', '4240'),
    ArgOption('RQBIT_UPNP_SERVER_FRIENDLY_NAME', '--upnp-server-friendly-name', 'rqbit-docker'),
    ArgOption('RQBIT_CONCURRENT_INIT_LIMIT', '--concurrent-init-limit', '10'),
    ArgOption('RQBIT_DHT_BOOTSTRAP', '--dht-bootstrap-addrs'),
    ArgOption('RQBIT_RUNTIME_WORKER_THREADS', '--worker-threads'),
    ArgOption('RQBIT_LISTEN_IP', '--listen-ip'),
    ArgOption('RQBIT_BIND_DEVICE', '--bind-device'),
    ArgOption('RQBIT_RUNTIME_MAX_BLOCKING_THREADS', '--max-blocking-threads'),
    ArgOption('RQBIT_DEFER_WRITES_UP_TO', '--defer-writes-up-to'),
    ArgOption('RQBIT_SOCKS_PROXY_URL', '--socks-url'),
    ArgOption('RQBIT_UMASK', '--umask'),
    ArgOption('RQBIT_RATELIMIT_DOWNLOAD', '--ratelimit-download'),
    ArgOption('RQBIT_RATELIMIT_UPLOAD', '--ratelimit-upload'),
    ArgOption('RQBIT_BLOCKLIST_URL', '--blocklist-url'),
    ArgOption('RQBIT_ALLOWLIST_URL', '--allowlist-url'),
    ArgOption('RQBIT_TRACKERS_FILENAME', '--trackers-filename'),
]

RQBIT_FLAGS: list[BoolFlag] = [
    BoolFlag('RQBIT_HTTP_API_ALLOW_CREATE', '--http-api-allow-create'),
    BoolFlag('RQBIT_SINGLE_THREAD_RUNTIME', '--single-thread-runtime'),
    BoolFlag('RQBIT_DHT_DISABLE', '--disable-dht'),
    BoolFlag('RQBIT_DHT_PERSISTENCE_DISABLE', '--disable-dht-persistence'),
    BoolFlag('RQBIT_TCP_LISTEN_DISABLE', '--disable-tcp-listEN'),
    BoolFlag('RQBIT_TCP_CONNECT_DISABLE', '--disable-tcp-connect'),
    BoolFlag('RQBIT_EXPERIMENTAL_UTP_LISTEN_ENABLE', '--experimental-enable-utp-listen'),
    BoolFlag('RQBIT_UPNP_PORT_FORWARD_DISABLE', '--disable-upnp-port-forward'),
    BoolFlag('RQBIT_EXPERIMENTAL_MMAP_STORAGE', '--experimental-mmap-storage'),
    BoolFlag('RQBIT_DISABLE_UPLOAD', '--disable-upload'),
    BoolFlag('RQBIT_LSD_DISABLE', '--disable-lsd'),
    BoolFlag('RQBIT_TRACKERS_DISABLE', '--disable-trackers'),
    # Flags with defaults baked in
    BoolFlag('RQBIT_UPNP_SERVER_ENABLE', '--enable-upnp-server', default=True),
]

SERVER_OPTIONS: list[ArgOption] = [
    ArgOption('RQBIT_SESSION_PERSISTENCE_LOCATION', '--persistence-location'),
    ArgOption('RQBIT_FASTRESUME', '--fastresume'),
    ArgOption('RQBIT_WATCH_FOLDER', '--watch-folder'),
]

SERVER_FLAGS: list[BoolFlag] = [
    BoolFlag('RQBIT_SESSION_PERSISTENCE_DISABLE', '--disable-persistence'),
]


def parse_command(argv: Sequence[str]) -> list[str]:
    if argv:
        return list(argv)
    # Default command when no arguments are given
    return ['server', 'start', '/home/rqbit/downloads']


def is_server_start(cmd: Sequence[str]) -> bool:
    return len(cmd) >= 2 and cmd[0] == 'server' and cmd[1] == 'start'


def build_full_command(cmd: Sequence[str]) -> list[str]:
    base = ['/usr/local/bin/rqbit']
    rqbit_args = build_args(RQBIT_OPTIONS, RQBIT_FLAGS)

    if is_server_start(cmd):
        server_args = build_args(SERVER_OPTIONS, SERVER_FLAGS)
        # ['server', 'start'] + server flags + remaining user args (e.g. path)
        return base + rqbit_args + list(cmd[:2]) + server_args + list(cmd[2:])

    return base + rqbit_args + list(cmd)


def main() -> NoReturn:
    cmd = parse_command(sys.argv[1:])
    full_cmd = build_full_command(cmd)
    os.execvp(full_cmd[0], full_cmd)


if __name__ == '__main__':
    main()

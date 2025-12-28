# ---------- Toolchain / Build Stage ----------
FROM debian:12-slim AS toolchain

LABEL org.opencontainers.image.source="https://github.com/arcdev-llc/rqbit"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get -y --no-install-recommends install \
        curl \
        ca-certificates \
        git \
        build-essential \
        pkg-config \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

ADD https://curl.se/ca/cacert.pem /etc/ssl/cacerts.pem

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV MISE_DATA_DIR=/mise \
    MISE_CONFIG_DIR=/mise \
    MISE_CACHE_DIR=/mise/cache \
    MISE_INSTALL_PATH=/usr/local/bin/mise \
    PATH=/mise/shims:${PATH}

RUN curl -fsSL https://mise.run | sh

# ---------- Builder Stage ----------
FROM toolchain AS builder

WORKDIR /tmp

COPY .mise.toml /tmp/.mise.toml

RUN mise trust \
    && mise install \
    && mise reshim

RUN git clone --depth 1 https://github.com/ikatson/rqbit /tmp/rqbit

WORKDIR /tmp/rqbit

RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/tmp/rqbit/target \
    cargo build --release \
    && cp target/release/rqbit /usr/local/bin/rqbit

WORKDIR /
RUN rm -rf /tmp/rqbit

# ---------- Final Runtime Stage ----------
FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/rqbit /usr/local/bin/rqbit

RUN useradd -m -u 1000 rqbit \
    && mkdir -p \
        /home/rqbit/db \
        /home/rqbit/cache \
        /home/rqbit/downloads \
    && chown -R rqbit:rqbit /home/rqbit

WORKDIR /home/rqbit

ENV XDG_DATA_HOME=/home/rqbit/db \
    XDG_CACHE_HOME=/home/rqbit/cache \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

COPY entrypoint.py /usr/local/bin/entrypoint.py
RUN chmod +x /usr/local/bin/entrypoint.py

VOLUME /home/rqbit/db
VOLUME /home/rqbit/cache
VOLUME /home/rqbit/downloads

EXPOSE 3030
EXPOSE 4240

HEALTHCHECK --interval=90s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -fsSL http://localhost:3030/health || exit 1

USER rqbit

ENTRYPOINT ["python", "/usr/local/bin/entrypoint.py"]
CMD ["server", "start", "/home/rqbit/downloads"]

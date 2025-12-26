FROM debian:12-slim AS builder

ARG TARGETPLATFORM

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
ENV MISE_DATA_DIR=/mise
ENV MISE_CONFIG_DIR=/mise
ENV MISE_CACHE_DIR=/mise/cache
ENV MISE_INSTALL_PATH=/usr/local/bin/mise
ENV PATH=/mise/shims:${PATH}

RUN curl https://mise.run | sh

WORKDIR /tmp

COPY .mise.toml /tmp/.mise.toml

RUN mise trust && mise install && mise reshim
RUN git clone https://github.com/ikatson/rqbit /tmp/rqbit

WORKDIR /tmp/rqbit
RUN cargo build --release
RUN cp target/release/rqbit /usr/local/bin/rqbit

WORKDIR /
RUN rm -rf /tmp/rqbit

FROM python:3.13-slim

COPY --from=builder /usr/local/bin/rqbit /usr/local/bin/rqbit

ENV XDG_DATA_HOME=/home/rqbit/db
ENV XDG_CACHE_HOME=/home/rqbit/cache
ENV SSL_CERT_FILE=/etc/ssl/cacerts.pem

COPY entrypoint.py /usr/local/bin/entrypoint.py
RUN chmod +x /usr/local/bin/entrypoint.py

VOLUME /home/rqbit/db
VOLUME /home/rqbit/cache
VOLUME /home/rqbit/downloads

EXPOSE 3030
EXPOSE 4240

ENTRYPOINT ["/usr/local/bin/mise", "exec", "python", "--", "/usr/local/bin/entrypoint.py"]
CMD ["server", "start", "/home/rqbit/downloads"]
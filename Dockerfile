FROM arm64v8/python:3.9.9-slim-bullseye

WORKDIR /shorten

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    vsftpd \
    git \
    ffmpeg \
    curl \
    cron \
    build-essential \
    pkg-config \
    libssl-dev \
    bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Get the latest Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --profile minimal --default-toolchain stable
ENV PATH="/root/.cargo/bin:${PATH}"

COPY . /shorten

RUN mkdir /shorten/videosToUpload
COPY ./scripts/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab && \
    crontab /etc/cron.d/crontab

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN RUSTFLAGS="-C target-cpu=native" cargo build --release

ENTRYPOINT ["cron", "-f"]

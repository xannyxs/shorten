FROM arm64v8/python:3.9.9-slim-bullseye

WORKDIR /shorten

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    clang \
    make \
    vsftpd \
    git \
    libmagic-dev \
    cmake \
    ffmpeg \
    curl \
    libcurl4-openssl-dev \
    cron \
    bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Use clang if available, otherwise use gcc. (Using slim-bullseye for clang++)
RUN if [ -x "$(command -v clang)" ]; then \
        export CC=clang; \
        export CXX=clang++; \
    else \
        export CC=gcc; \
        export CXX=g++; \
    fi

COPY . /shorten

RUN mkdir /shorten/videosToUpload
COPY ./scripts/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab && \
    crontab /etc/cron.d/crontab

# CMake cannot find libmagic without link
RUN ln -s /usr/lib/x86_64-linux-gnu/libmagic.so /usr/lib/libmagic.so

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN cmake -S . -B cmake-build && \
    cmake --build cmake-build

ENTRYPOINT ["cron", "-f"]

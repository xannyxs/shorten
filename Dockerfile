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
    bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Use clang if available, otherwise use gcc
RUN if [ -x "$(command -v clang)" ]; then \
        export CC=clang; \
        export CXX=clang++; \
    else \
        export CC=gcc; \
        export CXX=g++; \
    fi

COPY . /shorten

# CMake cannot find libmagic without link
RUN ln -s /usr/lib/x86_64-linux-gnu/libmagic.so /usr/lib/libmagic.so

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN cmake -S . -B cmake-build && \
    cmake --build cmake-build

CMD tail -f /dev/null

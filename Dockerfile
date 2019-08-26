FROM ubuntu:18.04

ENV SERVICE_PATH /var/www/
ENV DEBIAN_FRONTEND noninteractive

WORKDIR $SERVICE_PATH
# Distr update
RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Install base packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    wget \
    locales \
    git \
    dpkg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set locales
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

# Install Chrome required tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libxss1 \
    xdg-utils \
    libx11-xcb1 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && rm -rf google-chrome-stable_current_amd64.deb

# Download and unpack chromedriver
RUN wget https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && rm -rf chromedriver_linux64.zip \

# Install Python 3.7
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    python3.7 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    && rm -rf /var/lib/apt/lists/*

# Update pip
RUN python3.7 -m pip install --upgrade pip

# Install requirements
ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt \
    && rm -rf requirements.txt

# Make python alias
RUN alias python=python3.7

WORKDIR $SERVICE_PATH/service

ADD ./config config
ADD ./gatherproxy_parser_web_service gatherproxy_parser_web_service
ADD ./main.py main.py

EXPOSE 80

ENTRYPOINT ["python3.7", "main.py"]

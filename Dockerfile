# Use a specific Ubuntu LTS version
FROM ubuntu:20.04

LABEL maintainer="jpmateo@gmail.com"
LABEL description="A simple gitserver"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Manila

# Update package lists and install required packages
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        openssh-server \
        vim \
        curl \
        less \
        iputils-ping \
        openssl \
        git \
        supervisor \
        python3 \
        python3-pip \
        nginx \
        fcgiwrap \
        apache2-utils \
    && rm -rf /var/lib/apt/lists/*

# Create directories and set the working directory
RUN mkdir /var/scripts /var/git /var/app
WORKDIR /var/git

# Copy required files
COPY scripts /var/scripts
COPY config/sshd_config /etc/ssh/sshd_config
COPY supervisor /etc/supervisor/conf.d
COPY nginx /etc/nginx/sites-enabled
COPY app /var/app

RUN pip install -r /var/app/requirements.txt

# Expose necessary ports
EXPOSE 80 8080 22 443

# Set executable permissions for scripts
RUN chmod -R +x /var/scripts

# Set the entrypoint
ENTRYPOINT ["/var/scripts/entrypoint.sh"]
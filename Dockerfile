# Filename: Dockerfile
FROM centos
WORKDIR /root
COPY go1.16.5.linux-amd64.tar.gz ./
RUN rm -rf /usr/local/g
RUN tar -C /usr/local -xzf go1.16.5.linux-amd64.tar.gz
RUN export PATH=$PATH:/usr/local/go/bin

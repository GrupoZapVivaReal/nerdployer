FROM python:3.7.4-slim

RUN apt-get update && apt-get -y install curl
RUN curl -L -s https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl && chmod +x /usr/local/bin/kubectl

WORKDIR /nerdployer

ADD . /nerdployer

RUN python3 -m easy_install .

ENTRYPOINT ["/usr/local/bin/nerdployer"]
CMD ["--help"]
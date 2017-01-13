FROM python:3.6-alpine

WORKDIR /nerdployer

ADD . /nerdployer

RUN apk add --update git
RUN python3 -m easy_install .

ENTRYPOINT ["/usr/local/bin/nerdployer"]
CMD ["--help"]
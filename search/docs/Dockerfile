FROM python:3.6 AS builder

WORKDIR /home
COPY . ./

RUN pip install -U pip sphinx recommonmark
RUN make html

FROM nginx:alpine
COPY default.conf htpasswd /etc/nginx/conf.d/
COPY --from=builder /home/_build/html /usr/share/nginx/html

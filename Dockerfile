FROM kong:latest
USER root
# Example for Python
# PYTHONWARNINGS=ignore is needed to build gevent on Python 3.9
RUN apk update && \
    apk add python3 py3-pip python3-dev musl-dev libffi-dev gcc g++ file make && \
    PYTHONWARNINGS=ignore pip3 install kong-pdk requests geopy
WORKDIR /opt/kong-python-pdk
COPY ./kong-python-pdk .
# reset back the defaults
USER kong
ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 8000 8443 8001 8444
STOPSIGNAL SIGQUIT
HEALTHCHECK --interval=10s --timeout=10s --retries=10 CMD kong health
CMD ["kong", "docker-start"]
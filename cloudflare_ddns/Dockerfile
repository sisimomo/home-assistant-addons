ARG BUILD_FROM
FROM $BUILD_FROM

ADD https://raw.githubusercontent.com/timothymiller/cloudflare-ddns/master/requirements.txt /tmp/requirements.txt

# Install packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libportaudio2 \
        libasound2-plugins \
        pulseaudio-utils \
        python3 \
        python3-dev \
        build-essential \
    && curl --silent --show-error --retry 5 \
        "https://bootstrap.pypa.io/get-pip.py" \
        | python3 \
    && pip3 install -r /tmp/requirements.txt \
    && apt-get remove -y --purge \
        python3-dev \
        build-essential \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ENV CONFIG_PATH=/data

# Add Python script
COPY rootfs/options_converter.py .
ADD https://raw.githubusercontent.com/timothymiller/cloudflare-ddns/master/cloudflare-ddns.py .

# Add run script
COPY rootfs/run.sh .
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
# CMD ["sleep", "5m"]

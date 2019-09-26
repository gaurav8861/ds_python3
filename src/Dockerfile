FROM openjdk:8
WORKDIR /app
COPY nuodb-ce_4.0.1.1_amd64.deb /app/

ENV NUODB_HOME /opt/nuodb
ENV BROKER true
ENV DOMAIN_USER domain
ENV DOMAIN_PASSWORD bird
ENV AGENT_PORT 48004
ENV NEW_PROCESS_PORT_RANGE 48005

ENV BROKER_ALT_ADDR #altAddr = ${BROKER_ALT_ADDR}
ENV ADVERTISE_ALT #advertiseAlt = true
ENV REGION #region =
ENV AUTOMATION false
ENV AUTOMATION_BOOTSTRAP false
ENV LOG_LEVEL log = INFO

ENV NUOAGENT_START true
ENV NUORESTSVC_START true
ENV NUOWEBCONSOLE_START true

### Install ###

# Install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
  apt-get -yq install pwgen supervisor gettext-base default-jre-headless&& \
  rm -rf /var/lib/apt/lists/*

# Install NuoDB
ADD nuodb-ce_4.0.1.1_amd64.deb  /tmp/nuodb-ce_4.0.1.1_amd64.deb
RUN dpkg -i /tmp/nuodb-ce_4.0.1.1_amd64.deb

### Configure ###

# Mount volume
RUN mkdir -p /opt/nuodb/data &&\
    mkdir -p /nuodb-override &&\
    chown nuodb:nuodb /opt/nuodb/data
VOLUME ["/opt/nuodb/data", "/nuodb-override"]
RUN chown nuodb:nuodb /opt/nuodb/data

# Add NuoDB default.properties file
ADD default.properties /opt/nuodb/etc/default.properties
#RUN rm -f /opt/nuodb/etc/default.properties

# Add Supervisor configuration files
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

### Run ###
ADD run.sh /run.sh
RUN chmod +x /run.sh

# Define working directory.
WORKDIR /opt/nuodb

CMD ["/run.sh"]
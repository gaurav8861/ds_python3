#!/bin/sh

envsubst < '/etc/supervisor/conf.d/supervisord.conf' > '/etc/supervisor/conf.d/supervisord.conf';
envsubst < '/opt/nuodb/etc/default.properties' > '/opt/nuodb/etc/default.properties';
chown nuodb:nuodb /opt/nuodb/etc/default.properties;
/usr/bin/supervisord;
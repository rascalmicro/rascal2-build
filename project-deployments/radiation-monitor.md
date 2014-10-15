### Modifications to rsyslog ###

Modify `/etc/rsyslog.conf`

Uncomment:

    $ModLoad immark

Add:

    $MarkMessagePeriod  60
    
And at the bottom of the file:

    *.*          @logs2.papertrailapp.com:43550

Then `sudo /etc/init.d/rsyslog restart`

### Make Supervisor log to syslog ###

Install `supervisor-logging` plugin

    sudo pip install supervisor-logging

Restart Supervisor.

Add to `/etc/profile`

    # Set variables so Supervisor will log to Papertrail
    
    SYSLOG_SERVER="logs2.papertrailapp.com"
    SYSLOG_PORT="43550"
    SYSLOG_PROTO="udp"
    
    export SYSLOG_SERVER
    export SYSLOG_PORT
    export SYSLOG_PROTO

The proper strings then show up `os.environ`, but this still doesn't seem to work properly.

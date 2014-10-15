### Modifications to rsyslog ###

Modify `/etc/rsyslog.conf`

Uncomment:

    $ModLoad immark

Add:

    $MarkMessagePeriod  60
    
And at the bottom of the file:

    *.*          @logs2.papertrailapp.com:43550

Then `sudo /etc/init.d/rsyslog restart`

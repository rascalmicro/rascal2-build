# Run once: ssh-keygen
#
# Append /root/.ssh/id_rsa.pub to rascalmicro.com, /home/sms/.ssh/authorized_keys
# Ensure that in /etc/ssh/sshd_config, we have: GatewayPorts yes
#
# Useful debugging commands
#
# netstat -lptu
# nc -v rascalmicro.com 12345 (tries to open TCP connection, which is first step of HTTP POST)
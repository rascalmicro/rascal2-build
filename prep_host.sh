#!/bin/sh

# Set the password. Can't log in to blank-password host with Fabric.

# New hashes can be generated in two ways:
#
# 1. Use passwd on a Rascal, copy the hash from /etc/shadow.
#
# 2. In Python, use crypt.crypt("the-new-password", "$6$salt")
# (The $6 prefix means to use the algorithm based on SHA512 rounds.)

root_hash='$6$2Bpv0ePX$DBU/1CpgTU1Rj007wwqueGmmLIxsAdBQhWFXzLEwKr5vbvXo376EmtjXwIdlDuich/twnFTJtiLCfcPcaOn7j0'
debian_hash='$6$t7VMAO0x$FY2MfREVzWT30trEoVivVhLuCA1cc99TddCXxMpWzaOctoLefiRz89kG49Ybft6UJBBsl9JHQv3EbfdoMd/5U1'

SCRIPT="usermod -p '${debian_hash}' debian; usermod -p '${root_hash}' root;"

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root beaglebone.local "${SCRIPT}"

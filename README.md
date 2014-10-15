### Other useful stuff ###

Kernel upgrade

    rm -rf /boot/uboot/App
    rm -rf /boot/uboot/.Spotlight-V100/
    rm -rf /boot/uboot/Drivers/Windows/
    rm -rf /boot/uboot/Drivers/MacOSX/

    wget --no-check-certificate https://rcn-ee.net/deb/wheezy-armhf/v3.17.0-bone4/install-me.sh
    chmod +x ./install-me.sh
    ./install-me.sh

### Setting up Rascal 2 repo with Aptly ###

Start a t2.micro instance of Ubuntu 14.04 LTS 64-bit on EC2.

Apply Ubuntu fixups from: https://github.com/pingswept/dev-log/blob/master/2014-04-ubuntu-fixups.markdown

Install `aptly`: http://www.aptly.info/download/

Generate GPG on laptop with GPG Tools from: https://gpgtools.org/

Not sure how to export keys / import to gpg keychain on EC2 instance.

Then maybe this would work?

    aptly mirror create -architectures=armhf -filter='Priority (required) | Priority (important) | Priority (standard)' wheezy-main http://ftp.ru.debian.org/debian/ wheezy main

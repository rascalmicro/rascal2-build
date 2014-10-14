***Other useful stuff***

Kernel upgrade

    wget --no-check-certificate https://rcn-ee.net/deb/wheezy-armhf/v3.17.0-bone4/install-me.sh
    chmod +x ./install-me.sh
    ./install-me.sh

    rm -rf /boot/uboot/App
    rm -rf /boot/uboot/.Spotlight-V100/
    rm -rf /boot/uboot/Drivers/Windows/
    rm -rf /boot/uboot/Drivers/MacOSX/

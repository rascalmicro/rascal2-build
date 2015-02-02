echo " "
echo "/////////////////////////////////////////"
echo "//                                     //"
echo -e "// \e[0;31mRascal Micro\e[0m                        //"
echo -e "// \e[0;31mSmall computers for art and science\e[0m //"
echo "//                                     //"
echo "/////////////////////////////////////////"
echo " "
echo -en "Successfully logged in to \e[0;31m"; uname -n ; echo -en "\e[0m"
echo -n "Linux kernel version: "; uname -r
echo -n "System time: "; date
echo -n "IP address: "; ifconfig eth0 | awk '/inet addr:/{print $2}' | cut -d: -f2
echo " "

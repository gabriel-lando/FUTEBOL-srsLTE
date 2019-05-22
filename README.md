srsLTE LandoNet
========

Build Instructions
------------------

On Ubuntu 16.04, you can install the required libraries with:
```
sudo apt-get install build-essential cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libsctp-dev uhd-host libuhd003 libuhd-dev
```

Install GCC-7 & G++-7:
```
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo apt update
sudo apt install g++-7 -y

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 --slave /usr/bin/g++ g++ /usr/bin/g++-7 
sudo update-alternatives --config gcc
```

Download, build and install Pistache: 
```
git clone https://github.com/oktal/pistache.git
cd pistache
git submodule update --init
mkdir build
cd build
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ../
make
sudo make install
sudo ldconfig
```

Download and build srsLTE: 
```
git clone https://gitlab.com/futebol/srsLTE_LandoNet.git
cd srsLTE_LandoNet
mkdir build
cd build
cmake ../
make
```

Install srsLTE:

```
sudo make install
sudo srslte_install_configs.sh service
sudo ldconfig
```

This installs srsLTE and also copies the default srsLTE config files to ```/etc/srslte```.

Execution Instructions
----------------------

The srsENB and srsEPC applications include example configuration files
that should be copied (manually or by using the convenience script) and modified,
if needed, to meet the system configuration.
On many systems they should work out of the box.

By default, all applications will search for config files in the ```/etc/srslte```
directory upon startup.

Note that you have to execute the applications with root privileges to enable
real-time thread priorities and to permit creation of virtual network interfaces.

srsENB and srsEPC can run on the same machine as a network-in-the-box configuration.

If you have installed the software suite using ```sudo make install``` and
have installed the example config files using ```sudo srslte_install_configs.sh service```,
you may just start all applications with their default parameters.

### srsEPC

On machine 1, run srsEPC as follows:

```
sudo srsepc
```

Using the default configuration, this creates a virtual network interface
named "LandoNet" on machine 1 with IP 172.16.0.1. All connected UEs
will be assigned an IP in this network.

### srsENB

Also on machine 1, but in another console, run srsENB as follows:

```
sudo srsenb
```

### Change gain

To change the Tx and Rx gain parameters, it is necessary to make a request to the address:

http://localhost:9080/gain/$TX_VALUE/$RX_VALUE

Where ```$TX_VALUE``` is the value at which the antenna gain Tx will be changed and ```$RX_VALUE``` is the value at which the gain of Rx will be changed.


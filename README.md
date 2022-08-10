# GR-CYBERRADIO

## Compatibility
This software has been built and tested against Ubuntu 16.04 and Ubuntu 18.04

## Build and Install

`git clone git@github.com:CyberRadio/gr-cyberradio.git`

### libcyberradio
    
    git clone https://github.com/CyberRadio/libcyberradio.git
    cd libcyberradio
    cmake ../ -DCMAKE_INSTALL_PREFIX=/usr
    make && sudo make install
    cd ../
    
### cyberradiodriver

    git clone https://github.com/CyberRadio/CyberRadioDriver.git
    cd cyberradiodriver
    sudo python setup.py install
    cd ../
    
### gr-CyberRadio

    git clone https://github.com/CyberRadio/gr-cyberradio.git
    cd gr-CyberRadio 
    git checkout maint-3.10
    mkdir build
    cd build
    cmake ../ -DCMAKE_INSTALL_PREFIX=/usr
    make
    sudo make install
    

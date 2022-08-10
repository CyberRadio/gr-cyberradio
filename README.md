# GR-CYBERRADIO

## Compatibility
This software has been built and tested against: 
- Ubuntu 16.04 (GNURadio 3.7.13.3) (maint-3.7)
- Ubuntu 18.04 (GNURadio 3.8.1.0)  (maint-3.8)
- Ubuntu 20.04 (GNURadio 3.10.3.0) (maint-3.10)

## Build and Install

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
    

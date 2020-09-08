# GR-CYBERRADIO

## Compatibility
This software has been built and tested against Ubuntu 16.04 and Ubuntu 18.04

## Build and Install

`git clone git@github.com:CyberRadio/gr-cyberradio.git`

### libcyberradio
    
    cd gr-cyberradio && cd libcyberradio && mkdir build && cd build
    cmake ../
    make && sudo make install
    cd ../
    
### cyberradiodriver

    cd cyberradiodriver
    sudo python setup.py install
    cd ../
    
### gr-CyberRadio

    cd gr-CyberRadio && mkdir build && cd build
    cmake ../
    make && sudo make install
    

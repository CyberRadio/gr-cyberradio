#ifndef LCR_STREAM_THROTTLE_H
#define LCR_STREAM_THROTTLE_H

#include <iostream>
#include <unistd.h>
#include <chrono>

class Throttle {

private:
    unsigned long long sample_rate;
    double MB_sent;
    double seconds_elapsed;
    double target_rate;
    std::chrono::system_clock clock;
    std::chrono::time_point<std::chrono::system_clock,std::chrono::nanoseconds> start_time;

public:
    Throttle(double);
    void throttle(unsigned int bytes_sent);
};

#endif
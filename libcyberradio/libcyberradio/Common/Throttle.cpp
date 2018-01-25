#include <LibCyberRadio/Common/Throttle.hpp>

Throttle::Throttle(double sample_rate)
{
    this->sample_rate = sample_rate;
    this->target_rate = (double)(sample_rate) * (4136/1024); // Convert from samples to bytes
    this->target_rate /= (1024*1024); // Convert to MB
    std::chrono::system_clock clock;
    this->MB_sent = 0;
    this->start_time = clock.now();
}

void Throttle::throttle(unsigned int bytes_sent)
{
    this->MB_sent += ((double)bytes_sent)/(1048576);
    std::chrono::time_point<std::chrono::system_clock,std::chrono::nanoseconds> curr_time = this->clock.now();
    std::chrono::duration<double> elapsed = curr_time - start_time;
    double current_rate = ((this->MB_sent)) / (elapsed.count());

    if (current_rate > this->target_rate) {
        usleep(1e4);
    }

}
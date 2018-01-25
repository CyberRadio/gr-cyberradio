#include <iostream>
#include <signal.h>
#include <LibCyberRadio/NDR651/TXClient.h>

static volatile int keepRunning = 1;
void intHandler(int sig) {
    keepRunning = 0;
}

int main()
{

	bool debug = true;
	signal(SIGINT, intHandler);

	/* Configuration */
	// DUC
	const std::string txInterfaceName 	= "eth2";
	unsigned int tenGbeIndex 			= 1;
	unsigned int ducChannel 			= 1;
	double attenuation 					= 0.0;
	unsigned int ducRateIndex 			= 1;
	unsigned int rfChannel 				= 1;
	unsigned short txUdpPort        	= 34567;  // Also going to use this for stream ID
	unsigned int ducFreq 				= 0;

	// TXF, SHF
	double txFreq 						= 950;
	
	// DUCHS
	double ducFullThreshPercent			= 0.90;
	double ducEmptyThreshPercent        = 0.82;
	unsigned int updatesPerSecond 		= 20;

	// Pre-compute a set of samples for transmission - a sinusoid that spans a number of frames
	const int period = 127;
	int row = 0;
	const unsigned int samplesPerFrame = 1024;
	short sampleBuffer[period][2*samplesPerFrame];
	double amplitude = 0x3fff;
	double t, re, im;
	int ind = 0;
	for (row=0; row<period; row++) {
		for (int samp=0; samp<samplesPerFrame; samp++) {
			ind = (row*samplesPerFrame) + samp;
			t = ((double)ind)/samplesPerFrame;
			re = cos( 2*M_PI*t/period );
			im = sin( 2*M_PI*t/period );
			sampleBuffer[row][2*samp] = (short)(re*amplitude);
			sampleBuffer[row][(2*samp)+1] = (short)(im*amplitude);
		}
	}

	// Create a Transmit Client
	LibCyberRadio::NDR651::TXClient *txClient = new LibCyberRadio::NDR651::TXClient("ndr651", debug);

	// Call configuration methods
	bool configSuccess = txClient->setDUCParameters(ducChannel, ducRateIndex, rfChannel);  // DUC
	configSuccess = configSuccess && txClient->setEthernetInterface(tenGbeIndex, txInterfaceName, txUdpPort);  // COM
	if (configSuccess == false)
	{
		std::cout << "Configuration Errors" << std::endl;
		return 0;
	}

	// Start Transmit Client
	txClient->start();

	// Send Frames for until someone presses CTRL+C
	unsigned long long n = 0;
	while (keepRunning != 0)
	{
		txClient->sendFrame(sampleBuffer[row], samplesPerFrame);
		row = (row + 1) % period;
	}

	// Stop Transmit Client
	txClient->stop();
	
	// Cleanup
	delete txClient;
	std::cout << "Graceful Exit" << std::endl;
}

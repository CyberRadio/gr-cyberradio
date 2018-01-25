#include <LibCyberRadio/NDR651/SyncTXClient.h>
#include <signal.h>
#include <vector>
#include <gnuradio/digital/glfsr.h>
#include <fstream>
#include <iostream>

static volatile int keepRunning = 1;
void intHandler(int sig) {
    keepRunning = 0;
}

/*
 * Simple algorithm to find the greatest common divisor.
 */
int gcd(int a, int b)
{
    for (;;)
    {
        if (a == 0) return b;
        b %= a;
        if (b == 0) return a;
        a %= b;
    }
}

/*
 * Computes the least common multiple.
 * lcm = a*b/gcd(a,b)
 */
// Computs
int lcm(int a, int b)
{
    int temp = gcd(a, b);
    return temp ? (a / temp * b) : 0;
}

int getNumberOfSamples(int degree, int ovs, int frameSize) {
	int pnLen = pow(2,degree)-1;
	int seqLen = ovs*pnLen;
	int numSamp = lcm(seqLen, frameSize);
	return numSamp;
}


// PN Sequence
std::vector< std::complex<float> > genTxSeq( unsigned int degree, unsigned int samplesPerBit, unsigned int zeroPad, float amplitude ) {
	unsigned int i, j;
	unsigned int spb = samplesPerBit>1?samplesPerBit:1;
	float sample = 0;
	unsigned int seqLen = (1<<degree)-1;
	std::vector< std::complex<float> > pnSeq( seqLen*spb+zeroPad, std::complex<float>(0,0) );
	std::vector< std::complex<float> >::iterator it = pnSeq.begin();
	gr::digital::glfsr pngen( gr::digital::glfsr::glfsr_mask(degree), 1<<(degree-1) );
	std::cout << "mask = " << gr::digital::glfsr::glfsr_mask(degree) << std::endl;
	for (i = 0; i<seqLen; i++) {
		//define sample amplitude based on bit value
		sample = pngen.next_bit()>0?amplitude:-amplitude;
		//create spb complex samples for each bit out of the PN generator
		for (j=0;j<spb;j++) {
			*it = std::complex<float>(sample,sample);
			it++;
		}
		//the preceeding loop is the same operation as:
		//	std::fill (it,it+spb,std::complex<float>(sample,sample));
		//	it += spb;
	}
	return pnSeq;
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

	// Pre-compute a PN sequence
	unsigned int degree = 10;
	//~ unsigned int numSamples = 1047552; // 1024 should be a factor of num samples
	unsigned int samplesPerBit = 8;
	const unsigned int samplesPerFrame = 1024;
	unsigned int numSamples = getNumberOfSamples(degree, samplesPerBit, samplesPerFrame);
	std::cout << "numSamples = " << numSamples << std::endl;
	float amplitude = 0x3fff;
	std::cout << "Amplitude = " << (amplitude/32767) << std::endl;
	std::vector<std::complex<float> > sampleVec = genTxSeq(degree, samplesPerBit, 0, amplitude);

	// Create the sample array
	std::ofstream outfile;
	outfile.open("/run/shm/synch_tx_sequence.ishort", std::ios::out|std::ios::binary);
	
	int row = 0;
	
	int sampleArrLen = numSamples/samplesPerFrame;
	short sampleBuffer[sampleArrLen][2*samplesPerFrame];
	int currSampleVecInd = 0;
	for (row = 0; row < sampleArrLen; row++) {
		for (int samp = 0; samp < samplesPerFrame; samp++) {
			sampleBuffer[row][2*samp] = sampleVec[currSampleVecInd].real();
			sampleBuffer[row][2*samp+1] = sampleVec[currSampleVecInd].imag();
			if ((row<10)&&(samp<samplesPerBit)) {
				std::cout << "Sample " << samp << " = " << sampleVec[currSampleVecInd].real() << "+" << sampleVec[currSampleVecInd].imag() << "j" << std::endl;
				std::cout << "\t" << sampleBuffer[row][2*samp] << "+" << sampleBuffer[row][2*samp+1] << "j" << std::endl;
			}
			currSampleVecInd = (currSampleVecInd + 1) % sampleVec.size();
			outfile.write( (char*)&sampleBuffer[row][2*samp], 2 );
			outfile.write( (char*)&sampleBuffer[row][2*samp+1], 2 );
			
		}
	}
	outfile.close();

	// Create a Transmit Client
	LibCyberRadio::NDR651::TXClient *txClient1 = new LibCyberRadio::NDR651::TXClient("ndr651", debug);
	txClient1->setDUCParameters(ducChannel, ducRateIndex, rfChannel);  // DUC
	txClient1->setEthernetInterface(tenGbeIndex, txInterfaceName, txUdpPort);  // COM

	// Create a Transmit Client
	LibCyberRadio::NDR651::TXClient *txClient2 = new LibCyberRadio::NDR651::TXClient("ndr651", debug);
	txClient2->setDUCParameters(ducChannel + 1, ducRateIndex, rfChannel + 1);  // DUC
	txClient2->setEthernetInterface(2, "eth3", txUdpPort + 1);  // COM

	// Pass clients to a SyncTXClient Wrapper
	std::vector<LibCyberRadio::NDR651::TXClient *> txClients = std::vector<LibCyberRadio::NDR651::TXClient *>();
	txClients.push_back(txClient1);
	txClients.push_back(txClient2);
	LibCyberRadio::NDR651::SyncTXClient * syncTXClient = new LibCyberRadio::NDR651::SyncTXClient(txClients, debug);

	syncTXClient->setDucGroup(2);

	// Setup the same sample payload to each client
	short *samples[2]; // array of short pointers. I C what you did there.

	// Send the samples
	syncTXClient->start();
	row = 0;
	while (keepRunning != 0)
	{
		samples[0] = sampleBuffer[row];
		samples[1] = sampleBuffer[row];
		syncTXClient->sendFrames((short **)samples, samplesPerFrame);
		row = (row+1)%sampleArrLen;
	}
	syncTXClient->stop();

	// Cleanup (SyncTX Constructor deletes TXClients)
	delete syncTXClient;

	return 0;
}

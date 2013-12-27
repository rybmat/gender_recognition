from __future__ import division
import scipy.io.wavfile
import struct
from pylab import *
from numpy import *
from scipy import *
from os import listdir
from os.path import isfile, join, splitext

def makePlots(samples):
    '''makes plots for a collection of samples
        argument: dictionary returned by loadFiles
    '''
    print "drowing plots..."
    for s in samples:
        print "processing " + s['name']
        w = s['sampleRate']
        T = 1

        n = T * w
            
        signal = s['signal'][0:n]             # funkcja sprobkowana

        print "......fft"
        signal1 = fft(signal)      
        signal1 = abs(signal1)        

        print "......plot"
        freqs = linspace(0, w, n, endpoint=False)
        plot(freqs, signal1, '-')
        xlabel("czestotliwosc probkowania")
        ylabel("liczba probek/stala")
       
        print "...saveFig"
        savefig("plots/" + s['name'] + ".pdf")
    


def loadFiles(path):
    """reads wave files from path and returns dictionary with fields:
        - "name" - name of file
        - "nameGender" - a sex readed from filename
        - "signal" - numpy array with sound signal readed from file
        - "sampleRate" - sample rate of the file

        and dictionary that contains numbers of male and female voices
    """
    print "reading files..."

    files = [ f for f in listdir(path) if isfile(join(path,f)) and splitext(f)[1] == ".wav" ]

    samples = []
    maleCount = 0
    femaleCount = 0
    for f in files:
        p = path + '/' + f

        print "...", f
        with open(p, "rb") as wavFile:
            wavFile.read(24)
            
            rate = wavFile.read(4)
            rate = struct.unpack("<i",rate)[0]
            print "......rate: ", rate
            
            wavFile.read(6)
            
            bps = wavFile.read(2)
            bps = struct.unpack("<h",bps)[0]
            print "......bps: ", bps

            wavFile.read(8)
            
            print "......reading data"
            sig = []
            sampleSize = bps/8
            b = wavFile.read(int(sampleSize))
            while b != "":
                b = struct.unpack("<h", b)
                sig.append(b[0])
                b = wavFile.read(int(sampleSize))
            
            
        samples.append({'name': f, 'nameGender': f[-5:-4], 'signal': sig, 'sampleRate': rate})
        
        if f[-5:-4] == "M":
            maleCount += 1
        else:
            femaleCount += 1
    
    counters = {"maleCount":maleCount, "femaleCount":femaleCount}
    return samples, counters

def recognizeGender(sample):
    """This function recognizes the sex of person who is speaking
        
        argument: single sample from dictionary that is returned by loadFiles
        
        returns: string - 'M' i a man is speaking, 'K' if a woman is speaking
    """
    pass

if __name__ == '__main__':
    samples, counters = loadFiles("train")
    #print samples
    print counters
    makePlots(samples)

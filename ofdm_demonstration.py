#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

def scatterPlot(complexVec):
    plt.scatter(complexVec.real, complexVec.imag)
    plt.xlabel('Real')
    plt.ylabel('Imag')
    plt.grid(True)
    plt.show()

def realAndImagPlots(complexVec, title = None):
    length = len(complexVec)
    
    yMax = max([max(complexVec.real), max(complexVec.real)])
    
    yMin = min([min(complexVec.real), min(complexVec.real)])

    maxVal = max([-yMin, yMax])

    if title:
        plt.title(title)
        
    plt.subplot(211)
    plt.plot(range(length), complexVec.real)
    plt.ylim(-maxVal - 0.25 * maxVal, maxVal + 0.25 * maxVal)
    plt.xlabel('n')
    plt.ylabel('Real')
    

    plt.subplot(212)
    plt.plot(range(length), complexVec.imag)
    plt.ylim(-maxVal - 0.25 * maxVal, maxVal + 0.25 * maxVal)
    plt.xlabel('n')
    plt.ylabel('Imag')
    
    plt.waitforbuttonpress()

def realAndImagStem(complexVec, title = None):
    length = len(complexVec)
    
    yMax = max([max(complexVec.real), max(complexVec.real)])
    
    yMin = min([min(complexVec.real), min(complexVec.real)])

    maxVal = max([-yMin, yMax])

    if title:
        plt.title(title)
        
    plt.subplot(211)
    plt.stem(range(length), complexVec.real)
    plt.ylim(-maxVal - 0.25 * maxVal, maxVal + 0.25 * maxVal)
    plt.xlabel('n')
    plt.ylabel('Real')
    

    plt.subplot(212)
    plt.stem(range(length), complexVec.imag)
    plt.ylim(-maxVal - 0.25 * maxVal, maxVal + 0.25 * maxVal)
    plt.xlabel('n')
    plt.ylabel('Imag')
    
    plt.show()

symbolMapping = {(0,0) : 1 + 1j, (0, 1) : 1 - 1j, (1, 0) : -1 + 1j, (1, 1) : -1 - 1j}

def bitSequenceToQpskSequence(bitSequence):
    numSymbols = len(bitSequence) / 2
    symbolSequence = np.empty(numSymbols, dtype=complex)
    for i in xrange(numSymbols):
        symbolSequence[i] = symbolMapping[(bitSequence[2 * i], bitSequence[2 * i + 1])]
    return symbolSequence

def bitSequenceToBpskSequence(bitSequence):
    numSymbols = len(bitSequence)
    symbolSequence = np.empty(numSymbols, dtype=complex)
    for i in xrange(numSymbols):
        symbolSequence[i] = 1 - 2 * bitSequence[i]
    return symbolSequence


def complexSignalEnergy(complexVec):
    result = 0.0
    for s in complexVec:
        result += s * np.conjugate(s)
    return result

numBits = 6
fftSize = 2 ** 12
bitSequence = np.random.random_integers(0, 1, size=numBits)
symbolSequence = bitSequenceToBpskSequence(bitSequence)

# Pad to power of 2
symbolSequence = np.pad(symbolSequence, (0, fftSize - len(symbolSequence)), 'constant', constant_values = (0))
realAndImagStem(symbolSequence[0:numBits * 2], "Freq Domain")
plt.close()

timeSignal = np.fft.ifft(symbolSequence)
timeSignal *= np.sqrt(len(timeSignal))

print "Energy in freq domain signal", complexSignalEnergy(symbolSequence)
print "Energy in time domain signal", complexSignalEnergy(timeSignal)
realAndImagPlots(timeSignal, "Time Domain Signal")
plt.close()

symbolSequence = np.zeros(numBits / 2)
symbolSequence = np.pad(symbolSequence, (0, fftSize - len(symbolSequence)), 'constant', constant_values = (0))

for i in xrange(10):
    symbolSequence[i] = 1
    if i > 0:
        symbolSequence[i-1] = 0
    timeSignal = np.fft.ifft(symbolSequence)
    timeSignal *= np.sqrt(len(timeSignal))
    realAndImagPlots(timeSignal, "Time Domain Signal")
    print "Symbol number", i
plt.show()

#!/app/vbuild/RHEL6-x86_64/python/2.7.9/bin/python

import sys
import os
sys.path.extend(["/app/vbuild/RHEL6-x86_64/python/2.7-addons-numpy/lib/python2.7/site-packages/",
                 "/app/vbuild/RHEL6-x86_64/python/2.7-addons-matplotlib/lib/python2.7/site-packages/"])

for p in sys.path:
  print p
import numpy as np
import matplotlib.pyplot as plt
def quit_figure(event):
    if event.key in ['q', 'escape', 'spacebar']:
        plt.close(event.canvas.figure)

def scatterPlot(complexVec):
    plt.scatter(complexVec.real, complexVec.imag)
    plt.xlabel('Real')
    plt.ylabel('Imag')
    plt.grid(True)
    cid = plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)
    plt.show()

def realAndImagPlots(complexVec, title = None):
    plt.figure(figsize=(16, 10))
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
    cid = plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)
    plt.show()

def realAndImagPlotsWithAccumulatedSignal(complexVec, accumulatedSig, title = None):
    plt.figure(figsize=(16, 10))
    length = len(complexVec)
    
    yMax = max([max(complexVec.real), max(complexVec.real)])
    yMin = min([min(complexVec.real), min(complexVec.real)])
    maxVal = max([-yMin, yMax])

    if title:
        plt.title(title)
        
    plt.subplot(221)
    plt.stem(range(length), complexVec.real)
    plt.ylim(-maxVal - 0.25 * maxVal, maxVal + 0.25 * maxVal)
    plt.xlabel('n')
    plt.ylabel('Real')
    
    plt.subplot(222)
    plt.stem(range(length), complexVec.imag)
    plt.ylim(-maxVal - 0.25 * maxVal, maxVal + 0.25 * maxVal)
    plt.xlabel('n')
    plt.ylabel('Imag')
    
    yMax = max([max(accumulatedSig.real), max(accumulatedSig.real)])
    yMin = min([min(accumulatedSig.real), min(accumulatedSig.real)])
    maxVal = max([-yMin, yMax])
    
    plt.subplot(223)
    plt.stem(range(length), accumulatedSig.real)
    plt.ylim(-maxVal - 0.25 * maxVal, maxVal + 0.25 * maxVal)
    plt.xlabel('n')
    plt.ylabel('Real')
    
    plt.subplot(224)
    plt.stem(range(length), accumulatedSig.imag)
    plt.ylim(-maxVal - 0.25 * maxVal, maxVal + 0.25 * maxVal)
    plt.xlabel('n')
    plt.ylabel('Imag')
    
    cid = plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)
    plt.show()
symbolMappingQpsk = {(0,0) : 1 + 1j, (0, 1) : 1 - 1j, (1, 0) : -1 + 1j, (1, 1) : -1 - 1j}

def bitSequenceToSymbolSequence(bitSequence):
    numSymbols = len(bitSequence) / 2
    symbolSequence = np.empty(numSymbols, dtype=complex)
    for i in xrange(numSymbols):
        symbolSequence[i] = symbolMappingQpsk[(bitSequence[2 * i], bitSequence[2 * i + 1])]
    return symbolSequence
  
def bitsToBpsk(bitSequence):
    numSymbols = len(bitSequence)
    symbolSequence = np.empty(numSymbols, dtype=complex)
    for i in xrange(numSymbols):
        symbolSequence[i] = 1 - 2 * bitSequence[i]
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

numBits = 240
fftSize = 2 ** 10
bitSequence = np.random.random_integers(0, 1, size=numBits)
sc_fdma = True
print "Bits to transmit", bitSequence
symbolSequence = bitSequenceToSymbolSequence(bitSequence)

print "Bits mapped to symbols", symbolSequence
# Pad to power of 2
symbolSequence = np.pad(symbolSequence, (0, fftSize - len(symbolSequence)), 'constant', constant_values = (0))
print "Mapping symbols to Subcarriers"
for i, symbol in enumerate(symbolSequence):
  print 'Subcarrier:{0:3d}'.format(i), "Symbol: ", symbol

realAndImagStem(symbolSequence[0:numBits * 2], "Freq Domain")
plt.close()

if sc_fdma:
  symbolSequence = np.fft.fft(symbolSequence[0:numBits])
  print "SC-FDMA DFT precoding step, symbolSequence length = ", len(symbolSequence)
  realAndImagPlots(symbolSequence, "Freq Domain")
  symbolSequence = np.pad(symbolSequence, (0, fftSize - len(symbolSequence)), 'constant', constant_values = (0))

  
print "Computing", fftSize, "point IFFT"
timeSignal = np.fft.ifft(symbolSequence)
timeSignal *= np.sqrt(len(timeSignal))

print "Energy in freq domain signal", complexSignalEnergy(symbolSequence)
print "Energy in time domain signal", complexSignalEnergy(timeSignal)
realAndImagPlots(timeSignal, "Time Domain Signal")
plt.close()

symbolPadded = np.zeros(fftSize, dtype = np.complex128)
accumulatedTimeSignal = np.zeros(fftSize, dtype = np.complex128)
assert(len(symbolPadded) == len(symbolSequence))
for i, s in enumerate(symbolSequence):
for i in xrange(10):
    symbolPadded[i] = s
    if i > 0:
        symbolPadded[i-1] = 0
    timeSignal = np.fft.ifft(symbolPadded)
    timeSignal *= np.sqrt(len(timeSignal))
    accumulatedTimeSignal += timeSignal
    if s == 0:
      break
    print "Plotting time-domain signal for subcarrier{0:3d}".format(i), "symbol value", s
    realAndImagPlotsWithAccumulatedSignal(timeSignal, accumulatedTimeSignal, "Time Domain Signal")

realAndImagPlots(accumulatedTimeSignal, "Time Domain Signal")

print "Energy in time domain signal", complexSignalEnergy(accumulatedTimeSignal)
mu, sigma = 0, 0.02 # mean and standard deviation
noise = np.random.normal(mu, sigma, fftSize) +1j * np.random.normal(mu, sigma, fftSize)
timeSignalWithNoise = accumulatedTimeSignal + noise

print "Time Domain Signal With Noise"

freqSignalWithNoise = np.fft.fft(timeSignalWithNoise)

print "Freq Domain Signal With Noise"
realAndImagPlotsWithAccumulatedSignal(freqSignalWithNoise, symbolSequence, "Time Domain Signal With Noise")

detectedBits = np.zeros(numBits, dtype=np.int)
for i in xrange(numBits):
  if freqSignalWithNoise[i] < 0:
    detectedBits[i] = 1
  else:
    detectedBits[i] = 0

print "Detected the bits: ", detectedBits

numBits = 32
fftSize = 2 ** 7
compoundSignal = np.array([])
numAttempts = 100
for i in xrange(numAttempts):
  bitSequence = np.random.random_integers(0, 1, size=numBits)
  symbolSequence = np.pad(symbolSequence, (0, fftSize - len(symbolSequence)), 'constant', constant_values = (0))
  


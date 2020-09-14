import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np


class MusicPiece():
    def __init__(self,path, name): #kontruktor
        #max_time = 16 #s, maksymalna dlugosc pliku - wydajnosc        
        
        self.fs, stereo = wavfile.read(path) 
        self.signal = stereo[:, 0] #only one channel is needed              
        self.title = name
        self.tempo = 0
        self.time_taken = 0
        self.find_tempo()            

    def plot_wave(self):
        #Plot a basic waveform
        
        time = np.arange(len(self.signal)) / self.fs
        plt.ylabel('Amplitude')  
        plt.xlabel('Time [s]')
        plt.plot(time ,self.signal)
    
    def plot_fft_semilog(self):
         #Plot a frequency based, semi-log waveform
         
        N = len(self.signal)
        freqs = self.fs*np.arange((N/2))/N

        signal_fft = np.fft.fft(self.signal)[0:int(N/2)]/N
        signal_fft[1:] = 2*signal_fft[1:]
        signal_fft = np.abs(signal_fft)
    
        print("FS: ", self.fs)
        print("Rozdzielczosc:", self.fs/(N), " Hz")
        fig,ax = plt.subplots() 
        plt.plot(freqs,signal_fft)
        ax.set_xscale('log')        
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency [Hz]')
        plt.show()
        
    def find_tempo(self):
        pass
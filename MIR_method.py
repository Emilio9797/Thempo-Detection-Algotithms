from . import MusicPiece
import numpy as np
from scipy.signal import hilbert
import time
import scipy


class MusicPiece_MIR(MusicPiece):   
    
    def Hilbert(self, signal):     
        analytical_signal = hilbert(signal)
        amplitude_envelope = np.abs(analytical_signal)

        return amplitude_envelope
    
    
    def bandpass_filter(self, low_freq, high_freq):
        order = 1
        fs = self.fs
        signal = self.signal
        low_cutoff = low_freq *2 / fs
        high_cutoff = high_freq *2 / fs
        
        b,a = scipy.signal.butter(order, [low_cutoff, high_cutoff] , btype='band')        
        result = scipy.signal.lfilter(b,a,signal)
    
        return result
    
    
    @staticmethod
    def diff_HWR(signal):
        diff_hwr = np.abs(np.gradient(signal))
        diff_hwr[0:1000] = 0
        diff_hwr[len(diff_hwr) - 1000 : len(diff_hwr)] = 0
        #zabezpieczneie przed wysokimi wartosicami na koncu i poczatku, wynika  z nieliniowosci filtracji
        
        return diff_hwr
    
   
    def autocorelate(self, signal):        
        tempo_max = 180
        tempo_min =50
        autocored = np.correlate(signal,signal, mode = 'same')       
        
        #Usuniecie ujemnych indeksów:
        N = len(autocored)        
        half = autocored[N//2:]
        
        #Korekta wartosci dla wysokich indeksów:
        lengths = range(N, N//2, -1)
        half /= lengths
        
        #pominięcie ineksów nieistotnych w kontekcie analizy tempa:  
        half[0:np.round(np.int(self.fs*60/tempo_max))] = 0
        half_short = []
        half_short = half[0 : np.round(np.int(self.fs*60/tempo_min)) ]      
        
        return half_short        
    
                 
    def find_tempo(self): 
        print("Robie MIR: ", self.title)
        start = time.time()        
        freq_window = 10 #Hz
        freq_max = 130 #Hz, maksymalna badana częsottliwosc, c trojkreslne
        signal_filtered_diff = [] #lista list przefiltrownaego sygnału
        signal_sumed = []
        
        for i in range(2,np.int(freq_max/freq_window)): # i = 2, fstart = 40 Hz            
            signal_filtered_diff.append(self.diff_HWR(self.Hilbert(self.bandpass_filter(i*freq_window +1,(i+ 1) * freq_window))))
        signal_sumed = np.sum(signal_filtered_diff, axis=0)
        

        periodogram = list(self.autocorelate(signal_sumed)) 
        treshold = 0.1
# =============================================================================
#        Check 'Harmonic Tempos' issue      
# =============================================================================
        self.tempo =  np.round(60 * self.fs / periodogram.index(max(periodogram)))
        if periodogram[int(np.round(periodogram.index(max(periodogram)))/2)] / max(periodogram) > (1 - treshold) :
            self.tempo = np.round(60 * self.fs / periodogram.index(periodogram[int(np.round(periodogram.index(max(periodogram)))/2)]))
            print("Ponizej trehsold!!:")    
        stop = time.time()              
        
        self.time_taken = np.round(stop - start, 2)
        print("tempo to: ",self.tempo, "  Dla utoworu: ", self.title, "W czasie: ", self.time_taken)
         
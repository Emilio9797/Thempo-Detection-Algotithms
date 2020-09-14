from . import MusicPiece
import numpy as np
import time


class MusicPiece_FFT(MusicPiece):          
    
    def find_tempo(self):  
        max_time = 32 #s, maksymalny czas analizowania sygnalu
        if len(self.signal) > max_time * self.fs:
            self.signal = self.signal[0:max_time*self.fs]       
        
        #basic data, ensuring efficency of algorithm
        min_no_of_windows = 16 
        min_bpm  = 50
        max_bpm = 180
        min_no_winodws_genereted = len(self.signal) / self.fs *min_bpm / 60
        
        #check min number of windows:
        if min_no_winodws_genereted  < min_no_of_windows:
            self.tempo =  -1
            self.time_taken = -10
            print("Piece: ", self.title, " too short to analyze!")
        else:
            start = time.time()         
            
            #those variables can vary for measure / general efficiency
            step = 3
            init_step = 0
            summed_vector = []
            
            for bpm in range(min_bpm, max_bpm): 
                
                fft_segment_buffer_len, foo_freqs = self.fft_segments(bpm)             
                i = 0
                sumed_bpm = 0
                
                while init_step + (i+1)*step < len(fft_segment_buffer_len) - 1:
                    
                    fft_segment_buffer, foo_freqs = self.fft_segments(bpm)                                                 
                    sumed_bpm += self.compare_fft(fft_segment_buffer[init_step + i*step], fft_segment_buffer[init_step + (i+1)*step])
                    i +=1
                
                summed_vector.append(sumed_bpm)   
             
 
            stop = time.time()
            
            self.tempo = summed_vector.index(min(summed_vector)) + min_bpm            
            self.tempo = MusicPiece_FFT.check_harmonic_bpm(min_bpm, summed_vector, summed_vector.index(min(summed_vector)))               
            self.time_taken = np.round(stop - start, 2)
            

    def fft_get_amps(self, fs, signal):        

#       Return list, containing amplitude value for each frequency  

            
        N = len(signal)
        
        signal_fft = np.fft.fft(signal)[0:int(N/2)]/N
        signal_fft[1:] = 2*signal_fft[1:]
        signal_fft = np.abs(signal_fft)           
        
        return signal_fft
    

    def fft_get_freqs(self,fs, signal):
        N = len(signal)
        return fs*np.arange((N/2) - 1)/N
        
    
    def segment (self, bpm):
        
        fs = self.fs
        signal = self.signal
        samples_in_frame = int(round(fs * 60 / bpm))        
        signal_segmented = []        
        no_of_frames = int(round(len(signal) / samples_in_frame) - 1)
            
        for i in range(0, no_of_frames):
            #sprawia, ze zawsze bierze przedzial od 1:no_of_frames, potem 1+no_ff: 2*no_ff itp...
            signal_segmented.append(signal[i*samples_in_frame +1 : (1 +i) *samples_in_frame ])
        
        return signal_segmented
    
    
    def fft_segments(self, bpm):
        #returns list of amplitudes and corepsonging frequencies
        fs = self.fs      
        signal_seg = self.segment(bpm)
        segment_amps = []
        i = 0
       
        while i < len(signal_seg):           
            segment_amps.append(self.fft_get_amps(fs, signal_seg[i]))
            i += 1
        freqs  = 0
        
        return segment_amps, freqs
    

    def compare_fft (self, fft_amps1, fft_amps2):        
        i = 0
        difference = []
        for i in range(0, np.int(np.round(len (fft_amps1)/10))):
        
            buffer = ( (fft_amps1[i] - fft_amps2[i]))
            difference.append(buffer**2)
            
        
        suma = sum(difference)
        suma /=  len(difference)
        return suma
    
    
    @staticmethod
    def check_harmonic_bpm(min_bpm, summed_vector, min_value_index, order=2):        
# =============================================================================
#         min_bpm         - najmniejsze tempo dla badanego zakresu
#         summed_vector   - lista wskaźników prawdopodobieństwa
#         min_value_index - indeks najmniejszego znalezionego tempa
#         treshold        - próg okreslający maksymalną wartoc wskaźnika dla temp harmonicznych#         
# =============================================================================
        treshold = 0.1
        
        next_value_index = order * (min_value_index + min_bpm) - min_bpm
        current_value_index = (order-1) * (min_value_index + min_bpm) - min_bpm
       
        if  next_value_index > len(summed_vector) - 1:            
            tempo = summed_vector.index(summed_vector[current_value_index]) + min_bpm
            
            if summed_vector[current_value_index - 1] < summed_vector[current_value_index]:
                tempo += -1
            if summed_vector[current_value_index+ 1] < summed_vector[current_value_index]:
                tempo += 1
                
            return tempo
        
        if summed_vector[next_value_index] /max(summed_vector)  > treshold :           
            tempo = summed_vector.index(summed_vector[current_value_index]) + min_bpm
            
            if summed_vector[current_value_index - 1] < summed_vector[current_value_index]:
                tempo += -1
            if summed_vector[current_value_index + 1] < summed_vector[current_value_index]:
                tempo += 1
            
            return tempo
        
        order +=1    
        return MusicPiece_FFT.check_harmonic_bpm(min_bpm, summed_vector, min_value_index, order)              

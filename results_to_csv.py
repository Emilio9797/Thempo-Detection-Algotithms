import csv
from . import MusicPiece_MIR, MusicPiece_FFT
import os


class TempoFinder():    
      
    def tempo_MIR(self, path_read, title_write):
        results = []        
        dir_list = os.listdir(path_read)
        
        for i in range(0,len(dir_list)-1):
            results.append(MusicPiece_MIR(path_read + dir_list[i], dir_list[i]))       
    
        TempoFinder.write_results(title_write, 'MIR', results)        
    
    def tempo_FFT(self,path_read, title_write):
        results = []
        dir_list = os.listdir(path_read)
        
        for i in range(0,len(dir_list)-1):
           results.append(MusicPiece_FFT(path_read + dir_list[i], dir_list[i]))
           
        TempoFinder.write_results(title_write, 'FFT', results)
        
    @staticmethod
    def write_results(results_title_write, method_name, results):        
        with open(results_title_write, 'w', newline='') as csvfile:
            fieldnames = ['METODA', 'TEMPO', 'CZAS', 'TYTUŁ' ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()        
            
        for i in range(0, len(results)):        
            writer.writerow({'METODA': method_name, 'TEMPO': results[i].tempo, 'CZAS': results[i].time_taken, 'TYTUŁ': results[i].title})
                          

#path = "insert/path/where/.wav/files/are/located"  
TempoFinder.tempo_FFT(path, 'tempo_fft_results')
TempoFinder.tempo_MIR(path, 'tempo_MIR_results')
import time
import os
import pandas as pd
from psutil import process_iter

from text_processing.TextProcessing import TextProcessing
class TextHandle():    

        #IMPORTAÇÃO DA BASE DE DADOS 
    def readData(self, fileName = 'BaseDadosNew', extension = "csv"):  
        try:
            filepath = f'{fileName}.{extension}'
            data = pd.read_csv(filepath, sep=',')
            print(f'Quantidade de registros encontrados: {len(data)}')
            data = data.dropna()
            print(f'Quantidade de registros válidos carregados: {len(data)}')
            return data
        except:
            print.error('Falha ao ler arquivo!')
            return None

    def handle_batch_processing(self):
            
            start = time.time()
            data_filter = self.readData()
            SIZE = len(data_filter)
            batch_size =  int(SIZE / os.cpu_count())
            process_list = []
            
            print(f'Lotes: {batch_size}')
            print(f'Threads Disponíveis: {os.cpu_count()}')
            previous = 0
            for sequence in range(batch_size, SIZE, batch_size):
                print('Sequencia:' + str(sequence))
                text_process = TextProcessing()
                if(sequence + batch_size <= SIZE):
                    text_process.data_filter = data_filter.iloc[previous:sequence]
                    text_process.start()
                    process_list.append(text_process)
                else:
                    text_process.data_filter = data_filter[previous:SIZE] 
                    text_process.start()
                    process_list.append(text_process)

                previous = sequence

            print('Aguardando conclusão do processamento')

            for thread in process_list:
                thread.join()
            tempo = time.time() - start
            print(f'Tempo thread: {tempo}')

    def handle_single_processing(self):
            
            start = time.time()
            data_filter = self.readData()
            text_process = TextProcessing()
            text_process.data_filter = data_filter
            text_process.start()

            tempo = time.time() - start
            print(f'Tempo sequencial: {tempo}')
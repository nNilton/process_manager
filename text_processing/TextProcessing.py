import threading
import re

class TextProcessing(threading.Thread):

    data_filter = None

    def run(self):
        data_filter = self.preproccessDataFrame(self.data_filter)

    def preproccessDataFrame(self, dataFrame, targetColumns = ['PEDIDO']):
        if(not dataFrame.empty):
            #print(f'Processando data frame. Quantidade de colunas a serem tratadas {len(targetColumns)}')
            for columnItem in targetColumns:
                #print(f'Pré-processando coluna: {columnItem}')
                #print(dataFrame[columnItem])
                dataFrame[columnItem] = dataFrame[columnItem].map(lambda x: x.lower())
                dataFrame[columnItem] = self.applyRegex(dataFrame, column = columnItem)
                dataFrame[columnItem] = self.filterWordsByLength(dataFrame, column = columnItem)

                dfReturn = dataFrame.dropna(subset=targetColumns, axis=0) #remover dps
                thID = threading.get_ident()
                dfReturn.to_csv(f'perguntasProcessadas{thID}.csv')
                return dfReturn
        print('Data frame vazio')
        return None


    def applyRegex(self, dataFrame, column):
        dfSize = len(dataFrame)
        coluna_tmp = [0] * dfSize
        for i in range(dfSize):
            coluna_tmp[i] = dataFrame.iloc[i][column]
            letra_sem_acento = "a"
            coluna_tmp[i] = re.sub(r'([áàãâ])', letra_sem_acento, str(coluna_tmp[i]))
            letra_sem_acento = "e"
            coluna_tmp[i] = re.sub(r'([éê])', letra_sem_acento, str(coluna_tmp[i]))
            letra_sem_acento = "i"
            coluna_tmp[i] = re.sub(r'([í])', letra_sem_acento, str(coluna_tmp[i]))
            letra_sem_acento = "o"
            coluna_tmp[i] = re.sub(r'([óôõ])', letra_sem_acento, str(coluna_tmp[i]))
            letra_sem_acento = "u"
            coluna_tmp[i] = re.sub(r'([ú])', letra_sem_acento, str(coluna_tmp[i]))
            letra_sem_acento = "c"
            coluna_tmp[i] = re.sub(r'([ç])', letra_sem_acento, str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'[/(){}\[\]\|@,;]', '', str(coluna_tmp[i]))
            coluna_tmp[i] = re.sub(r'([/\"-.,;:º@!?&%1234567890])', '', str(coluna_tmp[i]))
        return coluna_tmp

    def filterWordsByLength(self, dataFrame, column, length = 3):
        dfSize = len(dataFrame)
        coluna_tmp = [0] * dfSize
        for i in range(dfSize):
            str_data = dataFrame.iloc[i][column]
            tokens = str(str_data).split()
            word_tmp = ""
            for word in tokens:
                if len(word) > length:
                    word_tmp = word_tmp + " " + word
            coluna_tmp[i] = word_tmp
        return coluna_tmp
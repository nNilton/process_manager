import threading
import re
import spacy
import pt_core_news_sm

nlp = pt_core_news_sm.load()

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

                dfReturn = self.proccessTokensDf(dfReturn, column = 'PEDIDO')


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

    def lemmatize(self, dataFrame, columnName):
        print(f'Aplicando Lemmatização')
        lemmaWords = []
        for pedido in dataFrame[columnName]:
            doc = nlp(''.join(str(item) for item in pedido))
            temp = ''
            for token in doc:
                temp = temp + ' ' + token.lemma_
                lemmaWords.append(temp.strip())
        print(f'Lemmatização concluído(a)')
        return lemmaWords

    def stemmer(self, dataFrame, columnName):
        print(f'Aplicando RSLPStemmer')
        stemmer = RSLPStemmer()
        tam_length = len(dataFrame)
        coluna_tmp = [0] * tam_length
        for i in range(tam_length):
            doc = nlp(str(dataFrame.iloc[i][columnName]))
            tokens = doc.text.split()
            temp = ""
            for token in tokens:
                if token != "nan":
                    temp = temp + " " + stemmer.stem(token)

            coluna_tmp[i] = temp.strip()
        print(f'RSLPStemmer concluído(a)')
        return coluna_tmp

    def removeStopWords(self, dataFrame, columnName):
        print(f'Removendo stopwords')
        tam_length = len(dataFrame)
        coluna_tmp = [0] * tam_length
        for i in range(tam_length):
            coluna_tmp[i] = removeStopWordsAux(str(dataFrame.iloc[i][columnName]))
        print(f'Stopwords removidas')
        return coluna_tmp

    def removeStopWordsAux(self, sentence):
            stopwords = nltk.corpus.stopwords.words('portuguese')
            phrase = []
            for word in sentence.split(' '):
                if word not in stopwords:
                    phrase.append(word)
            return ' '.join(str(item) for item in phrase)

    def proccessTokensDf(self, dataFrame, column = 'PEDIDO'):
        dataFrame[column] = self.lemmatize(dataFrame, column)
        dataFrame[column] = self.stemmer(dataFrame, column)
        dataFrame[column] = self.removeStopWords(dataFrame, column)
        dataFrame[column] = dataFrame[column].map(lambda x: x.lower()) ####NO LUGAR DE DATA_FILTER DEVERIA SER DATAFRAME N???
        return dataFrame
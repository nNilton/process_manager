#Test your code here
from random import randint
import threading
import time
import os


class CPFThread(threading.Thread):

    batch_size = 0
        
    def generate_random_sequence(self):
        #gera sequencia de 11 digitos aleatória
        return ''.join(["{}".format(randint(0, 9)) for num in range(0, 11)])
    
    def run(self):
        sequence_list = []
        for sequence in range(self.batch_size):
            sequence_list = self.generate_random_sequence() + '\n'

        with open('teste.txt', 'a') as f:
            f.writelines(sequence_list)

class CPFValidator(threading.Thread):

    cpf = ''

    def validate_cpf(self, cpf):
        cpf = str(cpf)
        # Obtém apenas os números do CPF, ignorando pontuações
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se o CPF possui 11 números ou se todos são iguais:
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def run(self):
        if(self.validate_cpf(cpf)):
            print(f'CPF Valido')
        
            



class CPFHandler: 

    def __init__(self, size = 100) -> None:
        self.SIZE = size
        self.cpf_sequence = []

    def generate_n_sequence_thread(self):
        start = time.time()
        batch_size =  int(self.SIZE / os.cpu_count())
        print(f'Lotes: {batch_size}')
        print(f'Threads: {os.cpu_count()}')
        for sequence in range(10000000000, 10000100000):
            print('Sequencia:' + str(sequence))
            cpf_thread = CPFValidator()
            cpf_thread.cpf = str(sequence)
            cpf_thread.start()
            '''if(self.fvalidate_cpf(sequence)):
                print(f'Valido')'''

        
        tempo = time.time() - start
        print(f'Tempo thread: {tempo}')


    def generate_n_sequence(self):
        start = time.time()
        for sequence in range(self.SIZE):
            self.generate_random_sequence()
        
        tempo = time.time() - start
        print(f'Tempo seq: {tempo}')
            
    
    def generate_random_sequence(self):
        #gera sequencia de 11 digitos aleatória
        return ''.join(["{}".format(randint(0, 9)) for num in range(0, 11)])

    def fvalidate_cpf(self, cpf):
        cpf = str(cpf)
        # Obtém apenas os números do CPF, ignorando pontuações
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se o CPF possui 11 números ou se todos são iguais:
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True


cpf = CPFHandler()

#cpf.generate_n_sequence()
cpf.generate_n_sequence_thread()


import multiprocessing
from multiprocessing import Pool
import csv
import string
import sys

# Process Large file using Multiprocessing in Python


class AtbashCipherEncryption(object):

    def __init__(self):
        self.results = []
    
    def cipher_encryption(self, sentence):
        """
        @param : sentence containing string data for cipher encryption
        @return : cipher encryption text
        """
        upper_cipher = {k:v for k, v in zip(string.ascii_uppercase, string.ascii_uppercase[::-1])}
        lower_cipher = {k:v for k, v in zip(string.ascii_lowercase, string.ascii_lowercase[::-1])}

        list_sentence = list(sentence)
        
        for index, char in enumerate(sentence):
            if char.islower():
                list_sentence[index] = lower_cipher[char]
            elif char.isupper():
                list_sentence[index] = upper_cipher[char]
            
        return "".join(list_sentence)

    def open_file(self,filename):
        """
        @param : csv file contring text data
        @return : file object
        """
        file = open(filename,encoding="utf-8")
        return file

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def parse_chunk(self,data):
        results = []
        for line in data:
            try:
                parsed = dict()
                parsed['data'] = self.cipher_encryption(line)
                results.append(parsed)
            except Exception as e:
                print(e)
        return results

    def run_process(self, file):
        
        file = self.open_file(file)
        read = csv.reader(file)
        listify = [row[0].strip()for row in read]

        data = self.chunks(listify, int(len(listify) / (multiprocessing.cpu_count() - 2)))
        p = Pool(processes=multiprocessing.cpu_count() - 2)
        results = [p.apply_async(self.parse_chunk, args=(list(x),)) for x in data]

        # wait for results afer processing
        results = [item.get() for item in results]
        self.results = sum(results, []) #  concatenate list 

    def save_to_csv(self, output_file):
        headers = self.results[0].keys()
        with open(output_file, 'w', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, headers)
            writer.writeheader()
            writer.writerows(self.results)

    def clear_results(self):
        self.results = []

if __name__ == '__main__':
    # To Run Program
    # >>python read_csv.py csv_file_path
    file_path = sys.argv[1]
    obj = AtbashCipherEncryption()
    obj.run_process(file_path)
    obj.save_to_csv('results.csv')
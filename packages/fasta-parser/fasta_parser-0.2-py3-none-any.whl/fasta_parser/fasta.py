from Bio import SeqIO
import re

class Fasta_object():
    def __init__(self, text):
        self.text = text
        self.record = self.text_indentifier(text)
        print('Sequence succesfully recorded\n')

    def __getitem__(self, item):
        return self.record[item]

    def text_indentifier(self, text):
        filepaths = re.findall("(/[a-zA-Z\./]*[\s]?.*fasta$)", text)
        if filepaths:
            for file in filepaths:
                a = self.fasta_load(file)
                return a
        elif text.startswith(">"):
            lines = text.splitlines()
            name, seq = [], []
            for line in lines:
                if line.startswith(">"):
                    name.append(line[1:len(line)])
                else:
                    seq.append(line)
            dicc = {}
            for i in range(len(name)):
                dicc[name[i]] = seq[i]
            return dicc
        else:
            print("The input isn't a pasta file or string\n")

    def fasta_load(self, file):
        record = SeqIO.index(file, 'fasta')
        return record

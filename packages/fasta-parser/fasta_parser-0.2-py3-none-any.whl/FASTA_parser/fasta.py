from Bio import SeqIO
import re

def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

def is_fasta():
    user_input = input('Please enter the route to your file or the sequence in FASTA format')
    filepaths = re.findall("(/[a-zA-Z\./]*[\s]?)", user_input)
    if filepaths:
        for filepath in filepaths:
            with open(filepath, mode='r',) as fp:
                for name, seq in read_fasta(fp):
                    print('nombre', name)
                    print('secuencia', seq)
    else:
        for name, seq in read_fasta(user_input):
            print(name, seq)

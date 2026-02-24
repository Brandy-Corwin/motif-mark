# Motif Mark (OOP)

This program takes a FASTA file and a file with given motifs and outputs one image showing where each motif shows up in each sequence.

To run the program you will need pycairo installed.

There are two required arguments to run motif-mark-oop.py:
- -f: the FASTA file (max 10 sequences each with <= 1,000 bases)
- -m: the file containg one motif per line (max 5 motifs)

An example run would be ```./motif-mark-oop.py -f Figure_1.fasta -m Fig_1_motifs.txt```
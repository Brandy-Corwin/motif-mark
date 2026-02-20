#!/usr/bin/env python

import cairo
import re
import argparse
import bioinfo

# Define arguments that the user needs to input
def get_args():
    parser = argparse.ArgumentParser(description="This script produces an image displaying given motifs in each sequence of the inputted fasta file.")
    parser.add_argument("-f", "--fasta", help="The path to the fasta file (str)", required=True, type=str)
    parser.add_argument("-m", "--motifs", help="The path to the motifs file (str)", required=True, type=str)
    return parser.parse_args()
	
args = get_args()

# Classes
class Motif:
    def __init__(self, motif, start, end):
        '''This holds the information of which motif it is and where in the sequence it is'''
        self.motif = motif
        self.start = start
        self.end = end
        self.length = end - start

class Exon:
    def __init__(self, start, end):
        '''This holds the information of where in the sequence it is'''
        self.start = start
        self.end = end
        self.length = end - start

class Intron:
    def __init__(self, start, end):
        '''This holds the information of where in the sequence it is'''
        self.start = start
        self.end = end
        self.length = end - start

# Make the sequences in the fasta file one line each
bioinfo.oneline_fasta(args.fasta, f"oneline_{args.fasta}")

# Make set of motifs
motifs = set()
with open(args.motifs, "r") as fh:
    for line in fh:
        line = line.strip("\n")
        motifs.add(line)

# Hardcode colors for max of 5 motifs
#colors = tuple(context.set_source_rgba(242, 37, 37, 1), context.set_source_rgba(240, 207, 26, 1), context.set_source_rgba(79, 212, 56, 1), context.set_source_rgba(34, 79, 235, 1), context.set_source_rgba(172, 56, 245, 1))

# Initialize image
width, height = 1100, 1300

surface = cairo.SVGSurface(f"{args.fasta.split(".")[0]}.svg", width, height)
context = cairo.Context(surface)

# Make image legend
# NOT DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Loop through fasta file, finding all motifs and creating diagram for each one
num_seq = 0
with open(f"oneline_{args.fasta}", "r") as fh:
    for line in fh:
        line = line.strip("\n")

        # Keep track of which sequence it is
        if line.startswith(">"):
            header = line
        else:
            seq = line
            num_seq += 1
        
            # Find each intron and the exon for the sequence
            the_introns = re.finditer(r"[a-z]+", seq)
            starts = []
            ends = []
            for intron in the_introns:
                starts.append(intron.start())
                ends.append(intron.end())
            intron1 = Intron(starts[0], ends[0])
            intron2 = Intron(starts[1], ends[1])

            the_exon = re.search(r"[A-Z]+", seq)
            exon = Exon(the_exon.start(), the_exon.end())

            context.set_line_width(2)
            context.move_to(50, (100*num_seq) + 150)
            context.line_to(50 + intron1.length, (100*num_seq) + 150)
            context.stroke()

            context.rectangle(50 + intron1.length, (100*num_seq) + 125, exon.length, 50)
            context.stroke()

            context.move_to(50 + intron1.length + exon.length, (100*num_seq) + 150)
            context.line_to(50 + intron1.length + exon.length + intron2.length, (100*num_seq) + 150)
            context.stroke()







surface.write_to_png (f"{args.fasta.split(".")[0]}.png")

# NOTES FOR ME:
# make a hard-coded tuple of 5 colors because you won't ever have more than 5 motifs.
# For however many motifs you have, get the first that many colors.

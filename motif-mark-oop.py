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
motifs = []
with open(args.motifs, "r") as fh:
    for line in fh:
        line = line.strip("\n")
        motifs.append(line)

# Make a dictionary of ambiguous bases and regular bases
bases = {'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T', 'U': 'T',
         'W': '[AT]', 'S': '[CG]', 'M': '[AC]', 'K': '[GT]', 'R': '[AG]', 'Y': '[CT]',
         'B': '[CGT]', 'D': '[AGT]', 'H': '[ACT]', 'V': '[ACG]', 'N': '[ACGT]'}

# Initialize image
width, height = 1100, 1300
surface = cairo.SVGSurface(f"{args.fasta.split(".")[0]}.svg", width, height)
context = cairo.Context(surface)
context.set_source_rgb(1,1,1)
context.paint()

# Hardcode colors for max of 5 motifs
colors = ((242/255.0, 37/255.0, 37/255.0), (240/255.0, 207/255.0, 26/255.0), (79/255.0, 212/255.0, 56/255.0), (34/255.0, 79/255.0, 235/255.0), (172/255.0, 56/255.0, 245/255.0))

# Make image legend
context.set_font_size(25)
context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
context.move_to(50, 50)
context.show_text("Legend")

context.set_font_size(20)
num_motif = 0
for motif in motifs:
    context.set_source_rgb(*colors[num_motif])
    context.rectangle(50 + (num_motif * 200), 75, 25, 25)
    context.fill()
    context.move_to(50 + (num_motif * 200) + 30, 95)
    context.set_source_rgb(0, 0, 0)
    context.show_text(f"{motif}")
    num_motif += 1

# Loop through fasta file, finding all motifs and creating diagram for each one
num_seq = 0
num_header = 0
with open(f"oneline_{args.fasta}", "r") as fh:
    for line in fh:
        line = line.strip("\n")

        # Keep track of which sequence it is and write on image
        if line.startswith(">"):
            header = line
            num_header += 1
            context.set_font_size(15)
            context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            context.move_to(50, (100 * num_header) + 65)
            context.show_text(header)

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

            # Draw each intron and the exon for the current sequnce
            context.set_line_width(2)
            context.move_to(50, (100 * num_seq) + 100)
            context.line_to(50 + intron1.end, (100 * num_seq) + 100)
            context.stroke()

            context.rectangle(50 + intron1.end, (100 * num_seq) + 75, exon.length, 50)
            context.stroke()

            context.move_to(50 + intron2.start, (100 * num_seq) + 100)
            context.line_to(50 + intron2.end, (100 * num_seq) + 100)
            context.stroke()

            # Find each motif at each point in the sequence and place on image
            n = 0
            for motif in motifs:
                # Set color of current motif
                context.set_source_rgb(*colors[n])

                # Change motif to cotain regex for ambiguous nucleotides
                searchable_motif = ""
                for letter in motif:
                    if letter.upper() in bases:
                        searchable_motif += bases[letter.upper()]

                # Search through current gene for all instances of current motif
                for match in re.finditer(searchable_motif, seq, flags=re.IGNORECASE):
                    m = Motif(match.group(), match.start(), match.end())
                    context.rectangle(50 + m.start, 75 + (100 * num_seq) + (n * 10), m.length, 10)
                    context.fill()
                n += 1

            # Reset color
            context.set_source_rgb(0, 0, 0)


# Write image
surface.write_to_png(f"{args.fasta.split(".")[0]}.png")
import sys
from pathlib import Path
import os

def get_original_sequence_and_coords(read_file, output_file):
    with open(file, "w") as out:
        file_contents = file.read_text()
        remarks = file_contents.split("REMARK")

        for i, x in enumerate(remarks):
            line = x.strip()
            remarks[i] = line

        for i, x in enumerate(remarks):
            if remarks[i-1].find("Native sequence") != -1:
                original_sequence = ""

                while len(remarks[i]) > 0:
                    original_sequence += remarks[i]
                    i += 1
            elif x.find("*") != -1:
                coord_str = x[1:]

                while len(remarks[i+1]) > 0:
                    coord_str += remarks[i+1]
                    i += 1
                break

        binary_sequence = get_binary_sequence(original_sequence)
        coords = get_coordinates(coord_str)
        num_contacts = count_contacts(coords, binary_sequence)
        print(binary_sequence, file=out)
        print(num_contacts, file=out)

def get_binary_sequence(amino_acid_sequence):
    ONES = ['A', 'C','G', 'I', 'L', 'M', 'F', 'P', 'W', 'Y', 'V']
    ZEROS = ['R', 'N', 'D', 'Q', 'E', 'H', 'K', 'S', 'T']

    sequence = ""

    for x in amino_acid_sequence:
        if x in ONES:
            sequence += "1"
        elif x in ZEROS:
            sequence += "0"
        else:
            raise Exception("ERROR: invalid character in sequence: {x}")

    return sequence

def get_coordinates(coord_str):
    coords = list()
    coords.append([0,0,0])

    for i, c in enumerate(coord_str):
        coord = list(coords[i])

        if c == "L":
            coord[0] += 1
        elif c == "R":
            coord[0] -= 1
        elif c == "F":
            coord[1] += 1
        elif c == "B":
            coord[1] -= 1
        elif c == "U":
            coord[2] += 1
        elif c == "D":
            coord[2] -= 1
        else:
            raise Exception("Error: unrecognized coordinate character: {c}")

        coords.append(coord)

    return coords

def count_contacts(coords, string):
    contacts = 0

    for i, x in enumerate(coords):
        if string[i] == "0":
            continue
        for j, y in enumerate(coords[i+2:]):
            if string[i+2+j] == "0":
                continue
            if x[0] == y[0] and x[1] == y[1] and abs(x[2] - y[2]) == 1:
                contacts += 1
            elif x[0] == y[0] and x[2] == y[2] and abs(x[1] - y[1]) == 1:
                contacts += 1
            elif x[1] == y[1] and x[2] == y[2] and abs(x[0] - y[0]) == 1:
                contacts += 1
    return contacts

def main(argv):
    if (len(argv) < 2):
        raise Exception("ERROR: Usage\n\tpython3 get_sequences.py {path to file to read from}")
    elif len(argv) == 3:
        flag = argv[2]
        directory = Path(argv[1])
    else:
        flag = "-f"
        file = Path("./Dataset/" + argv[1] + "_cubic.pdb")

    out_file = Path("./input/" + argv[1] + ".txt")

    if flag == "-d": # loop through directory
        directory_contents = os.listdir(directory)

        for x in directory_contents:
            with open(x, "w") as f:
                write_binary_sequence_and_contact_number(x)
    else:
        with open(file, "w")

    # parse the remarks and assign original_sequence and coordinates


main(sys.argv)


"""
A     1
R     0
N     0
D     0
C     1
Q     0
E     0
G     1
H     0
I      1
L     1
K     0
M    1
F     1
P     1
S     0
T     0
W    1
Y     1
V     1
"""

#!/usr/bin/env python3

import re
from argparse import ArgumentParser, RawDescriptionHelpFormatter

def move_headings(file_in, file_out, amount):
    hashes = amount * "#"
    matches = []
    def extend(m):
        matches.append(m.group())
        # [:-1] to remove whitespace before adding new # and whitespace.
        return f"{m.group()[:-1]}{hashes} " if amount >= 0 else f"{m.group()[:-1 + amount]} "

    with open(file_in) as f:

        pattern = re.compile("#{1,6} ")
        c = f.read()
        c = re.sub(pattern, extend, c)

        with open(file_out, "w") as fw:
            fw.write(c)
        
        
if __name__ == "__main__":
    description = """
    
    Description:
    
    Takes input file, output path and amount of #'s to push either up or down.
    There are no limit to how much you can push to either side. Have fun!
    
    
    Usage:
    
    Push down by one:
    
        move_headings.py -i sql.md -o sql2.md -a 1
    
    Push back by two:
    
        move_headings.py -i oof.md -o oof.md -a -2
    
    Push down by crash:
    
        move_headings.py -i t.md -o t2.md -a 9999999999999999999
    
    Author: pauliusbaulius
    Date: 2020-06-23
    """
    
    parser = ArgumentParser(description=description, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input", type=str, help="path to markdown file.", required=True)
    parser.add_argument("-o", "--output", type=str, help="path to output file.", required=True)
    parser.add_argument("-a", "--amount", type=int, help="how many to push down or up", required=True)
    args = parser.parse_args()
    move_headings(args.input, args.output, args.amount)


import os
import argparse
import requests
from sklearn import base

UNIPROT_URL = "https://rest.uniprot.org/uniprotkb/search"

# Download Fasta Results from Uniprot, send to output file
def download_uniprot_data(query: str, seq_limit: int, output: str):
    """Download Sequences and save to outputfile """
    params = {"query": query, "format": "fasta", "size": seq_limit, "compressed": "false",}
    r = requests.get(UNIPROT_URL, params=params, timeout=60)
    r.raise_for_status()

    dirpath = os.path.dirname(output)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)


    # Read in line by line
    seq_placement = 0
    with open(output, "w") as protein_file:
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            line = line.strip()
            if line.startswith(">"):
                seq_placement += 1
                if seq_placement > seq_limit:
                    break
            protein_file.write(line + "\n")  


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default = "data/raw/uniprot")
    parser.add_argument("--seq_limit", default = 500, type=int)
    parser.add_argument("--reviewed", action="store_true")
    args = parser.parse_args() 

    
    base = "reviewed:true" if args.reviewed else None
    positive = "keyword:KW-0812" if base is None else f"{base} AND keyword:KW-0812"
    negative = "NOT keyword:KW-0812" if base is None else f"{base} AND NOT keyword:KW-0812"  

    positive_output = os.path.join(args.output, "positive.fasta")
    negative_output = os.path.join(args.output, "negative.fasta")     

    print(f"Positive Transmembrane: {positive_output}")
    download_uniprot_data(positive, args.seq_limit, positive_output)
    print(f"Negative Transmembrane: {negative_output}")
    download_uniprot_data(negative, args.seq_limit, negative_output)


if __name__ == "__main__":
     main()

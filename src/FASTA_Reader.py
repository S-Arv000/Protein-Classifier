# Read FASTA file protien sequences an yield id & sequence tuples
def read_fasta(file_path):
    """Yield (id, sequence) tuples from a FASTA file."""
    seq_id = None
    parts = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            # when we encounter a new header, yield the previous sequence
            if line.startswith(">"):
                if seq_id is not None:
                    yield seq_id, "".join(parts)
                seq_id = line[1:]
                parts = []
            else:
                parts.append(line)

    # consider last sequence in file
    if seq_id is not None:
        yield seq_id, "".join(parts)
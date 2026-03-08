import numpy as np
from dataclasses import dataclass

# Standard amino acid codes
AA = "ARNDCEQGHILKMFPSTWYV"
AA_set = set(AA)

# Hydrophobicity from KD scale (+ve = hydrophobic)
KD = {
    "I": 4.5, "V": 4.2, "L": 3.8, "F": 2.8, "C": 2.5, "W": -0.9, "Y": -1.3,
    "A": 1.8, "M": 1.9, "G": -0.4, "T": -0.7, "S": -0.8, "P": -1.6, "H": -3.2,
    "E": -3.5, "Q": -3.5, "D": -3.5, "N": -3.5, "K": -3.9, "R": -4.0,
}


@dataclass(frozen=True)
class FeatureQuantifier:
    window: int = 15  # Window size for sliding window
    hydro_threshold: float = 1.8  # Threshold for hydrophobic residues
    min_length: int = 30


# Fraction of each aa in sequence
def aa_composition(seq: str) -> dict:
    """Return fraction of every standard amino acid in *seq*."""
    seq_len = len(seq)
    if seq_len == 0:
        return {aa: 0.0 for aa in AA}

    return {aa: seq.count(aa) / seq_len for aa in AA}


# Average KD score
def hydrophobicity(seq: str) -> float:
    """Mean KD hydrophobicity of *seq*."""
    if len(seq) == 0:
        return 0.0
    hydro_values = [KD.get(aa, 0.0) for aa in seq]
    return np.mean(hydro_values)

# Find average KD of window sequences
def aa_window(seq: str, window: int) -> float:
    """Highest average hydrophobicity over any sliding window of length *window*."""
    if len(seq) == 0:
        return 0.0

    if len(seq) < window:
        return hydrophobicity(seq)

    vals = np.array([KD.get(x, 0.0) for x in seq])
    cumsum = np.cumsum(np.insert(vals, 0, 0.0))
    # Use Cumulative sums
    window_sums = cumsum[window:] - cumsum[:-window]
    return float(np.max(window_sums / window))


# Find longest run of hydrophobic residues
def longest_phobic_seq(seq: str, threshold: float) -> int:
    """Length of the longest consecutive run with KD ≥ *threshold*."""
    max_len = 0
    current_len = 0

    for aa in seq:
        if KD.get(aa, 0.0) >= threshold:
            current_len += 1
        else:
            max_len = max(max_len, current_len)
            current_len = 0

    return max(max_len, current_len)


# Fraction of residues that are charged (KRDE)
def charged_residues(seq: str) -> float:
    charged = set("KRDE")
    count = sum(1 for aa in seq if aa in charged)
    return count / len(seq) if len(seq) > 0 else 0.0


def quantify_features(seq: str, quantifier: FeatureQuantifier) -> dict:
    feature = {}
    feature.update(aa_composition(seq))
    feature["length"] = float(len(seq))
    feature["avg_hydro"] = hydrophobicity(seq)
    feature["max_window"] = aa_window(seq, quantifier.window)
    feature["longest_hydrophobic"] = longest_phobic_seq(
        seq, quantifier.hydro_threshold
    )
    feature["charged_residues"] = charged_residues(seq)
    return feature


# fixed column order for feature vector
def feature_columns(quantifier: FeatureQuantifier) -> list:
    dummy_seq = quantify_features("A", quantifier)
    return list(dummy_seq.keys())
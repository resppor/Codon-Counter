import argparse
import logging

import pandas as pd

from collections import Counter


logging.basicConfig(
    level="INFO",
    format="%(levelname)s: [%(module)s - L%(lineno)d] %(message)s",
)
LOGGER = logging.getLogger("codon_counter")


def count_codons(sequence):
    # Split sequence in codons
    codons = []
    for idx in range(0, len(sequence), 3):
        codons.append(sequence[idx:idx+3].upper())

    # Count codons
    codons_counter = Counter(codons)

    # Compute percentages. Round to 4 decimals
    codons_percent = dict([
        (i, round(codons_counter[i] / (len(sequence)/3) * 100.0, 4))
        for i, count in codons_counter.most_common()
    ])

    return codons_percent


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Codon Counter - let me help you count your codons!"
    )

    parser.add_argument("--data_folder", default="./data")
    parser.add_argument("--file_name", "--f", required=True)
    parser.add_argument("--header_length", "--h", type=int, default=1)

    args = parser.parse_args()

    file_position = args.data_folder + "/" + args.file_name
    LOGGER.info("Reading from file %s", file_position)

    # Read all lines from .txt file
    with open(file_position, "r") as f:
        content = f.read().splitlines()

        # Isolate header from content
        header = content[:args.header_length]
        sequence = "".join(content[args.header_length:]).upper()

    # Replace T -> U for RNA codons
    rna_sequence = sequence.replace("T", "U")

    LOGGER.info(
        "Displaying first 18 elements in DNA sequence: %s...", sequence[0:18])
    LOGGER.info(
        "Displaying first 18 elements in RNA sequence: %s...", rna_sequence[0:18])

    # Calculate codons percentage
    codons_percent = count_codons(sequence)
    codons_rna_percent = count_codons(rna_sequence)

    # Sort counts alphabetically
    sorted_codons_percent = dict(sorted(codons_percent.items()))
    sorted_codons_rna_percent = dict(sorted(codons_rna_percent.items()))

    LOGGER.info(
        "Displaying 5 most common codons in DNA sequence...  %s",
        list(codons_percent.items())[0:5])
    LOGGER.info(
        "Displaying 5 most common codons in RNA sequence...  %s",
        list(codons_rna_percent.items())[0:5])

    # Convert counters to DataFrames
    codons_df = pd.DataFrame.from_dict(
        codons_percent, orient="index", columns=["Percentage"])
    codons_sorted_df = pd.DataFrame.from_dict(
        sorted_codons_percent, orient="index", columns=["Percentage"])
    codons_rna_df = pd.DataFrame.from_dict(
        codons_rna_percent, orient="index", columns=["Percentage"])
    codons_rna_sorted_df = pd.DataFrame.from_dict(
        sorted_codons_rna_percent, orient="index", columns=["Percentage"])

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    output_name = "CODON_COUNTS_" + args.file_name.split(".txt")[0] + ".xlsx"
    writer = pd.ExcelWriter(output_name, engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    codons_df.to_excel(writer, sheet_name='Codons count')
    codons_sorted_df.to_excel(writer, sheet_name='Codons count (alphabetical)')
    codons_rna_df.to_excel(writer, sheet_name='RNA codons count (T -> U)')
    codons_rna_sorted_df.to_excel(
        writer, sheet_name='RNA codons count (alphabetical)')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    LOGGER.info("Saved .xlsx file in %s", output_name)
    LOGGER.info("All done! Enjoy your data analysis <3")

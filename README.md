
## USAGE


Launch the script by calling from terminal
```
python3 codon_counter.py --f <your_txt_file_name_here>.txt
```

The scripts accepts the following arguments
 - `--file_name`, no default, **required**. Name of the `.txt` file to process
 - `--data_folder`, default `./data`. Where to look for the `.txt` file
 - `--header_length`, defaul to 1. Lenght (in lines) of the header

The script will output a `.xlsx` file in the root folder named `CODON_COUNTS_<original_txt_file_name>.xlsx`. The file has 4 sheets with the following counts (in percentages):
 - % of DNA codons, sorted by most present
 - % of DNA codons, sorted alphabetically
 - % of RNA codons, sorted by most present
 - % of RNA codons, sorted alphabetically

NOTE: the RNA sequence is obtained by replacing "T" with "U".

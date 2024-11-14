# Parse-Protein-FASTAs-for-Domains-of-Interest
InterPro allows you to download .TSVs of proteins indicating where certain domains of interest occur. Using these files, you can parse a protein FASTA for key domains of interest.
Supply the program with the following files in the following order:
1. The InterPro TSV indicating the domain information (format: Accession, Source Database, Name, Tax ID, Tax Name, Length, Entry, Accession, Matches)
2. FASTA sequence file with the proteins of interest
3. Name of the New FASTA File
Version 2.0:
Look for a domain of interest in a general .tsv output from an InterPro Pfam search. Inputs are the same, but 'search' variable needs to be set to whatever the name of the search must be for e.g. 'Glycoside hydrolase 18'. Double-check in the .tsv output exactly what the name is of your domain of interest in the 5th column (generally includes an ID#, e.g. 'PF00704	Glycosyl hydrolases family 18')

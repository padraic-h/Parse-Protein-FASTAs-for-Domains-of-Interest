import sys
import textwrap

'''InterPro allows you to download .TSVs of proteins indicating where certain domains of interest occur,
and in my particular case, I'm interested in isolating the GH18 (Glycoside hydrolase 18) domains of several proteins 
of interest across fungi.
Version 1.0:
Supply the program with the following files in the following order:
1. The InterPro TSV indicating the domain information (format: Accession, Source Database, Name, Tax ID, Tax Name, Length, Entry, Accession, Matches)
2. FASTA sequence file with the proteins of interest
3. Name of the New FASTA File
Version 2.0:
Look for a domain of interest in a general .tsv output from an InterPro Pfam search. Inputs are the same, but 'search'
variable needs to be set to whatever the name of the search must be for e.g. 'Glycoside hydrolase 18'. Double-check
in the .tsv output exactly what the name is of your domain of interest in the 5th column (generally includes an ID#)
'''
info = {}   # This will contain the name of the protein as a key and its start and end of domain of interest
newnames = {} # If running version 1, their FASTAs contain names that are too long and without species labels- this outputs something more descriptive and concise
domains_seq = {}    # This will contain the sequences of the isolated domains of each protein
search = 'PF00704	Glycosyl hydrolases family 18'  # If search=='N', run version 1 (general InterPro db); if version 2, include search label
with open(sys.argv[1], 'r') as hits:
    for line in hits:
        i = line.rstrip().split('\t')  # isolate information in line as a list
        if search == 'N':
            tax = 'taxID:' + i[3]
            name = '>' + "|".join([i[0], i[1], i[2], tax])
            species = "_".join(i[4].split()[0:2])
            newname = '>' + species + '_' + i[0] + '_' + "_".join(i[2].split())  # New FASTA labels
            info[name] = i[-1]
            newnames[name] = newname
        else:
            if search in line:
                start = i[6]
                end = i[7]
                name = '>' + i[0]    # InterPro looks for first blank space to cut-off name
                info[name] = start + '..' + end
            else:
                continue
print(info)
with open(sys.argv[2], 'r') as fasta, open(sys.argv[3], 'w') as fout:
    seq = ''
    count = 0
    wrapper = textwrap.TextWrapper(width=80)
    for line in fasta:
        if '>' in line:
            if count == 0:
                header = line.rstrip()
                count += 1
            elif header.split()[0] in info.keys():
                start, end = info[header.split()[0]].split('..')    # header.split()[0] argument used because interpro looks for the first blank space to make a name
                domain = seq[int(start)-1:int(end)]   # counting doesn't start at 0 in these databases- need to account for that
                domain = wrapper.fill(text=domain)
                if search == 'N':
                    header =newnames[header]    # change to the new header label
                o = header + '\n' + domain + '\n'   # output
                fout.write(o)
                header = line.rstrip()
                seq = ""
            else:
                seq = ""    # in case the protein did not have a domain of interest
                header = line.rstrip()
        else:
            seq += line.rstrip()
    start, end = info[header.split()[0]].split('..')   # record final entry
    domain = seq[int(start) - 1:int(end)]  # counting doesn't start at 0 in these databases- need to account for that
    domain = wrapper.fill(text=domain)
    o = header + '\n' + domain + '\n'  # output
    fout.write(o)
# to install dask: pip install dask
from dask import dataframe as dd
import gzip
import time

def vcf_parser(filename):
    with gzip.open(filename, "rt") as ifile, open("vcf.tsv", "w") as ofile:
        for line in ifile:
            if not line.strip().startswith("##"):
                ofile.write("\t".join(line.strip().split("\t")))
                ofile.write("\n")
                
start_time = time.time()
vcf_parser("ALL.chr22_GRCh38.genotypes.20170504.vcf.gz")
print("--- %s seconds ---" % (time.time() - start_time))

df = dd.read_csv("vcf.tsv", delimiter="\t")
df.head()

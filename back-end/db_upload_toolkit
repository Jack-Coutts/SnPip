import re
from itertools import chain
from itertools import repeat


# NOTE: Parses the information needed for the chromosome table and uploads it
# NOTE: (POS, ID, REF, ATL)
def vcfsnp(file, database):
    patt = re.compile("[^\t]+")
    mycursor = database.cursor()
    sql = "INSERT INTO snp (CHROM, POS, ID, REF, ALT) VALUES (%s, %s, %s, %s, %s)"
    with open(file, "rt") as f:
        lines = [line for line in f if "#" not in line]
        for line in lines:
            l = patt.findall(line)
            nl = [i.split(';') for i in l]
            row = list(chain.from_iterable(nl))
            chrom = tuple(row[:5])
            mycursor.execute(sql, chrom)
            database.commit()


# NOTE: Parses the information needed for the Population table and uploads it
# NOTE: (ID, AF, AFR, AMR, EAS, EUR, SAS)
def vcfpop(file, database):
    patt = re.compile("[^\t]+")
    pointer = ","
    rowlist = []
    mycursor = database.cursor()
    sql = "INSERT IGNORE into pop (ID, AF, AFR, AMR, EAS, EUR, SAS) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    with open(file, "rt") as f:
        lines = [line for line in f if "#" not in line]
        for line in lines:
            l = patt.findall(line)
            # NOTE: Splits the info column up
            nl = [i.split(';') for i in l]
            row = list(chain.from_iterable(nl))
            # NOTE: Removes unwanted collumns
            pop = row[2:17]
            del pop[1:5]
            del pop[1]
            del pop[3:5]
            del pop[2]
            # NOTE: Removes each row Population stat identifier
            num = [re.sub("[A-Z].+=", '', i) for i in pop]
            # NOTE: Notices if snp has multiple values
            pointout = any(pointer in i for i in num)
            if pointout is True:
                # NOTE: Splits the snp into two new rows and adds them to db
                split = [i.split(",") for i in num]
                for i in split:
                    if isinstance(i, list) and len(i) == 1:
                        index = split.index(i)
                        for x in i:
                            split[index] = ([x for item in i for x in repeat(item, 2)])
                rowlist.append(tuple([i[0] for i in split]))
                rowlist.append(tuple([i[1] for i in split]))
                mycursor.executemany(sql, rowlist)
                database.commit()
            else:
                val = tuple(num)
                mycursor.execute(sql, val)
                database.commit()


# NOTE: Inputs the gene for each snp in the snp table
def genetag(file, database):
    with open("anno_peru.vcf") as f:
        patt = re.compile("[^\t]+")
        patt2 = re.compile("GENE=[A-Za-z0-9]+")
        mycursor = database.cursor()
        sql = "UPDATE snp SET GENE = %s WHERE ID = %s"
        for line in f:
            lines = [line for line in f if "#" not in line]
            for line in lines:
                l = patt.findall(line)
                # NOTE: Splits the info column up
                nl = [i.split(';') for i in l]
                row = list(chain.from_iterable(nl))
                # NOTE: retrieves snp ID and gene and matches gene to id in db
                for i in row:
                    if patt2.search(i):
                        gene_ls = tuple([re.sub("GENE=", '', i), row[2]])
                        mycursor.execute(sql, gene_ls)
                        database.commit()

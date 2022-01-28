# file for database models

from pickle import TRUE

from sqlalchemy import ForeignKey
from . import db # importing db from current package (website folder)


class Location(db.Model):
    snp_name = db.Column(db.String(150), primary_key=TRUE)
    locate = db.Column(db.String(150))
    gene_name = db.Column(db.String(150))
    chromosome = db.Column(db.Integer)


class SNP(db.Model):
    name = db.Column(db.String(150), primary_key=TRUE)
    gene = db.Column(db.String(150))
    ref = db.Column(db.String(150))
    new = db.Column(db.String(150))
    location_SNP = db.Column(db.String(150), db.ForeignKey('location.snp_name'))


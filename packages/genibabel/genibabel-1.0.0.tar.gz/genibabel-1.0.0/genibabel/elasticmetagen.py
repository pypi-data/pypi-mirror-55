# -*- coding: utf-8 -*-
###############################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
###############################################################################


"""
This module provides tools to generate/request an ElasticSearch genetic
reference.
"""

# Imports
import time
import ssl
import progressbar
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, parallel_bulk
from elasticsearch.connection import create_ssl_context


class MetaGen(object):
    """ This class enables us to construct a bioresource with ElasticSearch.
    """

    def __init__(self, url, bulk=False, verify_certs=True):
        """ Initialize the MetaGen class.

        Parameters
        ----------
        url: str
            the server url.
        bulk: bool, default False
            if set use the bulk API to perform many index operations in a
            single API call. This can greatly increase the indexing speed.
        verify_certs: bool, default True
            verify server certificate.
        """
        kwargs = {}
        if not verify_certs:
            ssl_context = create_ssl_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            kwargs["verify_certs"] = verify_certs
            kwargs["ssl_context"] = ssl_context
        self.session = Elasticsearch([url], **kwargs)
        self.bulk = bulk

    @classmethod
    def _format_result(cls, res):
        """ Format the result of a query.

        Parameters
        ----------
        res: dict
            the returned query result.

        Returns
        -------
        format_res: dict
            the formated returned query result.
        """
        format_res = dict((item["_id"], item["_source"])
                          for item in res["hits"]["hits"])
        return format_res

    ###########################################################################
    #   Public Methods
    ###########################################################################

    def status(self):
        """ Display the content status.
        """
        query = {"query": {"match_all": {}}}
        print("=" * 50)
        for key, val in self.session.info().items():
            print("- ", key, ": ", val)
        print("-" * 5)
        for index in self.session.indices.get_alias().keys():
            status = self.session.count(index=index, body=query)
            print("- ", index, ": ", status["count"])
        print("=" * 50)


    def get_genes(self, chromosome=None, gene=None, pos_low=None, pos_up=None,
                  pathway=None, cpg=None):
        """ Filter/retrieve the available genes.

        Parameters
        ----------
        chromosome: str, default None
            a chromosome name.
        gene: str, default None
            a gene name.
        pos_low, pos_up: int, default None
            a position interval to look for SNPs.
        pathway: str, default None
            a pathway name.
        cpg: str, default None
            a CpG name.

        Returns
        -------
        data: dict
            the requested SNPs.
        """
        conditions = []
        if chromosome is not None:
            conditions.append({
                "match": {
                    "chrom": chromosome
                }
            })
        if gene is not None:
            conditions.append({
                "match": {
                    "hgnc_name": gene
                }
            })
        if pathway is not None:
            conditions.append({
                "match": {
                    "related_pathways": pathway
                }
            })
        if cpg is not None:
            conditions.append({
                "match": {
                    "related_cpgs": cpg
                }
            })
        if pos_low is not None or pos_up is not None:
            interval = {}
            if pos_low is not None:
                interval["start"] = {"gte": pos_low}
            if pos_up is not None:
                interval["end"] = {"lte": pos_up}
            conditions.append({
                "range" : {
                    interval
                }
            })

        query = {
            "size": 10000,
            "query": {
                "bool": {
                    "must": conditions
                }
            }
        }
        return MetaGen._format_result(
            self.session.search(index="genes", body=query, request_timeout=500))

    def get_snps(self, chromosome=None, gene=None, pos_low=None, pos_up=None):
        """ Filter/retrieve the available SNPs.

        Parameters
        ----------
        chromosome: str, default None
            a chromosome name.
        gene: str, default None
            a gene name.
        pos_low, pos_up: int, default None
            a position interval to look for SNPs.

        Returns
        -------
        data: dict
            the requested SNPs.
        """
        conditions = []
        if chromosome is not None:
            conditions.append({
                "match": {
                    "chrom": chromosome
                }
            })
        if gene is not None:
            conditions.append({
                "match": {
                    "related_genes": gene
                }
            })
        if pos_low is not None or pos_up is not None:
            interval = {}
            if pos_low is not None:
                interval["gte"] = pos_low
            if pos_up is not None:
                interval["lte"] = pos_up
            conditions.append({
                "range" : {
                    "pos" : interval
                }
            })

        query = {
            "size": 10000,
            "query": {
                "bool": {
                    "must": conditions
                }
            }
        }
        return MetaGen._format_result(
            self.session.search(index="snps", body=query, request_timeout=500))

    def import_data(self, chromosome_name, genes, gene_pathways, cpg_islands,
                    cpgs, snps, thread_count=1):
        """ Method that import one chromsome data in the database.

        Parameters
        ----------
        chromosome_name: str
            the chromosome name that will be inserted.
        genes: list of list
            [[gene_id, chromosome, start, end, hgnc_name, gene_type], ...]
        cpg_islands: list of list
            [[chromosome, start, end], ...]
        cpgs: list of list
            [[cg_id, chromosome, position, related_genes, cpg_island_id], ...]
        snps: list of list
            [[rs_id, chromsome, start, end, maf, related_genes], ...]
        thread_count: int, default 1
            size of the threadpool to use for the bulk requests.
        """

        print("Processing chromosome %s..." % chromosome_name)
        actions = []

        #######################################################################
        # Insert the SNPs
        #######################################################################

        print("-- adding SNPs...")
        snp_gene_map = {}
        if not self.bulk:
            bar = progressbar.ProgressBar(
                max_value=len(snps), redirect_stdout=True)
        for cnt, (rs_id, chrom, pos, maf, related_genes) in enumerate(snps):
            assert chrom == chromosome_name, rs_id
            chrom = chrom.lower()
            for gene_id in related_genes:
                snp_gene_map.setdefault(gene_id, []).append(rs_id)
            data = {
                "chrom": chrom,
                "pos": pos,
                "maf": maf,
                "related_genes": related_genes
            }
            if self.bulk:
                actions.append({
                    "_op_type": "create",
                    "_index": "snps",
                    "_type": "hg38_dbsnp149",
                    "_id": rs_id,
                    "_source": data
                })
            else:
                result = self.session.index(
                    doc_type="hg38_dbsnp149",
                    index="snps",
                    id=rs_id,
                    body=data)
                if result["result"] == "updated":
                    print("[warn] SNP '{0}' updated.".format(rs_id))
                bar.update(cnt + 1)

        #######################################################################
        # Insert CpGIslands (genomic region with many CpGs)
        #######################################################################

        print("-- adding CpGIslands...")
        cpgisland_gene_map = {}
        cpgisland_chromosome_list = []
        if not self.bulk:
            bar = progressbar.ProgressBar(
                max_value=len(cpg_islands), redirect_stdout=True)  
        for cnt, (chrom, start, end, related_genes) in enumerate(cpg_islands):
            cpg_island_id = "chr%s:%i:%i" % (chrom, start, end)
            assert chrom == chromosome_name, cpg_island_id
            chrom = chrom.lower()
            for gene_id in related_genes:
                cpgisland_gene_map.setdefault(gene_id, []).append(
                    cpg_island_id)
            cpgisland_chromosome_list.append(cpg_island_id)
            data = {
                "chrom": chrom,
                "start": start,
                "end": end,
                "related_genes": related_genes
            }
            if self.bulk:
                actions.append({
                    "_op_type": "create",
                    "_index": "cpg_islands",
                    "_type": "hg38_dbsnp149",
                    "_id": cpg_island_id,
                    "_source": data
                })
            else:
                result = self.session.index(
                    doc_type="hg38_dbsnp149",
                    index="cpg_islands",
                    id=cpg_island_id,
                    body=data)
                if result["result"] == "updated":
                    print("[warn] CpGIsland '{0}' updated.".format(cpg_island_id))
                bar.update(cnt + 1)

        #######################################################################
        # Insert CpGs (methylation loci)
        #######################################################################

        print("-- adding CpGs...")
        cpg_gene_map = {}
        cpg_chromosome_list = []
        if not self.bulk:
            bar = progressbar.ProgressBar(
                max_value=len(cpgs), redirect_stdout=True)
        for cnt, (cg_id, chrom, position, related_genes,
                  cpg_island_id) in enumerate(cpgs):
            cpg_island_id = cpg_island_id or []
            assert chrom == chromosome_name, cg_id
            chrom = chrom.lower()
            for gene_id in related_genes:
                cpg_gene_map.setdefault(gene_id, []).append(cg_id)
            cpg_chromosome_list.append(cg_id)
            data = {
                "chrom": chrom,
                "position": position,
                "related_cpg_island": cpg_island_id,
                "related_genes": related_genes
            }
            if self.bulk:
                actions.append({
                    "_op_type": "create",
                    "_index": "cpgs",
                    "_type": "hg38_dbsnp149",
                    "_id": cg_id,
                    "_source": data
                })
            else:
                result = self.session.index(
                    doc_type="hg38_dbsnp149",
                    index="cpgs",
                    id=cg_id,
                    body=data)
                if result["result"] == "updated":
                    print("[warn] CpG '{0}' updated.".format(cg_id))
                bar.update(cnt + 1)

        #######################################################################
        # Insert the genes
        #######################################################################

        print("-- adding genes...")
        all_genes = []
        gene_pathway_map = {}
        if not self.bulk:
            bar = progressbar.ProgressBar(
                max_value=len(genes), redirect_stdout=True)
        for cnt, (gene_id, chrom, start, end, hgnc_name, gene_type,
                  related_pathways) in enumerate(genes):
            assert chrom == chromosome_name, gene_id
            chrom = chrom.lower()
            all_genes.append(gene_id)
            for pathway_id in related_pathways:
                gene_pathway_map.setdefault(pathway_id, []).append(gene_id)
            data = {
                "chrom": chrom,
                "start": start,
                "end": end,
                "hgnc_name": hgnc_name,
                "gene_type": gene_type,
                "related_snps": snp_gene_map.get(gene_id, []),
                "related_pathways": related_pathways,
                "related_cpg_islands": cpgisland_gene_map.get(gene_id, []),
                "related_cpgs": cpg_gene_map.get(gene_id, [])
            }
            if self.bulk:
                actions.append({
                    "_op_type": "create",
                    "_index": "genes",
                    "_type": "hg38_dbsnp149",
                    "_id": gene_id,
                    "_source": data
                })
            else:
                result = self.session.index(
                    doc_type="hg38_dbsnp149",
                    index="genes",
                    id=gene_id,
                    body=data)
                if result["result"] == "updated":
                    print("[warn] Gene '{0}' updated.".format(gene_id))
                bar.update(cnt + 1)

        #######################################################################
        # Insert the chromosomes
        #######################################################################

        print("-- adding chromosome...")
        data = {
            "related_genes": all_genes,
            "related_cpg_islands": cpgisland_chromosome_list,
            "related_cpgs": cpg_chromosome_list
        }
        if self.bulk:
            actions.append({
                "_op_type": "create",
                "_index": "chromosomes",
                "_type": "hg38_dbsnp149",
                "_id": "chr{0}".format(chromosome_name),
                "_source": data
            })
        else:
            result = self.session.index(
                doc_type="hg38_dbsnp149",
                index="chromosomes",
                id="chr{0}".format(chromosome_name),
                body=data)

        #######################################################################
        # Dump actions
        #######################################################################

        if self.bulk:
            time.sleep(2)
            chunk_size = 50000
            print("-- adding actions...")
            if thread_count == 1:
                result = bulk(self.session, actions, chunk_size=chunk_size,
                              stats_only=True, request_timeout=500)
                print(result)
            else:
                parallel_bulk(self.session, actions, thread_count=thread_count,
                              chunk_size=chunk_size)


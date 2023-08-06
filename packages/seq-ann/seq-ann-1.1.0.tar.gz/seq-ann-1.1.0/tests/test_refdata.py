#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    seqann Sequence Annotation.
#    Copyright (c) 2017 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#



"""
test_refdata
----------------------------------

Tests for `seqann.models.reference_data` module.
"""

import os
import json
import pymysql
import unittest

from Bio import SeqIO
from BioSQL import BioSeqDatabase

from seqann.util import get_features
from seqann.models.annotation import Annotation
from seqann.models.reference_data import ReferenceData


neo4jpass = 'gfedb'
if os.getenv("NEO4JPASS"):
    neo4jpass = os.getenv("NEO4JPASS")

neo4juser = 'neo4j'
if os.getenv("NEO4JUSER"):
    neo4juser = os.getenv("NEO4JUSER")

neo4jurl = "http://neo4j.b12x.org:80"
if os.getenv("NEO4JURL"):
    neo4jurl = os.getenv("NEO4JURL")

biosqlpass = "my-secret-pw"
if os.getenv("BIOSQLPASS"):
    biosqlpass = os.getenv("BIOSQLPASS")

biosqluser = 'root'
if os.getenv("BIOSQLUSER"):
    biosqluser = os.getenv("BIOSQLUSER")

biosqlhost = "localhost"
if os.getenv("BIOSQLHOST"):
    biosqlhost = os.getenv("BIOSQLHOST")

biosqldb = "bioseqdb"
if os.getenv("BIOSQLDB"):
    biosqldb = os.getenv("BIOSQLDB")

biosqlport = 3307
if os.getenv("BIOSQLPORT"):
    biosqlport = int(os.getenv("BIOSQLPORT"))


def conn():
    try:
        conn = pymysql.connect(host=biosqlhost,
                               port=biosqlport, user=biosqluser,
                               passwd=biosqlpass, db=biosqldb)
        conn.close()
        return True
    except Exception as e:
        print("Exception while checking MYSQL Connection:" + str(e))
        return False


class TestRefdata(unittest.TestCase):

    def setUp(self):
        self.data_dir = os.path.dirname(__file__) + "/resources"
        self.dblist = [str(i) + str(0) for i in range(315, 329)]
        expected_json = self.data_dir + "/expected.json"
        with open(expected_json) as json_data:
            self.expected = json.load(json_data)
        pass

    def test_001_noserver(self):
        refdata = ReferenceData()
        self.assertIsInstance(refdata, ReferenceData)
        self.assertFalse(refdata.server_avail)
        self.assertGreater(len(refdata.hla_names), 10)
        self.assertEqual(refdata.structure_max['HLA-A'], 17)
        self.assertFalse(refdata.server_avail)
        self.assertTrue(refdata.hlaref)
        self.assertTrue(refdata.seqref)
        self.assertGreater(len(refdata.seqref), 10)
        self.assertGreater(len(refdata.hlaref), 10)
        pass

    @unittest.skipUnless(conn(), "TestRefdata 002 Requires MySQL connection")
    def test_002_server(self):
        server = BioSeqDatabase.open_database(driver="pymysql",
                                              user=biosqluser,
                                              passwd=biosqlpass,
                                              host=biosqlhost,
                                              db=biosqldb,
                                              port=biosqlport)
        refdata = ReferenceData(server=server)
        self.assertIsInstance(refdata, ReferenceData)
        self.assertTrue(refdata.server_avail)
        self.assertFalse(refdata.seqref)
        self.assertFalse(refdata.hlaref)
        server.close()
        pass

    @unittest.skipUnless(conn(), "TestRefdata 003 Requires MySQL connection")
    def test_003_dblist(self):
        server = BioSeqDatabase.open_database(driver="pymysql",
                                              user=biosqluser,
                                              passwd=biosqlpass,
                                              host=biosqlhost,
                                              db=biosqldb,
                                              port=biosqlport)
        for db in self.dblist:
            refdata = ReferenceData(server=server, dbversion=db)
            self.assertEqual(refdata.dbversion, db)
            self.assertTrue(refdata.server_avail)
            self.assertFalse(refdata.seqref)
            self.assertFalse(refdata.hlaref)
        server.close()
        pass

    @unittest.skipUnless(conn(), "TestRefdata 004 requires MySQL connection")
    def test_004_selectserv(self):
        server = BioSeqDatabase.open_database(driver="pymysql",
                                              user=biosqluser,
                                              passwd=biosqlpass,
                                              host=biosqlhost,
                                              db=biosqldb,
                                              port=biosqlport)
        refdata = ReferenceData(server=server)
        input_seq = self.data_dir + '/exact_seqs.fasta'
        self.assertFalse(refdata.hlaref)
        self.assertFalse(refdata.seqref)
        for ex in self.expected['exact']:
            i = int(ex['index'])
            locus = ex['locus']
            allele = ex['name']
            hla, loc = locus.split("-")
            in_seq = list(SeqIO.parse(input_seq, "fasta"))[i]
            annotation = refdata.search_refdata(in_seq, locus)
            self.assertIsNone(annotation.features)
            self.assertEqual(annotation.method, "match")
            self.assertIsInstance(annotation, Annotation)
            self.assertTrue(annotation.complete_annotation)
            self.assertGreater(len(annotation.annotation.keys()), 1)
            db = refdata.server[refdata.dbversion + "_" + loc]
            expected = db.lookup(name=allele)
            expected_seqs = get_features(expected)

            for feat in expected_seqs:
                if feat not in annotation.annotation:
                    self.assertEqual(feat, None)
                else:
                    self.assertEqual(str(expected_seqs[feat]),
                                     str(annotation.annotation[feat]))
        server.close()
        pass

    def test_005_select(self):
        refdata = ReferenceData()
        input_seq = self.data_dir + '/exact_seqs.fasta'
        self.assertTrue(refdata.hlaref)
        self.assertTrue(refdata.seqref)
        for ex in self.expected['exact']:
            i = int(ex['index'])
            locus = ex['locus']
            allele = ex['name']
            hla, loc = locus.split("-")
            in_seq = list(SeqIO.parse(input_seq, "fasta"))[i]
            annotation = refdata.search_refdata(in_seq, locus)
            self.assertIsNone(annotation.features)
            self.assertEqual(annotation.method, "match")
            self.assertIsInstance(annotation, Annotation)
            self.assertTrue(annotation.complete_annotation)
            self.assertGreater(len(annotation.annotation.keys()), 1)
            expected = refdata.hlaref[allele]
            expected_seqs = get_features(expected)
            for feat in expected_seqs:
                if feat not in annotation.annotation:
                    self.assertEqual(feat, None)
                else:
                    self.assertEqual(str(expected_seqs[feat]),
                                     str(annotation.annotation[feat]))
        pass

    @unittest.skipUnless(conn(), "TestRefdata 006 requires MySQL connection")
    def test_006_dbtodat(self):
        server = BioSeqDatabase.open_database(driver="pymysql",
                                              user=biosqluser,
                                              passwd=biosqlpass,
                                              host=biosqlhost,
                                              db=biosqldb,
                                              port=biosqlport)
        refdata1 = ReferenceData(server=server)
        refdata2 = ReferenceData()

        datseqs = refdata2.hlaref['HLA-A*01:01:01:01']

        db = refdata1.server[refdata1.dbversion + "_" + 'A']
        expected = db.lookup(name='HLA-A*01:01:01:01')

        expected_seqs1 = get_features(datseqs)
        expected_seqs2 = get_features(expected)

        for feat in expected_seqs1:
            if feat not in expected_seqs2:
                self.assertEqual(feat, None)
            else:
                self.assertEqual(str(expected_seqs1[feat]),
                                 str(expected_seqs2[feat]))
        server.close()
        pass

    @unittest.skipUnless(conn(), "TestBioSeqAnn 007 Requires MySQL connection")
    def test_007_align(self):
        # TODO: Add class II tests
        server = BioSeqDatabase.open_database(driver="pymysql",
                                              user=biosqluser,
                                              passwd=biosqlpass,
                                              host=biosqlhost,
                                              db=biosqldb,
                                              port=biosqlport)
        refdata = ReferenceData(server=server, alignments=True)
        for ex in self.expected['align']:
            locus = ex['locus']
            allele = ex['name'].split("_")[0]
            hla, loc = locus.split("-")
            align = "".join([refdata.annoated_alignments[loc][allele][s]['Seq'] for s in refdata.annoated_alignments[loc][allele].keys()])
            self.assertEqual(str(align),
                             str(ex['alignment']))



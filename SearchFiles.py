#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""


def run(searcher, analyzer,keyword,way):
    while True:
        try:
            command = keyword.encode('utf8')
        except UnicodeDecodeError:
            command = keyword
        if command == '':
            return []
        if way=='contents':
            query = QueryParser(Version.LUCENE_CURRENT, "contents",analyzer).parse(command)
        elif way=='tags':
            query = QueryParser(Version.LUCENE_CURRENT, "tag",analyzer).parse(command)            
        scoreDocs = searcher.search(query, 50).scoreDocs
        result=[]
        result.append(command)
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            item=[]
            item.append(doc.get('title'))
            item.append(doc.get('url'))
            item.append(doc.get('price'))
            item.append(doc.get('imgurl'))
            item.append(doc.get('wellrate'))
            item.append(doc.get('comment'))
            item.append(doc.get('tag'))
            #print doc.get('comment').encode('utf8')
            result.append(item)
	#print result
        
        return result

# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 11:28:48 2020

@author: cdekeyser
"""

import crawler
import db

base_url = "http://www.allocine.fr"
major_medias = ["cahiers du cinéma", "le monde", "les inrockuptibles", "brazil"]
possible_scores = {None: 0, "n10": 1, "n20": 2, "n30": 3, "n40": 4, "n50": 5}

conn_string = "mongodb+srv://soliton:instantsia@solitontest-mmj4o.azure.mongodb.net/?retryWrites=true&w=majority"               
db_name = "allocine"                    

crawler_instance = crawler.Crawler(base_url, major_medias, possible_scores)
found_new_films = crawler_instance.crawl()

db_writer = db.Writer(conn_string, db_name)
db_writer.create_update_docs(found_new_films)

print("done")
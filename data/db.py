# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 10:35:14 2020

@author: cdekeyser
"""

import pymongo


class Writer:
    
    
    client = None
    db = None
    
    
    def __init__(self, conn_string, db_name):
        
        if conn_string is None or db_name is None:
            print("Writer constructor arguments cannot be None")
            raise TypeError
            
        self.client = pymongo.MongoClient(conn_string)
        self.db = self.client[db_name]
        
        
    def create_update_docs(self, found_films):
        
        for film in found_films:
            existing_doc = self.db.films.find_one({"name" : film["name"]})
            if existing_doc is not None:
                self.db.films.replace_one({'_id' : existing_doc['_id']}, film, True)
            else:
                self.db.films.insert_one(film)
                
        
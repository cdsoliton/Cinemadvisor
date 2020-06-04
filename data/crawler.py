# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:30:51 2020

@author: cdekeyser
"""

#%%

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import json
import re

class Crawler:
    
    
    base_url = None
    major_medias = None
    scores = None
    
    
    def __init__(self, base_url, major_medias, possible_scores):
        
        if base_url is None or major_medias is None or possible_scores is None:
            print("Crawler constructor arguments cannot be None")
            raise TypeError
            
        self.base_url = base_url
        self.major_medias = major_medias
        self.possible_scores = possible_scores
        
        
    def __try_get_peope_rating_film_sheet(self, film_sheet_url):
        
        # handle missing rating links in film sheets
        html = urllib.request.urlopen(self.base_url + film_sheet_url)
        soup = BeautifulSoup(html.read(), 'html.parser')
        
        parent_score_aggregation_tag = soup.find(type = "application/ld+json")
        
        try:
            parent_score_aggregation_dic = json.loads(parent_score_aggregation_tag.string)
            score_aggregation_dic = parent_score_aggregation_dic["aggregateRating"]
            avg_rating_score = float(score_aggregation_dic["ratingValue"].replace(',', '.'))
            rating_count = int(score_aggregation_dic["ratingCount"].replace(',', '.'))
       
        except:
            return None
        
        return avg_rating_score, rating_count


    def __process_media_review_tag(self, tag):
        
        media_header_tag = tag.find("h2")
        media_tag = media_header_tag.find("span")
        media_name = media_tag.string
        
        if media_name.lower() not in self.major_medias:
            return False, None, None
        
        rating_tag = tag.find(class_ = re.compile(".*stareval-stars.*"))
        regexp = re.compile(r"(\w\d{2})")
        
        for class_ in rating_tag["class"]:
            match = regexp.match(class_)
            if match is not None:
                major_media_rating = self.possible_scores[match[1]]
        
        return True, media_name, major_media_rating


    def __is_review_tag(self, tag):
        
        if tag.name != "div":
            return False
        
        if not tag.has_attr("class"):
            return False
        
        if tag["class"] != ["item", "hred"]:
            return False
        
        return "pressreview" in tag["id"]


    def __process_review_medias_url(self, review_url):
        
        html = urllib.request.urlopen(self.base_url + review_url)
        soup = BeautifulSoup(html.read(), 'html.parser')
        
        parent_score_aggregation_tag = soup.find(type = "application/ld+json")
        parent_score_aggregation_dic = json.loads(parent_score_aggregation_tag.string)
        score_aggregation_dic = parent_score_aggregation_dic["aggregateRating"]
        avg_rating_score = float(score_aggregation_dic["ratingValue"].replace(',', '.'))
        rating_count = float(score_aggregation_dic["ratingCount"].replace(',', '.'))
        review_tags = soup.find_all(self.__is_review_tag)
        major_ratings = {}
        
        for review_tag in review_tags:
             is_major, media_name, rating = self.__process_media_review_tag(review_tag)
             if is_major:
                 major_ratings[media_name] = rating
        
        return avg_rating_score, rating_count, major_ratings


    def __process_review_people_url(self, review_url):
        
        html = urllib.request.urlopen(self.base_url + review_url)
        soup = BeautifulSoup(html.read(), 'html.parser')
        
        big_note_tag = soup.find(class_ = "big-note")
        note_tag = big_note_tag.find(class_ = "note")
        note_count_tag = big_note_tag.find(class_ = "user-note-count")
        regexp = re.compile(r"(.\d+) note.*")
        
        return float(note_tag.string.replace(',', '.')), int(regexp.match(note_count_tag.string)[1].replace(',', '.'))


    def __is_review_url_tag(self, tag):
        
        if tag.name != "a":
            return False
        
        if not(tag.has_attr("class")) or not(tag.has_attr("href")):
            return False
        
        if "end-section-link" not in tag["class"]:
            return False
        
        return r"/critiques/" in tag["href"]


    def __process_film_sheet(self, film):
        
        html = urllib.request.urlopen(self.base_url + film["url"])
        soup = BeautifulSoup(html.read(), 'html.parser')
        review_url_tags = soup.find_all(self.__is_review_url_tag)
        
        # from there find overall and major media scores from critique web pages
        for review_url_tag in review_url_tags:
            relative_url = review_url_tag["href"]
            if "presse" in relative_url: 
                film["Media Rating"] = self.__process_review_medias_url(relative_url)
            else:
                film["People Rating"] = self.__process_review_people_url(relative_url)
        
        if "People Rating" not in film:
            film["People Rating"] = self.__try_get_peope_rating_film_sheet(film["url"])
        
        if "Media Rating" not in film:
            film["Media Rating"] = None
        
        return film


    def __process_film_tag(self, film_tag):
        
        film = {}
        
        if not film_tag.has_attr("href"):
            return None # not a film tag
        
        if "film" in film_tag["href"] :
            film["name"] = film_tag.string.rstrip().lstrip()
            film["url"] = film_tag["href"]
            return self.__process_film_sheet(film)
        
        return None # article tag


    def crawl(self):
        
        url = self.base_url + "/film/aucinema/"
        global_html = urllib.request.urlopen(url)
        global_soup = BeautifulSoup(global_html.read(), 'html.parser')
        main = global_soup.main
        
        film_tags = main.find_all(class_ = "meta-title-link")
        
        global_films = []
        for film_tag in film_tags:
            film = self.__process_film_tag(film_tag)
            if film is not None:
                global_films.append(film)
        
        return global_films



    


    
    
        
        
        

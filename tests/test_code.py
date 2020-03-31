# -*- coding: utf-8 -*-
from app.classes import user_input
from app.assets import stop_words
import pytest, json, requests
from io import BytesIO


test_data = user_input("Papi ou se trouve le stade de River Plate?")


def test_my_question():
    assert test_data.question == "Papi ou se trouve le stade de River Plate?"


def test_my_data_parsed_question():
    assert test_data.parser() == ['stade', 'river', 'plate']


class mock_get_lat_lng():

    def __init__(self, url):
        pass

    def json(self):
        result = {
                "candidates": [
                    {
                        "geometry": {
                            "location": {
                                "lat": -34.5453062,
                                "lng": -58.44977489
                            }
                        },
                        "name": "Stade Monumental Antonio Vespucio Liberti",
                        "place_id": "ChIJ340B5jq0vJURijD6W6dgfz0"
                    }
                ]
                }
        return result


def test_get_lat_lng(monkeypatch):
    monkeypatch.setattr('requests.get', mock_get_lat_lng)
    assert test_data.get_lat_lng() == (-34.5453062, -58.44977489,
                                    "ChIJ340B5jq0vJURijD6W6dgfz0")


class mock_get_wiki_id():

    def __init__(self, url, params):
        pass

    def json(self):
        result = {
                "query": {"search": [
                    {"pageid": 236374}
                                    ]}
        }
        return result


def test_get_wiki_id(monkeypatch):
    monkeypatch.setattr('requests.get', mock_get_wiki_id)
    assert test_data.get_wiki_id() == (236374)


class mock_get_wiki_content():

    def __init__(self, url):
        pass
    
    def json(self):
        result = {        
            "query": {
                "pages": {
                    "236374": {
                        "pageid": 236374,
                        "ns": 0,
                        "title": "Stade Monumental Antonio Vespucio Liberti",
                        "extract": "Le stade Monumental Antonio Vespucio Liberti, plus communément surnommé El Monumental, est un stade de football situé dans la capitale argentine de Buenos Aires. Parfois appelé l'Estadio Monumental de Núñez du nom du quartier Núñez, il se situe en fait aux limites de Belgrano, un des quartiers chics de la ville. \nIl a pour résident le Club Atlético River Plate, un des clubs les plus prestigieux d'Amérique du Sud, dont il porte le nom d'un ancien président, Antonio Vespucio Liberti, mort en 1978. L'enceinte sert également à l'accueil des matchs de l'équipe nationale argentine, dont il a accueilli la victoire en finale de la Coupe du monde de football 1978."
                    }
                }
            }
            }
        return result


def test_get_wiki_content(monkeypatch):
    monkeypatch.setattr('requests.get', mock_get_wiki_content)
    assert test_data.get_wiki_content() == "Le stade Monumental Antonio Vespucio Liberti, plus communément surnommé El Monumental, est un stade de football situé dans la capitale argentine de Buenos Aires. Parfois appelé l'Estadio Monumental de Núñez du nom du quartier Núñez, il se situe en fait aux limites de Belgrano, un des quartiers chics de la ville. \nIl a pour résident le Club Atlético River Plate, un des clubs les plus prestigieux d'Amérique du Sud, dont il porte le nom d'un ancien président, Antonio Vespucio Liberti, mort en 1978. L'enceinte sert également à l'accueil des matchs de l'équipe nationale argentine, dont il a accueilli la victoire en finale de la Coupe du monde de football 1978."


class mock_get_wiki_picture():

    def __init__(self, url):
        pass
    
    def json(self):
        result = {     
            "query": {
                "pages": {
                    "236374": {
                        "pageid": 236374,
                        "ns": 0,
                        "title": "Stade Monumental Antonio Vespucio Liberti",
                        "original": {
                            "source": "https://upload.wikimedia.org/wikipedia/commons/5/54/RiverPlateStadium.jpg",
                            "width": 3648,
                            "height": 2736
                        }
                    }
                }
            }
        }
        return result


def test_get_wiki_picture(monkeypatch):
    monkeypatch.setattr('requests.get', mock_get_wiki_picture)
    assert test_data.get_wiki_picture() == "https://upload.wikimedia.org/wikipedia/commons/5/54/RiverPlateStadium.jpg"

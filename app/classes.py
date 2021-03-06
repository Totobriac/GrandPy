from .assets import stop_words, api_key
import requests
import re

class user_input ():
    """Get the user input and process it."""

    def __init__(self, question):
        self.question = question
        

    def parser(self):
        """"
            Parses  the input.
            
            Returns:
                list: parsed words.
        """
        self.lower_case = self.question.lower()
        self.splitted_text = re.split('[- ? ; , \' . : ' ' " "]',self.lower_case)
        print (self.splitted_text)
        self.parsed_question = []        
        for i in self.splitted_text:
            if i not in stop_words and i != '':
                alphanumeric = ""
                for character in i:
                    if character.isalnum():
                        alphanumeric += character
                self.parsed_question.append(alphanumeric)
        print(self.parsed_question)
        return (self.parsed_question)

    def get_lat_lng(self):
        """
            Passes the parsed words into Google Maps API.
            
            Returns:
                list: the latitude, longitude and Google Maps place_id.
        """
        self.input_api = '%20'.join(self.parsed_question)
        self.input_api = ' '.join(self.parsed_question)
        self.google_api_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=geometry,name,place_id&types=point_of_interest&key={}'.format (self.input_api, api_key)     
        self.r = requests.get(url=self.google_api_url)
        self.data = self.r.json()
        self.name = self.data['candidates'][0]['name']
        self.place_id = self.data['candidates'][0]['place_id']
        self.lat = self.data['candidates'][0]['geometry']['location']['lat']
        self.lng = self.data['candidates'][0]['geometry']['location']['lng']
        print(self.lat, self.lng, self.place_id)
        return (self.lat, self.lng, self.place_id)

    def get_place_details(self):
        """
            Get the place city from the place_id.
        
        Returns:
            list: the name of the city, if none, it passes.
        """
        self.google_api_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(self.place_id, api_key)
        self.r = requests.get(url=self.google_api_url)
        self.data = self.r.json()
        self.address_components = self.data['result']['address_components']

        for i in self.address_components:
            if i['types'][0] == 'locality':
                self.city = (i['long_name'])
                return (self.city)
            else:
                pass

    def small_map(self):
        """
            Get the place map url from Google Maps API
            
            Returns:
                str: the place map of 350x350 px.
        """
        self.map_url = "https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=12&size=350x350&key={}".format(self.lat, self.lng, api_key)        
        return (self.map_url)

    def get_wiki_id(self):
        """
            Search for the wikipedia page id from the place name and city,
            or just the name if none.         
            Returns:
                int: wikipedia page_id.
        """
        self.url = "https://fr.wikipedia.org/w/api.php"

        try:
            self.searchpage = self.name + (" ") + self.city
        except AttributeError:
            self.searchpage = self.name

        self.params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": self.searchpage}

        self.response = requests.get(url=self.url, params=self.params)
        self.data = self.response.json()
        self.page_id = (self.data['query']['search'][0]['pageid'])
        return (self.page_id)

    def get_wiki_content(self):
        """
            Get a resume from the wikikepdia page 
            
            Returns:
                str: an extract of the page of 4 pages.
        """
        url = "https://fr.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=4&explaintext=&pageids={}&format=json".format(self.page_id)
        self.page = str(self.page_id)
        self.response = requests.get(url)
        self.data = self.response.json()
        self.wiki_data = (self.data['query']['pages'][self.page]['extract'])
        return (self.wiki_data)

    def get_wiki_picture(self):
        """
            Get the main picture of the wikipedia page. If none,
            get the first one of the page.
            
            Returns:
                str: the url of the image.
        """
        url = "https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&pageids={}".format(self.page_id)        
        self.page = str(self.page_id)
        self.response = requests.get(url)
        self.data = self.response.json()

        try:
            self.wiki_pic = (self.data['query']['pages'][self.page]['original']['source'])
            return (self.wiki_pic)

        except KeyError:
            self.s = requests.Session()
            url = "https://fr.wikipedia.org/w/api.php?action=query&prop=images&format=json&piprop=original&pageids={}&imlimit=1".format(self.page_id)                        
            self.response = self.s.get(url)
            self.data = self.response.json()
            self.wiki_pic_name = sxelf.data['query']['pages'][self.page]['images'][0]['title']
            self.s = requests.Session()
            url = "https://fr.wikipedia.org/w/api.php?action=query&titles={}&prop=imageinfo&iiprop=url&format=json".format(self.wiki_pic_name)                        
            self.response = self.s.get(url)
            self.data = self.response.json()
            self.wiki_pic = self.data['query']['pages']['-1']['imageinfo'][0]['url']
            return (self.wiki_pic)

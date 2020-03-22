from .assets import stop_words, api_key
import requests

class user_input ():
    
    def __init__ (self,question):
        self.question = question
    
    def parser (self):
        self.lower_case = self.question.lower()
        self.splitted_text = self.lower_case.split()
        self.parsed_question = []
        for i in self.splitted_text:
            if i not in stop_words:
                self.parsed_question.append(i)
        return (self.parsed_question)
    
    def get_lat_lng (self):
        self.input_api = '%20'.join(self.parsed_question)
        self.google_api_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=geometry,name&key={}'.format (self.input_api, api_key)
        self.r = requests.get (url = self.google_api_url)
        self.data = self.r.json()
        self.name = self.data['candidates'][0]['name']        
        self.lat = self.data['candidates'][0]['geometry']['location']['lat']        
        self.lng = self.data['candidates'][0]['geometry']['location']['lng']        
        return (self.lat, self.lng)

    def small_map (self):
        self.map_url = "https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=12&size=350x350&key={}".format (self.lat, self.lng, api_key)
        return (self.map_url)

    def get_wiki_id (self):
        self.s = requests.Session()
        self.url = "https://fr.wikipedia.org/w/api.php"
        self.searchpage = self.name
        self.params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": self.searchpage
        }
        self.response = self.s.get(url= self.url, params= self.params)
        self.data = self.response.json()
        self.page_id = (self.data['query']['search'][0]['pageid'])
        return (self.page_id)

    def get_wiki_content (self):
        self.s = requests.Session()        
        url=  "https://fr.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=4&explaintext=&pageids={}&format=json".format(self.page_id)       
        self.page = str(self.page_id)
        self.response = self.s.get(url)
        self.data= self.response.json()            
        self.wiki_data = (self.data['query']['pages'][self.page]['extract'])        
        return (self.wiki_data)
        
    def get_wiki_picture (self):
        self.s = requests.Session()        
        url=  "https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&pageids={}".format(self.page_id)
        # url = "https://fr.wikipedia.org/w/api.php?action=query&prop=pageimages&pageids={}&pithumbsize=350&format=json".format(self.page_id)       
        self.page = str(self.page_id)
        self.response = self.s.get(url)
        self.data= self.response.json()            
        self.wiki_pic = (self.data['query']['pages'][self.page]['original']['source'])
        print (self.data['query'])        
        return (self.wiki_pic)
from flask import Flask, render_template, request, jsonify 
import json
from .classes import user_input

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('main.html')

@app.route('/process', methods=['POST'])
def process():          
    user_question = request.form['question']          
    new_question = user_input(user_question)
    new_question.parser()
    new_question.get_lat_lng()                
    new_question.small_map()
    pic_map = new_question.map_url
    new_question.get_wiki_id()
    new_question.get_wiki_content()
    wiki_data = new_question.wiki_data
    new_question.get_wiki_picture()
    wiki_pic = new_question.wiki_pic
    print(wiki_pic)  
    return jsonify({'response' : pic_map , 'user_question' : user_question, 'wiki_data' : wiki_data, 'wiki_pic' : wiki_pic})
    

if __name__ == '__main__':
    app.run(debug=True)       		    

        
   

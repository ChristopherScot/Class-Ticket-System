from pygments import lexers
from pygments import highlight 
from flask import Flask                     #I'm sure there is a way to do all this without all of these imports
from flask_sqlalchemy import SQLAlchemy     #I will look into simpler python sql libraries later.
from datetime import datetime               #I feel like including flask for this is crazy.
import os
import secrets


from pygments.formatters import HtmlFormatter
formatter = HtmlFormatter(full=True, linenos=True, style="monokai") #full argument creates css alongside the html
SQLALCHEMY_TRACK_MODIFICATIONS = False


file_path = os.path.abspath(os.getcwd())+"\database.db"

app = Flask("pastebin") #Is this safe to change? Original: app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

db = SQLAlchemy(app)

class Paste(db.Model):
    SnippetNum = db.Column(db.Integer, primary_key=True)
    Code  = db.Column(db.Text, unique=False, nullable=True)
    Time = db.Column(db.String(100), unique=False,nullable=False)
    Hash = db.Column(db.String(160))
    Image = db.Column(db.LargeBinary)  #For use later with screenshots https://jsfiddle.net/m91doy0h/3

class ImagePaste(db.Model):
    SnippetNum = db.Column(db.Integer, primary_key=True)
    Time = db.Column(db.String(100), unique=False,nullable=False)
    Hash = db.Column(db.String(160))
    Image = db.Column(db.Text)  #For use later with screenshots https://jsfiddle.net/m91doy0h/3

#Takes code, creates a file with that code as html. Gives it a random name and then returns a url to it.
#Ideal version

def screenshotStoreAndHash(dataURL):
    try:
        shotHash = secrets.token_urlsafe(16)
        shotSub = ImagePaste(Image=dataURL,Time=datetime.now().strftime("%x %X"),Hash=shotHash)
        db.session.add(shotSub)        
        db.session.commit()    
        
    except Exception as e: print(e)

    return shotHash

def pygmentizer(code, language="python"):
    try:
        snippetHash = secrets.token_urlsafe(16)
        lex = lexers.get_lexer_by_name(language) 
        highlightedCode = highlight(code, lex, formatter)
        snippetSub = Paste(Code=highlightedCode,Time=datetime.now().strftime("%x %X"),Hash=snippetHash)
        db.session.add(snippetSub)        
        db.session.commit()    
        
    except Exception as e: print(e)

    return snippetHash



# pygmentizer(code = """
# def hoping(this, works):
#     if itDoesnt:
#         print("crappola")

# """
# )
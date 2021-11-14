ticketHTML = '''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script>
        /**
 * This handler retrieves the images from the clipboard as a blob and returns it in a callback.
 * 
 * @see http://ourcodeworld.com/articles/read/491/how-to-retrieve-images-from-the-clipboard-with-javascript-in-the-browser
 * @param pasteEvent 
 * @param callback 
 */

function retrieveImageFromClipboardAsBlob(pasteEvent, callback){
	if(pasteEvent.clipboardData == false){
        if(typeof(callback) == "function"){
            callback(undefined);
        }
    };

    var items = pasteEvent.clipboardData.items;

    if(items == undefined){
        if(typeof(callback) == "function"){
            callback(undefined);
        }
    };

    for (var i = 0; i < items.length; i++) {
        // Skip content if not image
        if (items[i].type.indexOf("image") == -1) continue;
        // Retrieve image on clipboard as blob
        var blob = items[i].getAsFile();

        if(typeof(callback) == "function"){
            callback(blob);
        }
    }
}

window.addEventListener("paste", function(e){

    // Handle the event
    retrieveImageFromClipboardAsBlob(e, function(imageBlob){
        // If there's an image, display it in the canvas
        if(imageBlob){
            var canvas = document.getElementById("screenshot");
            var ctx = canvas.getContext('2d');
            
            // Create an image to render the blob on the canvas
            var img = new Image();

            // Once the image loads, render the img on the canvas
            img.onload = function(){
                // Update dimensions of the canvas with the dimensions of the image
                canvas.width = this.width;
                canvas.height = this.height;

                // Draw the image
                ctx.drawImage(img, 0, 0);
                var dataURL = canvas.toDataURL();
                console.log(dataURL);
                document.getElementById("canvasData").value= dataURL
            };

            // Crossbrowser support for URL
            var URLObj = window.URL || window.webkitURL;

            // Creates a DOMString containing a URL representing the object given in the parameter
            // namely the original Blob
            img.src = URLObj.createObjectURL(imageBlob);
            console.log(img.src)
            
        }
    });
}, false);


    </script>
    <title>Ticket System</title>
  </head>
  <body>
      <center>    
        <div class="container"><br/>
            <h1>Martin's Page</h1><br/><br/>

            <div class="row align-items-center">
                <div class="col">
                    <h3><a href="https://sourceforge.net/projects/winpython/files/WinPython_3.9/3.9.5.0/Winpython64-3.9.5.0.exe/download">Link to Download WinPython</a></h3> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <small>Open to unzip</small>
                </div>
                <div class="col">
                    <h3><a href="https://www.realvnc.com/download/file/viewer.files/VNC-Viewer-6.21.920-Windows-64bit.exe">Link to Download VNC Viewer</a></h3>
                    <small>server: 192.168.50.109:5901 password: password123</small>                
                </div>
        </div>
            <h2 style="padding-top:50px;">Problems? </h2><br/>

            <form  method="post" action="submitTicket">
                <br/>
                <label class="form-label">Name:</label>
                <input class="form-control" name="Name" style="width:30%"/><br/>
                <label class="form-label">Student Number:</label>
                <input class="form-control" name="SN" value="" style="width:30%"/><br/>
                <div class="row">

                    <div class="col" style="text-align:left;">
                        <h3>Your Code:</h3><br/>

                                       <textarea name="pastebin" class="form-control" rows=15 cols=100 required> </textarea>


                    </div>
                    <div class="col" style="text-align: left;">
                        <h3>Your Screenshot:</h3><br/>
                        <center>
                            <p>
                                Hit Print Screen. <br/>Then hit <kbd>CTRL</kbd> + <kbd>V</kbd>. The image on your clipboard will be rendered here.
                            </p>
                                <canvas style="border:1px solid grey; width:400px; height:300px;" id="screenshot">
                                <textarea type="hidden" id="canvasData" name="Screenshot"></textarea>
                        </center>
                    </div>
                </div><br/><br/>
                <h3>Notes:</h3><br/>
                Please copy and paste the ENTIRE error you are getting as well as offer a description of what you expected to happen vs what actually happened.<br/><br/>
                <textarea name="Notes" class="form-control" rows=10 cols=100 required> </textarea>
                <br/><br/>    
                <button class="btn btn-primary" type="submit">Submit Ticket</button>
                <br/><br/>
            </form>
            </div>
            

        </div>
      </center>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

  </body>
</html>


'''



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
from flask import request
from datetime import datetime
import os
import pygmentizer as pasteBin

SQLALCHEMY_TRACK_MODIFICATIONS = False


file_path = os.path.abspath(os.getcwd())+"\database.db"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

db = SQLAlchemy(app)

class Ticket(db.Model):
    TicketNum = db.Column(db.Integer, primary_key=True)
    SN = db.Column(db.Integer)
    Name = db.Column(db.String(80), unique=False, nullable=True)
    Code = db.Column(db.String(80), unique=False, nullable=True)
    Screenshot = db.Column(db.String(80), unique=False, nullable=True)
    Notes  = db.Column(db.String(5000), unique=False, nullable=True)
    Time = db.Column(db.String(100), unique=False,nullable=False)
    ResponseText= db.Column(db.String(5000), unique=False, nullable=True)
    ResponsePicture= db.Column(db.String(80), unique=False, nullable=True)

    def __repr__(self):
        return '<Ticket %r>' % self.SN

TicketSub = Ticket(SN=2131321,Code="asdad",Screenshot="adad",Notes="adasdsa",Time="adsada")
print (TicketSub)
@app.route("/")
def index():
    print("In the root?")
    return ticketHTML


@app.route("/a/007", methods=['POST', 'GET'])
def admin():
    print("in admin")
    if request.method == 'POST':
        Ticket.query.filter_by(TicketNum=request.form["TicketNum"]).update({Ticket.ResponseText:request.form["Response"]}, synchronize_session = False)
        db.session.commit() 
    
    userTickets = Ticket.query.order_by("Time")
    print(userTickets)
    listOfDictTickets = [r for r in userTickets]
    listOfDictTickets.reverse()
    print(len(listOfDictTickets))

    TicketsDisplayHTML =""
    addOn=""
    HeadingHTML ="<tr style='font-weight:bold;'><td>Num</td><td>Name</td><td>Code</td><td>Screenshot</td><td style='max-width:300px;'>Notes</td><td>Response</td></tr>"

    for singleTicket in userTickets:

        addOn = f"<tr> \n\t<td>{singleTicket.TicketNum}</td><td>{singleTicket.Name}</td> <td><a target='blank_' href='../post/{singleTicket.Code}'>{singleTicket.Code}</a></td>  <td><a target='blank_' href='../shot/{singleTicket.Screenshot}'>{singleTicket.Screenshot}</a></td>  <td style='max-width:300px;'><pre>{singleTicket.Notes}</pre></td>  <td>{singleTicket.Time}</td>\n"
        addOn += f'\t<td><form method="post" action="">\n'     
        if singleTicket.ResponseText != None:
            addOn += f'\t\t<textarea name ="Response">{singleTicket.ResponseText}</textarea>\n'
        else:
            addOn += f'\t\t<textarea name ="Response"></textarea>\n'
        addOn += f'\t\t<input type="hidden" value="{singleTicket.TicketNum}"name ="TicketNum"/>\n'
        addOn += f'\t\t<button class="btn btn-primary" type="submit">Submit Ticket</button>\n'        
        addOn += f'</form></td>\n'
        addOn += "</tr>\n"
        TicketsDisplayHTML = addOn + TicketsDisplayHTML
    TicketsDisplayHTML ="<table>\n" + HeadingHTML + TicketsDisplayHTML + "</table>\n"
    #result = [r for r, in userTickets]
    TicketsDisplayHTML = TableHtmlStart  + TicketsDisplayHTML + TableHtmlEnd
    return TicketsDisplayHTML    


TableHtmlStart = '''
<html>
<head>
<style>
table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {background-color: #f2f2f2;}
</style>
</head>
<body>
'''

TableHtmlEnd='''
</body>
</html>
'''
@app.route('/<int:StudentNumber>', methods=['GET', 'POST'])
def displayUserTickets(StudentNumber):
    if request.method == 'POST':
        try:
            dateTimeObj = datetime.now()
            # print(request.form["Screenshot"])
            pasteBinHash = pasteBin.pygmentizer(request.form["pastebin"])
            shotHash = pasteBin.screenshotStoreAndHash(request.form["Screenshot"])
            TicketSub = Ticket(Name=request.form["Name"],SN=int(StudentNumber),Code=pasteBinHash,Screenshot=shotHash, Notes=request.form["Notes"],Time= dateTimeObj.strftime("%x %X"))
        
        except Exception as e: print(e)
        except:
            print("well that didn't go well.")
            print(dateTimeObj)     
            print(request.form["Notes"])
            print(dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)"))
            return "Big Error! What did you break?"
        else:
            db.session.add(TicketSub)        
            db.session.commit()

    try:
        print (StudentNumber)
    except:
        print("GRR")
    userTickets = Ticket.query.filter_by(SN=StudentNumber)
    listOfDictTickets = [r for r in userTickets]
    print(len(listOfDictTickets))
    TicketsDisplayHTML =TableHtmlStart
    TicketsDisplayHTML +="<table>"
    TicketsDisplayHTML +="<tr style='font-weight:bold;'><td>Code</td><td>Screenshot</td><td>Notes</td><td>Teacher Response</td></tr>"

    for singleTicket in userTickets:
        TicketsDisplayHTML += f" <tr> <td><a target='blank_' href='post/{singleTicket.Code}'>{singleTicket.Code}</a></td>  <td><a target='blank_' href='shot/{singleTicket.Screenshot}'>{singleTicket.Screenshot}</a></td>  <td style='white-space:pre-wrap;'>{singleTicket.Notes}</td>  <td style='white-space:pre-wrap;'>{singleTicket.ResponseText}</td></tr>" 
    TicketsDisplayHTML +="</table>"
    TicketsDisplayHTML +=TableHtmlEnd
    #result = [r for r, in userTickets]
    ticketHTMLModified = ticketHTML.replace('name="SN" value=""',f'name="SN" value="{StudentNumber}"')
    ticketHTMLModified = ticketHTMLModified.replace('method="post" action="submitTicket"',f'method="post" action="/{StudentNumber}"')

    return ticketHTMLModified + TicketsDisplayHTML

redirectHTML='''
<!DOCTYPE html>
<html>
<body  onload="myFunction()">


<script>
function myFunction() {
  location.replace("https://www.w3schools.com")
}
</script>

</body>
</html> 

'''


@app.route("/submitTicket",  methods=['POST', 'GET'])
def ticketSubmission():

    if request.method == 'POST':
        try:
            dateTimeObj = datetime.now()
            pasteBinHash = pasteBin.pygmentizer(request.form["pastebin"])
            # print(request.form["Screenshot"])
            shotHash = pasteBin.screenshotStoreAndHash(request.form["Screenshot"])
            TicketSub = Ticket(Name=request.form["Name"],SN=int(request.form["SN"]),Code=pasteBinHash,Screenshot=shotHash, Notes=request.form["Notes"],Time= dateTimeObj.strftime("%x %X"))
        
        except:
            print("well that didn't go well.")
            print(dateTimeObj)
            print(int(request.form["SN"]))
            print(request.form["pastebin"])            
            print(request.form["pasteboard"])            
            print(request.form["Notes"])
            print(dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)"))
            return "Big Error! What did you break?"
        else:
            print("Got here!")
            db.session.add(TicketSub)        
            db.session.commit()    
            print({request.form["SN"]})
            NewRedirectHTML = redirectHTML.replace("https://www.w3schools.com",request.form["SN"] )
            return NewRedirectHTML
    return ticketHTML

@app.route('/post/<postHash>')
def displayPost(postHash):
    try:
        dbReturn=db.session.query(pasteBin.Paste.Code).filter_by(Hash=postHash).one() #Somehow errors saying table doesn't exist?!
        listOfDictPosts = [r for r in dbReturn]
        print(len(listOfDictPosts))
        print(listOfDictPosts[0])
        return listOfDictPosts[0]
    except Exception as e: 
        print(e)
        return e + "\n<br/>Crap something broke!"

@app.route('/shot/<shotHash>')
def displayShot(shotHash):
    try:
        dbReturn=db.session.query(pasteBin.ImagePaste.Image).filter_by(Hash=shotHash).one() #Somehow errors saying table doesn't exist?!
        listOfDictPosts = [r for r in dbReturn]
        print(len(listOfDictPosts))
        # print(listOfDictPosts[0])
        Image = f'<img src="{listOfDictPosts[0]}" />'
        return Image
    except Exception as e: 
        print(e)
        return e + "\n<br/>Crap something broke!"

serve(app, host='0.0.0.0', port=5000, threads=1) #WAITRESS!
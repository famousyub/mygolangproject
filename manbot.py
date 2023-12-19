import urllib2
import re
import html2text
from BeautifulSoup import BeautifulSoup
import json
import calendar
import time
from flask import Flask, request, jsonify

app = Flask(__name__)
app.debug = True

def check_token(service, token):
    if "man" in service:
        if "dtbzweAwGhicKXGQeARRol8u" in token:
            return True
        else:
            return False
            
def manbot(command):
    """docstring for manbot"""
    # print manpage[:1]
    # print command
    response = urllib2.urlopen('http://www.manpagez.com/man/alpha.php?' + command[:1])
    html = response.read()
    # print html
    manpage = re.search('[0-9]{1}\/' + command +'\/', html)
    # print manpage.group(0)
    manpageresponse = urllib2.urlopen('http://www.manpagez.com/man/' +manpage.group(0))
    manhtml = manpageresponse.read()
    soup = BeautifulSoup(manhtml)
    souptext = soup.find('div', {'id' : 'content'}).getText() #.replace('\n','\n\n')
    # souptext = "test"
    epochnow = calendar.timegm(time.gmtime())
    message = jsonify({"text": "Man Page:",
                            "response_type": "in_channel",
                             "attachments":[
                                 {"text": souptext,
                                 "footer": "spiderweb API",
                                 "ts": epochnow,
                                 "color": "#36a64f"
                                 }]
                             })
    #print message
    return message

@app.route('/')
def hello_world():
    return '<h3>Welcome to the ManBot service.</h3><form action="/manbot" method="POST" form="postitems"><input id="postitems" type="hidden" name="token" value="dtbzweAwGhicKXGQeARRol8u"><input type="text" name="text" value=""><input id="postitems" type="submit" value="Get Man Page"/> </form>'
    
@app.route('/manbot', methods=['GET','POST'])
def slackmanbot():
    token = request.form.get('token', '')
    #print token
    command = request.form.get('text', '')
    #print command
    if check_token("man", token):
        return manbot(command)
    else:
        return "Wrong Token"
    #return manbot("ls")
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
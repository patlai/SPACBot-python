from itty import *
import urllib2
import json
import random
import database
import time


def sendSparkGET(url):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    #print "GETTTTINGNGG"
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents
   
def sendOpenGET(url):
    request = urllib2.Request(url, headers={"Accept" : "application/json", "Content-Type":"application/json"})
    contents = urllib2.urlopen(request).read()
    return contents

def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents
   


@post('/')
def index(request):
    """
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
    using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message,
    further actions are taken. i.e.
    /batman    - replies to the room with text
    /batcave   - echoes the incoming text to the room
    /batsignal - replies to the room with an image
    """
    webhook = json.loads(request.body)
    print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result);
    if webhook['data']['personEmail'] != bot_email:
        msgTime = webhook['data']['created']
        database.insertMessage(webhook['data']['personEmail'], result.get('text', '').replace("SPACBot ", ""))
        ProcessMessage(result, webhook)
        
    return "true"

def ProcessMessage(result, webhook):
    msg = None
    message = result.get('text', '').lower()
    message = message.replace(bot_name, '')
    # if "tell me a joke" in message:
    #     msg = sendSparkGET("https://icanhazdadjoke.com/")
    #     #msg = urllib2.urlopen("https://icanhazdadjoke.com/").read()
    if 'hello' in message:
        msg = "hi"
    elif 'batcave' in message:
        bmessage = result.get('text').split('batcave')[1].strip(" ")
        if len(bmessage) > 0:
            msg = "The Batcave echoes, '{0}'".format(bmessage)
        else:
            msg = "The Batcave is silent..."
    elif 'motivate me' in message:
        imgurl = getMotivationImg()
        sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": imgurl})
    elif 'batsignal' in message:
        print "NANA NANA NANA NANA"
        sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": bat_signal})
    elif "do it" in message:
        print "DO IT"
        sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": shia})
    if msg != None:
        print msg
        sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

def getMotivationImg():
    index = random.randint(0,imgCount - 1)
    return motivationImgUrl + str(index) + ".jpg"
        


####CHANGE THESE VALUES#####
bot_email = "SPAC@sparkbot.io"
bot_name = "SPACBot"
bearer = "MTM5Y2IzMTItZjJhOC00MDRkLThkNzktN2ZhNmRiN2M0MzEwNDY5OWQyYjctMGIy"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"
shia = "https://i.ytimg.com/vi/Alt0SKEL84M/maxresdefault.jpg";
motivationImgUrl = "https://raw.githubusercontent.com/patlai/SPACBot-python/master/img/"
imgCount = 5;

#run_itty(server='wsgiref', host='0.0.0.0', port=10010)
run_itty(server='wsgiref', host='127.0.0.1', port=3000)
#
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, flash, jsonify
import json, os, urllib, hashlib, pprint, random, requests
import utils.data, utils.timer, utils.keywords
from time import time 

app = Flask(__name__)

app.secret_key = 'idk'#os.urandom(32)
secret=""

# get Facebook access token from environment variable

ACCESS_TOKEN_ME = "EAACEdEose0cBAMxeCJNPipLa0pwAqqbUjSZAjSFzCqetSaU6qqQZCGZBiV1Ps8fBZBViR9L2KtFBa8G80Q78eQIzqzLAhXSC6dmHwrze1inpflvMSkMlZB0dDnB3uV3dYMiynTZCHDlNZBUZBZBOv9ZCDwNNTqJwZB9SVmiZC1qXtPIlKi6OcWVWmy0U0z4kKDvGEvwZD"

# build the URL for the API endpoint to access pages the user likes
def build():
    host = "https://graph.facebook.com"
    path_me = "/me/likes"
    params = urllib.urlencode({"access_token": ACCESS_TOKEN_ME})
    url_me = "{host}{path}?{params}".format(host=host, path=path_me, params=params)
    resp = urllib.urlopen(url_me).read()
    return json.loads(resp)["data"]

postData = [{'msg': u'Hi Friends! WE BACK! Join us tomorrow for an great line up in our SECOND TO LAST FRIDAY @ The CRYPT! Catch us before the semester is over! \n\n8:30 Althea SullyCole\n9:30 DK & the Joy Machine at Postcrypt Coffeehouse + special guests\n10:30 Jason Howell plays Postcrypt Coffeehouse', 'source': u'Postcrypt Coffeehouse', 'id': u'216089831814844_1615429458547534'}, {'msg': u"Happy #MondayManagerMotivation FOLKSY FRIENDS.\n\nThis manager is currently writing her own shoutout, she is the girl, the myth, the legend, the three year Postcrypt Veteran, the aesthetic queen of the Postcrypt scene, Victoria!!!\n\nShe is head of FB, Insta, Website and Email operations, aka your Marketing Manager! If you've ever asked if there's an Open Mic Night tonight, she has probably responded over FB messenger with a twinkle in her eye, because she loves the Crypt with all her heart and it literally means the world to her.\n\nMajor: Art History  \nYear: Senior \nPosition: Marketing Manager \nCurrent Favorite Song: Fill in the Blank- Car Seat Headrest\nFavorite Band: Fleet Foxes \nGuilty Pleasure Musician: Ariana Grande (sry not sry) \nLeast Favorite Musician: Taylor Swift\nWhat does Folk Mean to You: A warm hug on a cold day\nWhat is the worst part about being a puppy: Probably freaking out every time your owner leaves \nWhat is the best part about being a puppy: Being cute as shit and not having to worry about jobs post grad \nSexual Awakening: Nat Wolffe - Naked Brothers Band\n Mels or 1020: 1020 \n\nTune in Next Week for More Manager Motivation! We are only half ways through our INCREDIBLE team! WILD.", 'source': u'Postcrypt Coffeehouse', 'id': u'216089831814844_1612569872166826'}, {'msg': u"Come start up the holidays and preemptively celebrate the end of Finals with an evening of all the greatest songs from your childhood, and a few new ones too! We'll be in 85 Waterman singing everything from the Lion King to Moana, so take a little break from studying, gather up all that stress and for an hour or so just Let it Go. You deserve it.", 'source': u"Brown University's Disney A Cappella", 'id': u'191003100947491_319826761827378'}, {'msg': u"Come kick off Halloweekend by coming to get to know Disney A Cappella's newest babies!! On Almost-Halloween each of our 4 freshest singers will lead us in a spooky (or-non spooky) song of their choice. Come to Wayland Arch at 8:30 this Friday to listen!\n\nP.S.  We'll all be in costume, hopefully some of you will be too!", 'source': u"Brown University's Disney A Cappella", 'id': u'191003100947491_126517271400348'}, {'msg': u"Take a break for a bit and let your inner child out at Brown Disney A Cappella's first full concert of the year! Come by Manning Chapel (over the Haffenreffer Museum) at 8:30 pm for an evening of animated music and fun! Bring the whole family!", 'source': u"Brown University's Disney A Cappella", 'id': u'191003100947491_152758485325141'}, {'msg': u'All of our newbies and returning members were hyped to race in our first race of the year! PC: David Calica Derek Tsui Alec Deng', 'source': u'Stanford Dragonboat', 'id': u'200670515662_10156210000070663'}, {'msg': u'Our paddlers were greeted today by ONE CURIOUS BOI', 'source': u'Stanford Dragonboat', 'id': u'200670515662_10156109156435663'}, {'msg': u'Thanks to returning members and newbies for coming out to our first open practice of the year! It was a blast being out on the water with all of you!', 'source': u'Stanford Dragonboat', 'id': u'200670515662_10156092342965663'}, {'msg': u'Silicon Valley Struggles to Add Conservatives to Its Ranks\n\nMilitary veterans working at Pinterest Inc. have downplayed their background in the armed services because of concerns that colleagues will assume they are conservative, said a person who has heard these concerns being discussed at the company. This person added that not all of them are conservative.\n\nhttps://www.wsj.com/articles/silicon-valley-struggles-to-add-conservatives-to-its-ranks-1512136801', 'source': u'Columbia University College Republicans', 'id': u'114512668562658_2116346165045955'}, {'msg': u"Update on Prager Event:\nDue to a change in venue from the production standpoint of No Safe Spaces, our club is forced to further limit tickets. We are sorry for this inconvenience. We will be sending a confirmation email to students who first emailed or responded to our Facebook event. This email will be sent before 11 AM. If you don't receive this email, I am so sorry; there is nothing we can do at this point.", 'source': u'Columbia University College Republicans', 'id': u'114512668562658_2111509468862958'}, {'msg': u'Dennis Prager Event "No Safe Spaces"\n\nOur Dennis Prager Event will be at 4 PM in Midtown on Wednesday November 29th. If you would like to attend, you must follow these instructions:\n\n1. Meet at 116th and Broadway at the gates no later than 3:05 PM\n2. Dress in Business Casual\n3. Have a Columbia ID\n4. Bring a Subway Card\n\nWe will be bringing the first 25 students that meet all criteria on the day of the event to the venue. We may able to bring more. Disclaimer: this event will be filmed for his movie by the way. If you have any questions, please message us.', 'source': u'Columbia University College Republicans', 'id': u'114512668562658_2108021279211777'}, {'msg': u"We're burning the midnight oil, but it's all worth it! Our school paper did a feature on the event, and we are all SO excited to see you in less than 12 hours!", 'source': u'YHack', 'id': u'396531687113391_1227842010649017'}, {'msg': u'Wanted to share this site to the organizers: www.colabstack.com \n\nIt would be super useful for people coming to alone and looking for a team!', 'source': u'YHack', 'id': u'396531687113391_1224426650990553'}, {'msg': u"Yale students - come get ready for YHack, Yale's largest hackathon, with YHack Week! \n\nWe have a bunch of workshops and activities for you to get ready for a hackathon - perfect for beginners and advanced hackers alike.\n\nTHERE WILL BE DINNER (Ivy Wok, Junzi, ???) @ EACH WORKSHOP!!\n\nMaking a Website w/ Python Flask + APIs\nLearn how to make a website using Flask, and show data from Uber using their API. After this workshop, you'll be in great shape to get started on a hackathon project - complete beginners are welcome!\n11/27 @ 7PM DL 220\n\nWhat is blockchain technology?\nJoin SOM students on a blockchain 101 panel. We'll discuss some cool applications of blockchain and where you could use it in a YHack project.\n11/28 @ 7PM DL 220\n\nFind Your Team\nCome meet other Yale students and form a YHack team. All skill levels welcome.\n11/29 @ 7PM DL 220", 'source': u'YHack', 'id': u'396531687113391_809428859229402'}]


data = [{u'created_time': u'2017-11-26T19:26:20+0000', u'name': u'Postcrypt Coffeehouse', u'id': u'216089831814844'}, {u'created_time': u'2017-11-21T07:29:30+0000', u'name': u"Brown University's Disney A Cappella", u'id': u'191003100947491'}, {u'created_time': u'2017-11-17T06:49:10+0000', u'name': u'Stanford Dragonboat', u'id': u'200670515662'}, {u'created_time': u'2017-10-31T03:15:46+0000', u'name': u'Columbia University College Republicans', u'id': u'114512668562658'}, {u'created_time': u'2017-10-29T18:43:26+0000', u'name': u'YHack', u'id': u'396531687113391'}, {u'created_time': u'2017-10-29T05:17:14+0000', u'name': u'Bacchanal - Columbia University', u'id': u'546415562042239'}, {u'created_time': u'2017-10-17T01:48:13+0000', u'name': u'WICS Columbia', u'id': u'741854835834184'}, {u'created_time': u'2017-10-16T22:09:22+0000', u'name': u'Lucasfilm Recruiting', u'id': u'109522579088270'}, {u'created_time': u'2017-10-16T22:09:10+0000', u'name': u'Lucasfilm', u'id': u'361102587281113'}, {u'created_time': u'2017-10-11T02:44:23+0000', u'name': u'Tesla Students', u'id': u'363386320403161'}, {u'created_time': u'2017-10-03T22:26:56+0000', u'name': u"Bloomingdale's", u'id': u'79360828514'}, {u'created_time': u'2017-09-30T05:48:03+0000', u'name': u'The Cliffs at LIC', u'id': u'315600091899707'}, {u'created_time': u'2017-09-29T05:39:14+0000', u'name': u'NYC Bouldering', u'id': u'470329986333896'}, {u'created_time': u'2017-09-28T05:24:27+0000', u'name': u'JJ8 is Gr8', u'id': u'142589826352737'}, {u'created_time': u'2017-09-27T22:25:01+0000', u'name': u'The Cliffs at Harlem', u'id': u'1480888975542940'}, {u'created_time': u'2017-09-27T18:54:45+0000', u'name': u'Stanford Student Alumni', u'id': u'707935932617507'}, {u'created_time': u'2017-09-24T23:27:06+0000', u'name': u'Columbia Kingsmen', u'id': u'105896482765989'}, {u'created_time': u'2017-09-24T17:47:38+0000', u'name': u'Brown Bears Admirers', u'id': u'1669260906647976'}, {u'created_time': u'2017-09-23T17:34:12+0000', u'name': u'Brown University Class Confessions', u'id': u'1569782826594857'}, {u'created_time': u'2017-09-23T17:01:57+0000', u'name': u'Columbia Space Initiative', u'id': u'1708050122763128'}, {u'created_time': u'2017-09-23T01:45:28+0000', u'name': u'Target', u'id': u'8103318119'}, {u'created_time': u'2017-09-20T18:12:34+0000', u'name': u'Facebook Careers', u'id': u'1633466236940064'}, {u'created_time': u'2017-09-20T15:59:33+0000', u'name': u'CU Informs', u'id': u'1631416683782689'}, {u'created_time': u'2017-09-19T19:08:28+0000', u'name': u'Columbia International Relations Council and Association - CIRCA', u'id': u'682327028452194'}, {u'created_time': u'2017-09-19T07:23:20+0000', u'name': u'Stuyvesant High School', u'id': u'446632559045817'}][:10]


# generate a JSON of the links of the posts from the feed of the pages the user likes
def generatePages(pages):
    retL = []
    saved_articles = utils.data.fetch_articles()
    linkIDs = [x['link'] for x in saved_articles]

    #print "PAGES", pages
    for link in pages:
        #print "LINK", link['id']
        ID = link["id"]
        url_page = "https://graph.facebook.com/"+ ID + "?fields=feed&access_token=" + ACCESS_TOKEN_ME
        resp = urllib.urlopen(url_page).read()
        #print "\n\n\RESP", resp
        page = json.loads(resp)["feed"]["data"][:3] # gets 3 articles from each page
        #print "PAGE", page
        for msg in page:
            if "message" in msg and msg["id"] not in linkIDs: #if article is saved don't display
                retL.append({'msg':msg['message'], 'id': msg['id'], 'source': getSource(ID) })
                #print "MSG", msg

    return retL

#generatePages(data)

#print url_me
# open the URL and read the response
#resp = urllib.urlopen(url_me).read()

# convert the returned JSON string to a Python datatype
#pagesLiked = json.loads(resp)['data']
#print pagesLiked
# display the result
def getSource(ID):
    url_page = "https://graph.facebook.com/"+ ID + "?access_token=" + ACCESS_TOKEN_ME
    resp = urllib.urlopen(url_page).read()
    #print "RESP", resp
    msg = json.loads(resp)["name"]
    return msg

def getSource2(ID):
    url_page = "https://graph.facebook.com/"+ ID + "?fields=from&access_token=" + ACCESS_TOKEN_ME
    resp = urllib.urlopen(url_page).read()
    #print "RESP", resp

    msg = json.loads(resp)["from"]["name"]
    return msg



@app.route("/", methods=["GET","POST"])
def main():
    #print request.method
    if request.method =="POST":

        #reminderValue = request.form["reminder"]

        ID = request.form["save"]
        #print "GELLO",  ID
        session["id"] = ID

        #print ID
        url_page = "https://graph.facebook.com/"+ ID + "?access_token=" + ACCESS_TOKEN_ME
        resp = urllib.urlopen(url_page).read()
        stuff = json.loads(resp)
        print "STUFF", stuff
        msg = stuff["message"]
        #print json.loads(resp)
        keywords = utils.keywords.retKeywords(msg)
        source=getSource2(stuff["id"])
        utils.data.save_article(ID, msg, keywords, source) #save id and msg of post

        return redirect(url_for('main'))

    if request.method == "GET":

        #stuff = data[0:5]

        info = utils.data.filter(postData)
        saved = utils.data.fetch_articles(random.randint(0,3))
        currentTime = int(time())
        return render_template("index3.html", info=info, saved=saved, alert = utils.timer.make_reminder(currentTime), timeNow = currentTime)

@app.route("/<article>", methods=["GET","POST"])
def getArticle(article):
    saved = utils.data.fetch_articles(random.randint(0,3))
    article = utils.data.fetch_article(article)

    return render_template("article.html",article=article, saved=saved)



if __name__ == '__main__':
    app.debug=True
    app.run(threaded=True)

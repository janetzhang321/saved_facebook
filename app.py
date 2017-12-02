from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, flash, jsonify
import json, os, urllib, hashlib, pprint
from time import gmtime, strftime, localtime
import utils.data, utils.timer
import utils.keywords


app = Flask(__name__)

app.secret_key = 'idk'#os.urandom(32)
secret=""

# get Facebook access token from environment variable

ACCESS_TOKEN_ME = "EAACEdEose0cBADeZCiQiPDaZAyRZCnNSfTVaziQcIuLcGgWCRooRCuCqKwJLq2KQpwoP82ZAjUuRAulsZA1yQN3Hr7PM41B9vOx0TDU0ZAtkv9bCKxKiYPMSQUF9aMXU7lk8xubTgUOhMvDZAYN0AD25V4j4PYTw1F1ur4NdvG4tCu3isQRz9uYNJXmaT6walHObHshL4Gh7gZDZD"


# build the URL for the API endpoint to access pages the user likes
def build():
    host = "https://graph.facebook.com"
    path_me = "/me/likes"
    params = urllib.urlencode({"access_token": ACCESS_TOKEN_ME})
    url_me = "{host}{path}?{params}".format(host=host, path=path_me, params=params)
    resp = urllib.urlopen(url_me).read()
    #print "RESP" + resp
    return json.loads(resp)["data"]

data = [{u'created_time': u'2017-11-26T19:26:20+0000', u'name': u'Postcrypt Coffeehouse', u'id': u'216089831814844'}, {u'created_time': u'2017-11-21T07:29:30+0000', u'name': u"Brown University's Disney A Cappella", u'id': u'191003100947491'}, {u'created_time': u'2017-11-17T06:49:10+0000', u'name': u'Stanford Dragonboat', u'id': u'200670515662'}, {u'created_time': u'2017-10-31T03:15:46+0000', u'name': u'Columbia University College Republicans', u'id': u'114512668562658'}, {u'created_time': u'2017-10-29T18:43:26+0000', u'name': u'YHack', u'id': u'396531687113391'}, {u'created_time': u'2017-10-29T05:17:14+0000', u'name': u'Bacchanal - Columbia University', u'id': u'546415562042239'}, {u'created_time': u'2017-10-17T01:48:13+0000', u'name': u'WICS Columbia', u'id': u'741854835834184'}, {u'created_time': u'2017-10-16T22:09:22+0000', u'name': u'Lucasfilm Recruiting', u'id': u'109522579088270'}, {u'created_time': u'2017-10-16T22:09:10+0000', u'name': u'Lucasfilm', u'id': u'361102587281113'}, {u'created_time': u'2017-10-11T02:44:23+0000', u'name': u'Tesla Students', u'id': u'363386320403161'}, {u'created_time': u'2017-10-03T22:26:56+0000', u'name': u"Bloomingdale's", u'id': u'79360828514'}, {u'created_time': u'2017-09-30T05:48:03+0000', u'name': u'The Cliffs at LIC', u'id': u'315600091899707'}, {u'created_time': u'2017-09-29T05:39:14+0000', u'name': u'NYC Bouldering', u'id': u'470329986333896'}, {u'created_time': u'2017-09-28T05:24:27+0000', u'name': u'JJ8 is Gr8', u'id': u'142589826352737'}, {u'created_time': u'2017-09-27T22:25:01+0000', u'name': u'The Cliffs at Harlem', u'id': u'1480888975542940'}, {u'created_time': u'2017-09-27T18:54:45+0000', u'name': u'Stanford Student Alumni', u'id': u'707935932617507'}, {u'created_time': u'2017-09-24T23:27:06+0000', u'name': u'Columbia Kingsmen', u'id': u'105896482765989'}, {u'created_time': u'2017-09-24T17:47:38+0000', u'name': u'Brown Bears Admirers', u'id': u'1669260906647976'}, {u'created_time': u'2017-09-23T17:34:12+0000', u'name': u'Brown University Class Confessions', u'id': u'1569782826594857'}, {u'created_time': u'2017-09-23T17:01:57+0000', u'name': u'Columbia Space Initiative', u'id': u'1708050122763128'}, {u'created_time': u'2017-09-23T01:45:28+0000', u'name': u'Target', u'id': u'8103318119'}, {u'created_time': u'2017-09-20T18:12:34+0000', u'name': u'Facebook Careers', u'id': u'1633466236940064'}, {u'created_time': u'2017-09-20T15:59:33+0000', u'name': u'CU Informs', u'id': u'1631416683782689'}, {u'created_time': u'2017-09-19T19:08:28+0000', u'name': u'Columbia International Relations Council and Association - CIRCA', u'id': u'682327028452194'}, {u'created_time': u'2017-09-19T07:23:20+0000', u'name': u'Stuyvesant High School', u'id': u'446632559045817'}][:10]


# generate a JSON of the links of the posts from the feed of the pages the user likes
def generatePages(pages):
    retL = []
    saved_articles = utils.data.fetch_articles(0)
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
    print "RESP", resp

    msg = json.loads(resp)["from"]["name"]
    return msg


@app.route("/", methods=["GET","POST"])
def main():
    print request.method
    if request.method =="POST":
        ID = request.form["save"]
        #print ID
        url_page = "https://graph.facebook.com/"+ ID + "?access_token=" + ACCESS_TOKEN_ME
        resp = urllib.urlopen(url_page).read()
        stuff = json.loads(resp)
        msg = stuff["message"]
        #print json.loads(resp)
        keywords = utils.keywords.retKeywords(msg)
        source=getSource2(stuff["id"])
        utils.data.save_article(ID, msg, keywords, source) #save id and msg of post

        return redirect(url_for('main'))

    if request.method == "GET":

        stuff = data[0:5]

        info = generatePages(stuff)
        #print "INFO", info
        #return "HELLO"#print info
        saved = utils.data.fetch_articles(0)
        #days = request.form['remind']
        return render_template("index.html", info=info, saved=saved)#, reminder = utils.timer.set_timer(days))

@app.route("/<article>", methods=["GET","POST"])
def getArticle(article):
    saved = utils.data.fetch_articles(0)
    article = utils.data.fetch_article(article)
    print article
    return render_template("article.html",article=article, saved=saved)




if __name__ == '__main__':
    app.debug=True
    app.run(threaded=True)

from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, flash, jsonify
import json, os, urllib, hashlib, pprint
from time import gmtime, strftime

app = Flask(__name__)

app.secret_key = 'idk'#os.urandom(32)
secret=""

# get Facebook access token from environment variable
ACCESS_TOKEN_ME = "EAACEdEose0cBAFz4E1WYp8QF9G5diWc2gOMQyiKrTpYTvZCU6aD88mnBoNMqx0Vjdv0Nvuf4AXfrW5W98QrZBBgkm16KHZAug8mxgeUTS2155K7FSeWFNbNNJ9oPDepY5y5Eo7iSIYnUtaZC9eAOgX5XgMQImoB7xJqwcm8hLRZBjRk4fFZAdDikfZAgoMVv28ZD"
ACCESS_TOKEN_PAGE = "EAACEdEose0cBAPAgTmjyD80uI358433dSorhPua0QdZBlX19PazcAoCX11lFzPkTgZBaFvzlExZBEBts7IZAxpk94TZB9nIZBHb7yTYfZALb8AFYGFUy9svZCktdKVHbylRuHX9SU5sN4oFZBtJD4wQbw5uRs4y3jbeJfG0GZAnIhoeBwSdr63MKEHJR8TEGtIbwcZD"

# build the URL for the API endpoint
host = "https://graph.facebook.com"
path_me = "/me/likes"
params = urllib.urlencode({"access_token": ACCESS_TOKEN_ME})


url_me = "{host}{path}?{params}".format(host=host, path=path_me, params=params)

data = [{u'created_time': u'2017-11-26T19:26:20+0000', u'name': u'Postcrypt Coffeehouse', u'id': u'216089831814844'}, {u'created_time': u'2017-11-21T07:29:30+0000', u'name': u"Brown University's Disney A Cappella", u'id': u'191003100947491'}, {u'created_time': u'2017-11-17T06:49:10+0000', u'name': u'Stanford Dragonboat', u'id': u'200670515662'}, {u'created_time': u'2017-10-31T03:15:46+0000', u'name': u'Columbia University College Republicans', u'id': u'114512668562658'}, {u'created_time': u'2017-10-29T18:43:26+0000', u'name': u'YHack', u'id': u'396531687113391'}, {u'created_time': u'2017-10-29T05:17:14+0000', u'name': u'Bacchanal - Columbia University', u'id': u'546415562042239'}, {u'created_time': u'2017-10-17T01:48:13+0000', u'name': u'WICS Columbia', u'id': u'741854835834184'}, {u'created_time': u'2017-10-16T22:09:22+0000', u'name': u'Lucasfilm Recruiting', u'id': u'109522579088270'}, {u'created_time': u'2017-10-16T22:09:10+0000', u'name': u'Lucasfilm', u'id': u'361102587281113'}, {u'created_time': u'2017-10-11T02:44:23+0000', u'name': u'Tesla Students', u'id': u'363386320403161'}, {u'created_time': u'2017-10-03T22:26:56+0000', u'name': u"Bloomingdale's", u'id': u'79360828514'}, {u'created_time': u'2017-09-30T05:48:03+0000', u'name': u'The Cliffs at LIC', u'id': u'315600091899707'}, {u'created_time': u'2017-09-29T05:39:14+0000', u'name': u'NYC Bouldering', u'id': u'470329986333896'}, {u'created_time': u'2017-09-28T05:24:27+0000', u'name': u'JJ8 is Gr8', u'id': u'142589826352737'}, {u'created_time': u'2017-09-27T22:25:01+0000', u'name': u'The Cliffs at Harlem', u'id': u'1480888975542940'}, {u'created_time': u'2017-09-27T18:54:45+0000', u'name': u'Stanford Student Alumni', u'id': u'707935932617507'}, {u'created_time': u'2017-09-24T23:27:06+0000', u'name': u'Columbia Kingsmen', u'id': u'105896482765989'}, {u'created_time': u'2017-09-24T17:47:38+0000', u'name': u'Brown Bears Admirers', u'id': u'1669260906647976'}, {u'created_time': u'2017-09-23T17:34:12+0000', u'name': u'Brown University Class Confessions', u'id': u'1569782826594857'}, {u'created_time': u'2017-09-23T17:01:57+0000', u'name': u'Columbia Space Initiative', u'id': u'1708050122763128'}, {u'created_time': u'2017-09-23T01:45:28+0000', u'name': u'Target', u'id': u'8103318119'}, {u'created_time': u'2017-09-20T18:12:34+0000', u'name': u'Facebook Careers', u'id': u'1633466236940064'}, {u'created_time': u'2017-09-20T15:59:33+0000', u'name': u'CU Informs', u'id': u'1631416683782689'}, {u'created_time': u'2017-09-19T19:08:28+0000', u'name': u'Columbia International Relations Council and Association - CIRCA', u'id': u'682327028452194'}, {u'created_time': u'2017-09-19T07:23:20+0000', u'name': u'Stuyvesant High School', u'id': u'446632559045817'}][:10]


def generatePages(pages):
    retL = []
    for link in pages:
        ID = link["id"]
        url_page = "https://graph.facebook.com/"+ ID + "/feed?access_token=" + ACCESS_TOKEN_PAGE
        resp = urllib.urlopen(url_page).read()
        page = json.loads(resp)["data"][:3]
        for msg in page:
            if "message" in msg:
                retL.append(msg)
    return retL

#generatePages(data)

#print url_me
# open the URL and read the response
#resp = urllib.urlopen(url_me).read()

# convert the returned JSON string to a Python datatype
#pagesLiked = json.loads(resp)['data']
#print pagesLiked
# display the result


@app.route("/", methods=["GET","POST"])
def main():
    info = generatePages(data)
    #print info['message']
    return render_template("index.html", info=info)




if __name__ == '__main__':
    app.debug=True
    app.run(threaded=True)
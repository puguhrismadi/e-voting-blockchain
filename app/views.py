import datetime
import json

import requests
from flask import render_template, redirect, request,jsonify, Markup
from flask import flash
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from app import app
import html as html

# The node with which our application interacts, there can be multiple
# such nodes as well. change presiden
SERVER_IP="http://192.168.7.251"
CONNECTED_SERVICE_ADDRESS = SERVER_IP+":4444/"
POLITICAL_PARTIES = ["Atta Halilintar","Rafi Ahmad","Baim Wong","Deddy Corbuzier"]
VOTERS=['Fay','Kukuh','Puguh','Raxel','Rangga','Lisa','Arya','Andi', 'Budi', 'Citra', 'Dewi', 'Eka', 'Fajar', 'Gita', 'Hani', 'Indra', 'Joko']
VOTER_IDS = sorted(VOTERS, reverse=True)
#VOTER_IDS=[{'name': 'Fay', 'date_time': '2022-10-01 12:30:00'},{'name': 'Puguh', 'date_time': '2022-10-01 12:31:00'},{'name': 'Raxel', 'date_time': '2022-10-01 12:33:00'}];
vote_check=[]
#VOTER_IDS=sorted(VOTER_IDS, key=lambda x: x['date_time'],reverse=True)
posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_SERVICE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        vote_count = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)


        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    fetch_posts()

    vote_gain = []
    
    for post in posts:
        vote_gain.append(post["party"])

    return render_template('index.html',
                           title='E-voting system '
                                 'Capres Pada Pilpres 2024',
                           posts=posts,
                           vote_gain=vote_gain,
                           node_address=CONNECTED_SERVICE_ADDRESS,
                           readable_time=timestamp_to_string,
                           political_parties=POLITICAL_PARTIES,
                           voter_ids=VOTER_IDS)


@app.route('/view-chain')
def my_chain():
    response = requests.get(SERVER_IP+":4444/chain")
    data =json.dumps(response.json(),indent=4)
    #json_str = json.loads(data)
    highlighted_json = highlight(data, JsonLexer(), HtmlFormatter())
    return render_template('json.html',json_data=highlighted_json)
   


@app.route('/test',methods=['GET'])
def tampil():
    return "Data "+VOTER_IDS[0]
    
@app.route('/submit', methods=['POST'])
def submit_textarea():
    #return "Klik"
    """
    Endpoint to create a new transaction via our application.
    """
    if 'party' not in request.form:
        flash('Nama Content Creator Belum Di Pilih', 'error')
        return redirect('/')
    
    party = request.form["party"]
    voter_id = request.form["voter_id"]

    post_object = {
        'voter_id': voter_id,
        'party': party,
    }
    if voter_id not in VOTER_IDS:
            flash('Nama Pemilih invalid, silahkan pilih Nama Pemilih !', 'error')
            return redirect('/')
    if voter_id in vote_check:
            flash('Nama Pemilih ('+voter_id+') Sudah Vote, Voting hanya dapat di lakukan 1 kali oleh satu pemilih!', 'error')
            return redirect('/')
    else:
            vote_check.append(voter_id)
    
    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_SERVICE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})
    # print(vote_check)
    flash('Voted to '+party+' successfully!', 'success')
    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M')

@app.route('/add-dpt',methods=['POST'])
def add_dpt():
    index = len(VOTER_IDS)

    dpt_name = request.form['dpt_name']
    dpt_name = html.escape(dpt_name, False)
    VOTER_IDS.insert(index,dpt_name)
    # VOTER_IDS=sorted(VOTER_IDS, key=lambda x: x['date_time'],reverse=True)
    flash('Data Pemilih  '+dpt_name+' Sukses di tambahkan', 'success')
    return redirect('/')
    


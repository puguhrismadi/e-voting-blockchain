import datetime
import json

import requests
from flask import render_template, redirect, request
from flask import flash
from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well. change presiden
CONNECTED_SERVICE_ADDRESS = "http://202.43.162.26:4444"
POLITICAL_PARTIES = ["Anies Baswedan","Ridwan Kamil","Ganjar Pranowo","Prabowo Subianto"]
VOTER_IDS=['Fadri','Alfi','Yudo','Haryo','Rizal','Tanzel','Gerdi','Farid','Fay','Kukuh','Puguh','Raxel','Rangga','Lisa','Arya']
vote_check=[]

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

@app.route('/test',methods=['GET'])
def tampil():
    return "Data "+VOTER_IDS[0]
    
@app.route('/submit', methods=['POST'])
def submit_textarea():
    #return "Klik"
    """
    Endpoint to create a new transaction via our application.
    """
    party = request.form["party"]
    voter_id = request.form["voter_id"]

    post_object = {
        'voter_id': voter_id,
        'party': party,
    }
    if voter_id not in VOTER_IDS:
        flash('Nama Pemilih invalid, please select Nama Pemilih from sample!', 'error')
        return redirect('/')
    if voter_id in vote_check:
        flash('Nama Pemilih ('+voter_id+') already vote, Vote can be done by unique vote ID only once!', 'error')
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
    VOTER_IDS.insert(index,dpt_name)
    return "Succed to add new Voter"


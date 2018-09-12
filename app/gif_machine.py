import os
import requests
import re
from flask import abort, Flask, jsonify, request


app = Flask(__name__)

SLACK_VERIFICATION_TOKEN = 'XDUhUEHB5lA7W1Bpet5MNls4'
SLACK_TEAM_ID = 'T025J29S7'
CHANNEL_ID = 'GC992JEGZ'
TESTING_CHANNEL_ID = 'DBMGMDGS1'

def is_request_valid(request):
    is_token_valid = request.form['token'] == SLACK_VERIFICATION_TOKEN
    is_team_id_valid = request.form['team_id'] == SLACK_TEAM_ID
    is_channel_id_valid = request.form['channel_id'] == CHANNEL_ID or request.form['channel_id'] == TESTING_CHANNEL_ID

    return is_token_valid and is_team_id_valid and is_channel_id_valid


def create_data(request):
    request_text = [text.strip() for text in request.form['text'].split("\"")]
    url = request_text[0]
    top = request_text[1]
    bot = request_text[3]

    return {
        'url' : url.strip(),
        'who' : request.form['user_name'],
        'meme_top' : top,
        'meme_bottom' : bot,
        'seekrit' : 'kGdW66<K75#/}n~fW?b~=EJ?oQDn',
    }

def success_message():
    return jsonify({
        'response_type' : 'in_channel',
        'text' : 'Success!',
        'attachments' : [
            {
                'pretext' : 'Take a look: <http://acquia-gifmachine.herokuapp.com>',
            }
        ]
    })
    return

def error_message():
    return jsonify({
        'response_type' : 'ephemeral',
        'text' : "Permission Denied!",
        'attachments' : [
            {
                'image_url' : 'https://vignette.wikia.nocookie.net/cuphead/images/9/9f/King_dice_stops_the_player.png/revision/latest?cb=20171010011628'
            }
        ]
    })


@app.route('/meme', methods=['POST'])
def post_gif():
    if not is_request_valid(request):
        return error_message()

    data = create_data(request)
    post_url = 'http://acquia-gifmachine.herokuapp.com/gif'
    response = requests.post(post_url, params=data)

    return success_message()

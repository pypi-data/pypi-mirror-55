import AIArena.games
from AIArena.AI import AI as AI
from AIArena.Ref import Ref as Ref

from AIArena.Human import Human_Connect4 as Human_Connect4

import pkgutil
import requests
import os
from memex_client.scientist import package
from memex_client.client import BrainiacClient

import json

name = "AIArena"

def runGame(Ais,game):
    gameName = game["name"]
    result = {
        "error":"None"
    }
    #Game setup
    try:
        ref = Ref()
        ref.createGame(gameName, Ais)
    except:
        result["error"] = "Game Creation"
        return result

    #Game run
    try:
        result["Winner"] = ref.runGame()
        if result["Winner"] == -1:
            result["error"] = "Game Run"
    except:
        result["error"] = "Game Run"
        return result

    #Game successfully finished
    result["moves"] = ref.moves
    return result

def runMove(AIs, data):
    try:
        AI = AIs[0]
        state = json.loads(data["gamestate"])
        move = AI.makeMove(state)

        results = {
            "error": "None"
        }

        if move == None:
            results['error'] = 'Bad move response'
        else:
            results['move'] = move

        return results
    except Exception as e:
        print("EXCEPTION:", e)
        return {'exception': e}


def upload(AI, aid):
    os.environ['BRAINIAC_CLIENT_USERNAME'] = "ai_olympics"
    os.environ['BRAINIAC_CLIENT_PASSWORD'] = "ai_Olympics_brainiac_#1"
    #brainiac = BrainiacClient(http=True)
    response = package(AI, aid, url="https://brainiac-backend.herokuapp.com")
    if response.status_code != 200:
        print("An error occurred when trying to upload:",response.status_code)
        return
    print("AI Packaged Successfully")
    payload = {
        "aid":aid,
        "game":AI.game
    }

    r = requests.get("https://us-central1-ai-olympics.cloudfunctions.net/newAiUpload",payload)
    #print(r.status_code)
    #print(r.headers)
    if r.status_code == 200:
        print(r.content.decode())
    else:
        print("A registration error occured:", r.status_code, r.content)
from flask import Flask, render_template, request, redirect, url_for
import requests

# VVV PUT YOUR API KEY HERE VVVV
Auth_Key_TBA = "2BwMbds992jtroDHCsZbGKVnJBC3Z9UvAxXivj7CnMpGCVzvxNPCEattPlvSyIG7"

app = Flask("__name__")

@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/team_page", methods=["POST", "GET"])
def team_page():
    try:
        if request.method == "POST":
            team_num = request.form.get("team_number")
        if request.method == "GET":
            team_num = request.args.get("team_num")
        team_dict = getTeamInfo(int(team_num))
        team_dict = getEvents(team_dict)
        team_dict = getMatches(team_dict)
        team_dict = getAverages(team_dict)
        return render_template("team_page.html", team_dict = team_dict)
    except:
        return render_template("team_error.html")


@app.route("/match", methods=["POST", "GET"])
def match():
    if request.method == "GET":
        match_id = request.args.get("match_id", "No ID")
        match_data = get_match_data(match_id)
        return render_template("match.html", match_data=match_data)
    
@app.route("/events", methods=["GET", "POST"])
def event():
    if request.method == "GET":
        event_id = request.args.get("event_id", "NONE")
        event_data = get_event_data(event_id)
        return render_template("event.html", event_data = event_data)

if __name__ == "__main__":
    app.run()

#FRC average scores app written by Matt Colbert
#This code heavily uses TheBlueAlliance's API. Documentation is here https://www.thebluealliance.com/apidocs
#You can see examples of how to pass arguments to get it to work at the bottom of the code
#Enjoy!

def getTeamInfo(teamnum):
    api_endpoint = ("https://www.thebluealliance.com/api/v3/team/frc" + str(teamnum))
    headers = {
        'X-TBA-Auth-Key' : Auth_Key_TBA
    }
    response = requests.get(
        api_endpoint,
        headers = headers
    ).json()
    
    team_dict = {}
    team_dict["TeamNum"] = response["team_number"]

    for key in ["school_name", "state_prov", "rookie_year", "nickname"]:
        team_dict[key] = response[key]
    return team_dict

def getEvents(team_dict):
    api_endpoint = ("https://www.thebluealliance.com/api/v3/team/frc" + str(team_dict["TeamNum"]) + "/events/2023")
    headers = {
        'X-TBA-Auth-Key' : Auth_Key_TBA
    }
    response = requests.get(
        api_endpoint,
        headers = headers
    ).json()

    team_dict["events"] = {}
    for event in range(len(response)):
        temp_dict = {}
        for key in ["start_date", "key", "name"]:
            temp_dict[key] = response[event][key]
        if "week" in response[event].keys():
            temp_dict["week"] = response[event]["week"]
        if "webcasts" in response[event].keys():
            temp_dict["webcasts"] = response[event]["webcasts"]
        temp_dict["matches"] = []
        team_dict["events"][temp_dict["key"]] = temp_dict

    return team_dict

def getMatches(team_dict):
    api_endpoint = ("https://www.thebluealliance.com/api/v3/team/frc" + str(team_dict["TeamNum"]) + "/matches/2023")

    headers = {
        'X-TBA-Auth-Key' : Auth_Key_TBA
    }
    response = requests.get(
        api_endpoint,
        headers = headers
    ).json()

    for match in response:
        team_dict["events"][match["event_key"]]["matches"].append(match)

    return team_dict

def getAverages(team_dict):
    opposites = {"red":"blue", "blue":"red"}
    information = {"scored":[], "allowed":[], "win-loss":[], "rp":[], "foul_points": [], "mobility": [], "endgame_charge":[], "auto_charge":[], "auto_gp":[], "teleop_gp":[], "link_pts":[], "auto_pts":[], "teleop_pts":[], "auto_bs":[], "endgame_bs":[], "matches":0}
    for event in team_dict["events"]:
        for match in team_dict["events"][event]["matches"]:
            alliance = "red" if "frc" + str(team_dict["TeamNum"]) in match["alliances"]["red"]["team_keys"] else "blue"
            pos = str(match["alliances"][alliance]["team_keys"].index("frc"+str(team_dict["TeamNum"]))+1)
            information["matches"] += 1
            information["scored"].append(match["alliances"][alliance]["score"])
            information["allowed"].append(match["alliances"][opposites[alliance]]["score"])
            information["win-loss"].append("win" if match["winning_alliance"] == alliance else "loss")
            if match["score_breakdown"] != None:
                information["rp"].append(match["score_breakdown"][alliance]["rp"])
                information["foul_points"].append(match["score_breakdown"][alliance]["foulPoints"])
                information["mobility"].append(match["score_breakdown"][alliance]["mobilityRobot" + pos])
                information["endgame_charge"].append(match["score_breakdown"][alliance]["endGameChargeStationRobot" + pos])
                information["auto_charge"].append(match["score_breakdown"][alliance]["autoChargeStationRobot" + pos])
                information["auto_gp"].append(match["score_breakdown"][alliance]["autoGamePiecePoints"])
                information["teleop_gp"].append(match["score_breakdown"][alliance]["teleopGamePiecePoints"])
                information["link_pts"].append(match["score_breakdown"][alliance]["linkPoints"])
                information["auto_pts"].append(match["score_breakdown"][alliance]["autoPoints"])
                information["teleop_pts"].append(match["score_breakdown"][alliance]["teleopPoints"])
                information["auto_bs"].append(match["score_breakdown"][alliance]["autoBridgeState"])
                information["endgame_bs"].append(match["score_breakdown"][alliance]["endGameBridgeState"])
    if information["matches"] == 0:
        for key in information.keys():
            information[key] = 0
    else:
        for key in ["scored", "allowed", "auto_pts", "teleop_pts", "auto_gp", "teleop_gp"]:
            information[key] = sum(information[key])/(len(information[key])*3)
        for key in ["rp", "foul_points", "link_pts"]:
            information[key] = sum(information[key])/(len(information[key]))
        for key in ["win-loss", "mobility", "auto_charge", "endgame_charge", "endgame_bs", "auto_bs"]:
            information[key] = (information[key].count("win") + information[key].count("Docked") + information[key].count("yes") + information[key].count("Level"))/len(information[key])
        for key in information.keys():
            information[key] = round(information[key], 3)
    team_dict["averages"] = information
    return team_dict

def get_match_data(match_id):
    api_endpoint = ("https://www.thebluealliance.com/api/v3/match/"+match_id)

    headers = {
        'X-TBA-Auth-Key' : Auth_Key_TBA
    }

    return requests.get(api_endpoint, headers = headers).json()

def get_event_data(event_id):
    api_endpoint = ("https://www.thebluealliance.com/api/v3/event/" + event_id + "/matches")

    headers = {
        'X-TBA-Auth-Key' : Auth_Key_TBA
    }
    response = requests.get(
        api_endpoint,
        headers = headers
    ).json()

    event_data = {"Name"}

    return event_data
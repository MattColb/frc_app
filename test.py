import requests

def get_match_data(match_id):
    Auth_Key_TBA = "2BwMbds992jtroDHCsZbGKVnJBC3Z9UvAxXivj7CnMpGCVzvxNPCEattPlvSyIG7"
    api_endpoint = ("https://www.thebluealliance.com/api/v3/match/"+match_id)

    headers = {
        'X-TBA-Auth-Key' : Auth_Key_TBA
    }

    return requests.get(api_endpoint, headers = headers).json()


def getTeamInfo(teamnum):
    Auth_Key_TBA = "2BwMbds992jtroDHCsZbGKVnJBC3Z9UvAxXivj7CnMpGCVzvxNPCEattPlvSyIG7"
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
    Auth_Key_TBA = "2BwMbds992jtroDHCsZbGKVnJBC3Z9UvAxXivj7CnMpGCVzvxNPCEattPlvSyIG7"
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
    Auth_Key_TBA = "2BwMbds992jtroDHCsZbGKVnJBC3Z9UvAxXivj7CnMpGCVzvxNPCEattPlvSyIG7"
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

def main(team_number):
    team_dict = getTeamInfo(team_number)
    team_dict = getEvents(team_dict)
    team_dict = getMatches(team_dict)
    return team_dict

def get_averages(team_dict):
    opposites = {"red":"blue", "blue":"red"}
    information = {"scored":[], "allowed":[], "win-loss":[], "RP":[], "foul_points": [], "auto_cargo_points":[], "taxi": [], "teleop_cargo": [], "teleop_cargo_points": [], "endgame":[]}
    for event in team_dict["events"]:
        for match in team_dict["events"][event]["matches"]:
            alliance = "red" if "frc" + str(team_dict["TeamNum"]) in match["alliances"]["red"]["team_keys"] else "blue"
            pos = str(match["alliances"][alliance]["team_keys"].index("frc"+str(team_dict["TeamNum"]))+1)
            print(pos)
            information["scored"].append(match["alliances"][alliance]["score"])
            information["allowed"].append(match["alliances"][opposites[alliance]]["score"])
            information["win-loss"].append("win" if match["winning_alliance"] == alliance else "loss")
            if match["score_breakdown"] != None:
                information["RP"].append(match["score_breakdown"][alliance]["rp"])
                information["foul_points"].append(match["score_breakdown"][alliance]["foulPoints"])
                information["auto_cargo_points"].append(match["score_breakdown"][alliance]["autoCargoPoints"])
                information["taxi"].append(match["score_breakdown"][alliance]["taxiRobot" + pos])
                information["teleop_cargo"].append(match["score_breakdown"][alliance]["teleopCargoTotal"])
                information["teleop_cargo_points"].append(match["score_breakdown"][alliance]["teleopCargoPoints"])
                information["endgame"].append(match["score_breakdown"][alliance]["endgameRobot"+pos])
    for key in ["scored", "allowed", "auto_cargo_points", "teleop_cargo", "teleop_cargo_points"]:
        information[key] = sum(information[key])/(len(information[key])*3)
    for key in ["RP", "foul_points"]:
        information[key] = sum(information[key])/(len(information[key]))
    for key in ["taxi", "win-loss"]:
        information[key] = (information[key].count("Yes") +information[key].count("win"))/len(information[key])
    endgame = {}
    for level in ["None", "Mid", "Low", "High", "Traversal"]:
        endgame[level] = information["endgame"].count(level)/len(information["endgame"])
    information["endgame"] = endgame
    team_dict["averages"] = information
    return team_dict

print(main(78))
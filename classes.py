import requests

Auth_Key_TBA = "2BwMbds992jtroDHCsZbGKVnJBC3Z9UvAxXivj7CnMpGCVzvxNPCEattPlvSyIG7"

class Team:
    def __init__(self, team_num):
        self.team_num = team_num
        self.getTeamInfo()


    def getTeamInfo(teamnum):
        api_endpoint = ("https://www.thebluealliance.com/api/v3/team/frc" + str(teamnum))
        headers = {
            'X-TBA-Auth-Key' : Auth_Key_TBA
        }
        response = requests.get(
            api_endpoint,
            headers = headers
        ).json()

        
        for key in ["school_name", "state_prov", "rookie_year", "nickname"]:
            locals()[key] = response[key]
        


class Event:
    def __init__(self, event_id):
        self.event_key = event_id


class Match:
    def __init__(self, match_id):
        self.match_id = match_id
        self.get_match_data()
        self.separate()
        self.get_event_name()

    def get_match_data(self):
        api_endpoint = ("https://www.thebluealliance.com/api/v3/match/"+ self.match_id)

        headers = {
            'X-TBA-Auth-Key' : Auth_Key_TBA
        }

        self.match_data = requests.get(api_endpoint, headers = headers).json()
    
    def separate(self):
        self.red_alliance = self.match_data["alliances"]["red"]["team_keys"]
        self.red_score = self.match_data["alliances"]["red"]["score"]
        self.blue_alliance = self.match_data["alliances"]["blue"]["team_keys"]
        self.blue_score = self.match_data["alliances"]["blue"]["score"]
        self.event_key = self.match_data["event_key"]
        self.comp_level = self.match_data["comp_level"]
        self.match_num = self.match_data["match_number"]
        if self.match_data["videos"] != []:
            self.video = "https://www.youtube.com/watch?v=" + self.match_data['videos'][0]['key']
        if self.match_data["score_breakdown"]:
            self.blue_breakdown = self.match_data["score_breakdown"]["blue"]
            self.red_breakdown = self.match_data["score_breakdown"]["red"]

    def get_event_name(self):
        api_endpoint = ("https://www.thebluealliance.com/api/v3/event/" + self.event_key + "/simple")
        headers = {
            'X-TBA-Auth-Key' : Auth_Key_TBA
        }
        response = requests.get(
            api_endpoint,
            headers = headers
        ).json()

        self.event_name = response["name"]
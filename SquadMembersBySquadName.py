import requests
import base64
import os

#Getting Bearer Access token 
#With Squad Name - retrieving all the squad member details
# Here collected only the member aaId as list. 

username = os.getenv('user')
password = os.getenv('password')

client_Key_secret = username+":"+password
client_key_secret_enc = base64.b64encode(client_Key_secret.encode()).decode()

headerAuth = {
	'Authorization' : 'Basic '+str(client_key_secret_enc)
}
data = {
	'grant_type' : 'client_credentials'
} 

response = requests.post('https://us-south.appid.cloud.ibm.com/oauth/v4/b6ec3b06-5c05-499d-a409-8761dff5a34d/token', headers = headerAuth, data = data ,verify = True)
bearer_access_token  = response.json()['access_token']

headerDetails = {
    'accept' : 'application/json',
    'Authorization' : 'Bearer '+bearer_access_token
}

class squad360API:

    #Retrieve Squad Members from Squad API - with squad name as input 
    #calling 2 squad Api's here 
    #1. calling 'https://squad360.mybluemix.net/api/simple/squads' to get the squad Id 
    #2, Calling 'https://squad360.mybluemix.net/api/simple/squads/{squadid}/members' to get the squad members from squad id
    def getSquadMembersBySquadName(self,squadName):
        #retrieving all squads and filtering with squad name filter
        squad_id = None
        #list to collect members aaId
        squad_member_ids = []
        allSquads_response  = requests.get('https://squad360.mybluemix.net/api/simple/squads', headers = headerDetails , verify = True )
        for squad in allSquads_response.json():
            if(squad['name'] != None and squadName in squad['name']):
                squad_id = squad['id']
                break
            # elif(squad['alias2'] != None and squadName in squad['alias2']):
            #     squad_id = squad['id']
            #     break
            # elif(squad['alias1'] != None and squadName in squad['alias1']):
            #     squad_id = squad['id']
            #     break
        if squad_id != None:
            squad_member_response = requests.get('https://squad360.mybluemix.net/api/simple/squads/' +str(squad_id)+'/members', headers = headerDetails , verify = True)
            squad_members = squad_member_response.json()['members']
            #iterating squad members from response
            for member in squad_members:
                squad_member_ids.append(member['aaId'])
        return squad_member_ids

api = squad360API()

#passing squad name to the method call
squad_name = 'A/V Digital Signage' #######################################<----Change Squad name here

#printing
#
squad_member_ids = api.getSquadMembersBySquadName(squad_name)
print ("Squad Members for Squad name :"+str(squad_name)+" --> "+str(squad_member_ids)+"\n")

import requests
import base64
import os

#Getting Bearer Access token 
#Set a variable for app_short_name with Value 'AppSec'
#Get all the squads and filtering with app_short_name to get the Squad id 
#With Squad id - retrieving all the squad member details
# Here collected only the member aaId as list. 

# username = "115b27f7-ebad-4690-b27f-3fee76aaa412"
# password = "MDVhNWRlYzctNmYyNy00Y2NiLWE3MjQtMmJmODg4Yzg3ZjM1"

#os.environ['client_id'] = "115b27f7-ebad-4690-b27f-3fee76aaa412"
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

    #Retrieve Squad ID from Squad API - with squad name 
    #With response filtering squad ID for provided squad name
    #https://squad360.mybluemix.net/api/simple/squads  
    def getSquadMembersBySquadName(self,squadName):
        #retrieving all squads and filtering with squad name filter
        squad_id = None
        #list to collect members aaId
        squad_member_ids = []
        allSquads_response  = requests.get('https://squad360.mybluemix.net/api/simple/squads', headers = headerDetails , verify = True )
        for squad in allSquads_response.json():
            if(squad['alias1'] != None and squadName in squad['alias1']):
                squad_id = squad['id']
                break
            elif(squad['alias2'] != None and squadName in squad['alias2']):
                squad_id = squad['id']
                break
            elif(squad['name'] != None and squadName in squad['name']):
                squad_id = squad['id']
                break
        print ("Squad Id -> "+str(squad_id))
        if squad_id != None:
            squad_member_response = requests.get('https://squad360.mybluemix.net/api/simple/squads/' +str(squad_id)+'/members', headers = headerDetails , verify = True)
            squad_members = squad_member_response.json()['members']
            #iterating squad members from response
            for member in squad_members:
                squad_member_ids.append(member['aaId'])
        return squad_member_ids

api = squad360API()

#passing squad name to the method call
squad_name = '29C' #<----Change Squad name here

squad_member_ids = api.getSquadMembersBySquadName(squad_name)
print ("Result for Squad Name : "+squad_name+"\n")


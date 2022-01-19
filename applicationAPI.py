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


# #retrieving all the application details (which has Short name ,archer_id(srcRecId)) - Shortname Dropdown values in UI
# application_details  = requests.get('https://squad360.mybluemix.net/api/simple/applications', headers = headerDetails , verify = True )
# app_response = application_details.json() 

# #Dynamically collecting Short Names of all applications to short_names list
# short_names = []
# for app in application_details:
#     short_names.append(app['shortName'])
#to pass short_names[0]


class ApplicationAPI:

    #Retrieve Application details with Short name as input parameter
    #https://squad360.mybluemix.net/api/simple/applications?shortName=AppSec
    def getApplicationsByShortName(self,app_short_name):
        app_details_by_shortName =   requests.get('https://squad360.mybluemix.net/api/simple/applications?shortName=' +app_short_name, headers = headerDetails , verify = True )
        pci_Detail = app_details_by_shortName.json()[0]['pci']
        archer_id = app_details_by_shortName.json()[0]['srcRecId']
        return  app_details_by_shortName.json()

    
    #Check if the Application's PCI value is True or Not with App Short Name as Input parameter
    #  (If True returning 'PCI' otherwise returning 'NON-PCI')
    #https://squad360.mybluemix.net/api/simple/applications?shortName=AppSec
    def checkAppPciVal(self,app_short_name):
        app_details_by_shortName =   requests.get('https://squad360.mybluemix.net/api/simple/applications?shortName=' +app_short_name, headers = headerDetails , verify = True )
        app_details =   app_details_by_shortName.json()
        #here checking PCI value of Application response
        if app_details[0]['pci'] == True:
               return 'PCI'# returning 'PCI' as value equals True
        else:
            return 'NON-PCI'# returning 'NON-PCI' as value other than True 


api = ApplicationAPI()

#Retrieving PCI value , Archer_id value of Application - Application API (v1/simple/applications)
application_details = api.getApplicationsByShortName('WebTPA')
print ("ShortName -> :"+str(application_details[0]['shortName']) + "  pci -> :"+str(application_details[0]['pci']) + "  archer_id -> : "+ str(application_details[0]['srcRecId']) )
print("-----------------------------------") 

#App with PCI value as True
app_pci_desc = api.checkAppPciVal('ChemSDS')
#printing the Application PCI value returned from checkAppPciVal() method call
print (str(app_pci_desc))

print ("-------------------------------------------------------")
#App with PCI value other than True
app_pci_desc = api.checkAppPciVal('1View')
print (str(app_pci_desc))

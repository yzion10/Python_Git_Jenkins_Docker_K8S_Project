import requests
from db_connector import DBConnector
import clean_environment
import os

# return (true/false) if the value is in the args.
def IsIn(value, *args):
    return value in args

def getUrl():
    return 'http://127.0.0.1:5000/users/1'

def getUserData():
    userData = {'user_name': 'yosi1'}
    return userData

Err200 = 200
Err400 = 400
Err500 = 500

log_file_path = 'app/logs/flasklog.txt'

# *************************************************************************************

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# remove the log file if exist
if os.path.exists(log_file_path):
    os.remove(log_file_path)

def writeToLog(text):
    with open(log_file_path, 'a') as f:
        f.write(text + '\n')

if __name__ == "__main__":
    print('\n*********** Running tests on the Dockerized app... ***********\n')
    writeToLog('\n*********** Running tests on the Dockerized app... ***********\n')

# 1
# POST - test a post of a new user data with the REST API method
def postRequest(api_url, userData):
    res = requests.post(api_url, json=userData)
    userName = ''
    if res.status_code == Err200:
        userName = res.json()['user_added']
        msg = f'user {userName} created successfully \n\n' \
              f'this is the json output:\n{res.json()}'
        print(msg)
        writeToLog(msg)
    elif IsIn(res.status_code, Err500, Err400):
        reason = res.json()['reason']
        msg = f'POST failed with reason: {reason} \n\n' \
              f'this is the json output:\n{res.json()}'
        print(msg)
        writeToLog(msg)
    else:
        print(f'POST failed with status code {res.status_code}')
        writeToLog(f'POST failed with status code {res.status_code}')
    return userName

if __name__ == "__main__":
    print('\n*********** postRequest ***********\n')
    writeToLog('\n*********** postRequest ***********\n')
    postRequest(getUrl(), getUserData())

# *************************************************************************************

# 2
# GET - test if the GET request returns the expected user data and status code
def getRequest(api_url, apiUserName):
    getRes = requests.get(api_url)
    userName = ''
    msg = ''
    if getRes.status_code == Err200:
        userName = getRes.json()['user_name']
        if(userName == apiUserName):
            msg = f'result user name: {userName} \napiUserName: {apiUserName} \n\n' \
                  f'this is the json output:\n{getRes.json()}'
            print(msg)
            writeToLog(msg)
        else:
            msg = f'result user name: {userName} \napiUserName: {apiUserName} \n' \
                  f'result user name dosent match the apiUserName'
            print(msg)
            writeToLog(msg)
    elif getRes.status_code == Err500:
        reason = getRes.json()['reason']
        msg = f'GET failed with reason: {reason} \n\n' \
              f'this is the json output:\n{getRes.json()}'
        print(msg)
        writeToLog(msg)
    else:
         print(f'GET failed with status code {getRes.status_code}')
         writeToLog(f'GET failed with status code {getRes.status_code}')
    return userName

if __name__ == "__main__":
    print('\n*********** getRequest ***********\n')
    writeToLog('\n*********** getRequest ***********\n')
    getRequest(getUrl(), 'yosi1')

# *************************************************************************************

# 3
# Check if posted data was stored inside DB
def checkPostUserStoredInDB(userID, apiUserName):
    host = 'devopsdb.cu3hwstmvfmq.eu-north-1.rds.amazonaws.com'
    port = 3306
    user = 'admin'
    password = 'oren123456'
    database = 'test'

    # initialize the DBConnector class
    db = DBConnector(host, port, user, password, database)

    dbUserName = db.getUserName(userID)
    msg = f'dbUserName: {dbUserName} \n' \
          f'apiUserName: {apiUserName} \n\n'
    if dbUserName is not None:
        if (dbUserName == apiUserName):
            print(msg + 'names are equal')
            writeToLog(msg + 'names are equal')
        else:
            print(msg + 'names are NOT equal')
            writeToLog(msg + 'names are NOT equal')
    else:
        print(f'no such ID: {userID}')
        writeToLog(f'no such ID: {userID}')

if __name__ == "__main__":
    print('\n*********** checkPostUserStoredInDB ***********\n')
    writeToLog('\n*********** checkPostUserStoredInDB ***********\n')
    checkPostUserStoredInDB('1', 'yosi1')

# *************************************************************************************

# 4
# PUT - test a post of an existing user to update his name in the DB
def putRequest(api_url, userData):
    putRes = requests.put(api_url, json=userData)
    userName = ''
    if putRes.status_code == Err200:
        userName = putRes.json()['user_updated']
        msg = f'user {userName} updated successfully \n\n' \
              f'this is the json output:\n{putRes.json()}'
        print(msg)
        writeToLog(msg)
    elif IsIn(putRes.status_code, Err500, Err400):
        reason = putRes.json()['reason']
        msg = f'PUT failed with reason: {reason} \n\n' \
              f'this is the json output:\n{putRes.json()}'
        print(msg)
        writeToLog(msg)
    else:
        print(f'PUT failed with status code {putRes.status_code}')
        writeToLog(f'PUT failed with status code {putRes.status_code}')
    return userName

if __name__ == "__main__":
    print('\n*********** putRequest ***********\n')
    writeToLog('\n*********** putRequest ***********\n')
    putRequest(getUrl(), getUserData())

# *************************************************************************************

# 5
# DELETE - test if the DELETE request delete the user from the DB by the given ID
def deleteRequest(api_url):
    deleteRes = requests.delete(api_url)
    userID = 0
    msg = ''
    if deleteRes.status_code == Err200:
        userID = deleteRes.json()['user_deleted']
        msg = f'user ID: {userID} deleted successfully \n\n' \
              f'this is the json output:\n{deleteRes.json()}'
        print(msg)
        writeToLog(msg)
    elif deleteRes.status_code == Err500:
        reason = deleteRes.json()['reason']
        msg = f'DELETE failed with reason: {reason} \n\n' \
              f'this is the json output:\n{deleteRes.json()}'
        print(msg)
        writeToLog(msg)
    else:
         print(f'DELETE failed with status code {deleteRes.status_code}')
         writeToLog(f'DELETE failed with status code {deleteRes.status_code}')
    return userID

if __name__ == "__main__":
    print('\n*********** deleteRequest ***********\n')
    writeToLog('\n*********** deleteRequest ***********\n')
    deleteRequest(getUrl())

if __name__ == "__main__":
    print('\n*********** stopRestServer ***********\n')
    writeToLog('\n*********** stopRestServer ***********\n')
    res = clean_environment.stopRestServer()
    print(res)
    writeToLog(res)
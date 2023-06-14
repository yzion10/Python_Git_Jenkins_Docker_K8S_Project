import requests

def stopRestServer():
    msg = ''
    try:
        requests.get('http://127.0.0.1:5000/stop_server')
        msg = 'Rest server stopped\n'
    except requests.exceptions.RequestException as ex:
        msg = 'rest server didnt stop because: \n' + str(ex) + '\n'
    return msg

if __name__ == "__main__":
    stopRestServer()
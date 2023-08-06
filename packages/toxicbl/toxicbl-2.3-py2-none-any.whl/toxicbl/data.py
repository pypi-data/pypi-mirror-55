import requests
def update(options : object):
    try:
        requests.post('http://www.toxic-bot-list.ml/api/postStatus', json={'token': options['token'],'serversCount': options['serversCount'],'usersCount': options['usersCount']})
        return {
            'Success': 'Post was pushed to server'
        }
    except:
        return {
            'Error' : 'Refer to docs'
        }

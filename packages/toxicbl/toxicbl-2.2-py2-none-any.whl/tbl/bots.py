import requests
def get_info(self,id=None):
    if(id is None) :
        return 'ID parameter is required'
    self.result = requests.get('https://toxic-api.glitch.me/api/bots/{}'.format(id)).text
    try:
        return self.result
    except:
        return 'Seems like you messed up your id . Refer to the docs'
    """
    @return : Returns the info about the given ID bot
    @rtype : object
    @param :
        id = The bot's unique ID
    """
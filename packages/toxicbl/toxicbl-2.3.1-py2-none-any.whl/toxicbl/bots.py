import requests
def get_info(id=None):
 try:
    # Needed declarations
    url = "https://www.toxicapi.ml/bots?id={}".format(id)
    data_returned = requests.get(url).text
    return data_returned
 except:
    return {
        'Error' : 'Server did not respond'
    }
    """
    @return : Returns the info about the given ID bot
    @rtype : object
    @param :
        id = The bot's unique ID
    @ptype : string
    """

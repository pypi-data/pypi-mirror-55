import requests
def get_info(id=None):
 if(len(id) == 18 and not id.isdigit()):
  try:
    # Needed declarations
    url = "https://www.toxicapi.ml/users?id={}".format(id)
    data_returned = requests.get(url).text
    return data_returned
  except:
    return {
        'Error' : 'Server did not respond'
    }
 else:
    return {
        'Error' : 'Check your ID\'s type and length'
    }
    """
    @return : Returns the info about the given ID bot
    @rtype : object
    @param :
        id = The bot's unique ID
    @ptype : string
    """
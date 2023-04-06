import requests#
import json#
from langdetect import detect#
import Levenshtein#

def is_english(sentence):

    """
    Determines if the given sentence is written in English.

    Args:
        sentence (str): The input sentence.

    Returns:
        bool: True if the input sentence is in English, False otherwise.
    """

    try:
        return detect(sentence) == 'en'
    except:
        return False

def umls_search(word_to_search, api_key = '1d344409-a2d8-41a5-89ac-729cc3763851'):

    """
    Searches the Unified Medical Language System (UMLS) for the given word and returns the concept unique identifier (CUI),
    name, and definition of the most relevant result.

    Args:
        word_to_search (str): The word to search for in the UMLS.
        api_key (str): The UMLS API key required for authentication.

    Returns:
        list or None: A list containing the CUI, name, and definition of the most relevant result if found, otherwise None.

    Raises:
        None.

    Example:
        >>> umls_search('diabetes', 'your_api_key_here')
        ['C0011849', 'Diabetes Mellitus', 'A metabolic disorder characterized by abnormally high blood sugar levels.']
    """

    # Define the base URL and headers for the UMLS API
    base_url = 'https://uts-ws.nlm.nih.gov/rest'

    # Search for the given word using the UMLS API
    search_url = f'{base_url}/search/current?string={word_to_search}&apiKey={api_key}'
    response = requests.get(search_url)


    if response.status_code != 200:# HTTP status code 200 means success
      print('Error:', response.status_code)
      return None

    search_results = json.loads(response.content)['result']["results"]



    # If no results are found, return None
    if len(search_results) == 0: 
      return None

    #print(search_results)

    # Check if the first result has a definition
    cui = search_results[0]['ui']
    definition_url = f'{base_url}/content/current/CUI/{cui}/definitions?language=ENG&apiKey={api_key}'
    #print(definition_url)
    response = requests.get(definition_url)
    if response.status_code != 200:# HTTP status code 200 means success
      #print('Error:', response.status_code)
      pass
    else:
      definitions = json.loads(response.content)['result']
      name = search_results[0]['name']

      print("########################",definitions)

      if len(definitions) > 0:
        for item in definitions:
          # print("########################",item['value'])
          # print("************************",is_english(item['value']))
          if is_english(item['value']):
            print(f"Find {name}")
            return [cui,name,item['value']]
            

    
    # If the first result has no vilid definition, find the most similar result using Levenshtein distance
    definition_dict = {}
    for result in search_results:
        cui = result['ui']
        definition_url = f'{base_url}/content/current/CUI/{cui}/definitions?language=ENG&apiKey={api_key}'
        response = requests.get(definition_url)
        #print(definition_url)
        if response.status_code != 200:# HTTP status code 200 means success
          #print('Error:', response.status_code)
          continue
        #print(response)
        definitions = json.loads(response.content)['result']
        if len(definitions) > 0:
          for item in definitions:
            if is_english(item['value']):
              #print(result['name'])
              definition_dict[result['name']] = [cui,item['value']]
              #print(definition_dict)

    #print(definition_dict)

    if len(definition_dict) > 0:
        most_similar = min(definition_dict, key=lambda x: Levenshtein.distance(word_to_search, x))
        print(f"Find {most_similar}")
        return [definition_dict[most_similar][0],most_similar,definition_dict[most_similar][1]]

    # If no results have definitions, return None
    print(f"Did not find {word_to_search}")
    return None

import openai#

def generalise_topic(list_of_keywords, openai_api_key="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"):
  """
    This function takes in a list of keywords and an OpenAI API key as input and returns a concise phrase under 20 words that generalizes the theme of the given keywords. A short phrase of the field of study is also attached in parenthesis.

    Args:
    list_of_keywords (list): A list of keywords to be generalized
    openai_api_key (str): The API key for OpenAI's API

    Returns:
    str: A concise phrase under 20 words that generalizes the theme of the given keywords.

    Raises:
    Exception: If the response from OpenAI's API is invalid or incomplete.
  """
  openai.api_key = openai_api_key

  words_for_prompt = ""
  for word in list_of_keywords:
    words_for_prompt += word+","

  prompt = f"Generalise theme from keywords ({words_for_prompt[:-1]}) into one line consice phrase under 13 words. Attach at end a short phrase of the field of study in parenthesis."
  #print(prompt)
  responose = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "user", "content": "'"+prompt+"'"},
      ]
      )
  
  #print(responose)

  result = responose["choices"][0]["message"]["content"]
  print(result)
  return result.replace('\n', '')




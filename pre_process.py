import os#
from stop_words import get_stop_words#
from nltk.corpus import stopwords#
from nltk.tokenize import word_tokenize#
from nltk.tokenize import sent_tokenize#
from nltk.text import TextCollection#
import string#
import re#
import shutil#
import itertools


def load_files(set_name):
  """
    Loads a set of text files from the specified directory.

    Args:
        set_name (str): The name of the directory containing the text files.

    Returns:
        List[str]: A list of the filenames of the text files in the specified directory.
  """
  all_files = os.listdir(set_name+"/")
  txt_files = list(filter(lambda x: x[-4:] == '.txt', all_files))
  #print(txt_files)
  return txt_files




def filter_a_list_of_words(a_list_of_words):
  """
    Given a list of strings, this function filters out non-words and returns a list of lowercase words.

    Args:
        a_list_of_words (list): A list of strings (words or non-words).

    Returns:
        list: A list of lowercase words extracted from the input list.

  """
  filtered = []
  for a_single_word in a_list_of_words.split():
    if is_a_word(a_single_word):
      filtered.append(a_single_word.lower())
  return filtered


def is_a_word(a_single_word):

  """
    Check if the given string is a valid word.

    Args:
        a_single_word (str): A string that can contain alphabets, numbers, and acceptable symbols (- and _).

    Returns:
        bool: Returns True if the given string is a valid word, otherwise returns False.

  """

	# List of acceptable symbols in a word
  acceptable_sympols = ['-','_']

  # Assume the word is valid
  is_word = True

  # Check if the given word is empty
  if len(a_single_word) == 0:
    is_word = False
    return is_word

	#check each char in the given word
  for each_char in a_single_word:
    # If the character is not a letter or a number
    if not (each_char.isalpha() or each_char.isnumeric()) :
      # If the character is not an acceptable symbol
      if not each_char in acceptable_sympols:
        is_word = False
        return is_word
        
  return is_word

#Extending stopword set from stopwords-json (https://github.com/6/stopwords-json)
extending_stopwords = ["a","a's","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along",
                       "already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone",
                       "anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away",
                       "awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between",
                       "beyond","both","brief","but","by","c","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes",
                       "concerning","consequently","consider","considering","contain","containing","contains","corresponding","could",
                       "couldn't","course","currently","d","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","e",
                       "each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex",
                       "exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former",
                       "formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't",
                       "happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself",
                       "hi","him","himself","his","hither","hopefully","how","howbeit","however","i","i'd","i'll","i'm","i've","ie","if","ignored",
                       "immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","j",
                       "just","k","keep","keeps","kept","know","known","knows","l","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look",
                       "looking","looks","ltd","m","mainly",
                       "many","may","maybe","me","mean","meanwhile","merely","might","more","moreover",
                       "most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody",
                       "non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or",
                       "other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible",
                       "presumably","probably","provides","q","que","quite","qv","r","rather",
                       "rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing",
                       "seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody",
                       "somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","t's","take",
                       "taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby",
                       "therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've",
                       "think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying",
                       "twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via",
                       "viz","vs","w","want","wants","was","wasn't","way","we",
                       "we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon",
                       "wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","wouldn't","x","y","yes",
                       "yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","z","zero"]


extending_stopwords2 = ["the"]
extended_stopwords = set(stopwords.words('english')).union(set(extending_stopwords)).union(set(string.punctuation))

def load_documents_into_a_list_of_text_string(set_name):
  """
    Given a set name, this function loads all the text files from that set
    and returns a list of text strings, where each string contains the contents
    of a single file. The text strings have newlines and symbols included.

    Args:
    - set_name (str): the name of the set containing the text files

    Returns:
    - final_text (list): a list of text strings, where each string contains the
      contents of a single file in the set with newlines and symbols included
  """

	#load files
  txt_files = load_files(set_name)

	# Create a list of text strings from the files, with newlines and symbols included
  texts=[]
  for each in txt_files:
    with open( set_name+"/"+each, 'r') as file:
      data = file.read().replace('\n', '')
      texts.append(data)
    file.close()

  final_text = texts
  
  # Uncomment the following lines if you want to filter out numeric characters
    # from the final text strings
    # for i in range(len(final_text)):
    #     final_text[i] = filter_out_numeric(final_text[i])

  # Write the final text strings to a file called 'output.txt'
  with open('output.txt', 'w') as file:
    for string in final_text:
        file.write(string + '\n')

  return final_text


def filter_out_stopwords_punctuation(raw_list_of_texts):
  """
    Tokenizes the input list of texts and removes stopwords and punctuation from each text.

    Args:
    - raw_list_of_texts: A list of raw texts to be tokenized and filtered.

    Returns:
    - A list of lists of tokenized words with stopwords and punctuation removed.

    Example Usage:
    raw_texts = ["This is a sample sentence.", "Another sentence."]
    filtered_texts = filter_out_stopwords_punctuation(raw_texts)
    # filtered_texts will be [['sample', 'sentence'], ['Another', 'sentence']]
    """

  #Stop words from NLTK
  stop_words = set(stopwords.words('english'))

  #Extending stopword set from stopwords-json (https://github.com/6/stopwords-json)
  stop_words= stop_words.union(set(extending_stopwords))

  #Extending stopword set from string.punctuation
  stop_words= stop_words.union(set(string.punctuation))

  filtered_list_of_list_of_words = []
  for list_of_words in raw_list_of_texts:
    word_tokens = filter_a_list_of_words(list_of_words)
    temp_word_tokens = [w for w in word_tokens if not w in stop_words]
    filtered_list_of_list_of_words.append(temp_word_tokens)
  return filtered_list_of_list_of_words

 
def standarise_a_list_of_word_tokens(list_of_string):
  """
    This function takes a list of string tokens and standardizes them by removing stop words,
    checking if they are a valid word, converting to lowercase, and removing digits.
    
    Args:
    list_of_string (list): A list of string tokens
    
    Returns:
    list: A list of standardized string tokens
  """
  result = []
  for j in list_of_string:
    i = j.lower()
    if (i not in extended_stopwords) and is_a_word(i) and (not any(c.isdigit() for c in i)):

      if j.isupper() and len(j)>1: # Remain uppercase for abbreviation
        i=j

      else:
        i = j.lower()

      #remove wrong spelling: "baseSocial","forwardSocial"
      pattern = r'^(?:[a-z]|[A-Z])[a-z]*[A-Z]+[a-z]+'
      if not re.match(pattern, j):
      # if not (j[0].islower() and any(c.isupper() for c in j[1:])):
        result.append(i)

  return result

def tokenise_texts(texts):
  """
    Tokenizes a list of texts into sentences and words using the nltk library.

    Args:
    texts (list): A list of strings representing the texts to be tokenized.

    Returns:
    tuple: A tuple containing two items:
           - A list of lists representing the tokenized sentences.
           - A TextCollection object representing the corpus of the tokenized texts.
  """

  # Initialize an empty list to store the tokenized sentences.
  tokenized_to_sentences=[]

  # Iterate over each text in the input list.
  for each_text in texts:
    # Tokenize each text into sentences and append to the list.
    tokenized_to_sentences.append(sent_tokenize(each_text))

  # Flatten the list of lists into a single list of sentences.
  tokenized_to_sentences = [item for sublist1 in tokenized_to_sentences for item in sublist1]

  # Tokenize each sentence into words.
  tokenized_to_words=[word_tokenize(sent) for sent in tokenized_to_sentences]

  # Initialize an empty list to store the standardized sentences.
  sentences=[]

  # Iterate over each list of word tokens in the tokenized sentences.
  for i in tokenized_to_words:
    # Standardize the list of word tokens and append to the list of standardized sentences.
    standarised = standarise_a_list_of_word_tokens(i)
    if len(i) != 0:
      sentences.append(standarised)
  # Create a TextCollection object from the standardized sentences.
  corpus=TextCollection(sentences)

  # Return a tuple containing the standardized sentences and the TextCollection object.
  return sentences,corpus

def tokenise_texts_one_doc(doc):
  """
  This function takes in a document string and tokenizes it into a list of sentences. Each sentence is then tokenized into a list of words, and each word is standardized using the standarise_a_list_of_word_tokens function. The resulting list of standardized words is returned.

  Args:
  doc (str): A string representing the document to be tokenized.

  Returns:
  A list of standardized word tokens extracted from the input document.

  """
  
  tokenized_to_sentences=sent_tokenize(doc)
  #print("*",tokenized_to_sentences)

  tokenized_to_sentences = [item for item in tokenized_to_sentences]

  tokenized_to_words = [word_tokenize(sent) for sent in tokenized_to_sentences]

  #print("*",tokenized_to_words)

  sentences=[]

  for i in tokenized_to_words:
    standarised = standarise_a_list_of_word_tokens(i)
    if len(i) != 0:
      sentences.append(standarised)
  
  sentences = [item for sublist in sentences for item in sublist]
  
  #print(sentences)


  return sentences

def extract_keywords_TF_IDF(sentences,corpus,number=20):
  result = []

  for i in set(list(itertools.chain(*sentences))):
    tf_idf=corpus.tf_idf(i,corpus)
    result.append([i,tf_idf])
    #print(i,len(result))
  
  sorted_result = sorted(result, key=lambda x: x[1],reverse=True)

  return sorted_result[:number]

def create_subrepositories(topic_list,lda_model, corpus, word_dict,collection_name,best_topic_index):
    """
    Create sub-repositories for each topic in the directory.

    """

    current_directory = os.getcwd()

    #print(current_directory)

    names = load_files(collection_name)

    if os.path.exists(str(current_directory+str(f"/{collection_name}_topics"))):
      shutil.rmtree(str(current_directory+str(f"/{collection_name}_topics")))


    # Create a sub-directory for each topic
    for i in best_topic_index:
        topic_dir = str(current_directory+str(f"/{collection_name}_topics/"+str(topic_list[i])+""))
        if not os.path.exists(topic_dir):
            os.makedirs(topic_dir)
        else:
            shutil.rmtree(topic_dir)
            os.makedirs(topic_dir)

    # Loop over all documents and copy them to the appropriate sub-directory
    for i in range(len(corpus)):
        doc_topic_dist = lda_model.get_document_topics(corpus[i], minimum_probability=0.0)
        topic_index, topic_prob = max(doc_topic_dist, key=lambda x: x[1])
        topic_dir = str(current_directory+str(f"/{collection_name}_topics/"+str(topic_list[topic_index])+""))
        doc_filename = str(names[i])
        doc_path = os.path.join(topic_dir, doc_filename)
        #print(doc_path)
        #print(topic_dir)
        shutil.copy(str(current_directory+"/"+collection_name+"/"+doc_filename), topic_dir)


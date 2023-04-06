import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pre_process

from stop_words import get_stop_words#
from nltk.stem.porter import PorterStemmer#
from nltk.tokenize import RegexpTokenizer#
from gensim import corpora
import gensim#]
#import pyLDAvis#
import re#

from multiprocessing import Process, freeze_support




def LDA_visualisation(collection,num_of_topics=3):
  """
    This function performs LDA (Latent Dirichlet Allocation) visualisation for a given collection of text documents.
    
    Args:
    collection (List[str]): A list of text documents.
    num_of_topics (int): The number of topics to extract. Default value is 100.
    
    Returns:
    Tuple: A tuple containing the LDA model and the prepared visualisation data for the collection of documents.
  """

  # Initialise tokenizer
  tokenizer = RegexpTokenizer(r'\w+')

  # Create English stop words list
  en_stop = get_stop_words('en')

  # Create p_stemmer of class PorterStemmer
  p_stemmer = PorterStemmer()
    
  # Load documents into a list of text strings
  doc_set1 = pre_process.load_documents_into_a_list_of_text_string(collection)
  #doc_set2 = load_documents_into_a_list_of_text_string("Hospital care")
  doc_set = doc_set1 

  # Tokenize documents and remove stop words
  texts = [pre_process.tokenise_texts_one_doc(i) for i in doc_set]

  # Create id <-> term dictionary
  id2word = corpora.Dictionary(texts)
    
  # Convert tokenized documents into a document-term matrix
  corpus = [id2word.doc2bow(text) for text in texts]

  # Generate LDA model
  lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_of_topics, id2word = id2word, passes=20)

  # Get the topic distribution for each document
  doc_lda = lda_model[corpus]

  # Prepare LDA visualisation data
  #LDAvis_prepared = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)

  # pyLDAvis.display(LDAvis_prepared)

  #return LDAvis_prepared

  topics = []
  for idx, topic in lda_model.show_topics(-1, 30):
      topic_to_add = re.findall(r'"(.*?)"', topic)
      topics.append(topic_to_add)
  
  # pyLDAvis.display(LDAvis_prepared)

  return [topics,lda_model,corpus,id2word]


def LDA_visualisation_optimised_number(collection):
  """
    This function performs LDA (Latent Dirichlet Allocation) visualisation for a given collection of text documents,
    and determines the optimal number of topics to extract by calculating coherence scores for different numbers
    of topics.
    
    Args:
    collection (List[str]): A list of text documents.
    
    Returns:
    Tuple: A tuple containing the LDA model and the prepared visualisation data for the collection of documents.
  """
  # Initialise tokenizer
  tokenizer = RegexpTokenizer(r'\w+')

  # Create English stop words list
  en_stop = get_stop_words('en')

  # Create p_stemmer of class PorterStemmer
  p_stemmer = PorterStemmer()
  
  # Load documents into a list of text strings
  doc_set1 = pre_process.load_documents_into_a_list_of_text_string(collection)
  #doc_set2 = load_documents_into_a_list_of_text_string("Hospital care")
  doc_set = doc_set1 

  # Tokenize documents and remove stop words
  texts = [pre_process.tokenise_texts_one_doc(i) for i in doc_set]

  # Create id <-> term dictionary
  id2word = corpora.Dictionary(texts)
    
  # Convert tokenized documents into a document-term matrix
  corpus = [id2word.doc2bow(text) for text in texts]

  # Find the optimal number of topics
  coherence_values = []
  model_list = []
  for num_topics in range(2, 11):
      model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics, random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)
      model_list.append(model)
      coherencemodel = gensim.models.CoherenceModel(model=model, texts=texts, dictionary=id2word, coherence='c_v')
      coherence_score = coherencemodel.get_coherence()
      coherence_values.append(coherence_score)

  best_num_topics = coherence_values.index(max(coherence_values)) + 1

  # Generate LDA model using optimal number of topics
  lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=best_num_topics, random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)
  
  # Get the topic distribution for each document
  doc_lda = lda_model[corpus]

  # Prepare LDA visualisation data
  #LDAvis_prepared = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
  
  # pyLDAvis.display(LDAvis_prepared)

  return LDAvis_prepared

def LDA_topics_keywords_optimised_number(collection):
  
  # Initialise tokenizer
  tokenizer = RegexpTokenizer(r'\w+')

  # Create English stop words list
  en_stop = get_stop_words('en')

  # Create p_stemmer of class PorterStemmer
  p_stemmer = PorterStemmer()
  
  # Load documents into a list of text strings
  doc_set1 = pre_process.load_documents_into_a_list_of_text_string(collection)
  #doc_set2 = load_documents_into_a_list_of_text_string("Hospital care")
  doc_set = doc_set1 

  # Tokenize documents and remove stop words
  texts = [pre_process.tokenise_texts_one_doc(i) for i in doc_set]

  # Create id <-> term dictionary
  id2word = corpora.Dictionary(texts)
    
  # Convert tokenized documents into a document-term matrix
  corpus = [id2word.doc2bow(text) for text in texts]

  num_topics = 10
  threshold = 0.002

  # Generate LDA model using optimal number of topics
  lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics, random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)
  
  # Get the topic distribution for each document
  doc_lda = lda_model[corpus]

  # Prepare LDA visualisation data
  # LDAvis_prepared = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)

  topics = []
  best_topic_index = []

  # Loop over each topic and check if it is significantly small
  for i in range(10):
      # Get the probability distribution for this topic
      topic = lda_model.get_topic_terms(i)
      topics.append([i[0] for i in lda_model.show_topic(i)])

      # Compute the average probability of the words in the vocabulary
      avg_prob = sum([p for w, p in topic]) / len(topic)

      # Check if the average probability is below the threshold
      if avg_prob > threshold:
          best_topic_index.append(i)
  
  
  # pyLDAvis.display(LDAvis_prepared)

  return [topics,lda_model,corpus,id2word,best_topic_index]

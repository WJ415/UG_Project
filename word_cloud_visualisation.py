import pre_process
import extraction_context
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import shutil
import os
import json

def visualise_one_set(upper_collection,collection, collection_name, specific_keywords=None):


  texts = pre_process.load_documents_into_a_list_of_text_string(collection)

  sentences,corpus = pre_process.tokenise_texts(texts)

  if specific_keywords==None:
    keywords_with_TF_IDF = pre_process.extract_keywords_TF_IDF(sentences,corpus)
    keywords = [sublist[0] for sublist in keywords_with_TF_IDF]
  else:
    keywords = specific_keywords

  keyword_with_five_context={}

  context = extraction_context.extract_context(sentences,keywords)
  # print(len(context))

  fig, axs = plt.subplots(nrows=len(keywords)*1, ncols=3,figsize=(22, 1*6*len(keywords)), constrained_layout=False)

  for i in range(len(keywords)):

    header_range = range(15)
    if 15 not in range(len(context[keywords[i]][0])):
      header_range = range(len(context[keywords[i]][0]))

    trailer_range = range(15)
    if 15 not in range(len(context[keywords[i]][1])):
      trailer_range = range(len(context[keywords[i]][1]))

    head_freq = [(context[keywords[i]][0][j][0],context[keywords[i]][0][j][1]) for j in header_range]
    tail_freq = [(context[keywords[i]][1][j][0],context[keywords[i]][1][j][1]) for j in trailer_range]
    #print("*",head_freq)

    five_headers= [i[0] for i in head_freq[:5]]
    five_trailers= [i[0] for i in tail_freq[:5]]

    keyword_with_five_context[keywords[i]] = [five_headers,five_trailers]

    head_data = dict(head_freq)
    tail_data = dict(tail_freq)

    # print("#",keywords[i])
    #print("*",head_data)

    def color_func_head(word, font_size, position, orientation, random_state=None, **kwargs):
      # print("#",word)
      # print("*",head_freq)
      if word == head_freq[0][0]:
          return "#DD3B11"
      elif word == head_freq[1][0]:
          return "#BC4729"
      elif word == head_freq[2][0]:
          return "#BF563B"
      elif word == head_freq[3][0]:
          return "#994C38"
      elif word == head_freq[4][0]:
          return "#75483C"
      else:
          return "#2A2A2A"

    def color_func_tail(word, font_size, position, orientation, random_state=None, **kwargs):

      if word == tail_freq[0][0]:
          return "#0A91D4"
      elif word == tail_freq[1][0]:
          return "#1D86BA"
      elif word == tail_freq[2][0]:
          return "#2E769A"
      elif word == tail_freq[3][0]:
          return "#3C667B"
      elif word == tail_freq[4][0]:
          return "#3D5D6E"
      else:
          return "#2F2F2F"

    if len(head_data) != 0:
      wc = WordCloud(color_func=color_func_head,background_color="white",max_words=100,relative_scaling=0.69,max_font_size=110,min_font_size=12,prefer_horizontal=1,repeat=False).generate_from_frequencies(head_data)

      axs[i,0].imshow(wc,interpolation="bilinear")
    axs[i,0].set_title('Header word', fontsize=15)
    axs[i,0].axis("off")

    axs[i,1].text(0.5, 0.5,keywords[i], size=35, ha='center', va='center', )
    axs[i,1].set_title(collection_name, fontsize=15)
    axs[i,1].axis("off")

    if len(tail_data) != 0:
      wc = WordCloud(color_func=color_func_tail,background_color="white",relative_scaling=0.69,max_font_size=110,min_font_size=12,prefer_horizontal=1,repeat=False).generate_from_frequencies(tail_data)

      axs[i,2].imshow(wc,interpolation="bilinear")
    axs[i,2].set_title('Trailer word', fontsize=15)
    axs[i,2].axis("off")

  if not os.path.exists(str(f"./Word_Cloud_Figures/{upper_collection}")):
      os.makedirs(str(f"./Word_Cloud_Figures/{upper_collection}"))
  # Save the dictionary to a file using the json module
  with open(f"./Word_Cloud_Figures/{upper_collection}/{collection_name}.json", 'w') as f:
      json.dump(keyword_with_five_context, f)

  plt.tight_layout()
  plt.savefig(f"./Word_Cloud_Figures/{upper_collection}/{collection_name}.png", format='png', dpi=200)

def visualise_two_set(collection1, collection2,joint_keywords):

  print("***** 0 *****")

  collection_name = collection1+" "+"&"+" "+collection2

  texts1 = pre_process.load_documents_into_a_list_of_text_string(collection1)
  texts2 = pre_process.load_documents_into_a_list_of_text_string(collection2)

  sentences1,corpus1 = pre_process.tokenise_texts(texts1)
  sentences2,corpus2 = pre_process.tokenise_texts(texts2)

  print("***** 0.5 *****")

  # keywords_with_TF_IDF1 = pre_process.extract_keywords_TF_IDF(sentences1,corpus1)
  # keywords1 = set([sublist[0] for sublist in keywords_with_TF_IDF1])

  # keywords_with_TF_IDF2 = pre_process.extract_keywords_TF_IDF(sentences2,corpus2)
  # keywords2 = set([sublist[0] for sublist in keywords_with_TF_IDF2])

  # keywords = list(keywords1.intersection(keywords2))

  keywords = joint_keywords

  keyword_with_five_context1={}
  keyword_with_five_context2={}

  print("***** 1 *****")

  context1 = extraction_context.extract_context(sentences1,keywords)
  context2 = extraction_context.extract_context(sentences2,keywords)

  # print(len(context))

  print("***** 2 *****")

  fig, axs = plt.subplots(nrows=len(keywords)*2, ncols=3,figsize=(22, 1*6*len(keywords)), constrained_layout=False)

  for i in range(len(keywords)):
    print("***** -- 3 -- *****")

    header_range1 = range(15)
    if 15 not in range(len(context1[keywords[i]][0])):
      header_range1 = range(len(context1[keywords[i]][0]))

    trailer_range1 = range(15)
    if 15 not in range(len(context1[keywords[i]][1])):
      trailer_range1 = range(len(context1[keywords[i]][1]))

    head_freq1 = [(context1[keywords[i]][0][j][0],context1[keywords[i]][0][j][1]) for j in header_range1]
    tail_freq1 = [(context1[keywords[i]][1][j][0],context1[keywords[i]][1][j][1]) for j in trailer_range1]
    #print("*",head_freq)

    five_headers1= [i[0] for i in head_freq1[:5]]
    five_trailers1= [i[0] for i in tail_freq1[:5]]

    keyword_with_five_context1[keywords[i]] = [five_headers1,five_trailers1]

    head_data1 = dict(head_freq1)
    tail_data1 = dict(tail_freq1)

    # print("#",keywords[i])
    #print("*",head_data)

    def color_func_head1(word, font_size, position, orientation, random_state=None, **kwargs):
      # print("#",word)
      # print("*",head_freq)
      if word == head_freq1[0][0]:
          return "#DD3B11"
      elif word == head_freq1[1][0]:
          return "#BC4729"
      elif word == head_freq1[2][0]:
          return "#BF563B"
      elif word == head_freq1[3][0]:
          return "#994C38"
      elif word == head_freq1[4][0]:
          return "#75483C"
      else:
          return "#2A2A2A"

    def color_func_tail1(word, font_size, position, orientation, random_state=None, **kwargs):

      if word == tail_freq1[0][0]:
          return "#0A91D4"
      elif word == tail_freq1[1][0]:
          return "#1D86BA"
      elif word == tail_freq1[2][0]:
          return "#2E769A"
      elif word == tail_freq1[3][0]:
          return "#3C667B"
      elif word == tail_freq1[4][0]:
          return "#3D5D6E"
      else:
          return "#2F2F2F"

    header_range2 = range(15)
    if 15 not in range(len(context2[keywords[i]][0])):
      header_range2 = range(len(context2[keywords[i]][0]))

    trailer_range2 = range(15)
    if 15 not in range(len(context2[keywords[i]][1])):
      trailer_range2 = range(len(context2[keywords[i]][1]))

    head_freq2 = [(context2[keywords[i]][0][j][0],context2[keywords[i]][0][j][1]) for j in header_range2]
    tail_freq2 = [(context2[keywords[i]][1][j][0],context2[keywords[i]][1][j][1]) for j in trailer_range2]
    #print("*",head_freq)

    five_headers2= [i[0] for i in head_freq2[:5]]
    five_trailers2= [i[0] for i in tail_freq2[:5]]

    keyword_with_five_context2[keywords[i]] = [five_headers2,five_trailers2]

    head_data2 = dict(head_freq2)
    tail_data2 = dict(tail_freq2)

    # print("#",keywords[i])
    #print("*",head_data)

    def color_func_head2(word, font_size, position, orientation, random_state=None, **kwargs):
      # print("#",word)
      # print("*",head_freq)
      if word == head_freq2[0][0]:
          return "#DD3B11"
      elif word == head_freq2[1][0]:
          return "#BC4729"
      elif word == head_freq2[2][0]:
          return "#BF563B"
      elif word == head_freq2[3][0]:
          return "#994C38"
      elif word == head_freq2[4][0]:
          return "#75483C"
      else:
          return "#2A2A2A"

    def color_func_tail2(word, font_size, position, orientation, random_state=None, **kwargs):

      if word == tail_freq2[0][0]:
          return "#0A91D4"
      elif word == tail_freq2[1][0]:
          return "#1D86BA"
      elif word == tail_freq2[2][0]:
          return "#2E769A"
      elif word == tail_freq2[3][0]:
          return "#3C667B"
      elif word == tail_freq2[4][0]:
          return "#3D5D6E"
      else:
          return "#2F2F2F"


    if len(head_data1) != 0:
      wc = WordCloud(color_func=color_func_head1,background_color="white",max_words=100,relative_scaling=0.69,max_font_size=110,min_font_size=12,prefer_horizontal=1,repeat=False).generate_from_frequencies(head_data1)

      axs[i*2,0].imshow(wc,interpolation="bilinear")
    axs[i*2,0].set_title('Header word', fontsize=15)
    axs[i*2,0].axis("off")

    axs[i*2,1].text(0.5, 0.5,keywords[i], size=35, ha='center', va='center')
    axs[i*2,1].set_title(collection1, fontsize=15)
    axs[i*2,1].axis("off")

    if len(tail_data1) != 0:
      wc = WordCloud(color_func=color_func_tail1,background_color="white",relative_scaling=0.69,max_font_size=110,min_font_size=12,prefer_horizontal=1,repeat=False).generate_from_frequencies(tail_data1)

      axs[i*2,2].imshow(wc,interpolation="bilinear")
    axs[i*2,2].set_title('Trailer word', fontsize=15)
    axs[i*2,2].axis("off")




    if len(head_data2) != 0:
      wc = WordCloud(color_func=color_func_head2,background_color="white",max_words=100,relative_scaling=0.69,max_font_size=110,min_font_size=12,prefer_horizontal=1,repeat=False).generate_from_frequencies(head_data2)

      axs[i*2+1,0].imshow(wc,interpolation="bilinear")
    axs[i*2+1,0].set_title('Header word', fontsize=15)
    axs[i*2+1,0].axis("off")

    axs[i*2+1,1].text(0.5, 0.5,keywords[i], size=35, ha='center', va='center')
    axs[i*2+1,1].set_title(collection2, fontsize=15)
    axs[i*2+1,1].axis("off")

    if len(tail_data2) != 0:
      wc = WordCloud(color_func=color_func_tail2,background_color="white",relative_scaling=0.69,max_font_size=110,min_font_size=12,prefer_horizontal=1,repeat=False).generate_from_frequencies(tail_data2)

      axs[i*2+1,2].imshow(wc,interpolation="bilinear")
    axs[i*2+1,2].set_title('Trailer word', fontsize=15)
    axs[i*2+1,2].axis("off")






  if not os.path.exists(str(f"./Word_Cloud_Figures/joint")):
      os.makedirs(str(f"./Word_Cloud_Figures/joint"))
  # Save the dictionary to a file using the json module
  with open(f"./Word_Cloud_Figures/joint/{collection1}.json", 'w') as f:
      json.dump(keyword_with_five_context1, f)
  with open(f"./Word_Cloud_Figures/joint/{collection2}.json", 'w') as f:
      json.dump(keyword_with_five_context2, f)
  plt.tight_layout()
  plt.savefig(f"./Word_Cloud_Figures/joint/{collection_name}.png", format='png', dpi=200)

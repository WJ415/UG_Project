#input: 
# 1.list of tokenised sentences
# 2.list keywords
#output: a dict map keywords to its header and trailer words with counts
def extract_context(sentences,keywords):

  result = {}

  for i in keywords:
    result[i] = extract_context_single_keyword(sentences,i)
  
  return result


#input: 
#output: a dict map keywords to its header and trailer words with counts
def extract_context_single_keyword(sentences,keyword):

  header = []
  trailer =[]

  for i in sentences:
    if keyword in i:
      header,trailer = get_header_and_trailer_word(i,keyword,header,trailer)

  result_header = []
  result_trailer =[]

  for i in set(header):
    if i != keyword:
      count = header.count(i)
      result_header.append([i,count])

  for i in set(trailer):
    if i != keyword:
      count = trailer.count(i)
      result_trailer.append([i,count])

  result_header = sorted(result_header, key=lambda x: x[1],reverse=True)
  result_trailer = sorted(result_trailer, key=lambda x: x[1],reverse=True)

  return [result_header,result_trailer]


def get_header_and_trailer_word(sentence,keyword,header,trailer):
  temp_header = header
  temp_trailer = trailer
  index = range(len(sentence))
  for i in index:
    if sentence[i] == keyword:
      if (i-1) in index:
        temp_header.append(sentence[i-1])
      if (i+1) in index:
        temp_trailer.append(sentence[i+1])
  return temp_header,temp_trailer



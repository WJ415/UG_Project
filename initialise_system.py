import streamlit as st
import UMLS_search
import pre_process
import LDA_clustering

from multiprocessing import Process, freeze_support

import multiprocessing
import generalise
import json

import word_cloud_visualisation

import time

import itertools

collection_1 = "Social care"
collection_2 = "Hospital care"


def LDA_keywords_result(collection):

	# Create an empty slot for the output
	#output_slot = st.empty()

	# Write some text to the output
	#output_slot.write(f'Analysing collections: "{topic_1}", "{topic_2}"')

	#LDA analysis
	LDA_result = LDA_clustering.LDA_topics_keywords_optimised_number(collection)

	#List of list of keywords of sub-topics
	generalised_topics_list = []

	#Generalise extracted topics
	generalised_topics = {}


	for i in range(len(LDA_result[0])):
		if i in LDA_result[4]:
			print("***************")
			print(LDA_result[0][i])
			generalise_result = generalise.generalise_topic(LDA_result[0][i]).replace("'", "").replace('"', '')
			generalised_topics[generalise_result] = LDA_result[0][i]
			generalised_topics_list.append(generalise_result.replace("'", "").replace('"', ''))
			time.sleep(2)
		else:
			generalised_topics_list.append("")

	print("***************")
	print(generalised_topics_list)
	pre_process.create_subrepositories(generalised_topics_list,LDA_result[1],LDA_result[2],LDA_result[3],collection,LDA_result[4])


	# Clear the output
	#output_slot.empty()

	return generalised_topics


generalised_1 = LDA_keywords_result(collection_1)
generalised_2 = LDA_keywords_result(collection_2)

keywords1 = list(generalised_1.values())
keywords1 = set(itertools.chain(*keywords1))

keywords2 = list(generalised_2.values())
keywords2 = set(itertools.chain(*keywords2))

joint_keywords = list(keywords1.intersection(keywords2))
word_cloud_visualisation.visualise_two_set(collection_1,collection_2,joint_keywords)


# Save the dictionary to a file using the json module
with open('./cache/generalised_1.json', 'w') as f:
    json.dump(generalised_1, f)
with open('./cache/generalised_2.json', 'w') as f:
    json.dump(generalised_2, f)

for topic in generalised_1:
	topic_path=str(f"./{collection_1}_topics/"+str(topic.replace("'", "").replace('"', '')))
	word_cloud_visualisation.visualise_one_set(collection_1,topic_path,topic,specific_keywords = generalised_1[topic])

for topic in generalised_2:
	topic_path=str(f"./{collection_2}_topics/"+str(topic.replace("'", "").replace('"', '')))
	word_cloud_visualisation.visualise_one_set(collection_2,topic_path,topic,specific_keywords = generalised_2[topic])





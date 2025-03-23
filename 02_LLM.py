import pandas as pd
from langchain_openai import ChatOpenAI
import os
import getpass
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pydantic import BaseModel, Field

# Set environment variables
os.environ['OPENAI_API_KEY'] = getpass.getpass()

# Choose the model to use for the LLM analysis
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = '''You are an intelligence agent helping policymakers analyze the international and political relations between China and Taiwan. You are tasked to analyze a Chinese newspaper article regarding Taiwan. Answer the following questions based on the title and body of a newspaper article:
{questions} 
Here is the title of newspaper article: {title} 
Here is the body of newspaper article: {body}
'''

# Types of questions
questions_scale = {}
questions_binary = {}
questions_qualitative = {}


# Binary questions
questions_binary["Mention_Taiwan_China_Relation"] = '''Does the article mention anything related to Taiwan and China relation? If so, give 1. If not, give 0.'''
questions_binary["Mention_Military"] = '''Does the article mention anything related to Taiwanese, Chinese, or/and US military, including but not limited to  military drill, national defense, national security, military invasion. If so, give 1. If not, give 0.'''
questions_binary["Mnetion_Unification"] = '''Does the article mention China's desire to unify Taiwan or the importance of unification of Taiwan? If so, give 1. If not, give 0.'''
questions_binary["Mention_One_China"] = '''Does the article mention there is only one China, Taiwan is part of China, or Taiwanese government cannot represent Taiwan? If so, give 1. If not, give 0.'''
questions_binary["Mention_Peace"] = '''Does the article mention it is important for China to maintain peace across the Taiwan Strait? If so, give 1. If not, give 0.'''
questions_binary["Mention_West_Taiwan_relationship"] = '''Does the article mention anything related to any Western country (including Japan), regarding its relationship with Taiwan, the role of that country in the Taiwan Strait, that country's and Taiwan's politicians' official or unofficial meetings, or the attitude of that country towards the relationship between China and Taiwan? If so, give 1. If not, give 0.'''
questions_binary["Mention_Taiwan_independence"] = '''Does the article mention Taiwan's implicit or explicit intention to claim independence from China? If so, give 1. If not, give 0.'''
questions_binary["Mention_Taiwan_negative_action"] = '''Does the article mention Taiwan's policy or actions will damage and hurt Chinese or Taiwanese welfare or lead to a negative consequence? If so, give 1. If not, give 0.'''

# Quantitative questions
questions_scale["Relevance"] = '''Is the topic of this article closely related to Taiwan? Or does the article just briefly mention Taiwan. Give a real number between 0 and 1.00 to indicate the relevance of the article to Taiwan. 1.00 indicates the most relevant, and 0 indicates the least relevant.'''
questions_scale["Relation"] = '''What is the relation between China and Taiwan at the current moment? Give a real number between 0 and 1.00 to indicate the current relation between China and Taiwan. 1.00 indicates the best relation, and -1.00 indicates the worst relation. Give O for a neutral relation. Give an O if the article does not mention anything related to the relation between China and Taiwan.'''
questions_scale["Tension"] = '''Is there any tension or conflict between China and Taiwan at the current moment? Give a real number between 0 and 1.00 to indicate the current tension or conflict between China and Taiwan. 1.00 indicates the highest tension, and 0 indicates the lowest tension. Give an O if the article does not mention anything related to tension or conflict between China and Taiwan.'''
questions_scale["Attitude_towards_Taiwan"] = '''Does the Chinese government have a positive or negative attitude towards Taiwan? Give a real number between -1.00 and 1.00 to indicate China's attitude. 1.00 indicates the most friendly attitude, and -1.00 indicates the most unfriendly attitude. Give O for a neutral attitude. If the article is not directly related to the Chinese government's attitude towards Taiwan, also give 0.'''
questions_scale["Attitude_towards_US"] = '''Does the Chinese government have a positive or negative attitude towards the United States? Give a real number between from -1.00 and 1.00 to indicate China's attitude. 1.00 indicates the most friendly attitude, and -1.00 indicates the most unfriendly attitude. Give O for a neutral attitude. If the article is not directly related to the Chinese government's attitude towards the US, also give 0.'''
questions_scale["Collaboration"] = '''Is there any collaboration or cooperation between China and Taiwan at the current moment, including but not limited to economic or trade agreements, cross-strait exchanges, official communications, culture and social exchanges? Give a real number between 0 and 1.00 to indicate the current collaboration or cooperation between China and Taiwan. 1.00 indicates the highest collaboration, and 0 indicates the lowest collaboration. Give an O if the article does not mention anything related to collaboration or cooperation between China and Taiwan.'''
questions_scale["Unification"] = '''Does this article indicate any possibility of unification between China and Taiwan at the current moment? Give a real number between 0 and 1.00 to indicate the possibility of unification between China and Taiwan at the current moment. 1.00 indicates the highest possibility, and 0 indicates the lowest possibility. Give an O if the article does not mention anything related to unification between China and Taiwan.'''
questions_scale["Military_activity"] = '''Is either Taiwan, China engaged in active or passive military actions against each other at the current moment, including but not limited to military exercise, missiles deployment, weapons purchases or testing? Give a real number between 0 and 1.00 to indicate the current military actions between China and Taiwan. 1.00 indicates the most prominent military actions, and 0 indicates the least prominent military actions. Give an O if the article does not mention anything related to military actions between China and Taiwan.'''
questions_scale["US_engagement"] = '''Is the United States engaged in the China and Taiwan relations in any way at the current moment? Please consider any US's military actions, US's political involvement, US's economic sanctions, US's diplomatic actions, US's official or unofficial meetings with Chinese or Taiwanese officials, or US's public statements. Give a real number between 0 and 1.00 to indicate the US's involvement in the China and Taiwan relations at the current moment. 1.00 indicates the most involvement, and 0 indicates the least involvement. Give an O if the article does not mention anything related to the US's involvement in the China and Taiwan relations.'''

# Qualitative questions
questions_qualitative["Topic"] = '''What is the main topic of the article? politics, military, economy, culture, society, or others?'''
questions_qualitative["Word_Count"] = '''How many words are there in the article?'''
questions_qualitative["Taiwan_Count"] = '''How many times does the article mention Taiwan?'''
questions_qualitative["US_count"] = '''How many times does the article mention the US?'''

# Combining all questions for prompt and for the output class
question_prompt = ""
n = 1
for questions_type in [questions_binary, questions_scale, questions_qualitative]:
    for topic, content in questions_type.items():
        topic = topic.replace("_", " ")
        question_prompt = question_prompt + f"{n}. {topic}: {content}\n"
        n += 1        
print(question_prompt)


# Create attributes the structured output class
output_class_attr = ""

for topic in questions_binary.keys():
    output_class_attr = output_class_attr + f"{topic}: int = Field(description = '{topic}')\n"
    
for topic in questions_scale.keys():
    output_class_attr = output_class_attr + f"{topic}: float = Field(description = '{topic}')\n"
    
for topic in questions_qualitative.keys():
    output_class_attr = output_class_attr + f"{topic}: str = Field(description = '{topic}')\n"
    
print(output_class_attr)


class PCI_output_class(BaseModel):
    exec(output_class_attr)

# Load data
events = ['text_96', 'text_24']
dfs = dict()
for x in events:
    dfs[x] = pd.read_csv(f"../Data/Processed/{x}.csv")
    dfs[x] = dfs[x].sort_values('year_month')


# Running LLM
for event in events:
    df_sample = dfs[event]

    try:
        df_results = pd.read_csv(f"../Output/LLM_{event}.csv")
        exist_id = list(df_results['id'].unique())
    except FileNotFoundError:
        exist_id = []
        df_results = pd.DataFrame(columns=output.__dict__.keys())

    for _, i in enumerate(df_sample['id']):
        if _ % 10 == 1: 
            print(_, "\\" , len(df_sample))
            df_results.to_csv(f"../Output/LLM_{event}.csv", index=False)
        if i in exist_id:
            continue
        
        title = df_sample[df_sample['id'] == i].title
        body = df_sample[df_sample['id'] == i].body

        structured_llm = model.with_structured_output(PCI_output_class)
        output = structured_llm.invoke(prompt.format(questions=question_prompt, title=title, body=body))

        df_ = pd.DataFrame(output.__dict__, index=[i])
        df_['id'] = i
        df_results = pd.concat([df_results, df_], axis=0)

    df_results.to_csv("../Output/LLM_{event}.csv", index=False)

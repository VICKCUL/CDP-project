import numpy as np
import random
import torch
import matplotlib.pyplot as plt
import pandas as pd
import os
import re
from collections import Counter




data_dir="/mnt/c/Users/hangh/Dropbox/Research/nlpprojectoncdpdata/data/"
supplychain_dir=data_dir+"SupplyChain/"
supplychain_filename_list= [f for f in os.listdir(supplychain_dir) if os.path.isfile(os.path.join(supplychain_dir, f))]
print(supplychain_filename_list)

investor_dir=data_dir+"Investor/"
investor_filename_list= [f for f in os.listdir(investor_dir) if os.path.isfile(os.path.join(investor_dir, f))]
print(investor_filename_list)
company_list=['Tessy Plastics', 'AptarGroup', 'Porton', 'DANFOSS', 'ABM INDUSTRIES INC', 'Bloomberg', 'DOMINGUES PAES EMPRESA DE SEGURANCA']
year_list=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
possible_name_keywords=['Company Name','Organisation','account_name','Organization']
table_summary=pd.DataFrame()


data = [["" for _ in year_list] for _ in company_list]

if os.path.exists('supplychain.csv'):
    df_gen = pd.read_csv('supplychain.csv', index_col=0)
else:
    df_gen = pd.DataFrame(data, index=company_list, columns=year_list)

    for idx,filename in enumerate(supplychain_filename_list):
        print(filename,idx)
        year=year_list[idx]
        
        df_dicts = pd.read_excel(supplychain_dir + filename, sheet_name=None) 
        df_names=list(df_dicts.keys())
        print(df_names)
    
        for df_name in df_names:
            # print(df_name)
        
            df=df_dicts[df_name]
            if df_name=="Emissions 11":
                print(df.columns)
        
            for company_idx,company in enumerate(company_list):
                # print(company)
                for possible_name_keyword in possible_name_keywords:
                    if possible_name_keyword in df.columns:
                        # print( df[df[possible_name_keyword] == company].values.tolist())
                        res = df[df[possible_name_keyword] == company].values.tolist()
                        if res != []:
                            res=res[0]
                
                            
                        for row in res:
                        
                            
                            if type(row) == str:
                                words = row.split()
                                if len(words) < 3 and row != company:
                                    continue
                                else:
                                    # print(company_idx, year-year_list[0])
                                    # print(row,df_gen.iloc[company_idx, year-year_list[0]])
                                    df_gen.iloc[company_idx, year-year_list[0]] += row
                                    # print(df.loc[company_idx, year-year[0]])
    
                    else:
                        continue
                    

    df_gen.to_csv('supplychain.csv')

print(df_gen.shape)

df_most_common = pd.DataFrame(np.nan, index=df_gen.index, columns=df_gen.columns)

stop_words = {"the", "of", "a", "is", "and", "in", "on", "at", "to", "over", "under", "with","our","we","from", "for", "by", "as", "an", "or", "are", "be", "it", "its", "that", "this", "these", "those", "there", "here", "where", "when", "who", "what", "how", "why", "which", "whom", "whose", "whether", "while", "whilst", "because", "since", "so", "if", "then", "else", "when", "before", "after", "during", "while", "until", "once", "twice", "thrice", "first", "second", "third", "last", "next", "previous", "same", "different", "other", "another", "each", "every", "all", "some", "any", "no", "none", "neither", "either", "both", "such", "so", "too", "enough", "as", "very", "more", "most", "less", "least", "few", "fewer", "fewest", "many", "much", "more", "most", "little", "less", "least", "lot", "lots", "great", "greater", "greatest", "good", "better", "best", "bad", "worse", "worst", "far", "farther", "farthest", "near", "nearer", "nearest", "behind", "front", "frontier", "back", "backer", "backest", "inside", "outside", "between", "among", "through", "throughout", "along", "alongside", "against", "with", "without", "within", "without", "above", "below", "beneath", "underneath", "under", "over", "across", "around", "about", "before", "after", "since", "during", "while", "until", "once", "twice", "thrice", "first", "second", "third", "last", "next", "previous", "same", "different", "other", "another", "each", "every", "all", "some", "any", "no", "none", "neither", "either", "both", "such", "so","not","have","jan",   "feb",   "mar",   "apr",   "may",   "jun",   "jul",   "aug",   "sep",   "oct",   "nov",   "dec",   "january",   "february",   "march",   "april",   "may",   "june",   "july",   "august",   "september",   "october",   "november",   "december",   "monday",   "tuesday",   "wednesday",   "thursday",   "friday",   "saturday",   "sunday",   "mon",   "tue",   "wed",   "thu",   "fri",   "sat",   "sun"}

# append all the word in the coppany name to stop words
for company in company_list:
    words=company.split()
    for word in words:
        stop_words.add(word.lower())


stop_words.add("segurancadomingues")
stop_words.add("applicablequestion")

for company_idx,company in enumerate(company_list):
    print(company)
    for year in year_list:
        print(year)
        text = df_gen.iloc[company_idx,year-year_list[0]]
        cleaned_text = re.sub(r'[^\w\s]', ' ', text).lower()

        # Split the string into words
        words = cleaned_text.split()
        words = [word for word in cleaned_text.split() if word not in stop_words]

        # Count the frequency of each word
        word_freq = Counter(words)

        most_common = word_freq.most_common(3)
        # change the word count to frequency
        most_common = [(word,count/len(words)) for word,count in most_common     ]
        # print(most_common)
        # print(df_most_common.iloc[company_idx,year-year_list[0]] )
        # de
        df_most_common.iloc[company_idx,year-year_list[0]] = [most_common]

df_most_common.to_csv('supplychain_most_common.csv')
# Analyzing Japanese: Analysis
# Author: Isabell Siem
# Matrikelnummer: 108018211002

import nagisa
from sudachipy import tokenizer
from sudachipy import dictionary
from fugashi import Tagger
import json
import os
import time
import pickle

def tokenize_nagisa(path):
    """A function to employ Nagisa in morphological analysis.
    Input: path to untagged KWDLC file
    Output: result dict (sid:[(word,tag),(word,tag),...]), elapsed time"""

    # initialize dict for results
    kwdlc_org = {}

    # record start time
    start_time = time.time()
        
    subfolders = [os.path.join(path, folder) for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    
    for subfolder in subfolders:
        # To make sure all files are processed
        files_to_process = [
            filename for filename in os.listdir(subfolder)
            if filename.endswith('.knp') or filename.endswith('.org')
        ]
        #print("NAGISA FTP",subfolder," Total Files:", len(subfolders) , " Total Files in subfodler:", len(files_to_process),datetime.now())
        
        # Iterate through files in each subfolder
        for filename in os.listdir(subfolder):
            file_path = os.path.join(subfolder, filename)
            try:
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.readlines()

                    # get token and tag
                    for line in content:
                        if line.startswith("#"):
                            sid = line.split()[1]
                            kwdlc_org[sid] = []
                        else: 
                            words = nagisa.tagging(line)
                            for token, tag in zip(words.words, words.postags):
                                pair = (token, tag)
                                kwdlc_org[sid].append(pair)

            # To catch any exceptions
            except Exception as exception:
                print(f"Error processing file {file_path}: {exception}")
    
    # calculate elapsed time
    elapsed_time = time.time()-start_time

    return kwdlc_org, elapsed_time

def tokenize_sudachipy(path):
    """Function to employ Sudachi in morphological analysis. 
    
    Sudachi provides multi granular tokenization:
    mode C output example: ['国家公務員']
    mode B output example: ['国家', '公務員']
    mode A output example: ['国家', '公務', '員']
    
    Input: path to untagged KWDLC file
    Output: result dicts for every mode, elapsed time
    """
    tokenizer_obj = dictionary.Dictionary().create()

    # result dicts
    kwdlc_org_A = {}
    kwdlc_org_B = {}
    kwdlc_org_C = {}

    start_time = time.time()

    # Get all folders in the root directory
    subfolders = [os.path.join(path, folder) for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    
    for subfolder in subfolders:
        # To make sure all files are processed
        files_to_process = [
            filename for filename in os.listdir(subfolder)
            if filename.endswith('.knp') or filename.endswith('.org')
        ]
        #print("SUDACHI FTP",subfolder," Total Files:", len(subfolders) , " Total Files in subfodler:", len(files_to_process), datetime.now())

        # Iterate through files in each subfolder
        for filename in os.listdir(subfolder):
            file_path = os.path.join(subfolder, filename)
            try:
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.readlines()

                    # Set tokenization modes
                    mode_C = tokenizer.Tokenizer.SplitMode.C
                    mode_B = tokenizer.Tokenizer.SplitMode.B
                    mode_A = tokenizer.Tokenizer.SplitMode.A
                    
                    for line in content:
                        line = line.strip()
                        if line.startswith("#"):
                            sid = line.split()[1]
                            kwdlc_org_A[sid] = []
                            kwdlc_org_B[sid] = []
                            kwdlc_org_C[sid] = []

                        else:
                            # tokenize line depending on set mode
                            m_C = tokenizer_obj.tokenize(line, mode_C)
                            m_B = tokenizer_obj.tokenize(line, mode_B)
                            m_A = tokenizer_obj.tokenize(line, mode_A)

                            # create list of morpheme information [word, dict, reading, (tag1, tag2, ...)]
                            for token in m_C:
                                kwdlc_org_C[sid].append([token.surface(), token.dictionary_form(), token.reading_form(), token.part_of_speech()])
                            
                            for token in m_B:
                                kwdlc_org_B[sid].append([token.surface(), token.dictionary_form(), token.reading_form(), token.part_of_speech()])
                            
                            for token in m_A:
                                kwdlc_org_A[sid].append([token.surface(), token.dictionary_form(), token.reading_form(), token.part_of_speech()])
            
            # To catch any exceptions
            except Exception as exception:
                print(f"File: {file_path}, Exception: {exception}")

    # calculate elapsed time
    elapsed_time = time.time()-start_time

    return kwdlc_org_C, kwdlc_org_B, kwdlc_org_A , elapsed_time

def tokenize_fugashi(path):
    """A function to employ Fugashi in morphological analysis.
    Input: path to file
    Output: result dict, elapsed_time"""
    tagger = Tagger()
    
    kwdlc_org = {}
    start_time = time.time()

    # Get all folders in the root directory
    subfolders = [os.path.join(path, folder) for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    
    for subfolder in subfolders:
        # To make sure all files are processed
        files_to_process = [
            filename for filename in os.listdir(subfolder)
            if filename.endswith('.knp') or filename.endswith('.org')
        ]
        #print("FUGASHI FTP",subfolder," Total Files:", len(subfolders) , " Total Files in subfodler:",len(files_to_process), datetime.now())

        # Iterate through files in each subfolder
        for filename in os.listdir(subfolder):
            file_path = os.path.join(subfolder, filename)
            try:
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.readlines()
                    
                    for line in content:
                        # Only extract needed information
                        line = line.strip()
                        if line.startswith("#"):
                            sid = line.split()[1]
                            kwdlc_org[sid] = []
                        else:
                            # create list of morpheme information [word, lemma, tag, tag, ...]
                            for word in tagger(line):
                                li = [word.surface, word.feature.lemma]
                                li.extend(word.pos.split(","))
                                kwdlc_org[sid].append(li)

            # To catch any exceptions
            except Exception as exception:
                print(f"File: {file_path}, Exception: {exception}")
         
    # calculate elapsed time
    elapsed_time = time.time()-start_time

    return kwdlc_org, elapsed_time

def save_dict(kwdlc_org_nagisa, kwdlc_org_C, kwdlc_org_B, kwdlc_org_A, kwdlc_org_fugashi):
    """save gold tags to a file using pickle
       input: all result dicts
       output: success message if .pkl files containing result dicts of all tokenizers have been saved"""
    
    # Save to .pkl file
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\Results1\kwdlc_nagisa.pkl', 'wb') as f:
        pickle.dump(kwdlc_org_nagisa, f)
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\Results1\kwdlc_sudachi_C.pkl', 'wb') as f:
        pickle.dump(kwdlc_org_C, f)
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\Results1\kwdlc_sudachi_B.pkl', 'wb') as f:
        pickle.dump(kwdlc_org_B, f)
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\Results1\kwdlc_sudachi_A.pkl', 'wb') as f:
        pickle.dump(kwdlc_org_A, f)
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\Results1\kwdlc_fugashi.pkl', 'wb') as f:
        pickle.dump(kwdlc_org_fugashi, f)

    print("Dictionary saved successfully!")

    # Save to a .txt file for overview (if needed)
    """
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\Results1\kwdlc_nagisa.txt', 'w', encoding='utf-8') as txt_file:
        json.dump(kwdlc_org_nagisa, txt_file, ensure_ascii=False, indent=4)
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\Results1\kwdlc_sudachi_C.txt', 'w', encoding='utf-8') as txt_file:
        json.dump(kwdlc_org_C, txt_file, ensure_ascii=False, indent=4)
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\Results1\kwdlc_sudachi_B.txt', 'w', encoding='utf-8') as txt_file:
        json.dump(kwdlc_org_B, txt_file, ensure_ascii=False, indent=4)
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\Results1\kwdlc_sudachi_A.txt', 'w', encoding='utf-8') as txt_file:
        json.dump(kwdlc_org_A, txt_file, ensure_ascii=False, indent=4)
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\Results1\kwdlc_fugashi.txt', 'w', encoding='utf-8') as txt_file:
        json.dump(kwdlc_org_fugashi, txt_file, ensure_ascii=False, indent=4)

    print("txt saved successfully!")"""

# Call functions for all models
path = "insert-path-KWDLC-ORG"
kwdlc_org_nagisa, elapsed_time_nagisa = tokenize_nagisa(path)
kwdlc_org_C, kwdlc_org_B, kwdlc_org_A, elapsed_time_sudachi = tokenize_sudachipy(path)
kwdlc_org_fugashi, elapsed_time_fugashi = tokenize_fugashi(path)

# Call function for saving result dics to .pkl file
save_dict(kwdlc_org_nagisa, kwdlc_org_C, kwdlc_org_B, kwdlc_org_A, kwdlc_org_fugashi)

# Output elapsed time results
print("elapses time fugashi:", elapsed_time_fugashi, "elapses time nagisa:", elapsed_time_nagisa, "elapses time sudachi:", elapsed_time_sudachi)



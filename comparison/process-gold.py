# Analyzing Japanese: Process Gold Data
# Author: Isabell Siem
# Matrikelnummer: 108018211002

import os
import re
import pickle

def pre_process_gold(root_directory):
    """Function that sorts tokens & tags from the KWDLC
    Input: tokenized and annoted KWDLC files as provided on git repository, path to KWDLC files
    Output: .kpn/.org file gold data (tokenized and tagged)
            file raw corpus
            dict {sid:[[word1orig, reading, dict, tag, etc],[word2orig,...],...]}"""

    # results dict
    kwdlc_gold = {}
    
    # Get all folders in the root directory
    subfolders = [os.path.join(root_directory, folder) for folder in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, folder))]
    
    for subfolder in subfolders:
        # Process only .knp files in each subfolder
        # To make sure the correct files are processed
        files_to_process = [
            filename for filename in os.listdir(subfolder)
            if filename.endswith('.knp')]
        
        #print(f"Subfolder:{subfolder}, Files: {files_to_process}")  
        
        # Iterate through files in each subfolder
        for filename in os.listdir(subfolder):
            file_path = os.path.join(subfolder, filename)
            try:
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.readlines()

                    for line in content:
                        # only read lines with required token infromation
                        if line.startswith(("*", "+")): continue
                        elif line.startswith("#"):
                            sid = line.split()[1]
                            kwdlc_gold[sid] = []
                        else: 
                            element = line.split()
                            temp_l = []
                            for tag in element:
                                if tag != "*" and tag != "+" and not re.match(r"[0-9]", tag) and tag != "NIL" and tag != "EOS":
                                    temp_l.append(tag)

                            # append list of token details to dict
                            if temp_l:
                                kwdlc_gold[sid].append(temp_l)
                            else: continue
            
            # To catch exceptions
            except Exception as exception:
                print(f"File: {file_path}, Exception: {exception}")

    return kwdlc_gold

def save_dict(kwdlc_gold):
    """Function for saving gold tokens & tags to a file using pickle
       input: dict kwdlc_gold
       output: success message if dict was saved as .pkl file"""
    
    with open('E:\BA-Arbeiten\Bachelor_thesis_2024\kwdlc_gold.pkl', 'wb') as f:
        pickle.dump(kwdlc_gold, f)

    print("Dictionary saved as .pkl file!")

kwdlc_gold = pre_process_gold('insert-path-KWDLC-TAGGED')
save_dict(kwdlc_gold)




# Analyzing Japanese: Evaluation
# Author: Isabell Siem
# Matrikelnummer: 108018211002

import pickle
import json

# Functions for evalutaion of results
def eval_sudachi(gold, sudachi):
    """Function that evaluates the tokenization and pos tagging results for Sudachi A, B, and C
    Input: Gold standard dict path (.pkl), list of paths to sudachi dicts (.pkl)
    Output: Prints the following values for every tokenization mode: 
                discrepancies_pos, discrepancies_tok, correct_count_pos, correct_count_tok, total_count"""

    # open result dictionaries
    with open(gold, 'rb') as f:
        gold_dict = pickle.load(f) 

    for dict in sudachi:
        with open(dict, 'rb') as f:
            dict2 = pickle.load(f)

        discrepancies_tok = []
        discrepancies_pos = []
        correct_count_pos = 0
        correct_count_tok = 0
        total_count = 0

        for sid, gold_data in gold_dict.items():
            # Extract tokens and tags from gold data
            gold_tokens = [(entry[0], entry[3]) for entry in gold_data]  
            dict2_tokens = [[entry[0], entry[3]] for entry in dict2[sid]]  

            # Initialize temporary lists
            g_temp = []
            dict2_temp = []

            # Extract tokens for comparison
            for g_tok, g_tag in gold_tokens:
                g_temp.append(g_tok)
            for dict2_tok, dict2_tag in dict2_tokens:
                dict2_temp.append(dict2_tok)

            total_count += len(gold_tokens)

            # list for mismatches
            mismatch = []

            # Get all tokenizer mismatches
            for elem in g_temp:
                if elem in dict2_temp:
                    dict2_temp.remove(elem)
                    correct_count_tok += 1
                else:
                    mismatch.append(elem)
                    discrepancies_tok.append({
                        "sid": sid,
                        "gold_word": elem,
                        "dict2_word": dict2_temp,  # Remaining tokens
                    })

            # For all correctly segmented tokens check if tag matches
            for tok, tag in gold_tokens:
                for sublist in dict2_tokens:
                    if tok == sublist[0]:  
                        # sublist[1] contains all tags assigned to tok (tag1, tag2, ...)
                        if tag in sublist[1] or tag == "名詞" and "代名詞" in sublist[1] or tag == "指示詞" and "代名詞" in sublist[1] or tag == "形容詞" and "形状詞" in sublist[1] or tag == "特殊" and "補助記号" in sublist[1]:
                            correct_count_pos += 1
                            sublist.remove(tok)
                        else:
                            discrepancies_pos.append({
                                "sid": sid,
                                "gold_word": tok,
                                "gold_tag": tag,
                                "dict2_word": sublist[0],
                                "dict2_tags": sublist[1]
                            })
                            sublist.remove(tok)

        if dict == sudachi[0]:
            # Insert path to save discrepancies in human readable .txt file (sudachi a)
            with open('insert-sudachi-a-TOK-eval-path.txt', 'w', encoding='utf-8') as txt_file:
                json.dump(discrepancies_tok, txt_file, ensure_ascii=False, indent=4)
            with open('insert-sudachi-a-POS-eval-path.txt', 'w', encoding='utf-8') as txt_file:
                json.dump(discrepancies_pos, txt_file, ensure_ascii=False, indent=4)
            print("\nSUDACHI A:\n", f"Correct matches TOK: {correct_count_tok}/{total_count}", "wrong TOK:", total_count - correct_count_tok, "Correct %:", correct_count_tok/total_count*100, "Incorrect %:", (total_count - correct_count_tok)/total_count*100)
            print(f"Correct matches POS: {correct_count_pos}/{correct_count_tok}", "wrong POS:", correct_count_tok - correct_count_pos, "Correct %:", correct_count_pos/correct_count_tok*100, "Incorrect %:", (correct_count_tok - correct_count_pos)/correct_count_tok*100)
            
        elif dict == sudachi[1]:
            # Insert path to save discrepancies in human readable .txt file (sudachi b)
            with open('insert-sudachi-b-TOK-eval-path.txt', 'w', encoding='utf-8') as txt_file:
                json.dump(discrepancies_tok, txt_file, ensure_ascii=False, indent=4)
            with open('insert-sudachi-b-POS-eval-path.txt', 'w', encoding='utf-8') as txt_file:
                json.dump(discrepancies_pos, txt_file, ensure_ascii=False, indent=4)
            print("\nSUDACHI B:\n", f"Correct matches TOK: {correct_count_tok}/{total_count}", "wrong TOK:", total_count - correct_count_tok, "Correct %:", correct_count_tok/total_count*100, "Incorrect %:", (total_count - correct_count_tok)/total_count*100)
            print(f"Correct matches POS: {correct_count_pos}/{correct_count_tok}", "wrong POS:", correct_count_tok - correct_count_pos, "Correct %:", correct_count_pos/correct_count_tok*100, "Incorrect %:", (correct_count_tok - correct_count_pos)/correct_count_tok*100)
            
        else: 
            # Insert path to save discrepancies in human readable .txt file (sudachi c)
            with open('insert-sudachi-c-TOK-eval-path.txt', 'w', encoding='utf-8') as txt_file:
                json.dump(discrepancies_tok, txt_file, ensure_ascii=False, indent=4)
            with open('insert-sudachi-c-POS-eval-path.txt', 'w', encoding='utf-8') as txt_file:
                json.dump(discrepancies_pos, txt_file, ensure_ascii=False, indent=4)
            print("\nSUDACHI C:\n", f"Correct matches TOK: {correct_count_tok}/{total_count}", "wrong TOK:", total_count - correct_count_tok, "Correct %:", correct_count_tok/total_count*100, "Incorrect %:", (total_count - correct_count_tok)/total_count*100)
            print(f"Correct matches POS: {correct_count_pos}/{correct_count_tok}", "wrong POS:", correct_count_tok - correct_count_pos, "Correct %:", correct_count_pos/correct_count_tok*100, "Incorrect %:", (correct_count_tok - correct_count_pos)/correct_count_tok*100)

def eval_fugashi(gold, fugashi):
    """Function that evaluates the tokenization and pos tagging results for Fugashi
    Input: Gold standard dict path (.pkl), Fugashi dict path (.pkl)
    Output: discrepancies_pos, discrepancies_tok, correct_count_pos, correct_count_tok, total_count"""

    with open(gold, 'rb') as f:
        gold_dict = pickle.load(f)

    with open(fugashi, 'rb') as f:
        dict2 = pickle.load(f)

    discrepancies_tok = []
    discrepancies_pos = []
    correct_count_pos = 0
    correct_count_tok = 0
    total_count = 0

    for sid, gold_data in gold_dict.items():
        # Extract tokens and tags from gold dict
        gold_tokens = [(entry[0], entry[3]) for entry in gold_data]  # `entry[3]` is the gold tag.
        dict2_tokens = [[entry[0], entry[2:]] for entry in dict2[sid]]  # `entry[2:]` contains all tags.
        
        # Initialize temporary lists
        g_temp = []
        dict2_temp = []

        # Extract tokens for comparison
        for g_tok, dict2_tag in gold_tokens:
            g_temp.append(g_tok)
        for dict2_tok, dict2_tag in dict2_tokens:
            dict2_temp.append(dict2_tok)
        
        total_count += len(gold_tokens)

        # Initialize an empty list to store mismatches
        mismatch = []

        # Get all tokenizer mismatches
        for elem in g_temp:
            if elem in dict2_temp:
                dict2_temp.remove(elem)
                correct_count_tok += 1
            else:
                mismatch.append(elem)
                discrepancies_tok.append({
                    "sid": sid,
                    "gold_word": elem,
                    "dict2_word": dict2_temp, 
                })
        
        # Out of correctly tokenized tokens, get POS tag mismatches
        for tok, tag in gold_tokens:
            for sublist in dict2_tokens:
                if tok == sublist[0]:  
                    # Check if tag matches any of the tags assigned by fugashi
                    if tag in sublist[1] or tag == "名詞" and "代名詞" in sublist[1] or tag == "指示詞" and "代名詞" in sublist[1] or tag == "形容詞" and "形状詞" in sublist[1] or tag == "特殊" and "補助記号" in sublist[1]:
                        correct_count_pos += 1
                        sublist.remove(tok)
                    else:
                        discrepancies_pos.append({
                            "sid": sid,
                            "gold_word": tok,
                            "gold_tag": tag,
                            "dict2_word": sublist[0],
                            "dict2_tags": sublist[1]
                        })
                        sublist.remove(tok)

    return discrepancies_pos, discrepancies_tok, correct_count_pos, correct_count_tok, total_count

def eval_nagisa(gold, nagisa):
    """Function that evaluates the tokenization and pos tagging results for Nagisa
    Input: Gold standard dict, nagisa dict
    Output: discrepancies_pos, discrepancies_tok, correct_count_pos, correct_count_tok, total_count"""

    # open result dictionaries 
    with open(gold, 'rb') as f:
        gold_dict = pickle.load(f)
    with open(nagisa, 'rb') as f:
        dict2 = pickle.load(f)

    discrepancies_tok = []
    discrepancies_pos = []
    correct_count_pos = 0
    correct_count_tok = 0
    total_count = 0

    for sid, gold_data in gold_dict.items():
        gold_tokens = [(entry[0], entry[3]) for entry in gold_data]  
        dict2_tokens =  [[entry[0], entry[1]] for entry in dict2[sid]]

        # initialize temporary lists
        g_temp = []
        dict2_temp = []

        # Extract tokens for comparison
        for g_tok, g_tag in gold_tokens:
            g_temp.append(g_tok)
        for dict2_tok, dict2_tag in dict2_tokens:
            dict2_temp.append(dict2_tok)
        
        total_count+= len(gold_tokens)
        
        # list for mismatches
        mismatch = []

        # Get all tokenizer mismatches
        for elem in g_temp:
            if elem in dict2_temp:
                dict2_temp.remove(elem)
                correct_count_tok+= 1
            else:
                mismatch.append(elem)
                discrepancies_tok.append({
                    "sid": sid,
                    "gold_word": elem,
                    "dict2_word": dict2_temp,
                })

        # Out of correctly tokenized tokens get POS tag mismatches
        for tok, tag in gold_tokens:
            for sublist in dict2_tokens:
                if len(sublist) == 2 and tok == sublist[0]: 
                    if tag == sublist[1] or tag == "名詞" and tag in sublist[1] or tag == "指示詞" and sublist[1] == "代名詞" or tag == "形容詞" and sublist[1] == "形状詞" or tag == "特殊" and sublist[1] == "補助記号":
                        correct_count_pos += 1
                        sublist.remove(tok)
                    else:
                        discrepancies_pos.append({
                        "sid": sid,
                        "gold_word": tok,
                        "gold_tag": tag,
                        "dict2_word": sublist[0],
                        "dict2_tag": sublist[1]
                    })
                        sublist.remove(tok)
                else: continue

    return discrepancies_pos, discrepancies_tok, correct_count_pos, correct_count_tok, total_count

# fugashi
# Insert path to dicts in .pkl format
discrepancies_pos, discrepancies_tok, correct_count_pos, correct_count_tok, total_count = eval_fugashi('insert-gold-dict-path.pkl', 'insert-fugashi-dict-path.pkl')
# nagisa
discrepancies_pos, discrepancies_tok, correct_count_pos, correct_count_tok, total_count = eval_nagisa('insert-gold-dict-path.pkl', 'insert-nagisa-dict-path.pkl')

# Output results
if discrepancies_tok:
    print(f"Correct matches TOK: {correct_count_tok}/{total_count}", "wrong TOK:", total_count - correct_count_tok, "Correct %:", correct_count_tok/total_count*100, "Incorrect %:", (total_count - correct_count_tok)/total_count*100)
    with open('insert-nagisa-OR-fugashi-TOK-eval-path.txt', 'w', encoding='utf-8') as txt_file:
        json.dump(discrepancies_tok, txt_file, ensure_ascii=False, indent=4)
else:
    print("All tokens match!")

if discrepancies_pos:
    print(f"Correct matches POS: {correct_count_pos}/{correct_count_tok}", "wrong POS:", correct_count_tok - correct_count_pos, "Correct %:", correct_count_pos/correct_count_tok*100, "Incorrect %:", (correct_count_tok - correct_count_pos)/correct_count_tok*100)
    with open('insert-nagisa-OR-fugashi-POS-eval-path.txt', 'w', encoding='utf-8') as txt_file:
        json.dump(discrepancies_pos, txt_file, ensure_ascii=False, indent=4)
else:
    print("All tags match!")

# Sudachi
discrepancies_pos, discrepancies_tok, correct_count_pos, correct_count_tok, total_count = eval_sudachi('insert-gold-dict-path.pkl',['insert-sudachi-a-dict-path.pkl', 'insert-sudachi-b-dict-path.pkl', 'insert-sudachi-c-dict-path.pkl'])



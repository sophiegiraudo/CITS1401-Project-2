"""
Author: Sophie Giraudo (22838134)
Date: 25/10/2019

A program to verify authorship using stylometry.
Formatted using PEP 8 guidelines
"""

import os
from math import *


def main(textfile1, textfile2, feature):
    
    file1, file2 = read_file(textfile1), read_file(textfile2)
    
    if not file1 or not file2:
        return None, None, None
    
    profile1, profile2, score = comparison(file1, file2, feature)
    
    if not profile1 or not profile2:
        return None, None, None
    
    return score, profile1, profile2



def read_file(textfile):
    """
    Verifies a file exists, reads it and returns its contents
    """
    if not os.path.isfile(textfile):
        print("File does not exist")
        return None
    else:
        openfile = open(textfile, 'r')
        file = openfile.read()
        openfile.close()
 
    return file



def comparison(file1, file2, feature):
    """
    Returns the profiles of boths files as dictionaries
    Returns their comparison score as a float.
    
    Keywords Arguments:
    
    file1 -- A string containing the contents of the first file
    file2 -- A string containing the contents of the second file
    feature -- The specification to compare the files on
    """
    try:
        feature = feature.lower()
    except AttributeError:
        print('Invalid feature name.')
        return None, None, None
    
    feature_list = ['conjunctions', 'unigrams', 'punctuation', 'composite']
    
    if feature not in feature_list:
        print("Feature does not exist")
        return None, None, None
    
    if feature == 'conjunctions':
        profile1, profile2 = conjunctions(file1), conjunctions(file2)
        score = conjunctions_score(profile1, profile2)
        
    elif feature == 'unigrams':
        profile1, profile2 = unigrams(file1, file2)
        score = unigrams_score(profile1, profile2)
    
    elif feature == 'punctuation':
        profile1, profile2 = punctuation(file1), punctuation(file2)
        score = punctuation_score(profile1, profile2)
        
    elif feature == 'composite':
        conjunctions_profile1 = conjunctions(file1)
        conjunctions_profile2 = conjunctions(file2)
        punctuation_profile1 = punctuation(file1)
        punctuation_profile2 = punctuation(file2)
        profile1 = composite(file1, conjunctions_profile1, punctuation_profile1)
        profile2 = composite(file2, conjunctions_profile2, punctuation_profile2)
        score = composite_score(profile1, profile2)
        
    return profile1, profile2, score



def conjunctions(file):
    """
    Returns the dictionary of the count of all conjunctions in a file.
    """
    
    conjunction_words = {"also":0, "although":0, "and":0, "as":0, "because":0,
              "before":0, "but":0, "for":0, "if":0, "nor":0, "of":0, "or":0,
              "since":0, "that":0, "thought":0,"until":0, "when":0,
              "whenever":0, "whereas":0, "which":0, "while":0, "yet":0}
    
    words = conjunctions_file(file)
    
    for word in words:
        if word in conjunction_words:
            conjunction_words[word] = conjunction_words.get(word, 0) + 1
            
    return conjunction_words



def conjunctions_file(file):
    """
    Returns a list of all words in a file excluding all punctuation.
    """
    
    file_list = []
    words = []
    punctuation = "!@#$%^&*()_=+`~[]{}|\"';:<,>.?/\\"
    
    file = file.replace("--", " ").replace("\n", " ")
    
    for mark in punctuation:
        file = file.replace(mark, "")

    file_list.append(file.split(" "))
    
    for word in file_list[0]:
        if word:
            words.append(word.lower())

    return words



def conjunctions_score(profile1, profile2):
    """
    Returns the comparison score of the dictionaries of conjunctions for
    each file, rounded to 4 decimal places.
    
    Keyword Arguments:
    
    profile1 -- A dictionary containing the count of conjunction words for
                file 1
    profile2 -- A dictionary containing the count of conjunction words for
                file 2
    """
    
    count = 0
    
    for word in profile1:
        count += (profile1[word]-profile2[word])**2
    
    distance = sqrt(count)
    
    return round(distance, 4)



def unigrams(file1, file2):
    """
    Returns dictionaries containing all words from both files and the counts
    of words from each respective file.
    """
    
    dictionary1 = {}
    dictionary2 = {}
    
    words1 = unigrams_file(file1)
    words2 = unigrams_file(file2)
    
    for word in words1:
        dictionary1[word] = dictionary1.get(word, 0) + 0
        dictionary2[word] = dictionary2.get(word, 0) + 0
    
    for word in words2:
        dictionary1[word] = dictionary1.get(word, 0) + 0
        dictionary2[word] = dictionary2.get(word, 0) + 0
    
    for word in words1:
        dictionary1[word] = dictionary1.get(word, 0) + 1
    
    for word in words2:
        dictionary2[word] = dictionary2.get(word, 0) + 1
        
    return dictionary1, dictionary2



def unigrams_file(file):
    """
    Returns a list of all words in a file.
    """
    
    file_list = []
    words = []
    punctuation = "!@#$%^&*()_=+`~[]{}|\"';:<,>.?/\\"
    
    file = file.replace("--", " ").replace("\n", " ")
    
    for mark in punctuation:
        file = file.replace(mark, "")

    file_list.append(file.split(" "))
    
    for word in file_list[0]:
        if word:
            words.append(word.lower())

    return words



def unigrams_score(profile1, profile2):
    """
    Returns the comparison score of the dictionaries of all words for
    each file, rounded to 4 decimal places.
    
    Keyword Arguments:
    
    profile1 -- A dictionary containing the count of all words for file 1
    profile2 -- A dictionary containing the count of all words for file 2
    """
    
    count = 0
    
    for word in profile1:
        count += (profile1[word]-profile2[word])**2
    
    distance = sqrt(count)
    
    return round(distance, 4)
    
    
    
def punctuation(file):
    """
    Returns a dictionary of the counts of specific punctuation marks in a file.
    """
    
    punctuation = {",":0, ";":0, "'":0, "-":0}
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    file = file.replace("--", " ").replace("\n", " ")

    for ch in range(len(file)):
        if file[ch] == ",":
            punctuation[file[ch]] = punctuation.get(file[ch], 0) + 1
        elif file[ch] == ";":
            punctuation[file[ch]] = punctuation.get(file[ch], 0) + 1
        elif file[ch] == "'":
            try:
                if file[ch-1] in alphabet and file[ch+1] in alphabet:
                    punctuation[file[ch]] = punctuation.get(file[ch], 0) + 1
            except IndexError:
                continue
        elif file[ch] == "-":
            try:
                if file[ch-1] in alphabet and file[ch+1] in alphabet:
                    punctuation[file[ch]] = punctuation.get(file[ch], 0) + 1
            except IndexError:
                continue
            
    return punctuation



def punctuation_score(profile1, profile2):
    """Returns the comparison score of the dictionaries of punctuation for
    each file, rounded to 4 decimal places.
    
    Keyword Arguments:
    
    profile1 -- A dictionary containing the count of punctuation marks for
                file 1
    profile2 -- A dictionary containing the count of punctuation marks for
                file 2
    """
    
    count = 0
    
    for mark in profile1:
        count += (profile1[mark]-profile2[mark])**2
    
    distance = sqrt(count)
    
    return round(distance, 4)



def composite(file, conjunctions_profile, punctuation_profile):
    """
    Returns a dictionary containing the count of conjunction words, punctuation
    marks, words per sentence and sentences per paragraph of a file.
    
    Keyword Arguments:
    
    file -- The text file to compare
    conjunctions_profile -- A dictionary containing the count of conjunction
                            words in the file
    punctuation_profile -- A dictionary containing the count of punctuation
                            makrs in the file
    """
    
    profile = conjunctions_profile
    profile.update(punctuation_profile)
    
    words_per_sentence = composite_sentences(file)
    profile["words_per_sentence"] = words_per_sentence
    
    sentence_per_para = composite_paragraphs(file)
    profile["sentence_per_paragraph"] = sentence_per_para

    return profile
    


def composite_sentences(file):
    """
    Returns the average number of words per sentence of a file
    """
    
    file_list = []
    sum_words = 0

    file_list.append(file.replace("!",".").replace("?",".").split("."))

    while file_list[0][len(file_list[0])-1] == "\n":
        file_list[0].remove(file_list[0][len(file_list[0])-1])
        
    no_sentences = len(file_list[0])  
    words_p_sentence = words_per_sentence(no_sentences, file_list)
    
    return words_p_sentence


        
def words_per_sentence(no_sentences, file_list):
    """
    Calculates and returns the number of words per sentence
    
    Keyword Arguments:
    
    no_sentences -- The number of sentences in a file
    file_list -- A list containing the file
    """
    
    sum_of_words = 0

    while file_list[0][len(file_list[0])-1] == "\n":
        file_list[0].remove(file_list[0][len(file_list[0])-1])

        
    for line in file_list[0]:
        words = []
        words.append(line.replace("--", " ").replace("\n", " ")
                     .strip(" ").split(" "))
        sum_of_words += len(words[0])
  
    words_p_sentence = sum_of_words / no_sentences

    return round(words_p_sentence, 4)



def composite_paragraphs(file):
    """
    Returns the number of sentences per paragraph
    """
    
    paragraph_list = []
    sentence_sum = 0
    
    paragraph_list.append(file.split("\n\n"))
    no_paragraphs = len(paragraph_list[0])
    
    for paragraph in range(len(paragraph_list[0])):
        sentence_list = []
        sentence_list.append(paragraph_list[0][paragraph].replace("!",".")
                             .replace("?",".").split("."))
        sentence_sum += len(sentence_list[0])-1
    
    sentences_per_paragraph = sentence_sum / no_paragraphs
    
    return round(sentences_per_paragraph, 4)
    
    

def composite_score(profile1, profile2):
    """Returns the comparison score of the dictionaries containing the count
    of conjunction words, punctuation marks, words per sentence and sentences
    per paragraph of a file.
    
    Keyword Arguments:
    
    profile1 -- A dictionary containing the count of conjunction words,
                punctuation marks, words per sentence and sentences per
                paragraph for file 1
    profile2 -- A dictionary containing the count of conjunction words,
                punctuation marks, words per sentence and sentences per
                paragraph for file 2
    """
    
    count = 0
    
    for word in profile1:
        count += (profile1[word]-profile2[word])**2
    
    distance = sqrt(count)

    return round(distance, 4)



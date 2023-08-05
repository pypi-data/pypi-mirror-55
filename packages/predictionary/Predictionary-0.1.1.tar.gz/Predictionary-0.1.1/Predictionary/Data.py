#IMPORTS
import sys
from tika import parser
from tqdm import tqdm
import numpy as np
from numpy import newaxis
import string
from itertools import chain, cycle
from keras.utils import np_utils, to_categorical

#pulls the strings from int values
def ints_to_string(ints_list, word_to_int_dictionary):
  final_string_list = []
  for x in ints_list:
    final_string_list.append(list(word_to_int_dictionary.keys())[list(word_to_int_dictionary.values()).index(x)])
  return final_string_list

#pulls the ints from string values
def string_to_ints(string_list, int_to_word_dictionary):
  #text = fully_processed_text(string)
  final_string_list = []

  for x in string_list:
    final_string_list.append(list(int_to_word_dictionary.keys())[list(int_to_word_dictionary.values()).index(x)])

  return final_string_list

#next steps, split up the list of processed text into sentences
#get indecies of all sentence splitters, so then we can split up the fully text into sentences
def splitter_index(fully_processed_text):
  main_list = []
  splitters = ['!','?','.']
  for splitter in splitters:
    main_list += [i for i, n in enumerate(fully_processed_text) if n == splitter] # List comprehension
  return sorted(main_list)

def make_sentences(fully_processed_text):
  full_splitter_index = splitter_index(fully_processed_text)
  clean_sentences = []
  sentence_lengths = []
  for x in range(len(full_splitter_index)):
    if x == 1:
      stop_index = full_splitter_index[x]
      clean_sentences.append(fully_processed_text[:stop_index+1])
    else:
      past_stop_index = full_splitter_index[x-1]
      curr_stop_index = full_splitter_index[x]
      clean_sentences.append(fully_processed_text[past_stop_index+1:curr_stop_index+1])

  return clean_sentences

def encode_sentences(clean_sentences_list_of_lists, int_to_word_dictionary):
  clean_encoded = []
  for sentence in clean_sentences_list_of_lists:
    clean_encoded.append(string_to_ints(sentence,int_to_word_dictionary))
  return clean_encoded



def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

def make_data(fully_processed_text, int_to_word_dictionary, sequence_length=50, X_one_hot=False, split_train_test=True, test_train_split_ratio=0.33, save_locally=True):
  #print("Creating Test & Train Datasets @ Sequence Length: ", sequence_length)
  start_index = 0
  end_and_answer = sequence_length
  n_unique_words = len(int_to_word_dictionary)
  x_data = []
  y_data = []

  #here we're making the actual raw text data, and should have the book's word length - 50
  #len(fully_processed_text) - 50 , double looping somwhere and tryping to convert letter not word
  data_range = range(len(fully_processed_text) - sequence_length)
  for x in tqdm(data_range):
    #getting lists of words that are 50, and 1 words long
    temp_x = fully_processed_text[start_index:end_and_answer]
    temp_y = [fully_processed_text[end_and_answer]]

    #append to a master list
    x_data.append(string_to_ints(temp_x, int_to_word_dictionary))
    y_data.append(string_to_ints(temp_y, int_to_word_dictionary))

    start_index += 1
    end_and_answer += 1

  if split_train_test:
      from sklearn.model_selection import train_test_split
      X_train, X_test, Y_train, Y_test = train_test_split(x_data, y_data, test_size=test_train_split_ratio, shuffle=True)

      #giving the user some info
      print("")
      print("Number of Train Examples: ", len(X_train))
      print("Number of Test Examples: ", len(X_test))
      print("")

      #converting to numpy
      print("Converting to Arrays...")
      print("")
      X_train = np.array(X_train)
      X_test = np.array(X_test)
      Y_train = np.array(Y_train)
      Y_train = np.array(Y_train)

      #turning the  target vars to categorical
      Y_train = to_categorical(Y_train, num_classes=n_unique_words, dtype='float32')
      Y_test = to_categorical(Y_test, num_classes=n_unique_words, dtype='float32')

      if X_one_hot:
        print("Setting X data to one-hot")
        print("")
        X_train = to_categorical(X_train, num_classes=n_unique_words, dtype='float32')
        X_test = to_categorical(X_test, num_classes=n_unique_words, dtype='float32')

      else:
        #if we don't encode using one-hot
        X_train = X_train.reshape((X_train.shape[0], sequence_length, 1))
        X_test = X_test.reshape((X_test.shape[0], sequence_length, 1))

        #save the files here
      if save_locally:
          print("Saving Files...")
          np.save('X_train_data.npy', X_train)
          np.save('Y_train_data.npy', Y_train)

          np.save('X_test_data.npy', X_test)
          np.save('Y_test_data.npy', Y_test)
          print("")

      print("Done.")
      return X_train, X_test, Y_train, Y_test

  else:
      X = np.array(x_data)
      Y = np.array(y_data)

      #turning the  target vars to categorical
      Y = to_categorical(Y, num_classes=n_unique_words, dtype='float32')

      if X_one_hot:
        X = to_categorical(X, num_classes=n_unique_words, dtype='float32')

      else:
        #if we don't encode using one-hot
        X = X.reshape((X.shape[0], sequence_length, 1))

      #save the files here
      if save_locally:
          print("Saving Files...")
          np.save('X_data.npy', X)
          np.save('Y_data.npy', Y)
          print("")

      print("Done.")
      return X, Y


 #return text

#remove punctuation
def kill_punctuation(s):
 return s.translate(str.maketrans('', '', string.punctuation))

#check if the word contains unwanted punctuation
def contains_punctuation(word):
 #punctuation we don't want
 chars = set("][-.,!?:_\"';)(")

 if len(word) > 1:
   #only checking here if there is punct we don't want at the beginning or end of the word.
   if word[0] in chars or word[len(word)-1] in chars:
       return True
   else:
       return False
 else:
   False

def intersperse(lst, item):
   result = [item] * (len(lst) * 2 - 1)
   result[0::2] = lst
   return result

#take in the word and check if the end or beginning of words has the nono char, then return
#the stripped word and the char, in the right order as a list
def split_up_punctuation(word):
 #punctuation we don't want
 chars = set("][-.,!?:_\"';)(")
 return_list = []

 #if we have punct in the first char
 if any((c in chars) for c in word[0]):
   unwanted_char = word[0]
   return_list.append(unwanted_char)
   return_list.append(word[1:])

 #if we have punct in the end
 elif any((c in chars) for c in word[len(word)-1]):
   unwanted_char = word[len(word)-1]
   return_list.append(word[:len(word)-1])
   return_list.append(unwanted_char)

 if len(return_list[0]) == 1:
   if contains_punctuation(return_list[1]):
     return_list = list(return_list[0]) + list(split_up_punctuation(return_list[1]))
 else:
   if contains_punctuation(return_list[0]):
     return_list = list(split_up_punctuation(return_list[0])) + list(return_list[1])

 return return_list


#edit the punctuation part to make words into chars

#make a function that turns the text into a huge list of lowercase words without periods, exclamation marks, or quotes, or commas
#if, while adding to new list, we run into a word with any of these, just use the kill punct function and append that char to the
#list afterwords.
def process_text(text, split_by_words=True, keep_spaces=False):
 #take the clean text and make a LIST of clean words
 raw_split_text = text.splitlines()
 clean_text_list = []
 for exerpt in raw_split_text:
   temp_list = exerpt.split()
   #this part adds a space betweem each list item so we can predict real sentence structures
   if keep_spaces:
       temp_list = intersperse(temp_list, " ")
   if split_by_words:
     for word in temp_list:
       #check if word has punctiation
       #if it does, find the index where it is, pull the char out,
       #append the word sans punctuation and the punctuation to a list in the order
       #they appear, and concat the list to the clean text list
       if contains_punctuation(word):

         #splitting up the word and last punctuation
         cleaned_pair = split_up_punctuation(word)

         #add the final clean text pair/group to text
         clean_text_list  = clean_text_list + cleaned_pair

       else:
         #split the word into a list THEN do it
         clean_text_list.append(word)
   else:
     for word in temp_list:
       clean_text_list += list(word)

 return clean_text_list

 #creating a dictionary with words being keys and ints being values
#if it has been added, pass, else, add it with a unique number
def word_to_int(fully_processed_text):
  dictionary = {"":0, "\r":1, "\n":2 }
  unique_chars = sorted(list(set(fully_processed_text)))
  for char in unique_chars:
    if char in dictionary:
      pass
    else:
      dictionary.update({char:len(dictionary)})
  return dictionary

#basically just flipping the word2int dict
def int_to_word(word_to_int_dictionary):
  int_to_word_dictionary = dict((v,k) for k,v in word_to_int_dictionary.items())
  return int_to_word_dictionary

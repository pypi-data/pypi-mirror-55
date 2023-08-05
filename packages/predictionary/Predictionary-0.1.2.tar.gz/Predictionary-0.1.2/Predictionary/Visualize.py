##methods make_prevelence_dict, plotTop
#IMPORTS
import sys
import numpy as np
from numpy import newaxis
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure



def plot_top(number, dict_prevelence):
    #making two lists so we can plot easily using numpy
    words_prevelence = []
    vals = []

    #adding each value and item in order to the plot lists
    for pair in dict_prevelence[:(number+1)]:
      words_prevelence.append(pair[0])
      vals.append(pair[1])

    #the actual data values in order of each element
    y_pos = np.arange(len(words_prevelence))

    #size and styling
    figure(num=None, figsize=((number*1.5), 5), dpi=80, facecolor='w', edgecolor='k')

    #plotting code
    plt.bar(y_pos, vals, align='center', alpha=0.85)
    plt.xticks(y_pos, words_prevelence)
    plt.ylabel('Instances                            ',rotation=0)
    plt.title('Instances of Each Word in Text')

    plt.show()

#take in the full cleaned text as a list and display the top n characters
def make_prevelence_dict(clean_text_list):
  #init dict for counting top 50 words
  dict_prevelence = {}
  for word in clean_text_list:
      #if not in dict, add to dict_prevelence, else, increment val
      if word not in dict_prevelence:
        dict_prevelence[word] = 1
      else:
        dict_prevelence[word] += 1
  dict_prevelence = sorted(dict_prevelence.items(), key=lambda x: x[1], reverse=True)
  print("Unique Words: ", len(dict_prevelence))
  return dict_prevelence

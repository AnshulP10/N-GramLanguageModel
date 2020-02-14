**********************Assignment 1****************************************
Task - Create a n-gram language model. Perform smoothing using Kneser-Ney/Witten-Bell Smoothing. 

How to Run - 1.python3 language_model.py <n(for n-gram)> <smoothing method> <path to txt file>
             2.<input sentence>  
n - 1/2/3 
smoothing method - k(Kneser-Ney) / w(Witten-Bell)

Comparison of Witten-Bell and Kneser-Ney Smoothing
Witten-Bell is a simple form of interpolation where the weight could be seen as the probability of using the higher order model. The weight depends on the applicability of the context(number of words followed by the context)
Kneser-Ney is an extension of of absolute discount where for lower order models instead of maximum likelihood prob it uses a continuation count which is dependant on the number of unique contexts it follows. The weight is dependant on the discounting factor.

Performance
1.Kneser-Ney gives higher probabilities for sensible sentences on an average(0.05 for len = 4) compared to Witten-Bell(0.001 for len = 4)
2.Kneser-Ney has a bigger difference between sensible and senseless sentences(0.05 to 0.0001 for len = 4 and words are common) compared to Witten-Bell(0.001 to 0.0005)
3.Witten-Bell gives unusually high probabilities for sentences which are senseless but feature high probability words. This could be due to the absence of a continuation count.
4.Witten-Bell gives a lower probability difference for sentences where a new word is seen(0.0001 to 0.00001) compared to Kneser-Ney(0.005 to 0.00001). This could be a good thing if the sentence is sensible and bad if it's not
5.On an overall scale we can confidently say that Kneser-Ney performs better than Witten-Bell for the given dataset.

How we built our code:
1.Preprocess the corpus(remove headings, sp chars, replace newline with '.')
2.Get unigram, bigram, trigram counts
3.Implement the smoothing algorithms using the defined formula
4.To get probability for an input divide it into n grams and using bayes' rule multiply the probability of each ngram to get probability of the whole input

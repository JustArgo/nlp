import nltk
brown_news_tagged = nltk.corpus.brown.tagged_words(categories='news')
tag_fd = nltk.FreqDist(tag for (word,tag) in brown_news_tagged)
tag_fd.keys()
word_tag_pairs = nltk.bigrams(brown_news_tagged)
list(nltk.FreqDist(a[1] for (a,b) in word_tag_pairs if b[1] == 'N'))
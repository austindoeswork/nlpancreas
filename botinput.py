# module botinput
import nltk
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

# Used when tokenizing words
sentence_re = r'''(?x)      # set flag to allow verbose regexps
      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''
#Taken from Su Nam Kim Paper and modified
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
    NBARS:
        {<CD><NBAR>} # count then a noun phrase
    NP:
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
        {<NBARS><IN><NBAR>}  # Above, connected with in/of/etc...
        {<NBAR>}
        {<NBARS>}
    TIME:
        {<IN><CD>}
"""
grammar2 = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
    NBARS:
        {<CD><NBAR>} # count then a noun phrase
    NP:
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
        {<NBARS><IN><NBAR>}  # Above, connected with in/of/etc...
        {<NBAR>}
        {<NBARS>}
    TIME:
        {<IN><CD>}
"""
chunker = nltk.RegexpParser(grammar)

def pos_tokenize(inputSentence):
    toks = nltk.regexp_tokenize(inputSentence, sentence_re)
    toks = nltk.word_tokenize(inputSentence)
    postoks = nltk.tag.pos_tag(toks)
    return postoks

def chunk_tree(postoks):
    tree = chunker.parse(postoks)
    return tree

def npleaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    # TODO implement stemming and lemmatization
    #  word = stemmer.stem_word(word)
    #  word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(0 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted

def get_terms(tree):
    for leaf in npleaves(tree):
        term = [ (normalise(w),t) for w,t in leaf if acceptable_word(w) ]
        yield term, classify_npterm(term)

#term is a list of strings
def classify_npterm(term):
    # TODO change this to a map for constant time lookup
    timeTokens = ["minutes", "hours", "seconds", "moments", "minute",
                    "hour", "second", "moment", "min", "mins",
                    "night", "tonight"]
    for tok in timeTokens:
        for f,p in term:
            if tok in f:
                return "time"
        #  if tok in term:
            #  return "time"
    return "food"

def parse_input(inputSentence, verbose):
    # TODO fix POS tagger
    # fails on I ate hummus 5 minutes ago
    postoks = pos_tokenize(inputSentence)
    tree = chunk_tree(postoks)
    terms = get_terms(tree)

    if verbose:
        print postoks
        print tree
    
    foodList = []
    for term in terms:
        foodList.append(term)
    return foodList

def print_guess(inputSentence):
    postoks = pos_tokenize(inputSentence)
    print postoks
    tree = chunk_tree(postoks)
    print tree
    terms = get_terms(tree)
    for term, _ in terms:
        for word in term:
            print word,


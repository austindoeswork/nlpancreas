# module botinput
import nltk
from nltk.corpus import stopwords
import csv

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
    AMOUNT:
        {<CD><QUAN>}
        {<QUAN>}
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
    NBARS:
        {<CD><NBAR>} # count then a noun phrase
        {<AMOUNT><NBAR>}
    FOOD:
        {<NBAR><IN><NBAR>}  
        {<NBAR><POS><NBAR>}  
        {<NBARS><IN><NBAR>}  
        {<NBARS><POS><NBAR>}  
        {<AMOUNT><IN><NBAR>}  
        {<AMOUNT><POS><NBAR>}  # Above, connected with in/of/etc...
        {<AMOUNT><IN><NBAR>}  
        {<AMOUNT><POS><NBAR>}  
        {<NBAR>}
        {<NBARS>}
    TIME:
        {<CD><TIMR>}
        {<JJ><TIMA>}
        {<TIMR>}
        {<TIMA>}
"""
chunker = nltk.RegexpParser(grammar)

# =============================================================================
# NLP
# =============================================================================
# TODO refactor all of this into a class

def is_confirm(inputSentence):
    toks = nltk.word_tokenize(inputSentence)
    confirmers = ['sure', 'y', 'great', 'yea', 'yeah', 'yes', 'yup', 'thanks', 'super', 'awesome', 'yee']
    for conf in confirmers:
        if conf in toks:
            return True
    return False

amendments = None
def set_amendments(filepath):
    global amendments
    amendments = {}
    data = list(csv.reader(open(filepath), delimiter=' '))
    for d in data:
        if len(d) == 2:
            word = d[0]
            tag = d[1]
            amendments[word] = tag

def pos_amend(tagged_list):
    if not amendments:
        return
    for i, tup in enumerate(tagged_list):
        word, tok = tup
        replacement = amendments.get(word)
        if replacement:
            tagged_list[i] = (word,replacement)

def pos_tokenize(inputSentence):
    #  toks = nltk.regexp_tokenize(inputSentence, sentence_re)
    toks = nltk.word_tokenize(inputSentence)
    #  toks = [normalise(w) for w in toks]
    postoks = nltk.tag.pos_tag(toks)
    pos_amend(postoks)
    return postoks

def chunk_tree(postoks):
    tree = chunker.parse(postoks)
    return tree

def npleaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='FOOD'):
        yield subtree.leaves()

def timeleaves(tree):
    time = []
    for subtree in tree.subtrees(filter = lambda t: t.label()=='TIME'):
        time.append(subtree)
    return time

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    # TODO implement stemming and lemmatization
    #  word = stemmer.stem_word(word)
    #  word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    if word.lower() == 'of':
        return True
    accepted = bool(0 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted

def get_terms(tree):
    terms = []
    foods = []

    foodTime = None
    time = timeleaves(tree)
    if len(time) > 0:
        foodTime = ""
        for taggedTime in time[0]:
            wor, ta = taggedTime
            if foodTime == "":
                foodTime = wor
            else:
                foodTime = foodTime + " " + wor

    terms = npleaves(tree)
    for food in terms:
        name = ""
        count = None
        quantity = None
        for i, taggedWord in enumerate(food):
            word, tag = taggedWord
            if tag == 'JJ' or tag == 'NN' or tag == 'NNS':
                if name == "":
                    name = word
                else:
                    name = name + " " + word
            elif tag == 'CD':
                count = word
            elif tag == 'QUAN':
                quantity = word
        f = Food(name, count, quantity)
        foods.append(f)

    return foods,foodTime

#term is a list of strings
def classify_npterm(term):
    return "food"

# =============================================================================
# PARSE INPUT
# =============================================================================
def parse_input(inputSentence, verbose):
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

# =============================================================================
# FOOD CLASS
# =============================================================================
class Food():
    def __init__(self, name, count=None, quantity=None):
        self.name = name
        self.count = count
        self.quantity = quantity
    def pprint(self):
        print "Food:", self.name
        if self.count:
            print "----Count:", self.count
        if self.quantity:
            print "----Quant:", self.quantity
        
#  def print_guess(inputSentence):
    #  postoks = pos_tokenize(inputSentence)
    #  print postoks
    #  tree = chunk_tree(postoks)
    #  print tree
    #  terms = get_terms(tree)
    #  for term, _ in terms:
        #  for word in term:
            #  print word,


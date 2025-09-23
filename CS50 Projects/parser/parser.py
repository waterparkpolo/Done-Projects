import nltk
import sys
nltk.download('punkt_tab')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj VP | NP VP Conj NP VP
NP -> N | Det N | P NP | Det AP N | NP P NP
VP -> V | V Adv | VP NP | Adv VP | V NP Adv
AP -> Adj | AP Adj
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    removed = set()  # Create an empty set to keep track of words that should be removed

    # Tokenize the input sentence into a list of words
    words = nltk.word_tokenize(sentence)

    for i in range(0, len(words)):
        # Convert the word to lowercase
        words[i] = words[i].lower()

        if not words[i].islower():
            removed.add(words[i])

    # Build a new list of words, excluding any that ended up in the 'removed' set
    words = [w for w in words if w not in removed]

    # Return the words
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Initialize an empty list to store the noun phrase (NP) chunks
    chunks = []

    # Loop through every subtree in the parse tree
    for s in tree.subtrees():
        # Check if the label of the current subtree is 'NP' (Noun Phrase)
        if s.label() == 'NP':
            # If it is, add the whole subtree to the list of chunks
            chunks.append(s)

    # Return the list of all noun phrase chunks found in the tree
    return chunks


if __name__ == "__main__":
    main()

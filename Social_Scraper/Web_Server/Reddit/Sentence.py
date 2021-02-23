import praw
import pprint
from datetime import datetime
import re
import string
import sqlite3
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
import numpy as np
from nltk import Tree
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


class Token:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.lemma = self.lem()
        print(self.lemma)

    def set_pos(self, pos):
        self.pos = pos

    def lem(self):
        l = WordNetLemmatizer()
        pre = self.nltk_tag_to_wordnet_tag(self.pos)
        if pre: return l.lemmatize(self.text, pos=pre)
        return None

        # function to convert nltk tag to wordnet tag
    def nltk_tag_to_wordnet_tag(self, nltk_tag):
        print(nltk_tag)
        if nltk_tag[1].startswith('J'):
            return wordnet.ADJ
        elif nltk_tag[1].startswith('V'):
            return wordnet.VERB
        elif nltk_tag[1].startswith('N'):
            return wordnet.NOUN
        elif nltk_tag[1].startswith('R'):
            return wordnet.ADV
        else:
            return None

    def __repr__(self):
        return str(self.text)

class Sentence:
    def __init__(self, text):
        self.text = text
        self.tokens = self.parts_of_speech()
        self.chunking()
        self.named_ents = self.named_entity()

    def named_entity(self):
        #nltk.ne_chunk(self.tags).draw()
        return nltk.ne_chunk(self.tags)

    def chunking(self):
        chunk_rule = ChunkRule("<.*>+", "Chunk everything")
        chink_rule = ChinkRule("<VBD|IN|\.>", "Chink on verbs/prepositions")
        split_rule = SplitRule("<DT><NN>", "<DT><NN>", "Split successive determiner/noun pairs")

        chunk_parser = RegexpChunkParser([chunk_rule], chunk_label='NP')
        chunked_text = chunk_parser.parse(self.tags)
        print(chunked_text)

    def parts_of_speech(self):
        tags = nltk.pos_tag(word_tokenize(self.text))
        self.tags = tags
        return [Token(t[0],t) for t in tags]

        '''
        POS Tags

        CC coordinating conjunction
        CD cardinal digit
        DT determiner
        EX existential there (like: "there is" ... think of it like "there exists")
        FW foreign word
        IN preposition/subordinating conjunction
        JJ adjective 'big'
        JJR adjective, comparative 'bigger'
        JJS adjective, superlative 'biggest'
        LS list marker 1)
        MD modal could, will
        NN noun, singular 'desk'
        NNS noun plural 'desks'
        NNP proper noun, singular 'Harrison'
        NNPS proper noun, plural 'Americans'
        PDT predeterminer 'all the kids'
        POS possessive ending parent's
        PRP personal pronoun I, he, she
        PRP$ possessive pronoun my, his, hers
        RB adverb very, silently,
        RBR adverb, comparative better
        RBS adverb, superlative best
        RP particle give up
        TO to go 'to' the store.
        UH interjection errrrrrrrm
        VB verb, base form take
        VBD verb, past tense took
        VBG verb, gerund/present participle taking
        VBN verb, past participle taken
        VBP verb, sing. present, non-3d take
        VBZ verb, 3rd person sing. present takes
        WDT wh-determiner which
        WP wh-pronoun who, what
        WP$ possessive wh-pronoun whose
        WRB wh-abverb where, when
        '''

    def __repr__(self):
        p = ''
        for t in self.tokens:
            p += str(t) + ' '
        p += '\n\n'
        for t in self.tokens:
            p += str(t.pos) + ' | '
        p += '\n\n'
        return p

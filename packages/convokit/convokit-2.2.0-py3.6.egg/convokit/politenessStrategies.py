"""Politeness Strategies features
See Section 4 of http://www.cs.cornell.edu/~cristian/Conversations_gone_awry.html
"""

import numpy as np
import pandas as pd

from collections import defaultdict

from .politeness_api.features.politeness_strategies import get_politeness_strategy_features
from .politeness_api.features.vectorizer import get_unigrams_and_bigrams

from .transformer import Transformer

class PolitenessStrategies(Transformer):
    """
    Encapsulates extraction of politeness strategies from utterances in a
    Corpus.

    :param verbose: whether or not to print status messages while computing features

    :ivar corpus: the PolitenessStrategies object's corpus
    """

    def __init__(self, verbose=False):
        self.ATTR_NAME = "politeness_strategies"
        self.verbose = verbose

    def transform(self, corpus):
        """Extract politeness strategies from each utterances in the corpus and annotate
        the utterances with the extracted strategies. Requires that the corpus has previously
        been transformed by a Parser, such that each utterance has dependency parse info in
        its metadata table.
        
        :param corpus: the corpus to compute features for.
        :type corpus: Corpus
        """
        
        if "parsed" not in corpus.meta_index["utterances-index"]:
            raise RuntimeError("Cannot extract politeness strategies from a Corpus that has not been parsed. Run Parser.transform(corpus) before calling this function.")

        # preprocess the utterances in the format expected by the API
        if self.verbose: print("Preprocessing comments...")
        comment_ids, processed_comments = self._preprocess_utterances(corpus)

        # use the bundled politeness API to extract politeness features for each
        # preprocessed comment
        if self.verbose: print("Extracting politeness strategies...")
        feature_dicts = [get_politeness_strategy_features(doc) for doc in processed_comments]

        # add the extracted strategies to the utterance metadata
        for utt_id, strats in zip(comment_ids, feature_dicts):
            corpus.get_utterance(utt_id).meta[self.ATTR_NAME] = strats

        return corpus

    def _preprocess_utterances(self, corpus):
        """Convert each Utterance in the given Corpus into the representation expected
        by the politeness API. Assumes that the Corpus has already been parsed, so that
        each Utterance contains the `parsed` metadata entry
        
        :param corpus: the corpus to compute features for.
        :type corpus: Corpus
        """

        utt_ids = [] # keep track of the order in which we process the utterances, so we can join with the corpus at the end
        documents = []
        for i, utterance in enumerate(corpus.iter_utterances()):
            if self.verbose and i > 0 and (i % self.verbose) == 0:
                print("\t%03d" % i)
            utt_ids.append(utterance.id)
            doc = {"text": utterance.text, "sentences": [], "parses": []}
            # the politeness API goes sentence-by-sentence
            for sent in utterance.meta["parsed"].sents:
                doc["sentences"].append(sent.text)
                sent_parses = []
                pos = sent.start
                for tok in sent:
                    if tok.dep_ != "punct": # the politeness API does not know how to handle punctuation in parses
                        ele = "%s(%s-%d, %s-%d)"%(tok.dep_, tok.head.text, tok.head.i + 1 - pos, tok.text, tok.i + 1 - pos)
                        sent_parses.append(ele)
                doc["parses"].append(sent_parses)
            doc["unigrams"], doc["bigrams"] = get_unigrams_and_bigrams(doc)
            documents.append(doc)
        if self.verbose:
            print("Done!")
        return utt_ids, documents

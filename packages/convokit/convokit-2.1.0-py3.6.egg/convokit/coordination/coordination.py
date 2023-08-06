import pkg_resources
import re
from convokit.model import Corpus, User, Utterance
from collections import defaultdict
from typing import Callable, Tuple, List, Dict, Optional, Collection, Hashable, Union


from convokit.transformer import Transformer

CoordinationWordCategories = ["article", "auxverb", "conj", "adverb",
    "ppron", "ipron", "preps", "quant"]

class CoordinationScore(dict):
    """Encapsulates results of :func:`Coordination.score()` and
    :func:`Coordination.pairwise_scores()`.

    The simplest way to use it is as a dictionary mapping speakers to their
    scores:

    ::

        {
            speaker_1: { dictionary of scores by coordination marker },
            speaker_2: scores,
            ...
        }

    The keys are of the same types as the input: if a username was 
    passed in, the corresponding key will be a username, etc. For pairwise
    scores, the keys are tuples (speaker, target).

    There are also helper functions for filtering scores or getting aggregate
    scores:
    """
    def scores_for_marker(self, marker: str) -> Dict[Union[User, Hashable], float]:
        """Return a dictionary from speakers to their scores for just the given
        marker.
        
        :param marker: The marker to return scores for.
        """
        return {speaker: scores[marker] for speaker, scores in self.items()}

    def averages_by_user(self) -> Dict[Union[User, Hashable], float]:
        """Return a dictionary from speakers to the average of each speaker's
        marker scores."""
        return {speaker: sum(scores.values()) / len(scores)
            for speaker, scores in self.items()}

    def averages_by_marker(self, strict_thresh: bool=False) -> Dict[str, float]:
        """Return a dictionary mapping markers to the average coordination score
        on that marker.
        
        :param strict_thresh: Whether to only include users with all 8 marker
            scores. This corresponds to Aggregate 1 in the Echoes paper (see
            top).
        """
        self.precompute_aggregates()
        return self.a1_avg_by_marker if strict_thresh else self.avg_by_marker

    def aggregate(self, method: int=3) -> Optional[float]:
        """Return the aggregate coordination score.

        :param method: Can be 1, 2 or 3, corresponding to which aggregate method
            to use:

            - aggregate 1: average scores only over users with a score for each
              coordination marker.
            - aggregate 2: fill in missing scores for a user by using the group
              score for each missing marker. (assumes different people in a
              group coordinate the same way.)
            - aggregate 3: fill in missing scores for a user by using the
              average score over the markers we can compute coordination for for
              that user. (assumes a user coordinates the same way across
              different coordination markers.)
        """
        assert 1 <= method <= 3
        self.precompute_aggregates()
        if method == 1:
            return self.agg1
        elif method == 2:
            return self.agg2
        else:
            return self.agg3

    # helper functions
    def precompute_aggregates(self) -> None:
        a1_scores_by_marker = defaultdict(list)
        scores_by_marker = defaultdict(list)
        for speaker, scores in self.items():
            for cat, score in scores.items():
                scores_by_marker[cat].append(score)
                if len(scores) == len(CoordinationWordCategories):
                    a1_scores_by_marker[cat].append(score)
        do_agg2 = False
        if len(scores_by_marker) == len(CoordinationWordCategories):
            do_agg2 = True
            avg_score_by_marker = {cat: sum(scores) / len(scores) 
                for cat, scores in scores_by_marker.items()}
        agg1s, agg2s, agg3s = [], [], []
        for speaker, scoredict in self.items():
            scores = list(scoredict.values())
            if len(scores) >= 1:
                avg = sum(scores) / len(scores)
                agg3s.append(avg)
                if len(scores) == len(CoordinationWordCategories):
                    agg1s.append(avg)
                if do_agg2:
                    for cat in avg_score_by_marker:
                        if cat not in scoredict:
                            scores.append(avg_score_by_marker[cat])
                    agg2s.append(sum(scores) / len(scores))
        agg1 = sum(agg1s) / len(agg1s) if agg1s else None
        agg2 = sum(agg2s) / len(agg2s) if agg2s else None  
        agg3 = sum(agg3s) / len(agg3s) if agg3s else None

        a1_avg_by_marker = {cat: sum(scores) / len(scores)
            for cat, scores in a1_scores_by_marker.items()}
        avg_by_marker = {cat: sum(scores) / len(scores)
            for cat, scores in scores_by_marker.items()}
        self.precomputed_aggregates = True
        self.a1_avg_by_marker = a1_avg_by_marker
        self.avg_by_marker = avg_by_marker
        self.agg1 = agg1
        self.agg2 = agg2
        self.agg3 = agg3

class Coordination(Transformer):
    """Encapsulates computation of coordination-based features for a particular
    corpus.
    
    :param corpus: the corpus to compute features for.
    :type corpus: Corpus

    :ivar corpus: the coordination object's corpus. 

    Note: labeling method is slightly different from that used in the paper --
    we no longer match words occurring in the middle of other words and that
    immediately follow an apostrophe. Most notably, we no longer separately
    count the "all" in "y'all."
    """

    def __init__(self, **thresh):
        #self.corpus = corpus
        self.thresh = thresh
        self.corpus = None
        self.precomputed = False

    def fit(self, corpus: Corpus):
        """Learn coordination information for the given corpus."""
        self.corpus = corpus
        self.precompute()

    def transform(self, corpus: Corpus) -> Corpus:
        """Generate coordination scores for the corpus you called fit on."""
        if corpus != self.corpus:
            raise Exception("Coordination: must fit and transform on same corpus")
        if not self.precomputed:
            raise Exception("Must fit before calling transform")

        pair_scores = self.pairwise_scores(corpus, self.corpus.speaking_pairs(),
            **self.thresh)
        for (s, t), score in pair_scores.items():
            if "coord-score" not in self.corpus.get_user(s.name).meta:
                self.corpus.get_user(s.name).meta["coord-score"] = {}
            else:
                self.corpus.get_user(s.name).meta["coord-score"][t] = score

        return self.corpus

    def precompute(self) -> None:
        """Call this to run the time-consuming annotation process explicitly.
        For example, this lets you save the annotated coordination object as a
        pickle to cache the precomputation results."""

        if not self.precomputed:
            self.compute_liwc_reverse_dict()
            self.annot_liwc_cats()
            #self.compute_liwc_reverse_dict_old()
            #self.annot_liwc_cats_old()
            #for u in self.corpus.utterances.values():
            #    if u.liwc_categories != u.liwc_categories_old:
            #        print("TEXT:", u.text)
            #        print("NEW:", u.liwc_categories)
            #        print("OLD:", u.liwc_categories_old)
            #        diff = (u.liwc_categories - u.liwc_categories_old) | \
            #                (u.liwc_categories_old - u.liwc_categories)
            #        print("DIFF:", diff)
            #        for cat in diff:
            #            print(self.liwc_patterns[cat])
            #        #print(u.text, u.liwc_categories, u.liwc_categories_old)
            #        input()
            self.precomputed = True

    def score(self, corpus: Corpus, speakers: Collection[Union[User, Hashable]],
              group: Collection[Union[User, Hashable]], focus: str="speakers",
              speaker_thresh: int=0, target_thresh: int=3,
              utterances_thresh: int=0, speaker_thresh_indiv: int=0,
              target_thresh_indiv: int=0,
              utterances_thresh_indiv: int=0,
              utterance_thresh_func: Optional[Callable[[Tuple[Utterance, Utterance]], bool]]=None,
              split_by_attribs: Optional[List[str]]=None,
              speaker_attribs: Optional[Dict]=None, target_attribs: Optional[Dict]=None) -> CoordinationScore:
        """Computes the coordination scores for each speaker, given a set of
        speakers and a group of targets.

        :param corpus: Corpus to compute scores on
        :param speakers: A collection of usernames or user objects corresponding
            to the speakers we want to compute scores for.
        :param group: A collection of usernames or user objects corresponding to
            the group of targets.
        :param focus: Either "speakers" or "targets". If "speakers", treat the
            set of targets for a particular speaker as a single person (i.e.
            concatenate all of their utterances); the returned dictionary will
            have speakers as keys. If "targets", treat the set of
            speakers for a particular target as a single person; the returned
            dictionary will have targets as keys.
        :param speaker_thresh: Thresholds based on
            minimum number of times the speaker uses each coordination
            marker.
        :type speaker_thresh: int

        :param target_thresh: Thresholds based on
            minimum number of times the target uses each coordination
            marker.
        :type target_thresh: int
        :param utterances_thresh: Thresholds based on
            the minimum number of utterances for each speaker.
        :type utterances_thresh: int
        :param speaker_thresh_indiv: Like
            `speaker_thresh` but only considers the utterances
            between a speaker and a single target; thresholds whether the
            utterances for a single target should be considered for a
            particular speaker.
        :type speaker_thresh_indiv: int
        :param target_thresh_indiv: Like
            `target_thresh` but thresholds whether a single target's
            utterances should be considered for a particular speaker.
        :type target_thresh_indiv: int
        :param utterances_thresh_indiv: Like
            `utterances_thresh` but thresholds whether a single target's
            utterances should be considered for a particular speaker.
        :type utterances_thresh_indiv: int
        :param utterance_thresh_func: Optional utterance-level
            threshold function that takes in a speaker `Utterance` and
            the `Utterance` the speaker replied to, and returns a `bool`
            corresponding to whether or not to include the utterance in
            scoring.
        :type utterance_thresh_func: function

        :type split_by_attribs: list
        :param split_by_attribs: Utterance meta attributes to split users by
            when tallying coordination (e.g. in supreme court transcripts,
            you may want to treat the same lawyer as a different person across
            different cases --- see coordination examples)

        :type speaker_attribs: dict
        :param speaker_attribs: attribute names and values the speaker must have

        :type target_attribs: dict
        :param target_attribs: attribute names and values the target must have

        :return: A :class:`CoordinationScore` object corresponding to the
            coordination scores for each speaker.
        """
        if corpus != self.corpus:
            raise Exception("Coordination: must fit and score on same corpus")
        if not self.precomputed:
            raise Exception("Must fit before calling score")

        if split_by_attribs is None: split_by_attribs = []
        if speaker_attribs is None: speaker_attribs = dict()
        if target_attribs is None: target_attribs = dict()

        #self.precompute()
        speakers = set(speakers)
        group = set(group)

        # are we referring to speakers by name or user obj?
        any_speaker = next(iter(speakers))
        fine_grained_speakers = not isinstance(any_speaker, str)

        # are we referring to targets by name or user obj?
        any_target = next(iter(group))
        fine_grained_targets = not isinstance(any_target, str)

        utterances = []
        for u in self.corpus.utterances.values():
            speaker = u.user if fine_grained_speakers else u.user.name
            if speaker in speakers:
                if u.reply_to is not None:
                    reply_to = self.corpus.utterances[u.reply_to]
                    target = reply_to.user if fine_grained_targets else \
                        reply_to.user.name
                    if target in group:
                        utterances.append(u)
        return self.scores_over_utterances(speakers, utterances,
            speaker_thresh, target_thresh, utterances_thresh,
            speaker_thresh_indiv, target_thresh_indiv,
            utterances_thresh_indiv, utterance_thresh_func,
            fine_grained_speakers, fine_grained_targets, focus,
            split_by_attribs, speaker_attribs, target_attribs)

    def pairwise_scores(self, corpus: Corpus,
                        pairs: Collection[Tuple[Union[User, Hashable], Union[User, Hashable]]],
                        speaker_thresh: int=0, target_thresh: int=3,
                        utterances_thresh: int=0, speaker_thresh_indiv: int=0,
                        target_thresh_indiv: int=0, utterances_thresh_indiv: int=0,
                        utterance_thresh_func: Optional[Callable[[Tuple[Utterance, Utterance]], bool]]=None) -> CoordinationScore:
        """Computes all pairwise coordination scores given a collection of
        (speaker, target) pairs.
        
        :param corpus: Corpus to compute scores on
        :param pairs: collection of (speaker, target) pairs where
            each speaker and target can be either a username or a user
            object.
        :type pairs: Collection
        
        Also accepted: all threshold arguments accepted by :func:`score()`.

        :return: A :class:`CoordinationScore` object corresponding to the
            coordination scores for each (speaker, target) pair.
        """
        if corpus != self.corpus:
            raise Exception("Coordination: must fit and score on same corpus")
        if not self.precomputed:
            raise Exception("Must fit before calling score")

        pairs = set(pairs)
        any_speaker = next(iter(pairs))[0]
        if isinstance(any_speaker, str):
            pairs_utts = self.corpus.pairwise_exchanges(lambda x, y:
                (x.name, y.name) in pairs, user_names_only=True)
        else:
            pairs_utts = self.corpus.pairwise_exchanges(lambda x, y:
                (x, y) in pairs, user_names_only=False)
        all_scores = CoordinationScore()
        for (speaker, target), utterances in pairs_utts.items():
            scores = self.scores_over_utterances([speaker], utterances,
                speaker_thresh, target_thresh, utterances_thresh,
                speaker_thresh_indiv, target_thresh_indiv,
                utterances_thresh_indiv, utterance_thresh_func,
                not isinstance(speaker, str), not isinstance(target, str))
            for m in scores.values():
                all_scores[speaker, target] = m
        return all_scores

    def score_report(self, corpus: Corpus, scores: CoordinationScore):
        """Create a "score report" of aggregate scores given a score output
        produced by `score` or `pairwise_scores`.

        - aggregate 1: average scores only over users with a score for each
            coordination marker.
        - aggregate 2: fill in missing scores for a user by using the group
            score for each missing marker. (assumes different people in a group
            coordinate the same way.)
        - aggregate 3: fill in missing scores for a user by using the average
            score over the markers we can compute coordination for for that 
            user. (assumes a user coordinates the same way across different
            coordination markers.)

        :param corpus: Corpus to compute scores on
        :param scores: Scores to produce a report for.
        :type scores: CoordinationScore

        :return: A tuple (marker_a1, marker, agg1, agg2, agg3):

            - marker_a1 is a dictionary of aggregate scores by marker,
                using the scores only over users included in Aggregate 1.
            - marker is a dictionary of aggregate scores by marker,
                using the scores of all users with a coordination score for
                that marker.
            - agg1, agg2 and agg3 are Aggregate 1, 2 and 3 scores respectively.

        """
        if corpus != self.corpus:
            raise Exception("Coordination: must fit and score on same corpus")
        if not self.precomputed:
            raise Exception("Must fit before calling score")

        marker_a1 = scores.averages_by_marker(strict_thresh=True)  
        marker = scores.averages_by_marker()
        agg1 = scores.aggregate(method=1)
        agg2 = scores.aggregate(method=2)
        agg3 = scores.aggregate(method=3)
        return (marker_a1, marker, agg1, agg2, agg3)

    # helper functions
    def compute_liwc_reverse_dict(self) -> None:
        with open(pkg_resources.resource_filename("convokit",
            "data/coord-liwc-patterns.txt"), "r") as f:
            all_words = []
            for line in f:
                cat, pat = line.strip().split("\t")
                #if cat == "auxverb": print(cat, pat)
                # use "#" to mark word boundary
                words = pat.replace("\\b", "#").split("|")
                all_words += [(w[1:], cat) for w in words]
            self.liwc_trie = Coordination.make_trie(all_words)

    @staticmethod
    def make_trie(words) -> Dict:
        root = {}
        for word, cat in words:
            cur = root
            for c in word:
                cur = cur.setdefault(c, {})
            if "$" not in cur:   # use "$" as end-of-word symbol
                cur["$"] = {cat}
            else:
                cur["$"].add(cat)
        return root

    def annot_liwc_cats(self) -> None:
        # add liwc_categories field to each utterance
        word_chars = set("abcdefghijklmnopqrstuvwxyz0123456789_")
        for k, u in self.corpus.utterances.items():
            cats = set()
            last = None
            cur = None
            text = u.text.lower() + " "
            #if "'" in text: print(text)
            for i, c in enumerate(text):
                # slightly different from regex: won't match word after an
                #   apostrophe unless the apostrophe starts the word
                #   -- avoids false positives
                if last not in word_chars and c in word_chars and (last != "'"
                    or not cur):
                    cur = self.liwc_trie
                if cur:
                    if c in cur and c != "#" and c != "$":
                        if c not in word_chars:
                            if "#" in cur and "$" in cur["#"]:
                                cats |= cur["#"]["$"]  # finished current word
                        cur = cur[c]
                    elif c not in word_chars and last in word_chars and \
                        "#" in cur:
                        cur = cur["#"]
                    else:
                        cur = None
                if cur and "$" in cur:
                    cats |= cur["$"]
                last = c
            self.corpus.utterances[k].meta["liwc-categories"] = cats

    def compute_liwc_reverse_dict_old(self) -> None:
        self.liwc_patterns = {}
        with open(pkg_resources.resource_filename("convokit",
            "data/coord-liwc-patterns.txt"), "r") as f:
            for line in f:
                cat, pat = line.strip().split("\t")
                self.liwc_patterns[cat] = re.compile(pat, re.IGNORECASE)

    def annot_liwc_cats_old(self) -> None:
        # add liwc_categories field to each utterance
        for k in self.corpus.utterances:
            self.corpus.utterances[k].liwc_categories_old = set()
        for cat in CoordinationWordCategories:
            pattern = self.liwc_patterns[cat]
            for k, u in self.corpus.utterances.items():
                s = re.search(pattern, u.text)
                if s is not None:
                    self.corpus.utterances[k].liwc_categories_old.add(cat)

    def scores_over_utterances(self, speakers: Collection[Union[User, Hashable]],
                               utterances: Collection[Utterance],
                               speaker_thresh: int, target_thresh: int,
                               utterances_thresh: int, speaker_thresh_indiv: int,
                               target_thresh_indiv: int, utterances_thresh_indiv: int,
                               utterance_thresh_func: Optional[Callable[[Tuple[Utterance, Utterance]], bool]]=None,
                               fine_grained_speakers: bool=False, fine_grained_targets: bool=False,
                               focus: str="speakers",
                               split_by_attribs: Optional[List[str]]=None,
                               speaker_attribs: Optional[Dict]=None,
                               target_attribs: Optional[Dict]=None) -> CoordinationScore:
        assert not isinstance(speakers, str)
        assert focus == "speakers" or focus == "targets"

        if split_by_attribs is None: split_by_attribs = []
        if speaker_attribs is None: speaker_attribs = {}
        if target_attribs is None: target_attribs = {}

        def annot_user(user: User, ut: Utterance):
            return (user, tuple([ut.meta[attrib] if attrib in ut.meta else None 
                for attrib in split_by_attribs]))

        m = self.corpus
        tally = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        cond_tally = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        cond_total = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        n_utterances = defaultdict(lambda: defaultdict(int))
        targets = defaultdict(set)

        real_speakers = set()
        for u2 in utterances:
            if u2.reply_to in m.utterances:
                speaker = u2.user if fine_grained_speakers else u2.user.name
                u1 = m.utterances[u2.reply_to]
                target = u1.user if fine_grained_targets else u1.user.name
                speaker, target = annot_user(speaker, u2), annot_user(target, u1)
                exclude = False
                for attrib in speaker_attribs:
                    if not u2.meta[attrib] == speaker_attribs[attrib]:
                        exclude = True
                for attrib in target_attribs:
                    if not u1.meta[attrib] == target_attribs[attrib]:
                        exclude = True
                if exclude: continue

                real_speakers.add(speaker)
                if speaker != target:
                    if utterance_thresh_func is None or \
                            utterance_thresh_func(u2, u1):
                        if focus == "targets": speaker, target = target, speaker
                        targets[speaker].add(target)
                        n_utterances[speaker][target] += 1
                        for cat in u1.meta["liwc-categories"] | u2.meta["liwc-categories"]:
                            if cat in u2.meta["liwc-categories"]:
                                tally[speaker][cat][target] += 1
                            if cat in u1.meta["liwc-categories"]:
                                cond_total[speaker][cat][target] += 1
                                if cat in u2.meta["liwc-categories"]:
                                    cond_tally[speaker][cat][target] += 1

        out = CoordinationScore()
        if focus == "targets":
            speaker_thresh, target_thresh = target_thresh, speaker_thresh
            speaker_thresh_indiv, target_thresh_indiv = \
                target_thresh_indiv, speaker_thresh_indiv
            real_speakers = targets.keys()
        for speaker in real_speakers:
            if speaker[0] not in speakers and not focus == "targets": continue
            coord_w = {}  # coordination score wrt a category
            for cat in CoordinationWordCategories:
                threshed_cond_total = 0
                threshed_cond_tally = 0
                threshed_tally = 0
                threshed_n_utterances = 0
                for target in targets[speaker]:
                    if tally[speaker][cat][target] >= speaker_thresh_indiv and \
                        cond_total[speaker][cat][target] >= \
                        target_thresh_indiv and \
                        n_utterances[speaker][target] >= \
                        utterances_thresh_indiv:
                        threshed_cond_total += cond_total[speaker][cat][target]
                        threshed_cond_tally += cond_tally[speaker][cat][target]
                        threshed_tally += tally[speaker][cat][target]
                        threshed_n_utterances += n_utterances[speaker][target]
                if threshed_cond_total >= max(target_thresh, 1) and \
                    threshed_tally >= speaker_thresh and \
                    threshed_n_utterances >= max(utterances_thresh, 1):
                    coord_w[cat] = threshed_cond_tally / threshed_cond_total - \
                            threshed_tally / threshed_n_utterances
            if len(coord_w) > 0:
                out[speaker if split_by_attribs else speaker[0]] = coord_w
        return out

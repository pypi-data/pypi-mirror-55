
from typing import Dict, List, Collection, Hashable, Callable, Set, Generator, Tuple, Optional, ValuesView
import pickle
import numpy as np
import pandas as pd
from collections import defaultdict
import json
import os
from .user import User
from .utterance import Utterance
from .conversation import Conversation

def warning(text: str):
	# Pre-pends a red-colored 'WARNING: ' to [text].
	# :param text: Warning message
	# :return: 'WARNING: [text]'
	return '\033[91m'+ "WARNING: " + '\033[0m' + text

pair_delim = '-q-a-'

KeyId = "id"
KeyUser = "user"
KeyConvoRoot = "root"
KeyReplyTo = "reply-to"
KeyTimestamp = "timestamp"
KeyText = "text"
DefinedKeys = {KeyId, KeyUser, KeyConvoRoot, KeyReplyTo, KeyTimestamp, KeyText}
KeyMeta = "meta"

BIN_DELIM_L, BIN_DELIM_R = "<##bin{", "}&&@**>"

class Corpus:
	"""Represents a dataset, which can be loaded from a folder or a
	list of utterances.
	"""

	def __init__(self, filename: Optional[str] = None, utterances: Optional[List[Utterance]] = None,
				 utterance_start_index: int = None, utterance_end_index: int = None, merge_lines: bool = False,
				 exclude_utterance_meta: Optional[List[str]] = None,
				 exclude_conversation_meta: Optional[List[str]] = None,
				 exclude_user_meta: Optional[List[str]] = None,
				 exclude_overall_meta: Optional[List[str]] = None,
				 version: Optional[int] = None):
		"""

		:param filename: Path to a folder containing a Corpus or to an utterances.jsonl / utterances.json file to load
		:param utterances: List of utterances to initialize Corpus from
		:param utterance_start_index: For utterances.jsonl, specify the line number (zero-indexed) to begin parsing utterances from
		:param utterance_end_index: For utterances.jsonl, specify the line number (zero-indexed) of the last utterance to be parsed.
		:param merge_lines: whether to merge adjacent lines from same user if the two utterances have same root
		:param exclude_utterance_meta: utterance metadata to be ignored
		:param exclude_conversation_meta: conversation metadata to be ignored
		:param exclude_user_meta: user metadata to be ignored
		:param exclude_overall_meta: overall metadata to be ignored
		:param version: version no. of corpus
		"""


		if filename is None:
			self.original_corpus_path = None
		elif os.path.isdir(filename):
			self.original_corpus_path = filename
		else:
			self.original_corpus_path = os.path.dirname(filename)
		self.meta = {}
		self.meta_index = {}

		self.vector_reprs = {}
		
		convos_meta = defaultdict(dict)
		if exclude_utterance_meta is None: exclude_utterance_meta = []
		if exclude_conversation_meta is None: exclude_conversation_meta = []
		if exclude_user_meta is None: exclude_user_meta = []
		if exclude_overall_meta is None: exclude_overall_meta = []

		self.version = version if version is not None else 0

		if filename is not None:
			if os.path.isdir(filename):
				if os.path.exists(os.path.join(filename, 'utterances.jsonl')):
					with open(os.path.join(filename, 'utterances.jsonl'), 'r') as f:
						utterances = []
						if utterance_start_index is None: utterance_start_index = 0
						if utterance_end_index is None: utterance_end_index = float('inf')
						idx = 0
						for line in f:
							if utterance_start_index <= idx <= utterance_end_index:
								utterances.append(json.loads(line))
							idx += 1

				elif os.path.exists(os.path.join(filename, 'utterances.json')):
					with open(os.path.join(filename, "utterances.json"), "r") as f:
						utterances = json.load(f)

				if exclude_utterance_meta:
					for utt in utterances:
						for field in exclude_utterance_meta:
							del utt["meta"][field]

				with open(os.path.join(filename, "users.json"), "r") as f:
					users_meta = defaultdict(dict)
					for k, v in json.load(f).items():
						if k in exclude_user_meta: continue
						users_meta[k] = v
				with open(os.path.join(filename, "conversations.json"), "r") as f:
					for k, v in json.load(f).items():
						if k in exclude_conversation_meta: continue
						convos_meta[k] = v
				with open(os.path.join(filename, "corpus.json"), "r") as f:
					for k, v in json.load(f).items():
						if k in exclude_overall_meta: continue
						self.meta[k] = v
				with open(os.path.join(filename, "index.json"), "r") as f:
					self.meta_index = json.load(f)

				# load all processed text information, but don't load actual text. 
				# also checks if the index file exists.
				# try:
				#     with open(os.path.join(filename, "processed_text.index.json"), "r") as f:
				#         self.processed_text = {k: {} for k in json.load(f)}
				# except:
				#     pass

				if version is not None:
					if "version" in self.meta_index:
						if self.meta_index["version"] != version:
							raise warning("Requested version does not match file version")
						self.version = self.meta_index["version"]

				# unpack utterance meta
				for field, field_type in self.meta_index["utterances-index"].items():
					if field_type == "bin" and field not in exclude_utterance_meta:
						with open(os.path.join(filename, field + "-bin.p"), "rb") as f:
							l_bin = pickle.load(f)
						for i, ut in enumerate(utterances):
							for k, v in ut[KeyMeta].items():
								if k == field and type(v) == str and v.startswith(BIN_DELIM_L) and \
										v.endswith(BIN_DELIM_R):
									idx = int(v[len(BIN_DELIM_L):-len(BIN_DELIM_R)])
									utterances[i][KeyMeta][k] = l_bin[idx]
				for field in exclude_utterance_meta:
					del self.meta_index["utterances-index"][field]

				# unpack user meta
				for field, field_type in self.meta_index["users-index"].items():
					if field_type == "bin" and field not in exclude_utterance_meta:
						with open(os.path.join(filename, field + "-user-bin.p"), "rb") as f:
							l_bin = pickle.load(f)
						for user, metadata in users_meta.items():
							for k, v in metadata.items():
								if k == field and type(v) == str and str(v).startswith(BIN_DELIM_L) and \
										str(v).endswith(BIN_DELIM_R):
									idx = int(v[len(BIN_DELIM_L):-len(BIN_DELIM_R)])
									metadata[k] = l_bin[idx]
				for field in exclude_user_meta:
					del self.meta_index["users-index"][field]

				# unpack convo meta
				for field, field_type in self.meta_index["conversations-index"].items():
					if field_type == "bin" and field not in exclude_utterance_meta:
						with open(os.path.join(filename, field + "-convo-bin.p"), "rb") as f:
							l_bin = pickle.load(f)
							
						for convo_id, convo_meta in convos_meta.items():
							for k, v in convo_meta.items():
								if k == field and type(v) == str and str(v).startswith(BIN_DELIM_L) and \
										str(v).endswith(BIN_DELIM_R):
									idx = int(v[len(BIN_DELIM_L):-len(BIN_DELIM_R)])
									convo_meta[k] = l_bin[idx]

				for field in exclude_conversation_meta:
					del self.meta_index["conversations-index"][field]

				# unpack overall meta
				for field, field_type in self.meta_index["overall-index"].items():
					if field_type == "bin" and field not in exclude_utterance_meta:
						with open(os.path.join(filename, field + "-overall-bin.p"), "rb") as f:
							l_bin = pickle.load(f)
						for k, v in self.meta.items():
							if k == field and type(v) == str and v.startswith(BIN_DELIM_L) and \
									v.endswith(BIN_DELIM_R):
								idx = int(v[len(BIN_DELIM_L):-len(BIN_DELIM_R)])
								self.meta[k] = l_bin[idx]
				for field in exclude_overall_meta:
					del self.meta_index["overall-index"][field]

			else:
				users_meta = defaultdict(dict)
				convos_meta = defaultdict(dict)
				with open(filename, "r") as f:
					try:
						ext = filename.split(".")[-1]
						if ext == "json":
							utterances = json.load(f)
						elif ext == "jsonl":
							utterances = []
							if utterance_start_index is None: utterance_start_index = 0
							if utterance_end_index is None: utterance_end_index = float('inf')
							idx = 0
							for line in f:
								if utterance_start_index <= idx <= utterance_end_index:
									utterances.append(json.loads(line))
								idx += 1
					except Exception as e:
						raise Exception("Could not load corpus. Expected json file, encountered error: \n" + str(e))

			self.utterances = dict()
			self.all_users = dict()

			for i, u in enumerate(utterances):

				u = defaultdict(lambda: None, u)
				user_key = u[KeyUser]
				if user_key not in self.all_users:
					self.all_users[user_key] = User(name=u[KeyUser], meta=users_meta[u[KeyUser]])

				user = self.all_users[user_key]

				# temp fix for reddit reply_to
				if "reply_to" in u:
					reply_to_data = u["reply_to"]
				else:
					reply_to_data = u[KeyReplyTo]

				ut = Utterance(id=u[KeyId], user=user,
							   root=u[KeyConvoRoot],
							   reply_to=reply_to_data, timestamp=u[KeyTimestamp],
							   text=u[KeyText], meta=u[KeyMeta])
				self.utterances[ut.id] = ut
		elif utterances is not None:
			self.all_users = {u.user.name: u.user for u in utterances}
			self.utterances = {u.id: u for u in utterances}

		if merge_lines:
			new_utterances = {}
			for uid, u in self.utterances.items():
				merged = False
				if u.reply_to is not None and u.user is not None:
					u0 = self.utterances[u.reply_to]
					if u0.root == u.root and u0.user == u.user:
						new_utterances[u0.id].text += " " + u.text
						merged = True
				if not merged:
					new_utterances[u.id] = u
			self.utterances = new_utterances

		# organize utterances by conversation
		convo_to_utts = defaultdict(list) # temp container identifying utterances by conversation
		for u in self.utterances.values():
			convo_key = u.root # each root is considered a separate conversation
			convo_to_utts[convo_key].append(u.id)
		self.conversations = {}
		for convo_id in convo_to_utts:
			# look up the metadata associated with this conversation, if any
			convo_meta = convos_meta.get(convo_id, None)
			convo = Conversation(self, id=convo_id,
								 utterances=convo_to_utts[convo_id],
								 meta=convo_meta)
			self.conversations[convo_id] = convo

		self.update_users_data()

	@staticmethod
	def dump_helper_bin(d: Dict, d_bin: Dict, utterances_idx: Dict, fields_to_skip=[]) -> Dict:
		"""

		:param d: The dict to encode
		:param d_bin: The dict of accumulated lists of binary attribs
		:param utterances_idx:
		:return:
		"""
		d_out = {}
		for k, v in d.items():
			if k in fields_to_skip: continue
			try:   # try saving the field
				json.dumps(v)
				d_out[k] = v
				if k not in utterances_idx:
					utterances_idx[k] = str(type(v))
			except (TypeError, OverflowError):   # unserializable
				d_out[k] = "{}{}{}".format(BIN_DELIM_L, len(d_bin[k]), BIN_DELIM_R)
				d_bin[k].append(v)
				utterances_idx[k] = "bin"   # overwrite non-bin type annotation if necessary
		#print(l_bin)
		#pickle.dump(l_bin, f)
		return d_out

	def dump(self, name: str, base_path: Optional[str]=None, save_to_existing_path: bool=False, fields_to_skip={}) -> None:
		"""Dumps the corpus and its metadata to disk.

		:param name: name of corpus
		:param base_path: base directory to save corpus in (None to save to a default directory)
		:param save_to_existing_path: if True, save to the path you loaded the corpus from (supersedes base_path)
		:param fields_to_skip: a dictionary of {object type: list of attributes to omit when writing to disk}. object types can be one of "user", "utterance", "conversation", "corpus".
		"""
		dir_name = name
		if base_path is not None and save_to_existing_path:
			raise ValueError("Not allowed to specify both base_path and save_to_existing_path!")
		if save_to_existing_path and self.original_corpus_path is None:
			raise ValueError("Cannot use save to existing path on Corpus generated from utterance list!")
		if not save_to_existing_path:
			if base_path is None:
				base_path = os.path.expanduser("~/.convokit/")
				if not os.path.exists(base_path):
					os.mkdir(base_path)
				base_path = os.path.join(base_path, "saved-corpora/")
				if not os.path.exists(base_path):
					os.mkdir(base_path)
			dir_name = os.path.join(base_path, dir_name)
		else:
			dir_name = os.path.join(self.original_corpus_path, name)

		if not os.path.exists(dir_name):
			os.mkdir(dir_name)

		utterances_idx, users_idx, convos_idx, overall_idx = {}, {}, {}, {}

		with open(os.path.join(dir_name, "users.json"), "w") as f:
			d_bin = defaultdict(list)
			users = {u: Corpus.dump_helper_bin(self.get_user(u).meta, d_bin,
											   users_idx, fields_to_skip.get('user',[])) for u in self.get_usernames()}
			json.dump(users, f)

			for name, l_bin in d_bin.items():
				with open(os.path.join(dir_name, name + "-user-bin.p"), "wb") as f_pk:
					pickle.dump(l_bin, f_pk)

		with open(os.path.join(dir_name, "conversations.json"), "w") as f:
			d_bin = defaultdict(list)
			convos = {c: Corpus.dump_helper_bin(self.get_conversation(c).meta,
												d_bin, convos_idx, fields_to_skip.get('conversation', [])) for c in self.get_conversation_ids()}
			json.dump(convos, f)

			for name, l_bin in d_bin.items():
				with open(os.path.join(dir_name, name + "-convo-bin.p"), "wb") as f_pk:
					pickle.dump(l_bin, f_pk)

		with open(os.path.join(dir_name, "utterances.jsonl"), "w") as f:
			d_bin = defaultdict(list)

			for ut in self.iter_utterances():
				ut_obj = {
					KeyId: ut.id,
					KeyConvoRoot: ut.root,
					KeyText: ut.text,
					KeyUser: ut.user.name,
					KeyMeta: self.dump_helper_bin(ut.meta, d_bin, utterances_idx, fields_to_skip.get('utterance', [])),
					KeyReplyTo: ut.reply_to,
					KeyTimestamp: ut.timestamp
				}
				json.dump(ut_obj, f)
				f.write("\n")

			for name, l_bin in d_bin.items():
				with open(os.path.join(dir_name, name + "-bin.p"), "wb") as f_pk:
					pickle.dump(l_bin, f_pk)

		with open(os.path.join(dir_name, "corpus.json"), "w") as f:
			d_bin = defaultdict(list)
			meta_up = Corpus.dump_helper_bin(self.meta, d_bin, overall_idx, fields_to_skip.get('corpus', []))
			#            keys = ["utterances-index", "conversations-index", "users-index",
			#                "overall-index"]
			#            meta_minus = {k: v for k, v in overall_idx.items() if k not in keys}
			#            meta_up["overall-index"] = meta_minus
			json.dump(meta_up, f)
			for name, l_bin in d_bin.items():
				with open(os.path.join(dir_name, name + "-overall-bin.p"), "wb") as f_pk:
					pickle.dump(l_bin, f_pk)

		self.meta_index["utterances-index"] = utterances_idx
		self.meta_index["users-index"] = users_idx
		self.meta_index["conversations-index"] = convos_idx
		self.meta_index["overall-index"] = overall_idx
		self.meta_index["version"] = self.version

		with open(os.path.join(dir_name, "index.json"), "w") as f:
			json.dump(self.meta_index, f)

		# with open(os.path.join(dir_name, "processed_text.index.json"), "w") as f:
		#     json.dump(list(self.processed_text.keys()), f)

	def get_utterance_ids(self) -> List:
		return list(self.utterances.keys())

	def get_utterance(self, ut_id: Hashable) -> Utterance:
		return self.utterances[ut_id]

	def iter_utterances(self) -> Generator[Utterance, None, None]:
		for v in self.utterances.values():
			yield v

	def get_conversation_ids(self) -> List[str]:
		return list(self.conversations.keys())

	def get_conversation(self, cid: Hashable) -> Conversation:
		return self.conversations[cid]

	def iter_conversations(self) -> Generator[Conversation, None, None]:
		for v in self.conversations.values():
			yield v

	def filter_utterances_by(self, regular_kv_pairs: Optional[Dict]=None,
							 meta_kv_pairs: Optional[Dict]=None) -> None:
		"""
		Creates a subset of the utterances filtered by certain attributes. Irreversible.
		If the method is run again, it will filter the already filtered subset.
		Always takes the intersection of the specified key-pairs
		"""
		if regular_kv_pairs is None: regular_kv_pairs = dict()
		if meta_kv_pairs is None: meta_kv_pairs = dict()
		new_utterances = dict()

		regular_keys = list(regular_kv_pairs.keys())
		meta_keys = list(meta_kv_pairs.keys())
		for uid, utterance in self.utterances.items():
			meta_dict = utterance.meta
			regular = all(utterance.get(key) == regular_kv_pairs[key] for key in regular_keys)
			meta = all(meta_dict[key] == meta_kv_pairs[key] for key in meta_keys)
			if regular and meta:
				new_utterances[uid] = utterance

		self.utterances = new_utterances

	#    def earliest_n_utterances(self, n, uts=None):
	#        """Returns the first n utterances (ordered by time)."""
	#        if uts is None:
	#            uts = self.utterances
	#        uts = list(sorted(uts.values(), key=lambda u: u.timestamp))
	#        return uts[:n]

	def utterance_threads(self, prefix_len: Optional[int]=None,
						  suffix_len: int=0,
						  include_root: bool=True) -> Dict[Hashable, Dict[Hashable, Utterance]]:
		"""
		Returns dict of threads, where a thread is all utterances with the
		same root.

		:param prefix_len: if an integer n, only get the first n utterances
			of each thread (sorted by ascending timestamp value)
		:param suffix_len: if an integer n, only get the last n utterances
			of each thread (sorted by descending timestamp value)
		:param include_root: True if root utterance should be included in the utterance thread.
			If False, thread begins from top level comment.

		:return: Dictionary from thread root ids to threads, where a thread is
			itself a dictionary from utterance ids to utterances.
		"""
		threads = defaultdict(list)
		for ut in self.utterances.values():
			if include_root:
				threads[ut.root].append(ut)
			else:
				top_level_comment = ut.get("meta")["top_level_comment"]
				if top_level_comment is None: continue # i.e. this is a post (root) utterance
				threads[top_level_comment].append(ut)
		return {root: {utt.id: utt for utt in list(sorted(l,
														  key=lambda x: x.timestamp))[-suffix_len:prefix_len]}
				for root, l in threads.items()}

	def get_meta(self) -> Dict:
		return self.meta

	def add_meta(self, key: Hashable, value) -> None:
		self.meta[key] = value

	def iter_users(self, selector: Optional[Callable[[User], bool]]=None) -> Generator[User, None, None]:
		"""Get users in the dataset.

		:param selector: optional function that takes in a
			`User` and returns True to include the user in the
			resulting list, or False otherwise.

		:return: Set containing all users selected by the selector function,
			or all users in the dataset if no selector function was
			used.
		"""
		if selector is None:
			for user in self.all_users.values():
				yield user
		else:
			for user in self.all_users.values():
				if selector(user):
					yield user

	def get_user(self, name: str) -> User:
		return self.all_users[name]

	def get_usernames(self, selector: Optional[Callable[[User], bool]]=None) -> Set[str]:
		"""Get names of users in the dataset.

		:param selector: optional function that takes in a
			`User` and returns True to include the user's name in the
			resulting list, or False otherwise.

		:return: Set containing all user names selected by the selector
			function, or all user names in the dataset if no selector function
			was used.
		"""
		return set([u.name for u in self.iter_users(selector)])

	def speaking_pairs(self, selector: Optional[Callable[[User, User], bool]]=None,
					   user_names_only: bool=False) -> Set[Tuple]:
		"""Get all directed speaking pairs (a, b) of users such that a replies
			to b at least once in the dataset.

		:param selector: optional function that takes in
			a speaker user and a replied-to user and returns True to include
			the pair in the result, or False otherwise.
		:param user_names_only: if True, return just pairs of
			user names rather than user objects.
		:type user_names_only: bool

		:return: Set containing all speaking pairs selected by the selector
			function, or all speaking pairs in the dataset if no selector
			function was used.
		"""
		pairs = set()
		for u2 in self.utterances.values():
			if u2.user is not None and u2.reply_to is not None and u2.reply_to in self.utterances:
				u1 = self.utterances[u2.reply_to]
				if u1.user is not None:
					if selector is None or selector(u2.user, u1.user):
						pairs.add((u2.user.name, u1.user.name) if
								  user_names_only else (u2.user, u1.user))
		return pairs

	def pairwise_exchanges(self, selector: Optional[Callable[[User, User], bool]]=None,
						   user_names_only: bool=False) -> Dict[Tuple, List[Utterance]]:
		"""Get all directed pairwise exchanges in the dataset.

		:param selector: optional function that takes in a
			speaker user and a replied-to user and returns True to include
			the pair in the result, or False otherwise.
		:param user_names_only: if True, index conversations
			by user names rather than user objects.
		:type user_names_only: bool

		:return: Dictionary mapping (speaker, target) tuples to a list of
			utterances given by the speaker in reply to the target.
		"""
		pairs = defaultdict(list)
		for u2 in self.utterances.values():
			if u2.user is not None and u2.reply_to is not None:
				u1 = self.utterances[u2.reply_to]
				if u1.user is not None:
					if selector is None or selector(u2.user, u1.user):
						key = (u2.user.name, u1.user.name) if user_names_only else (u2.user, u1.user)
						pairs[key].append(u2)
		return pairs

	def iterate_by(self, iter_type: str,
				   is_utterance_question: Callable[[str], bool]) -> Generator[Tuple[str, str, str], None, None]:
		"""Iterator for utterances.

		Can give just questions, just answers or questions followed by their answers
		"""
		i = -1
		for utterance in self.utterances.values():
			if utterance.reply_to is not None:
				root_text = self.utterances[utterance.reply_to].text
				if is_utterance_question(root_text):
					i += 1
					if iter_type == 'answers':
						pair_idx = utterance.reply_to + pair_delim + str(utterance.id)
						yield utterance.id, utterance.text, pair_idx
						continue
					question = self.utterances[utterance.reply_to]
					pair_idx = str(question.id) + pair_delim + str(utterance.id)
					yield question.id, question.text, pair_idx
					if iter_type == 'both':
						pair_idx = utterance.reply_to + pair_delim + str(utterance.id)
						yield utterance.id, utterance.text, pair_idx

	@staticmethod
	def _merge_utterances(utts1: List[Utterance], utts2: List[Utterance], warnings: bool) -> ValuesView[Utterance]:
		"""
		Helper function for merge().

		Combine two collections of utterances into a single dictionary of Utterance id -> Utterance.

		If metadata of utterances in the two collections share the same key, but different values,
		the second collections' utterance metadata will be used.

		May mutate original collections of Utterances.

		Prints warnings when:
		1) Utterances with same id from this and other collection do not share the same data
		2) Utterance metadata has different values for the same key, and overwriting occurs

		:param utts1: First collection of Utterances
		:param utts2: Second collection of Utterances
		:param warnings: whether to print warnings when conflicting data is found.
		:return: ValuesView for merged set of utterances
		"""
		seen_utts = dict()

		# Merge UTTERANCE metadata
		# Add all the utterances from this corpus
		for utt in utts1:
			seen_utts[utt.id] = utt

		# Add all the utterances from the other corpus, checking for data sameness and updating metadata as appropriate
		for utt in utts2:
			if utt.id in seen_utts:
				prev_utt = seen_utts[utt.id]
				try:
					assert prev_utt.root == utt.root
					assert prev_utt.reply_to == utt.reply_to
					assert prev_utt.user == utt.user
					assert prev_utt.timestamp == utt.timestamp
					assert prev_utt.text == utt.text

					# other utterance metadata is ignored if data is not matched
					for key, val in utt.meta.items():
						if key in prev_utt.meta and prev_utt.meta[key] != val:
							if warnings: print(warning("Found conflicting values for Utterance {} for metadata key: {}. "
										  "Overwriting with other corpus's Utterance metadata.".format(utt.id, key)))
						prev_utt.meta[key] = val

				except AssertionError:
					if warnings: print(warning("Utterances with same id do not share the same data:\n" +
								  str(prev_utt) + "\n" +
								  str(utt) + "\n" +
								  "Ignoring second corpus's utterance."
								  ))
			else:
				seen_utts[utt.id] = utt

		return seen_utts.values()

	@staticmethod
	def _collect_user_data(utt_sets: Collection[Collection[Utterance]]) -> Tuple[Dict[str, Dict[Hashable, str]], Dict[str, Dict[Hashable, bool]]]:
		"""
		Helper function for merge().

		Iterates through the input set of utterances, to collect User data and metadata.

		Collect User metadata in another Dictionary indexed by User ID

		Track if conflicting user metadata is found in another dictionary

		:param utt_sets: Collections of collections of Utterances to extract Users from
		:return: user metadata and the corresponding tracker
		"""
		# Collect USER data and metadata
		# all_users_data = defaultdict(lambda: defaultdict(set))
		all_users_meta = defaultdict(lambda: defaultdict(str))
		all_users_meta_conflict = defaultdict(lambda: defaultdict(bool))
		for utt_set in utt_sets:
			for utt in utt_set:
				for meta_key, meta_val in utt.user.meta.items():
					curr = all_users_meta[utt.user][meta_key]
					if curr != meta_val:
						if curr != "":
							all_users_meta_conflict[utt.user][meta_key] = True
						all_users_meta[utt.user][meta_key] = meta_val

		return all_users_meta, all_users_meta_conflict

	@staticmethod
	def _update_corpus_user_data(new_corpus, all_users_meta: Dict, all_users_meta_conflict: Dict, warnings: bool) -> None:
		"""
		Helper function for merge().

		Update new_corpus's Users' data (utterance and conversation lists) and metadata

		Prints a warning if multiple values are found for any user's metadata key; latest user metadata is used

		:param all_users_meta: Dictionary indexed by User ID, containing the collected User metadata
		:param all_users_meta_conflict: Dictionary indexed by User ID, indicating if there were value conflicts for the associated meta keys
		:return: None (mutates the new_corpus's Users)
		"""
		# Update USER data and metadata with merged versions
		for user in new_corpus.iter_users():
			for meta_key, meta_val in all_users_meta[user].items():
				if all_users_meta_conflict[user][meta_key]:
					if warnings: print(warning("Multiple values found for {} for meta key: {}. "
								  "Taking the latest one found".format(user, meta_key)))
				user.meta[meta_key] = meta_val

	def merge(self, other_corpus, warnings: bool = True):
		"""
		Merges this corpus with another corpus.

		Utterances with the same id must share the same data, otherwise the other corpus utterance data & metadata
		will be ignored. A warning is printed when this happens.

		If metadata of this corpus (or its conversations / utterances) shares a key with the metadata of the
		other corpus, the other corpus's metadata (or its conversations / utterances) values will be used. A warning
		is printed when this happens.

		May mutate original and other corpus.

		:param other_corpus: Corpus
		:param warnings: print warnings when data conflicts are encountered
		:return: new Corpus constructed from combined lists of utterances
		"""
		utts1 = list(self.iter_utterances())
		utts2 = list(other_corpus.iter_utterances())

		combined_utts = self._merge_utterances(utts1, utts2, warnings=warnings)
		new_corpus = Corpus(utterances=list(combined_utts))

		# Note that we collect Users from the utt sets directly instead of the combined utts, otherwise
		# differences in User meta will not be registered for duplicate Utterances (because utts would be discarded
		# during merging)
		all_users_meta, all_users_meta_conflict = self._collect_user_data([utts1, utts2])
		Corpus._update_corpus_user_data(new_corpus, all_users_meta, all_users_meta_conflict, warnings=warnings)

		# Merge CORPUS metadata
		new_corpus.meta = self.meta
		for key, val in other_corpus.meta.items():
			if key in new_corpus.meta and new_corpus.meta[key] != val:
				if warnings: print(warning("Found conflicting values for corpus metadata: {}. "
							  "Overwriting with other corpus's metadata.".format(key)))
			new_corpus.meta[key] = val

		# Merge CONVERSATION metadata
		convos1 = self.iter_conversations()
		convos2 = other_corpus.iter_conversations()

		for convo in convos1:
			new_corpus.get_conversation(convo.id).meta = convo.meta

		for convo in convos2:
			for key, val in convo.meta.items():
				curr_meta = new_corpus.get_conversation(convo.id).meta
				if key in curr_meta and curr_meta[key] != val:
					if warnings: print(warning("Found conflicting values for conversation: {} for meta key: {}. "
								  "Overwriting with other corpus's conversation metadata".format(convo.id, key)))
				curr_meta[key] = val

		new_corpus.update_users_data()

		return new_corpus

	def add_utterances(self, utterances=List[Utterance]):
		"""
		Add utterances to the Corpus

		If the corpus has utterances that share an id with an utterance in the input utterance list,

		Warnings will be printed:
		- if the utterances with same id do not share the same data (added utterance is ignored)
		- added utterances' metadata have the same key but different values (added utterance's metadata will overwrite)

		:param utterances: Utterances to be added to the Corpus
		:return: a new Corpus with the utterances from this Corpus and the input utterances combined
		"""
		helper_corpus = Corpus(utterances=utterances)
		return self.merge(helper_corpus)

	def update_users_data(self) -> None:
		"""
		Updates the conversation and utterance lists of every User in the Corpus
		:return: None
		"""
		users_utts = defaultdict(list)
		users_convos = defaultdict(list)

		for utt in self.iter_utterances():
			users_utts[utt.user].append(utt)

		for convo in self.iter_conversations():
			for utt in convo.iter_utterances():
				users_convos[utt.user].append(convo)

		for user in self.iter_users():
			user.utterances = {utt.id: utt for utt in users_utts[user]}
			user.conversations = {convo.id: convo for convo in users_convos[user]}

	def print_summary_stats(self) -> None:
		"""
		Helper function for printing the number of Users, Utterances, and Conversations in this Corpus

		:return: None
		"""
		print("Number of Users: {}".format(len(self.all_users)))
		print("Number of Utterances: {}".format(len(self.utterances)))
		print("Number of Conversations: {}".format(len(self.conversations)))


	# def generate_metadata(self, corpus_type: str) -> None:
	#     """
	#     Updates the metadata of the User based on the corpus type according to pre-determined rules
	#     :param corpus_type: The type of Corpus, e.g. reddit, wikiconv
	#     :return: None
	#     """
	#     for user in self.iter_users():
	#         if corpus_type == "reddit":
	#             num_posts = sum(utt.root == utt.id for utt in user.iter_utterances())
	#             user.add_meta("num_posts", num_posts)
	#             user.add_meta("num_comments", len(user.get_utterance_ids()) - num_posts)


	def get_vect_repr(self, id, field):
		"""
			gets a vector representation stored under the name field, for an individual object with a particular id.

			:param id: id of object
			:param field: the name of the particular representation
			:return: a vector representation of object <id> 
		"""

		vect_obj = self.vector_reprs[field]
		try:
			idx = vect_obj['key_to_idx'][id]
			return vect_obj['vects'][idx]
		except:
			return None

	def set_vect_reprs(self, field, keys, vects):
		"""
			stores a matrix where each row is a vector representation of an object

			:param field: name of representation
			:param keys: list of object ids, where each entry corresponds to each row of the matrix
			:param vects: matrix of vector representations
			:return: None
		"""

		vect_obj = {'vects': vects, 'keys': keys}
		vect_obj['key_to_idx'] = {k: idx for idx, k in enumerate(vect_obj['keys'])}
		self.vector_reprs[field] = vect_obj

	@staticmethod
	def _load_jsonlist_to_dict(filename, index_key='id', value_key='value'):
		entries = {}
		with open(filename, 'r') as f:
			for line in f:
				entry = json.loads(line)
				entries[entry[index_key]] = entry[value_key]
		return entries

	@staticmethod
	def _dump_jsonlist_from_dict(entries, filename, index_key='id', value_key='value'):
		with open(filename, 'w') as f:
			for k, v in entries.items():
				json.dump({index_key: k, value_key: v}, f)
				f.write('\n')

	@staticmethod
	def _load_vectors(filename):
		vect_obj = {}
		with open(filename + '.keys') as f:
			vect_obj['keys'] = [x.strip() for x in f.readlines()]
		vect_obj['key_to_idx'] = {k: idx for idx, k in enumerate(vect_obj['keys'])}
		vect_obj['vects'] = np.load(filename + '.npy')
		return vect_obj

	@staticmethod
	def _dump_vectors(vect_obj, filename):
		with open(filename + '.keys', 'w') as f:
			f.write('\n'.join(vect_obj['keys']))
		np.save(filename, vect_obj['vects'])

	def load_info(self, obj_type, fields=[], dir_name=None):
		"""
			loads attributes of objects in a corpus from disk. 
			This function, along with dump_info, supports cases where a particular attribute is to be stored separately from the other corpus files, for organization or efficiency. These attributes will not be read when the corpus is initialized; rather, they can be loaded on-demand using this function.

			For each attribute with name <NAME>, will read from a file called info.<NAME>.jsonl, and load each attribute value into the respective object's .meta field.

			:param obj_type: type of object the attribute is associated with. can be one of "utterance", "user", "conversation".
			:param fields: a list of names of attributes to load. if empty, will load all attributes stored in the specified directory dir_name.
			:param dir_name: the directory to read attributes from. by default, or if set to None, will read from the directory that the Corpus was loaded from.
			:return: None
		"""

		if (self.original_corpus_path is None) and (dir_name is None):
			raise ValueError('must specify a directory to read from')
		if dir_name is None:
			dir_name = self.original_corpus_path
		
		if len(fields) == 0:
			fields = [x.replace('info.','').replace('.jsonl', '') for x in os.listdir(dir_name)
				if x.startswith('info')]

		for field in fields:
			# self.aux_info[field] = self._load_jsonlist_to_dict(
			#     os.path.join(dir_name, 'feat.%s.jsonl' % field))
			if obj_type == 'utterance':
				getter = self.get_utterance
			elif obj_type == 'user':
				getter = self.get_user
			elif obj_type == 'conversation':
				getter = self.get_conversation
			entries = self._load_jsonlist_to_dict(
				os.path.join(dir_name, 'info.%s.jsonl' % field))
			for k, v in entries.items():
				try:
					obj = getter(k)
					obj.set_info(field, v)
				except:
					continue

	def dump_info(self, obj_type, fields, dir_name=None):
		"""
			writes attributes of objects in a corpus to disk. 
			This function, along with load_info, supports cases where a particular attribute is to be stored separately from the other corpus files, for organization or efficiency. These attributes will not be read when the corpus is initialized; rather, they can be loaded on-demand using this function.
	
			For each attribute with name <NAME>, will write to a file called info.<NAME>.jsonl, where rows are json-serialized dictionaries structured as {"id": id of object, "value": value of attribute}.

			:param obj_type: type of object the attribute is associated with. can be one of "utterance", "user", "conversation".
			:param fields: a list of names of attributes to write to disk. 
			:param dir_name: the directory to write attributes to. by default, or if set to None, will read from the directory that the Corpus was loaded from.
			:return: None
		"""

		if (self.original_corpus_path is None) and (dir_name is None):
			raise ValueError('must specify a directory to write to')
		
		if dir_name is None:
			dir_name = self.original_corpus_path
		# if len(fields) == 0:
		#     fields = self.aux_info.keys()
		for field in fields:
			# if field not in self.aux_info:
			#     raise ValueError("field %s not in index" % field)
			if obj_type == 'utterance':
				iterator = self.iter_utterances()
			elif obj_type == 'user':
				iterator = self.iter_users()
			elif obj_type == 'conversation':
				iterator = self.iter_conversations()
			if obj_type == 'user':
				entries = {obj.name: obj.get_info(field) for obj in iterator}
			else:
				entries = {obj.id: obj.get_info(field) for obj in iterator}
			# self._dump_jsonlist_from_dict(self.aux_info[field],
			#     os.path.join(dir_name, 'feat.%s.jsonl' % field))
			self._dump_jsonlist_from_dict(entries, os.path.join(dir_name, 'info.%s.jsonl' % field))

	def load_vector_reprs(self, field, dir_name=None):
		"""
			reads vector representations of Corpus objects from disk.

			Will read matrices from a file called vect_info.<field>.npy and corresponding object IDs from a file called vect_info.<field>.keys,

			:param field: the name of the representation
			:param dir_name: the directory to read from; by default, or if set to None, will read from the directory that the Corpus was loaded from.
			:return: None
		"""

		if (self.original_corpus_path is None) and (dir_name is None):
			raise ValueError('must specify a directory to read from')
		if dir_name is None:
			dir_name = self.original_corpus_path

		self.vector_reprs[field] = self._load_vectors(
				os.path.join(dir_name, 'vect_info.' + field)
			)

	def dump_vector_reprs(self, field, dir_name=None):
		"""
			writes vector representations of Corpus objects to disk.

			Will write matrices to a file called vect_info.<field>.npy and corresponding object IDs to a file called vect_info.<field>.keys,

			:param field: the name of the representation to write to disk
			:param dir_name: the directory to write to. by default, or if set to None, will read from the directory that the Corpus was loaded from.
			:return: None
		"""

		if (self.original_corpus_path is None) and (dir_name is None):
			raise ValueError('must specify a directory to write to')
		
		if dir_name is None:
			dir_name = self.original_corpus_path

		self._dump_vectors(self.vector_reprs[field], os.path.join(dir_name, 'vect_info.' + field))

	def get_attribute_table(self, obj_type, attrs):
		"""
			returns a dataframe, indexed by the IDs of objects of `obj_type`, containing attributes of these objects.

			:param obj_type: the type of object to get attributes for. can be `'utterance'`, `'user'` or `'conversation'`.
			:param attrs: a list of names of attributes to get.
			:return: a Pandas dataframe of attributes.
		"""

		if obj_type == 'utterance':
			iterator = self.iter_utterances()
		elif obj_type == 'user':
			iterator = self.iter_users()
		elif obj_type == 'conversation':
			iterator = self.iter_conversations() 

		table_entries = []
		for obj in iterator:
			entry = {}
			if obj_type == 'user':
				entry['id'] = obj.name 
			else:
				entry['id'] = obj.id 
			for attr in attrs:
				entry[attr] = obj.get_info(attr)
			table_entries.append(entry)
		return pd.DataFrame(table_entries).set_index('id')

	def set_user_convo_info(self, user_id, convo_id, key, value):
		'''
			assigns user-conversation attribute `key` with `value` to user `user_id` in conversation `convo_id`.

			:param user_id: user
			:param convo_id: conversation
			:param key: name of attribute
			:param value: value of attribute
			:return: None
		'''

		user = self.get_user(user_id)
		if 'conversations' not in user.meta:
			user.meta['conversations'] = {}
		if convo_id not in user.meta['conversations']:
			user.meta['conversations'][convo_id] = {}
		user.meta['conversations'][convo_id][key] = value

	def get_user_convo_info(self, user_id, convo_id, key=None):
		'''
			retreives user-conversation attribute `key` for `user_id` in conversation `convo_id`.

			:param user_id: user
			:param convo_id: conversation
			:param key: name of attribute. if None, will return all attributes for that user-conversation.
			:return: attribute value
		'''

		user = self.get_user(user_id)
		if 'conversations' not in user.meta: return None
		if key is None:
			return user.meta['conversations'].get(convo_id,{})
		return user.meta['conversations'].get(convo_id,{}).get(key)


	def organize_user_convo_history(self, utterance_filter=None):
		'''
			For each user, pre-computes a list of all of their utterances, organized by the conversation they participated in. Annotates user with the following:
				* `n_convos`: number of conversations
				* `start_time`: time of first utterance, across all conversations
				* `conversations`: a dictionary keyed by conversation id, where entries consist of:
					* `idx`: the index of the conversation, in terms of the time of the first utterance contributed by that particular user (i.e., `idx=0` means this is the first conversation the user ever participated in)
					* `n_utterances`: the number of utterances the user contributed in the conversation
					* `start_time`: the timestamp of the user's first utterance in the conversation
					* `utterance_ids`: a list of ids of utterances contributed by the user, ordered by timestamp.
			In case timestamps are not provided with utterances, the present behavior is to sort just by utterance id. 
			
			:param utterance_filter: function that returns True for an utterance that counts towards a user having participated in that conversation. (e.g., one could filter out conversations where the user contributed less than k words per utterance)
		'''

		if utterance_filter is None:
			utterance_filter = lambda x: True
		else:
			utterance_filter = utterance_filter

		user_to_convo_utts = defaultdict(lambda: defaultdict(list))
		for utterance in self.iter_utterances():
			if not utterance_filter(utterance): continue

			user_to_convo_utts[utterance.user.name][utterance.root].append((utterance.id, utterance.timestamp))
		for user, convo_utts in user_to_convo_utts.items():
			for convo, utts in convo_utts.items():
				sorted_utts = sorted(utts, key=lambda x: (x[1], x[0]))
				self.set_user_convo_info(user, convo, 'utterance_ids', [x[0] for x in sorted_utts])
				self.set_user_convo_info(user, convo, 'start_time', sorted_utts[0][1])
				self.set_user_convo_info(user, convo, 'n_utterances', len(sorted_utts))
		for user in self.iter_users():
			try:
				user.set_info('n_convos', len(user.get_info('conversations')))
			except: 
				continue

			sorted_convos = sorted(user.get_info('conversations').items(), key=lambda x: (x[1]['start_time'], x[1]['utterance_ids'][0]))
			user.set_info('start_time', sorted_convos[0][1]['start_time'])
			for idx, (convo_id, _) in enumerate(sorted_convos):
				self.set_user_convo_info(user.name, convo_id, 'idx', idx)



	def get_user_convo_attribute_table(self, attrs):
		'''
			returns a table where each row lists a (user, convo) level aggregate for each attribute in attrs. 

			:param attrs: list of (user, convo) attribute names
			:return: dataframe containing all user,convo attributes.
		'''

		table_entries = []
		for user in self.iter_users():

			if 'conversations' not in user.meta: continue
			for convo_id, convo_dict in user.meta['conversations'].items():
				entry = {'id': '%s__%s' % (user.name, convo_id),
				'user': user.name, 'convo_id': convo_id,
				'convo_idx': convo_dict['idx']}

				for attr in attrs:
					entry[attr] = convo_dict.get(attr,None)
				table_entries.append(entry)
		return pd.DataFrame(table_entries).set_index('id')

	def get_full_attribute_table(self, user_convo_attrs, user_attrs=[], convo_attrs=[], user_suffix='__user', convo_suffix='__convo'):
		'''
			returns a table where each row lists a (user, convo) level aggregate for each attribute in attrs, along with user-level and conversation-level attributes; by default these attributes are suffixed with '__user' and '__convo' respectively. 

			:param user_convo_attrs: list of (user, convo) attribute names
			:param user_attrs: list of user attribute names
			:param convo_attrs: list of conversation attribute names
			:param user_suffix: suffix to append to names of user-level attributes
			:param convo_suffix: suffix to append to names of conversation-level attributes.
			:return: dataframe containing all attributes.
		'''

		uc_df = self.get_user_convo_attribute_table(user_convo_attrs)
		u_df = self.get_attribute_table('user', user_attrs)
		u_df.columns = [x + user_suffix for x in u_df.columns]
		c_df = self.get_attribute_table('conversation', convo_attrs)
		c_df.columns = [x + convo_suffix for x in c_df.columns]
		return uc_df.join(u_df, on='user').join(c_df, on='convo_id')



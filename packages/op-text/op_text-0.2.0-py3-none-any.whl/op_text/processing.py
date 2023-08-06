import csv
from torch import tensor
from torch.utils.data import Dataset

class DataProcessor:
	"""Processing class to convert text to model input parameters"""

	def __init__(self, tokenizer, max_seq_len):
		"""
		Parameters:
			- tokenizer : The correct tokenizer for the specific model type. Used to tokenizer input data
			- max_seq_len: int : The maximum number of tokens in an input sequence
		"""
		self.tokenizer = tokenizer
		self.max_seq_len = max_seq_len

	def __call__(self, text):
		"""Converts a string of text into model input parameters
		
		Parameters:
			- text : str : A string of text

		Returns:
			- input_ids : list<int> : Each entry corresponds to a 
			  word in the tokenizers dictionary. 0's indicate padding tokens
			  when the sequence did not contain enough token ids to fill out
			  the list to a length of max_seq_len.

			- input_mask : list<int> : Used to mask out padding tokens in
			  the input_ids of length max_seq_len. 1's correspond to tokens from 
			  the vocabulary present in the input sequence and 0's correspond to padding tokens.

			- segment_ids : list<int> : Used to differentiate between two different
			  sequences combined into one long sequence. Only single sequences are used in these
			  models so this is always a list of 0's of length max_seq_len.

			- positional_ids : list<int> : Used to tell the model the position of a input
			  token in the sequence. Is of length max_seq_len.

			Assuming max_seq_len=8 the output and an 
			input text of "The man dropped his wallet" the
			input parameters for the model would look something
			like this:

			input_params={
				input_ids : [ 100, 51, 21952, 10, 354, 0, 0, 0],
				input_mask : [1, 1, 1, 1, 1, 0, 0, 0],
				segment_ids : [0, 0, 0, 0, 0, 0, 0, 0],
				positional_ids : [0, 1, 2, 3, 4, 5, 6, 7]
			}
		"""

		# Tokenize text and but discard tokens after max_seq_len - 2 to allow cls and sep token
		# to be appened to the sequence.
		input_tokens = self.tokenizer.tokenize(text)[:self.max_seq_len - 2]

		# Append cls and sep tokens
		input_tokens = [self.tokenizer.cls_token] + input_tokens + [self.tokenizer.sep_token]

		# Convert string tokens to integer tokens
		input_ids = self.tokenizer.convert_tokens_to_ids(input_tokens)

		# Generate padding mask for input tokens
		input_mask = [1] * len(input_ids)
		
		# Pad input ids and mask to max seq length  
		while len(input_ids) < self.max_seq_len:
			input_ids.append(0)
			input_mask.append(0)

		# Generate segment and positional ids
		segment_ids = [0] * len(input_ids)
		positional_ids = list(range(len(input_ids)))

		return input_ids, segment_ids, input_mask, positional_ids


class DataFetcher(Dataset):
	"""Retrieves and preprocesses samples for a PyTorch Dataloader"""

	def __init__(self, data, tokenizer, max_seq_len, rtn_seg_pos=True, labels=None):
		"""
		Parameters:
			- data : list<str> : List of strings that will be used as the inputs to the models
			- tokenizer : The correct tokenizer for the specific model type. Used to tokenizer input data
			- max_seq_len : int : Maximum length of an input sequence
			- rtn_seg_pos : bool : Whether to include segment and position ids in samples
			- labels : list<int> : List of integers that will be used as the class labels for inputs
		"""
		self.data = data
		self.data_processor = DataProcessor(tokenizer, max_seq_len)
		self.rtn_seg_pos = rtn_seg_pos
		self.labels = labels

	def __len__(self):
		"""Denotes the total number of samples"""
		return len(self.data)

	def __getitem__(self, index):
		"""Retrieves a single sample of data
		
		Parameters:
			- index : int : index of sample in the dataset

		Returns:
			- sample : dict : The input parameters for the model
		"""
		text = self.data[index]
		input_ids, segment_ids, input_mask, positional_ids = self.data_processor(text)

		# Convert all input parameters to tensors
		# and add them to a dictionary
		sample = {}
		sample["input_ids"] = tensor(input_ids)
		sample["attention_mask"] = tensor(input_mask)
		if self.rtn_seg_pos:
			sample["token_type_ids"] = tensor(segment_ids)
			sample["position_ids"] = tensor(positional_ids)
		if self.labels:
			sample["labels"] = tensor(self.labels[index])

		return sample
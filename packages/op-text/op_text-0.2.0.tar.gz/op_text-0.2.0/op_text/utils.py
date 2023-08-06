from torch.nn import Softmax
from torch.utils.data import DataLoader
from pytorch_transformers.optimization import AdamW, WarmupLinearSchedule
from op_text.processing import DataFetcher


def setup_dataloader(data, labels, tokenizer, rtn_seg_pos, max_seq_len, batch_size, shuffle=False):
	"""Sets up an iterator used to retrieve batches of data
	
	Parameters:
		- data : list<str> : List of strings that will be used as the inputs to the model
		- labels : list<int> : List of integers that will be used as the class labels for inputs
		- tokenizer : The correct tokenizer for the specific model type. Used to tokenizer input data
		- rtn_seg_pos : bool : Whether to include segment and position ids in samples
		- max_seq_len : int : Maximum length of an input sequence
		- batch_size : int : Number of samples in each mini batch
		- shuffle : bool : Whether to shuffle the data
	
	Returns:
		- dataloader : Iterator that returns batchs of data and labels 
	"""
	data_fetcher = DataFetcher(data, tokenizer, max_seq_len, rtn_seg_pos, labels)
	dataloader = DataLoader(data_fetcher, shuffle=shuffle, batch_size=batch_size)
	return dataloader


def setup_optim(named_params, learning_rate, adam_epsilon, warmup_steps, num_train_optim_steps):
	"""Sets up optimizer and scheduler for the model train loop
	
	Parameters:
		- named_params : List of models parameters
		- learning_rate : float : Between 0-1, recommended 3e-5
		- adam_epsilon : float : Between 0-1, recommended 1e-8
		- warmup_steps : int : Number training steps before regular learning is used
		- num_train_optim_steps : int : Total number of batches over all epochs

	Returns:
		- optimizer : AdamW Optimizer 
		- scheduler : WarmupLinearSchedule

	"""
	param_optimizer = list(named_params) # model.named_parameters()
	no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
	optimizer_grouped_parameters = [
		{'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
		{'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
	]
	optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate, eps=adam_epsilon)
	scheduler = WarmupLinearSchedule(optimizer, warmup_steps=warmup_steps, t_total=num_train_optim_steps)
	return optimizer, scheduler


def get_confidence_scores(logits):
	"""Convert raw model outputs to a probability distribution
	
	Parameters:
		- logits : Tensor : Raw outputs from model

	Returns:
		- Tensor : Probaility distribution that sums to 1
	"""
	return Softmax(dim=-1)(logits)


def calculate_accuracy(logits, labels):
	"""Calculates the number of correct predictions 
	
	Parameters:
		- logits : Tensor : Raw outputs from model
		- labels : List<int> : Ground truth labels

	Returns:
		- int : Number of labels the model correctly predicted
	"""
	_, pred_indices = get_confidence_scores(logits).max(-1)
	results = pred_indices == labels
	return results.sum().item()


class LabelConverter:
	"""Utility class used to convert prediction indices to text labels"""

	def __init__(self, converter_dict):
		"""
		Parameters:
			converter_dict : dictionary - Dictionary to convert indices to string labels
										  
			Example converter_dict:

				labels = {
					0: "Negative",
					1: "Postive"
				}


		"""
		self.converter = converter_dict

	def convert(self, indice):
		"""Converts a integer label to a string label 
		
		Parameters:
			- indice : int : Integer representation of a class label

		Returns:
			- label : str : String representation of a class label
		"""
		return self.converter[indice]

	def convert_indices(self, indices):
		"""Converts a list of integer labels to string labels
		
		Parameters:
			- indices : list<int> : List of integers

		Example Usage:
			int_labels = [0,1,0]
			convert_indices(int_labels) -> ["Negative", "Positive", "Negative"]

		"""
		return [self.convert(indice) for indice in indices]

	def __len__(self):
		"""Measure length of the label converter
		
		Returns:
			- int : Number of items in label converter
		"""
		return len(self.converter)

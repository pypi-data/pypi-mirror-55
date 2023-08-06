import os
import json
import torch

from pytorch_transformers.modeling_bert import BertConfig, BertForSequenceClassification
from pytorch_transformers.tokenization_bert import BertTokenizer

from pytorch_transformers.modeling_distilbert import DistilBertConfig, DistilBertForSequenceClassification
from pytorch_transformers.tokenization_distilbert import DistilBertTokenizer

from pytorch_transformers.modeling_roberta import RobertaConfig, RobertaForSequenceClassification
from pytorch_transformers.tokenization_roberta import RobertaTokenizer

from op_text.utils import setup_dataloader, setup_optim, get_confidence_scores, calculate_accuracy, LabelConverter

class TransformerModel:
	"""Base model class. Contains all attributes and functions to 
	train, evaluate and predict with models.
	"""

	def __init__(self, model_path, config_cls, tokenizer_cls, model_cls, downloadables, rtn_seg_pos, num_labels):
		"""
		Parameters:
			- model_path : str : Path to a local model directory on disk
			or the name of one of the models in the downloadables list

			- config_cls : Models specific config class
			- tokenizer_cls : Models specific tokenizer class 
			- model_cls : Models specific model class
			- downloadables : list<str> Pretrained models, available from PyTorch Transformers
			- rtn_seg_pos : bool : Whether to include segment and position ids in samples

			- num_labels : int : Number of class labels. This only needs to
			be provided if using one of the models in the downloadables
			list. Local models will already have this
		"""
		
		assert model_path in downloadables or os.path.isdir(model_path), ("model_path must be from either one of"
																		  f" {downloadables} or a path to the"
																		  " directory of a local model")

		self.config = config_cls.from_pretrained(model_path)
		if model_path in downloadables:
			self.config.num_labels = num_labels
		self.tokenizer = tokenizer_cls.from_pretrained(model_path)
		self.model = model_cls.from_pretrained(model_path)
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
		self.model.to(self.device)
		self.rtn_seg_pos = rtn_seg_pos


	def fit(self, X_train, y_train, validation_split=None,
			chkpt_model_every=None, model_save_dir=None, nb_epoch=1, batch_size=32,
			max_seq_len=128, learning_rate=3e-5, adam_epsilon=1e-8,
			warmup_steps=0, gradient_accumulation_steps=1, verbose=False, verbose_steps=1):
		"""Finetunes the model on a dataset for a number of epochs
		
		Parameters:
			- X_train : list<str> : List of strings that will be used as the inputs to the model
			- y_train : list<int> : List of integers that will be used as the class labels for inputs
			- validation_split : float : Between 0-1, amount of dataset to use as validation set

			- chkpt_model_every : int : Save the current version of the model at regular intervals
			each time this many epochs have been completed
			
			- model_save_dir : str : The directory to save each model checkpoint to
			- nb_epoch : int : Number of full passes of the dataset to train the model on
			- batch_size : int : Number of samples in each mini batch
			- max_seq_len : int : Maximum length of an input sequence
			- learning_rate : float : Between 0-1, recommended 3e-5
			- adam_epsilon : float : Between 0-1, recommended 1e-8
			- warmup_steps : int : Number training steps before regular learning is used

			- gradient_accumulation_steps : int : Accumulate gradient updates for this many batches.
			This is useful when not enough memory is present to use large batch sizes.

				An example of using gradient_accumulation_steps:

					A batch size of 32 is desired but not enough memory to hold the entire batch.
					Using a batch_size of 16 and gradient_accumulation_steps of 2 achieves the same 
					result. This will however take longer to train.

			-verbose : bool : Whether to print training information to the console
			-verbose_steps : int : Number of steps before training information is updated
		"""
		
		# If chkpt_model_every is used, this makes sure that it is an integer,
		# is greater than zero and the model_save_dir is existant.
		if chkpt_model_every:
			assert type(chkpt_model_every) == int, "@Param: 'chkpt_model_every' must be an integer"
			assert chkpt_model_every > 0, "@Param: 'chkpt_model_every' must be greater than zero"
			assert os.path.isdir(model_save_dir), (f"@Param: 'model_save_dir' == {model_save_dir}."
													" Directory does not exist"
													" Must supply an existing directory if @Param: "
													"'chkpt_model_every' is used")

		if verbose:
			assert type(verbose_steps) == int, "@Param: 'verbose steps' must be an integer" 
			assert verbose_steps > 0, "@Param: 'verbose_steps' must be a positive integer greater than 0"							

		if validation_split:
			assert validation_split > 0 and validation_split < 1, ("@Param: 'validation_split' =="
																  f" {validation_split} must be "
																  "a float between 0 and 1")

			split_percent = int(len(X_train) * (1 - validation_split))
			X_train = X_train[:split_percent]
			y_train = y_train[:split_percent]
			X_val = X_train[split_percent:]
			y_val = y_train[split_percent:]

		num_train_optim_steps = int(len(X_train) / batch_size) * nb_epoch
		optimizer, scheduler = setup_optim(self.model.named_parameters(), learning_rate, adam_epsilon, warmup_steps, num_train_optim_steps)
		train_dataloader = setup_dataloader(X_train, y_train, self.tokenizer, self.rtn_seg_pos, max_seq_len, batch_size, shuffle=True)


		self.model.zero_grad()
		self.model.train()
		tr_loss = 0
		for i in range(nb_epoch):
			step = 0
			train_accuracy = 0
			for batch in train_dataloader:
				batch = {k: t.to(self.device) for k, t in batch.items()}
				outputs = self.model(**batch)
				loss, logits = outputs[:2]
				loss.backward()
				train_accuracy += calculate_accuracy(logits, batch["labels"])

				if (step + 1) % gradient_accumulation_steps == 0:
					optimizer.step()
					scheduler.step()
					self.model.zero_grad()
				step += 1
				tr_loss += loss.item()

				batch = {k: t.detach().cpu() for k, t in batch.items()}
				del batch
				torch.cuda.empty_cache()

				if verbose and step % verbose_steps == 0:
					os.system('cls' if os.name == 'nt' else 'clear')
					print_str = (f"Current Epoch: {i + 1} \n"
								f"Steps Completed: {step}/{len(train_dataloader)} \n"
								f"Training Loss: {tr_loss/ ((i + 1) * (step * batch_size))} \n"
								f"Accuracy: {train_accuracy / (step * batch_size)}")
					print(print_str)

			
			validation_accuracy = None
			if validation_split:
				validation_accuracy = self.evaluate(X_val, y_val, max_seq_len, batch_size)
			
			if chkpt_model_every:
				if (i + 1) % chkpt_model_every == 0:
					results = {
						"train accuracy": train_accuracy / len(train_dataloader),
						"validation_accuracy": validation_accuracy,
						"train loss": tr_loss / ((i + 1) * len(train_dataloader))
					}
					chkpt_name = "chkpt epochs={0}".format(i + 1)
					self.save(model_save_dir, chkpt_name, results)

			
	def evaluate(self, X_test, y_test, batch_size=32, max_seq_len=128):
		"""Test the model on a dataset
		
		Parameters:
			- X_test : list<str> : List of strings that will be used as the inputs to the model
			- y_test : list<int> : List of integers that will be used as the class labels for inputs
			- batch_size : int : Number of samples in each mini batch
			- max_seq_len : int : Maximum length of an input sequence

		Returns:
			- accuracy : float : The percentage of samples that the model correctly predicted
			class labels for 	
		"""
		test_dataloader = setup_dataloader(X_test, y_test, self.tokenizer, self.rtn_seg_pos, max_seq_len, batch_size)
		accuracy = 0
		
		for batch in test_dataloader:
			with torch.no_grad():
				labels = batch["labels"].to(self.device)
				batch = {k: t.to(self.device) for k, t in batch.items() if k != "labels"}
				outputs = self.model(**batch)
				logits = outputs[0]
				accuracy += calculate_accuracy(logits, labels)
			
			batch = {k: t.detach().cpu() for k, t in batch.items()}
			del batch
			torch.cuda.empty_cache()

		accuracy = accuracy / len(test_dataloader)
		return accuracy


	def predict(self, data, label_converter=None, batch_size=32, max_seq_len=128):
		"""Use the model to predict the class labels of some data
		
		Parameters:
			- data : list<str> : List of strings that will be used as the inputs to the model
			- label_converter : LabelConverter : Used to convert integer labels to text labels 
			- batch_size : int : Number of samples in each mini batch
			- max_seq_len : int : Maximum length of an input sequence

		Returns:
			- predictions : list<tuple> : Each tuple is contains the confidence scores of the model,
			the integer label the predicted class and if the label_converter parameter is present, the
			string label of the predicted class
		"""
		if label_converter:
			assert type(label_converter) == LabelConverter, "@Param: 'label_converter' must be of Type: LabelConverter"
			assert len(label_converter) == self.config.num_labels, (f"@Param: 'label_coverter has length of {len(label_converter)}."
																	f"Must have same length as config.num_labels: {self.config.num_labels}")

		predictions_dataloader = setup_dataloader(data, None, self.tokenizer, self.rtn_seg_pos, max_seq_len, batch_size)
		predictions = []
		for batch in predictions_dataloader:
			with torch.no_grad():
				batch = {k: t.to(self.device) for k, t in batch.items()}
				outputs = self.model(**batch)
				logits = outputs[0]
				confidence_scores = get_confidence_scores(logits)
				pred_indices = confidence_scores.max(-1)[-1].tolist()
				preds = (confidence_scores.tolist(), pred_indices)
				if label_converter:
					preds =  preds + (label_converter.convert_indices(pred_indices),)
				predictions += list(zip(*preds))
				batch = {k: t.detach().cpu() for k, t in batch.items()}
				del batch
				torch.cuda.empty_cache()
		return predictions


	def save(self, output_dir, save_model_name, save_results=None):
		"""Saves the model to an specified directory
		
		Parameters:
			- output_dir : str : Path to the directory to save the model in
			- save_model_name : str : Name of the models save directory
			- save_results : dict : Results from training and testing
		"""

		assert os.path.isdir(output_dir), (f"@Param 'output_dir' == {output_dir}." 
										   " Directory does not exist.")

		save_path = os.path.join(output_dir, save_model_name)
		if not os.path.exists(save_path):
			os.mkdir(save_path)
			
		self.model.save_pretrained(save_path)
		self.tokenizer.save_pretrained(save_path)

		if save_results:
			fp = os.path.join(output_dir, save_model_name, "test_accuracy.json")
			json.dump(save_results, open(fp, 'w', encoding='utf-8'), indent=4)


class Bert(TransformerModel):
	"""Extension of TransformerModel class intializing with
	The Pytorch Transformers Bert implementation components. 
	"""

	DOWNLOADABLES = ['bert-base-uncased', 'bert-large-uncased']
	def __init__(self, model_path, num_labels=2):
		"""
		Parameters:
			- model_path : str : Path to a local model directory on disk
			or the name of one of the models in the Bert.DOWNLOADABLES list.

			- num_labels : int : Number of class labels. This only needs to
			be provided if using one of the models in the BERT.DOWNLOADABLES
			list. Local models will already have this.
		"""

		super().__init__(model_path, BertConfig, BertTokenizer, BertForSequenceClassification, Bert.DOWNLOADABLES, True, num_labels)


class Roberta(TransformerModel):
	"""Extension of TransformerModel class intializing with
	The Pytorch Transformers Roberta implementation components.
	"""

	DOWNLOADABLES = ['roberta-base', 'roberta-large']
	def __init__(self, model_path, num_labels=2):
		"""
		Parameters:
			- model_path : str : Path to a local model directory on disk
			or the name of one of the models in the Roberta.DOWNLOADABLES list.

			- num_labels : int : Number of class labels. This only needs to
			be provided if using one of the models in the Roberta.DOWNLOADABLES
			list. Local models will already have this.
		"""

		super().__init__(model_path, RobertaConfig, RobertaTokenizer, RobertaForSequenceClassification, Roberta.DOWNLOADABLES, True, num_labels)


class DistilBert(TransformerModel):
	"""Extension of TransformerModel class intializing with
	The Pytorch Transformers DistilBert implementation components.
	"""

	DOWNLOADABLES = ['distilbert-base-uncased']
	def __init__(self, model_path, num_labels=2):
		"""
		Parameters:
			- model_path : str : Path to a local model directory on disk
			or the name of one of the models in the DistilBert.DOWNLOADABLES list.

			- num_labels : int : Number of class labels. This only needs to
			be provided if using one of the models in the DistilBert.DOWNLOADABLES
			list. Local models will already have this.
		"""
		
		super().__init__(model_path, DistilBertConfig, DistilBertTokenizer, DistilBertForSequenceClassification, DistilBert.DOWNLOADABLES, False, num_labels)
	




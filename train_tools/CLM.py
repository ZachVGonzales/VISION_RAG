from transformers import DataCollatorForSeq2Seq
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
from transformers import TrainingArguments
from transformers import Trainer
from datasets import Dataset
import argparse


MODEL_NAME = "microsoft/Phi-3.5-mini-instruct"


def init():
  parser = argparse.ArgumentParser(prog="html.py", description="fine_tune model on unsupervised MLM task")
  parser.add_argument("hf_path", help="where the huggingface db is stored")
  parser.add_argument("model_path", help="path to saved model or NONE if none exists")
  return parser.parse_args()



if __name__ == "__main__":
  # init params:
  params = init()
  hf_path = params.hf_path
  model_path = params.model_path

  # Load the Phi 3.5 model and tokenizer
  if model_path == "NONE":
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
  else:
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)

  # Load the training dataset
  tokenized_mlm_dataset = Dataset.load_from_disk(hf_path)

  # Data collator for CLM
  clm_data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model
  )

  training_args = TrainingArguments(
    output_dir="./phi-3.5-finetuned",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    save_steps=10_000,
    logging_dir='./logs',
    logging_steps=200,
  )

  # MLM Training
  trainer_clm = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_mlm_dataset,
    data_collator=clm_data_collator,
    tokenizer=tokenizer,
  )

  trainer_clm.train()

  model.save_pretrained("./phi-3.5-finetuned")
  tokenizer.save_pretrained("./phi-3.5-finetuned")
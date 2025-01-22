from datasets import Dataset # type: ignore
from transformers import AutoTokenizer # type: ignore
import argparse
import sqlite3


def init():
  parser = argparse.ArgumentParser(prog="html.py", description="import html dir to FAISS file")
  parser.add_argument("db_path", help="path to sqlite .db file")
  parser.add_argument("hf_path", help="where the huggingface db should be stored")
  return parser.parse_args()


# Tokenization function
def tokenize_function(examples):
  return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=16000)
  

if __name__ == "__main__":
  params = init()
  db_path = params.db_path
  hf_path = params.hf_path

  connection = sqlite3.connect(db_path)
  c = connection.cursor()

  c.execute("SELECT content from paragraphs")
  rows = c.fetchall()
  data = [{"text": row[0]} for row in rows]

  c.execute("SELECT sentence from sentences")
  rows = c.fetchall()
  data += [{"text": row[0]} for row in rows]

  dataset = Dataset.from_list(data)

  tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
  tokenized_dataset = dataset.map(tokenize_function, batched=True)

  tokenized_dataset.save_to_disk(hf_path)
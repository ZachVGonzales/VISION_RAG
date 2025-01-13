"""
NAME: Zachary Gonzales
DATE: 01.05.2025

DESC: Import directory of HTML documents into A
sqlite3 file and then store said file in data dir
"""


from bs4 import BeautifulSoup # type: ignore
from requests_html import HTMLSession # type: ignore
from pathlib import Path
import argparse
import sqlite3
import nltk # type: ignore
nltk.download("punkt")
nltk.download('punkt_tab')


SENT_WC = 3


def init():
  parser = argparse.ArgumentParser(prog="html.py", description="import html dir to FAISS file")
  parser.add_argument("import_dir", help="name of import ")
  parser.add_argument("db_path", help="path to sqlite .db file")
  return parser.parse_args()


def split_paragraph(paragraph: str):
  sentences = nltk.sent_tokenize(paragraph)
  adj_sentences = [""]
  i = 0
  
  for sentence in sentences:
    adj_sentences[i] += sentence
    words = sentence.split(" ")
    if len(words) <= 1:
      adj_sentences[i] += " "
    else:
      adj_sentences.append("")
      i += 1

  if adj_sentences[-1] == "":
    adj_sentences.pop()
  
  return adj_sentences


def create_db(connection: sqlite3.Connection):
  c = connection.cursor()

  c.execute('''
            CREATE TABLE IF NOT EXISTS paragraphs (
                id INTEGER PRIMARY KEY,
                content TEXT
            )
            ''')

  c.execute('''
            CREATE TABLE IF NOT EXISTS sentences (
                id INTEGER PRIMARY KEY,
                paragraph_id INTEGER,
                sentence TEXT,
                FOREIGN KEY (paragraph_id) REFERENCES paragraphs(id)
            )
            ''')
  
  connection.commit()


def store(connection: sqlite3.Connection, sentences: list[str]):
  paragraph = " ".join(sentences)

  c = connection.cursor()
  c.execute('INSERT INTO paragraphs (content) VALUES (?)', (paragraph,))
  paragraph_id = c.lastrowid  # Get the id of the inserted paragraph

  for sentence in sentences:
    c.execute('INSERT INTO sentences (paragraph_id, sentence) VALUES (?, ?)', (paragraph_id, sentence))

  connection.commit()
  return True


if __name__ == "__main__":
  params = init()
  iDir = params.import_dir
  db_path = params.db_path
  session = HTMLSession()

  connection = sqlite3.connect(db_path)
  create_db(connection)

  # itter through all possible files (recursive)
  for file in Path(iDir).rglob("*"):

    # if file not valid skip
    if not (file.is_file() and file.suffix.lower() == '.html'):
      continue

    # otherwise process
    file_name = file.name
    print(f"-------------- Processing {file_name} --------------")
    
    file_url = "http://localhost:8000/" + file_name
    response = session.get(file_url)
    response.html.render()
    soup = BeautifulSoup(response.html.html, "html.parser")
    text_content = soup.get_text(separator=" ", strip=True)
    paragraphs = soup.find_all('p')
    prev_para = []
    
    for paragraph in paragraphs[::-1]:
      paragraph = paragraph.get_text(separator=' ', strip=True)
      words = paragraph.split(" ")

      if len(paragraph) <= SENT_WC or words[0] == "Navigation:":
        continue

      prev_para.insert(0, paragraph)
      sentences = split_paragraph(paragraph)
      
      
      if len(sentences) <= 1:
        continue
      else:
        store(connection, prev_para)
        prev_para = []
  
  connection.commit()
  connection.close()
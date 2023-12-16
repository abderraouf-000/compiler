import re;

def normalize_spaces(text):
     text = re.sub(r'\s*(\')\s*', r'\1', text);
     text = re.sub(r'\s*(=|:=|:|,|;|\*|\+|-|\.\.|\)|\(|\[|\])\s*', r' \1 ', text);
     text = re.sub(r'\s*(>=|<=|<|>|<>|end)\s*', r' \1 ', text);
     return text;
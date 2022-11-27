def print_big_list(x, cut = 30):
  if len(x) < 10:
    print(x)
  elif len(str(x)) < cut:
    print(x)
  else:
    text = str(x)
    print_text(text)
    
def print_text(x):
  words = x.split(', ')
  n = len(words)
  lengths = [len(word) for word in words]
  n_words_per_line = 4
  index = 0
  lines = list()
  while index < n:
    upper_limit = index + n_words_per_line
    text = words[index:upper_limit]
    text = ', '.join(text) + ',\n'
    lines.append(text)
    index = index + n_words_per_line
    
  text = ''.join(lines)
  print(text)

file_tm = 'cat/tests/data/TM_1k.csv'
file_glossary = 'cat/tests/data/Glossary_1K.csv'

from cat.models import TMContent, GlossaryContent, TranslationMemory, Glossary

import csv
t = TranslationMemory.objects.get(pk=3)
with open(file_tm, newline='') as csvfile:
  data = csv.reader(csvfile)
  for row in data:
    tm = TMContent(src_sentence=row[0], tar_sentence=row[1], translation_memory=t) 
    tm.save() 

glos = Glossary.objects.get(pk=2)
with open(file_glossary, newline='') as csvfile:
  data = csv.reader(csvfile)
  for row in data:
    g = GlossaryContent(src_phrase=row[0], tar_phrase=row[1], glossary=glos) 
    g.save() 


# Run it on shell :D
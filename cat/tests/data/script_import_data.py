path_to_file = 'cat/tests/data/1k.csv'


from cat.models import TMContent, GlossaryContent, TranslationMemory

import csv
t = TranslationMemory.objects.get(pk=1)
with open(path_to_file, newline='') as csvfile:
  data = csv.reader(csvfile)
  for row in data:
    b = TMContent(src_sentence=row[0], tar_sentence=row[1], translation_memory=t) 
    b.save() 


# open("cat/fixtures/initial_1k_data-new.yaml","wb").write(open("cat/fixtures/initial_1k_data.yaml").read().decode("unicode_escape"))

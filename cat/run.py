import sys
from django.conf import settings
import os

sys.path.append(os.path.join(settings.BASE_DIR,'preprocessing_python'))

print(sys.path)



# print(os.path.abspath)
from preprocessor import *
# # Khai báo đối tượng preprocessor cho tiếng Việt.
# # Khi khai báo, các file liên quan sẽ được nạp vào bộ nhớ.
p = Preprocessor(Language.vietnamese)
p.segment_files_to_sentences('kim.txt','kim_out.txt',{'overwrite': True})

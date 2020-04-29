# This is model for ocr
Contact bachquangtran98@gmail.com for more detail.
To use train.py:
  - Put your data to ./data
  - Put vocab.json to ./data
  - Data folder should have:
    - train.json = {'path_to_text_line_images_1': label1,
                     'path_to_text_line_images_2': label2}
    - images folder: contain textline images
 Test on SROIE dataset: 
  - acc_by_char ~ 98%
  - acc_by_word ~95% 

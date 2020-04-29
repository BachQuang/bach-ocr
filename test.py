import itertools

import torch
import numpy as np
import cv2

from ocr.data_loader.vocab import Vocab
from ocr.model.ctc_model import CTCModel
from ocr.data_loader.collate import process_image

class infer:
    def __init__(self, weights_path, vocab_path):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        # self.device = torch.device('cpu')
        self.voc = Vocab()
        self.voc.build_vocab_from_char_dict_file(vocab_path)
        self.model = CTCModel(self.voc.num_chars)
        self.model = self.model.to(self.device)

        # LOAD MODEL
        print("LOADING WEIGHTS ...")
        checkpoint = torch.load(weights_path, map_location=torch.device('cpu'))
        # print(checkpoint)
        state_dict = checkpoint['state_dict']
        self.model.load_state_dict(state_dict)

    def process(self, image):
        self.model.eval()
        # preprocess image, TODO: height = 64 (no need but to be more accurate)
        image = process_image(image)
        images = np.array([image])
        images = images.transpose((0, 3, 1, 2))
        images = torch.from_numpy(images).float()
        images = images.to(self.device)

        outputs = self.model(images)
        outputs = outputs.permute(1, 0, 2)
        output = outputs[0]

        out_best = list(torch.argmax(output, -1))  # [2:]
        out_best = [k for k, g in itertools.groupby(out_best)]
        pred_text = self.voc.get_label_from_indices(out_best)

        return pred_text, 1

if __name__ == "__main__":
    model = infer('./saved/models/OCR_test/0429_083602/checkpoint-epoch1.pth', './data/vocab.json')
    image = cv2.imread('./data/images/2_X51007103692.jpg')
    text, _ = model.process(image)
    print(text)

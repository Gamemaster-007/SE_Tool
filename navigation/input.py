import cv2
import numpy as np
import pyautogui
from tess2dict import TessToDict
td=TessToDict()

def convert_image(image):
    word_dict=td.tess2dict(image,'out','outfolder')
    word_dict.to_csv('outfolder/output.csv')
    text_plain=td.word2text(word_dict,(0,0,image.shape[1],image.shape[0]))
    print(text_plain,file=open('outfolder/output.txt','wt'))

if __name__ == '__main__':
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image),
                        cv2.COLOR_RGB2BGR)
    convert_image(image)
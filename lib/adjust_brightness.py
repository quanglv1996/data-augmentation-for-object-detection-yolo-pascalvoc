import torchvision.transforms.functional as F
import numpy as np
import cv2
from PIL import Image
from utils import draw_rect, get_info_bbox

class Adjust_Brightness(object):
    def __init__(self, brightness_factor=1.5):
        """
        Initialize the Adjust_Brightness augmentation class.

        Args:
            brightness_factor (float): Factor to adjust the brightness of the image. Default is 1.5.
        """
        # Store the provided brightness factor
        self.brightness_factor = brightness_factor
        
    def __call__(self, img, bboxes):
        """
        Apply the brightness adjustment to the input image.

        Args:
            img (numpy.ndarray or PIL.Image): The input image.
            bboxes (numpy.ndarray): An array of bounding boxes associated with the image.

        Returns:
            numpy.ndarray: The augmented image with adjusted brightness.
            numpy.ndarray: The bounding boxes associated with the augmented image.
        """
        # Convert the image to a PIL Image object if it is a numpy array
        if isinstance(img, np.ndarray):
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
        # Adjust the brightness of the image using torchvision.transforms.functional
        img = F.adjust_brightness(img, self.brightness_factor)
        
        # Convert the Image object back to a numpy array and reverse the color channels
        img = np.array(img)[:, :, ::-1].copy()
        
        # Return the image with adjusted brightness and the bounding boxes
        return img, bboxes

def main():
    label_mapping = {
        'disc': 0,
        'adapter':1,
        'guide':2,
        'qr':3,
        'gun':4,
        'boom': 5,
        'head': 6,
    }
    
    path_img = 'D:/data-augmentation-for-object-detection/data/1a7ff59a026f50acbf91d546e8048637.jpg'
    img = cv2.imread(path_img)
    path_xml = 'D:/data-augmentation-for-object-detection/data/1a7ff59a026f50acbf91d546e8048637.xml'
    bboxes = get_info_bbox(path_xml, label_mapping)
    
    img_res, bboxes_res = Adjust_Brightness(1.5)(img.copy(), bboxes.copy())
    draw_rect(img_res, bboxes_res, img)
    
if __name__ == '__main__':
    main()
    
    

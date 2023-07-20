import torchvision.transforms.functional as F
import numpy as np
import cv2
from PIL import Image
import random
from utils import draw_rect, get_info_bbox

class Lighting_Noise(object):
    def __init__(self):
        """
        Initialize the Lighting_Noise data augmentation object.
        """
        pass
        
    def __call__(self, img, bboxes):
        """
        Apply random color channel swapping to the input image.

        Args:
            img (numpy.ndarray or PIL.Image): The input image.
            bboxes (numpy.ndarray): An array of bounding boxes associated with the image.

        Returns:
            numpy.ndarray: The augmented image with random color channel swapping.
            numpy.ndarray: The original bounding boxes (no adjustment is made on the bounding boxes).
        """
        # Create a copy of the image
        img = img.copy()

        # Define permutations to swap color channels
        perms = ((0, 1, 2), (0, 2, 1), (1, 0, 2), 
                (1, 2, 0), (2, 0, 1), (2, 1, 0))
        swap = perms[random.randint(0, len(perms) - 1)]
        
        # Convert the image to RGB format if it is a numpy array
        if type(img) == np.ndarray:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
        
        # Convert the image to a PyTorch tensor
        img = F.to_tensor(img)

        # Perform color channel swapping
        img = img[swap, :, :]

        # Convert the tensor back to a PIL image and then to a NumPy array
        img = F.to_pil_image(img)
        img = np.array(img)[:, :, ::-1].copy()
        
        # Return the augmented image and original bounding boxes (no adjustment on bounding boxes)
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
    
    img_res, bboxes_res = Lighting_Noise()(img.copy(), bboxes.copy())
    draw_rect(img_res, bboxes_res, img)
    
if __name__ == '__main__':
    main()
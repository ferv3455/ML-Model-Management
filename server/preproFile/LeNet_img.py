def pre_process(img):
    import cv2
    import numpy as np

    img = cv2.resize(img, (28, 28))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img / 255
    img = np.ascontiguousarray(img)
    img = img.float()
    img = img.unsqueeze(0)
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    return img

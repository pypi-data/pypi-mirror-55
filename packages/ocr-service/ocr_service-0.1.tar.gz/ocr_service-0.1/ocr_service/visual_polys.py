import cv2
import matplotlib.pyplot as plt

def debug_polys(np_image, polys, BNMode=True, thickness=1, save_image_path=None):
    if BNMode:
        zeros_img = np.zeros(np_image.shape[:2])
    else:
        zeros_img = np_image.copy()
    for poly in polys:
        draw = cv2.polylines(zeros_img, [poly.astype('int32')], True, 255, thickness)
    plt.figure(figsize=(15,15))
    plt.imshow(draw)
    if save_image_path:
        cv2.imwrite(save_image_path, draw)
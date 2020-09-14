import numpy as np
from Consts import *


def build_show_image(ct_image, mask_image):
    mapping_maskR = np.where(mask_image[:, :, 0] != COLOR["red"][0], False, True)
    mapping_maskG = np.where(mask_image[:, :, 1] != COLOR["green"][1], False, True)
    mapping_maskB = np.where(mask_image[:, :, 2] != COLOR["blue"][2], False, True)

    mapping_mask = np.bitwise_or(mapping_maskR, mapping_maskG)
    mapping_mask = np.bitwise_or(mapping_mask, mapping_maskB)

    show_imageR = np.where(mapping_mask, 0, ct_image[:, :, 0])
    show_imageG = np.where(mapping_mask, 0, ct_image[:, :, 0])
    show_imageB = np.where(mapping_mask, 0, ct_image[:, :, 0])

    show_imageR = show_imageR.reshape((mapping_mask.shape[0], mapping_mask.shape[1], 1))
    show_imageG = show_imageG.reshape((mapping_mask.shape[0], mapping_mask.shape[1], 1))
    show_imageB = show_imageB.reshape((mapping_mask.shape[0], mapping_mask.shape[1], 1))

    show_image = np.concatenate([show_imageR, show_imageG, show_imageB], axis=2)

    show_image = show_image.astype(np.uint8) + mask_image

    return show_image


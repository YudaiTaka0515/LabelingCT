import pydicom as dicom

import numpy as np
from Consts import *


def load_ct(ct_dir):
    print(ct_dir)
    ROW = COL = 512
    # dicomファイルのパスをリストとして取得
    ct_slice_paths = []
    num_slice = 0
    for ct_slice in os.listdir(ct_dir):
        if not ct_slice.lower().endswith(".raw"):
            ct_slice_paths.append(os.path.join(ct_dir, ct_slice))
            num_slice += 1

    ct_images = np.empty((num_slice, ROW, COL), dtype='uint8')
    print(ct_images.shape)
    # Numpy配列として読み込む
    for i, path in enumerate(ct_slice_paths):
        print("Loading... : ", path)
        ct_image = dicom.dcmread(path, force=True)
        # WindowCenter, WindowWidthの取得
        try:
            window_center = ct_image.WindowCenter
            window_rescale_intercept = ct_image.RescaleIntercept
            window_center = window_center - window_rescale_intercept
            window_width = ct_image.WindowWidth
        except AttributeError:
            print("this is not dicom")
            return -1

        # 表示画素値の最大と最小を計算
        max_val = window_center + window_width / 2
        min_val = window_center - window_width / 2

        # Numpy配列に変換
        ct_image.convert_pixel_data()
        ct_image = ct_image.pixel_array

        # Window処理
        ct_image = 255 * (ct_image - min_val) / (max_val - min_val)  # 最大と最小画素値を0から255に変換
        ct_image[ct_image > 255] = 255  # 255より大きい画素値は255に変換
        ct_image[ct_image < 0] = 0  # JPEG画像として保存

        ct_image = ct_image.astype('uint8')
        ct_images[i] = ct_image

    ct_images = ct_images.reshape(ct_images.shape[0], ct_images.shape[1], ct_images.shape[2], 1)
    ct_images = np.concatenate([ct_images, ct_images, ct_images], axis=3)

    print("Converted dicom to numpy.")
    print("Shape : ", ct_images.shape)

    return ct_images


def load_raw(raw_file_path):
    ROW = COL = 512

    print(raw_file_path)
    file = open(raw_file_path, 'rb')
    raw_image = np.fromfile(file, np.uint8)
    print("shape : ", raw_image.dtype)
    num_slice = raw_image.shape[0] // (ROW * COL)
    raw_image = raw_image.reshape(num_slice, ROW, COL)

    raw_image = raw_image.reshape(raw_image.shape[0], raw_image.shape[1], raw_image.shape[2], 1)
    raw_image = np.concatenate([raw_image, raw_image, raw_image], axis=3)

    raw_image = np.where(raw_image == COLOR_PLATTE_FOR_RAW["red"], COLOR["red"], raw_image)
    raw_image = np.where(raw_image == COLOR_PLATTE_FOR_RAW["green"], COLOR["green"], raw_image)
    raw_image = np.where(raw_image == COLOR_PLATTE_FOR_RAW["blue"], COLOR["blue"], raw_image)
    # raw_image = np.where(raw_image == COLOR_PLATTE_FOR_RAW["yellow"], COLOR["yellow"], raw_image)
    raw_image = raw_image.astype(dtype="uint8")

    print("Converted raw to numpy.")
    print("shape : ", raw_image.shape)

    return raw_image





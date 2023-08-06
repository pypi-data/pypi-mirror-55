# -*- coding: utf-8 -*-
#
# Copyright © 2019 Stephan Seitz <stephan.seitz@fau.de>
#
# Distributed under terms of the GPLv3 license.

"""

"""

import glob
from os.path import join

import natsort
import numpy as np
import pydicom
from tqdm import tqdm


def natglob(pattern, recursive=True) -> list:
    """natglob

    :param pattern:
    :param recursive:
    :rtype: list
    """
    return natsort.natsorted(glob.glob(pattern, recursive=recursive))


def dicomdir2vol(dicom_dir, filter_type=None, series_filter=None, frame_of_reference_filter=None, report_progress=True):

    dicom_dir_files = natglob(join(dicom_dir, "*"))
    # print('Found %i files in DICOM directory' % len(dicom_dir_files))

    spacing = None
    # origin = None
    last_image_idx = -1
    arrays = []

    for file in tqdm(dicom_dir_files) if report_progress else dicom_dir_files:
        try:
            dc = pydicom.read_file(file)

            # print(file + ': ' + str(dc.ImageType))
            if filter_type and not str.lower(filter_type) in str.lower(str(dc.ImageType)):
                continue
            if series_filter and dc.SeriesNumber != series_filter:
                continue
            if frame_of_reference_filter and frame_of_reference_filter not in dc[0x20, 0x52].value:
                continue
            cur_image_idx = dc[0x20, 0x13].value
            if cur_image_idx <= last_image_idx:
                continue

            # print("Loading dicom slice %i" % cur_image_idx)
            arrays.append(dc.pixel_array)
            last_image_idx = cur_image_idx

            if not spacing:
                spacing = [float(dc.SliceThickness), float(dc.PixelSpacing[0]), float(dc.PixelSpacing[1])]
            # if not origin:
            #     origin = [float(dc[0x20, 0x32].value[0]), float(
            #     dc[0x20, 0x32].value[1]), float(dc[0x20, 0x32].value[2])]

        except Exception as e:
            print(e)

    vol = np.stack(arrays)
    return vol, spacing

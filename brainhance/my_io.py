#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Lucas Costa Campos <lqccampos@gmail.com>
#
# Distributed under terms of the MIT license.

import datetime
import numpy as np
import nibabel as nib
import tensorflow as tf

def normalize(img):
    mx = np.amax(img)
    mn = np.amin(img)

    img = (img - mn)/(mx - mn)
    return img, mx, mn

def denormalize(img, mx, mn):

    img = img*(mx - mn)  + mn
    return img


def read_chunk(chunk, q):

    # Get the first image to learn its size
    img_nii = nib.load(chunk[0][0])
    imgs = []
    HR = img_nii.get_fdata();
    HR, mx, mn = normalize(HR)
    imgs.append(img_nii)

    #Change shape to fit TF expectation
    xt_total_HR = np.empty((len(chunk), *HR.shape, 1))
    xt_total_HR[0, :, :, :, 0] = HR


    for idx, (input, _) in enumerate(chunk[1:]):
        img_nii = nib.load(input)
        HR = img_nii.get_fdata();
        HR, mx, mn = normalize(HR)
        imgs.append(img_nii)

        #Change shape to fit TF expectation
        xt_total_HR[idx+1, :, :, :, 0] = HR

    q.put(tf.convert_to_tensor(xt_total_HR))
    q.put(imgs)

def write_chunk(chunk, generated_image, imgs):
    for idx, (_, output) in enumerate(chunk):

        volume_generated = generated_image[idx, :, :, :, 0]
        img_volume_gen = nib.Nifti1Image(volume_generated, imgs[idx].affine*0.5, header=imgs[idx].header)
        img_volume_gen.to_filename(output)

def check_if_img(filename):

    if ".nii" in filename:
        return True
    else:
        return False
    # sniff = None
    # for image_klass in all_image_classes:
    #     is_valid, sniff = image_klass.path_maybe_image(filename, sniff)
    #     if is_valid:
    #         print(f"{filename} is valid")
    #         return True

    # return False

def make_filelist(inputs, outputs):

    if check_if_img(inputs):
        ins = [inputs]
    else:
        # Read input files
        with open(inputs, 'r') as f_input:
            ins = f_input.read().splitlines()

    print(outputs)
    if check_if_img(outputs):
        outs = [outputs]
    else:
        # Read input files
        with open(outputs, 'r') as f_output:
            outs = f_output.read().splitlines()

    data_names = list(zip(ins, outs))
    return data_names


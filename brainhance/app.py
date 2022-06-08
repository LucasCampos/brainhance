#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Lucas Costa Campos <lqccampos@gmail.com>
#
# Distributed under terms of the GPL license.
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}

import argparse
import numpy as np
import sys
import tensorflow as tf
import tqdm

from multiprocessing import Process, Queue
from brainhance.my_io import read_chunk, write_chunk, make_filelist


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def evaluate(input_filename, output_filename, network, batch_size=1):


    sd = os.path.dirname(__file__)
    generator = tf.keras.models.load_model(os.path.join(sd, f'saved_models/{network}'))
    generator.compile()

    data_names = make_filelist(input_filename, output_filename)
    batches = list(chunks(data_names, batch_size))

    # Start the parallel IO
    queue = Queue()
    chunk_reader = Process(target=read_chunk, args=(batches[0], queue))
    chunk_reader.start()
    chunk_writer = None

    with tqdm.tqdm(total=len(data_names)) as bar:
        for i_chunk in range(len(batches)):

            # Get the next data to be proccessed
            xt_total_HR_tensor = queue.get()
            imgs = queue.get()
            chunk_reader.join()

            # Start reading the data for the following iteration
            # This is done now so that we can have some IO and
            # computation at the same time
            if i_chunk < len(batches) -1:
                queue = Queue()
                chunk_reader = Process(target=read_chunk, args=(batches[i_chunk+1], queue))
                chunk_reader.start()

            generated_image = generator.predict_on_batch(xt_total_HR_tensor)

            # save volumes
            if chunk_writer is not None:
                chunk_writer.join()

            chunk_writer = Process(target=write_chunk, args=(batches[i_chunk], generated_image, imgs.copy()))
            chunk_writer.start()

            bar.update(len(batches[i_chunk]))

    chunk_writer.join()

def main():

    parser = argparse.ArgumentParser(description='Parse the input arguments.')

    parser.add_argument('input', type=str, help='file with list of NIFTIs to be upsampled')
    parser.add_argument('output', type=str, help='file with list of output NIFTIs to be generated')
    parser.add_argument('-n', '--network', required=False, choices=["Generalist", "1000BRAINS", "dHCP", "Brain_Tumor"], type=str, help='Which network to use.', default="Generalist")
    parser.add_argument('-b', '--batch_size', required=False, type=int, help='How many brains to upsample in a single batch. Larger values may lead to a speed up, but will require more memory.', default=1)
    args=parser.parse_args()


    evaluate(args.input, args.output, args.network, args.batch_size)

if __name__ == "__main__":
    main()

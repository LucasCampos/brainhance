# Braingan3d Software Release


## Usage

The usage of this software is relatively simple,

```bash
brainsgan input_file output_file
```

The `input_file` and `output_file` files can be either path to NIFTI images
(with extension either `.nii` or `.nii.gz`) or to a file (normally in the
`.txt` format) containing a list of images. For the upsampling for more
than on file, the second form is preferred, as it avoids loading the model onto
the GPU over and over again.

It is possible to choose the network used with the `-n/--network` flag. E.g.,

```bash
brainsgan LR_scan.nii.gz SR_scan.nii.gz --network dHCP
```

## Recommended settings

This code does not take advantage of more than one GPU. Thus, used in a
multi-GPU system, it is recommended to add the `CUDA_VISIBLE_DEVICES` before
running the code

```bash
CUDA_VISIBLE_DEVICES=<GPU_to_be_used> brainsgan input_file output_file
```

It is also possible to use only the CPU by leaving `GPU_to_be_used` empty.


## Runtime

Running on a single Nvidia P100, the upsampling takes roughly one second per
scan and roughtly 4s on the CPU.

## Developer Information

### Build

The following information is only useful for individuals who are actively
contributing to the program.

We use setuptool and wheel to build the distribution code. The process is
described next. More information can be found
[here](https://packaging.python.org/tutorials/packaging-projects/).

1. Be sure that setuptools, twine, and wheel are up-to-dated

```bash
python3 -m pip install --user --upgrade setuptools wheel twine
```

2. Run the build command

```bash
python3 setup.py sdist bdist_wheel
```

3. Upload the package to pip

```bash
python3 -m twine upload dist/*
```

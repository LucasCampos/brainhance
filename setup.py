import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brainhance",
    version="0.0.1",
    author="Lucas da Costa Campos",
    author_email="lqccampos@gmail.com",
    description="Command-line tool to perform MRI upsampling via SRGANS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LucasCampos/brainhance",
    include_package_data=True,
    packages=["brainhance"],
    package_data={"brainhance": ["brainhance"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "nibabel",
        "multiprocess",
        "protobuf==3.14.0",
        "tensorflow-gpu==2.4.0"
    ],
    entry_points={
        'console_scripts':[
            'brainhance = brainhance.app:main',
        ],
    }
)

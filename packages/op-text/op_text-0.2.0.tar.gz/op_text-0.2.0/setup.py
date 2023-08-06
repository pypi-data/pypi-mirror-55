import setuptools
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='op_text',
    version='0.2.0',
    license='MIT',
    description='Thin wrapper around HuggingFace Transformers sequence classification models for ease of use',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dean Knudson',
    author_email='knuddj1@student.op.ac.nz',
    url='https://github.com/knuddj1/op_text',
    keywords='NLP deep learning transformer pytorch BERT GPT GPT-2 google openai CMU sentiment text',
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'torch>=1.0.0',
        'boto3',
        'requests',
        'tqdm',
        'regex',
        'sentencepiece',
        'pytorch-transformers'
        ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.6',
)
from setuptools import setup, find_packages
from os import path
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='InterviewTranscriber',
    version='0.0.1',
    description="Python based interface for interacting with Google Cloud's Speech-to-Text API "
                "and Cloud Storage API.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mjfox3/InterviewTranscriber',
    author='Michael Joseph Fox',
    author_email='mjfox3@ncsu.edu',
    # classifiers=[
    #     'Development Status :: 3 - Alpha',
    #     'Intended Audience :: Sociolinguistic Researchers',
    #     'Topic :: Automatic Data Analysis :: Transcription',
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3.6',
    #     'Programming Language :: Python :: 3.7',
    # ],
    keywords='sociolinguistics, linguistics, automatic analysis, transcription, textgrids',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    python_requires='>=3.7',
    install_requires=['google==2.0.2',
                      'google-api-core==1.14.3',
                      'google-auth==1.6.3',
                      'google-cloud-speech==1.2.0',
                      'googleapis-common-protos==1.6.0',
                      'pandas==0.25.3',
                      'TextGrid==1.4'],

    project_urls={
        'Bug Reports': 'https://github.com/mjfox3/InterviewTranscriber/issues',
        'Source': 'https://github.com/mjfox3/InterviewTranscriber',
    },
)

# from setuptools import setup  # type: ignore

# with open("README.md", 'r', encoding="utf-8") as f:
#     long_description = f.read()

# REPO_NAME = "Books-Recommender-System"
# SRC_REPO = "src"
# LIST_OF_REQUIREMENTS = ['streamlit', 'numpy']  # Change to list

# setup(
#     name=REPO_NAME,  # Updated to use REPO_NAME variable
#     version='0.0.1',
#     author='Nikita',
#     author_email='nikitamishra2101.com',
#     description='A small package for book recommendation System',
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     url="https://github.com/NNM-21/Book-Recommender-System.git",
#     packages=[SRC_REPO],
#     license="MIT",
#     python_requires=">=3.7",
#     install_requires=LIST_OF_REQUIREMENTS  # Make sure this is a list
# )
from setuptools import setup

try:
    with open("README.md", 'r', encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A small package for book recommendation System"

REPO_NAME = "Books-Recommender-System"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = ['streamlit', 'numpy', 'scikit-learn', 'pandas', 'pickle-mixin', 'urllib3']

setup(
    name=REPO_NAME,
    version='0.0.1',
    author='Nikita',
    author_email='nikitamishra2101@gmail.com',
    description='A small package for book recommendation System',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/NNM-21/Book-Recommender-System.git",
    packages=[SRC_REPO],
    license="MIT",
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)

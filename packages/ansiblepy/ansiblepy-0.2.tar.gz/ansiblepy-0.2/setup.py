try:
    import setuptools
except ImportError:
    from distutils.core import setup, find_packages, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ansiblepy",
    version="0.2",
    author="Maheshkrishna A G",
    author_email="maheshkrishnagopal@gmail.com",
    description="AnsiblePy is an Ansible Playbook and Roles generator with vast information on Ansible Modules.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maheshkrishnagopal/Ansibly",
    packages=setuptools.find_packages(),
    use_2to3=True,
    
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Operating System :: OS Independent",
    ],
    install_requires=[
      'pymongo'
    ],
    python_requires='>=2.4',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="udt",
    version="0.1.0",
    author="kenblikylee",
    author_email="kenblikylee@126.com",
    description="udacity 翻译助手",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenblikylee/udt.git",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'udt = udt.cli:main'
        ]
    },
    python_requires='>=3.6',
)

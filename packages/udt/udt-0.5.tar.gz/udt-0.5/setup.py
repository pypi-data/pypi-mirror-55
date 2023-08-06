import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="udt",
    version="0.5",
    author="青笔",
    author_email="kenbliky@gmail.com",
    description="udacity 翻译助手",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cn.udacity.com/",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[
        'PyYAML>=5.1.2',
        'requests>=2.22.0',
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

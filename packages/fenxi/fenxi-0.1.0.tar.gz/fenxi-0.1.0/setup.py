import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fenxi",
    version="0.1.0",
    author="kenblikylee",
    author_email="kenblikylee@126.com",
    description="python 开源命令行分析工具。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenblikylee/fenxi.git",
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
            'fenxi = fenxi.cli:main'
        ]
    },
    python_requires='>=3.6',
)

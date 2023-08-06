import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="FakeFaceDetect",
    version="0.0.1",
    author="zhangqi",
    author_email="sy1617210@buaa.edu.cn",
    description = "None",
    packages=['FakeFaceDetect'],
    url = "https://github.com/zhangqizky",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'judge=FakeFaceDetect:judge',
        ]
    }
)
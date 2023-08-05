import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mediapro",
    version="0.0.1",
    author="MediaPro Developers",
    author_email="mediapro@shengbin.me",
    description="All about media processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shengbinmeng/mediapro",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)

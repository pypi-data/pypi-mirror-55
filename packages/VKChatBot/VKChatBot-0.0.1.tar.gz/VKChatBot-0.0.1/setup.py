import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name="VKChatBot",
    version="0.0.1",
    author="Pavel Shishmarev",
    author_email="pashawnn@gmail.com",
    description="Library for easy creating of chat bots for VK.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PashaWNN/vkchatbot/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
    ],
    python_requires='>=3.5, <4',
)

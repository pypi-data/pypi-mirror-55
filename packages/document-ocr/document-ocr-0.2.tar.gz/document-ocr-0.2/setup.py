from setuptools import setup

setup(
    name='document-ocr',
    version='0.2',
    install_requires=['pytesseract', 'opencv-python', 'numpy'],
    author="Shashank Singh",
    author_email="shashank.s.1903@gmail.com",
    description="Ocr For documents",
    # url='http://github.com/CubeConsumerServivesPvtLtd/simulator',
    license='CUBE',
    packages=['ocr'],
    zip_safe=False
)

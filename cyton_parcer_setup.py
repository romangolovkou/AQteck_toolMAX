from setuptools import setup
from Cython.Build import cythonize

setup(
    name="AqAutoDetectionLibrary",
    ext_modules=cythonize("AQ_lib/AQ_Devices/SystemLibrary/AqAutoDetectionLibrary.py", compiler_directives={"language_level": "3"}),
    zip_safe=False,
)

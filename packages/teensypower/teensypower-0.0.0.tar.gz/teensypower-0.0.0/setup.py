from setuptools import setup, find_packages
requirements = ['teensytoany',]
setup(
    author = "Jaehee Park",
    author_email = "jaehee@ramonaoptics.com",
    description = "teensy controlled power switch",
    install_requires = requirements,
    name = "teensypower",
    packages=find_packages(include=['teensypower']),
    version='0.0.0',
    python_requires='>=3.6',
    zip_safe=False,
)

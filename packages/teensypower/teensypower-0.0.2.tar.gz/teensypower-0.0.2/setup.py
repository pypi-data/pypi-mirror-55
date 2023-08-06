from setuptools import setup, find_packages
import versioneer
requirements = ['teensytoany',]
setup(
    author = "Jaehee Park",
    author_email = "jaehee@ramonaoptics.com",
    description = "teensy controlled power switch",
    install_requires = requirements,
    name = "teensypower",
    packages=find_packages(include=['teensypower']),
    python_requires='>=3.6',
    zip_safe=False,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)

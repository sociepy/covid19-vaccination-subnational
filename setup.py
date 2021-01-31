"""setup script."""


from setuptools import setup, find_packages
import os
import glob

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(this_directory, 'requirements.txt')) as f:
    requirements = f.readlines()


setup(
    name='covid19-subnational-updater',
    version="0.0.0",
    description="Update tools for covid19-vaccination-subnational project.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='sociepy',
    author_email='hi@lcsrg.me',
    license='GPL-v3',
    install_requires=requirements,
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[
        os.path.splitext(os.path.basename(path))[0] for path in glob.glob("src/*.py")
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords='whatsapp analysis parser chat',
    project_urls={
        'Github': 'http://github.com/sociepy/covid19-vaccination-subnational',
        'Bug Tracker': 'http://github.com/sociepy/covid19-vaccination-subnational/issues',
    },
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'covid-updater-generate-iso=covid_updater.iso:generate_iso'
        ]
    }
)
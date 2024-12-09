from setuptools import setup, find_packages

setup(
    name="montecarlo",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21",
        "pandas>=1.3",
    ],
    description="Monte Carlo Simulation package for games and analysis",
    author="William Rumph",
    author_email="usp7bf@virginia.edu",
    url="https://github.com/1wgrumph/montecarloprojectds5100/tree/main", 
    license="MIT",
    include_package_data=True,  # Include data files in the package
    package_data={"": ["*.txt"]},  # Ensure text files (e.g., english_letters.txt) are included
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: MIT License",
        #"Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

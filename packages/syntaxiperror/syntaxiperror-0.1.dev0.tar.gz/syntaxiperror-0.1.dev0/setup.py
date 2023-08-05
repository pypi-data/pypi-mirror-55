from setuptools import setup

setup(
    name="syntaxiperror",
    author="Marcos Fuenmayor",
    author_email="marcos.fuenmayorhtc@gmail.com",
    version="0.1-dev",
    description="Checkeador de Ips",
    packages=["syntaxiperror"],
    url="https://github.com/mdjfs/syntax_ip_error",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
    entry_points={
        "console_scripts": ["check-ip-address = syntaxiperror:test_address"],
    },
)

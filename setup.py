from setuptools import setup, find_packages

setup(
    name="Medical-Triage-Agent-Implementation",
    version="0.1",
    packages=find_packages(),
    install_requires=["python-docx==1.1.0"]  # Match requirements.txt
)
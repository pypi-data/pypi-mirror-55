from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='streamlabswater-streamlabswater',
    version='0.3.2',
    packages=find_packages(),
    keywords = ['streamlabs', 'streamlabswater', 'iot', 'water', 'sensor', 'smarthome', 'automation'],
    license='MIT',
    author='StreamLabs',
    author_email='support@streamlabswater.com',
    description='Python library for the StreamLabs Developer API',
    url="https://github.com/streamlabswater/stream-python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    python_requires='>=3.6',
)

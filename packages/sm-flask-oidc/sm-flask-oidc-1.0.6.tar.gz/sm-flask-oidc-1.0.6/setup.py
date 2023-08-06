from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='sm-flask-oidc',
    version='1.0.6',
    description='Useful tools to work with OIDC in Python and Flask',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Said Mustapha',
    author_email='said.mustapha7@outllok.com',
    keywords=['OIDC', 'Python', 'Flask', 'IdentityServer'],
    #url='https://github.com/ncthuc/elastictools',
    download_url='https://pypi.org/project/sm-flask-oidc/'
)

install_requires = [

]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)


# publish
# python -m pip install --user --upgrade setuptools wheel
# python -m pip install --user --upgrade twine

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*

# python -m pip install sm_flask_oidc --upgrade
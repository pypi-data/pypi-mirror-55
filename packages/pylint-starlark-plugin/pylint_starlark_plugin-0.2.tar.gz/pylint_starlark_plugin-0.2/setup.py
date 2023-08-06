from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'pylint_starlark_plugin',         # How you named your package folder (MyLib)
  packages = ['.'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Run pylint on Starklark files.',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Peter Hagen',                   # Type in your name
  author_email = 'peter@phgn.io',      # Type in your E-Mail
  url = 'https://github.com/phgn0/pylint-starlark-plugin',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/phgn0/pylint-starlark-plugin/archive/v0.2.tar.gz',    # I explain this later on
  keywords = ['pylint', 'starlark', 'plugin'],   # Keywords that define your package best
  install_requires=[
    'jedi',
    'astroid',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

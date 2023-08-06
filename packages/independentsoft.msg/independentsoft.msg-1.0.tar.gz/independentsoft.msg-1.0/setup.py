from distutils.core import setup
setup(
  name = 'independentsoft.msg',         # How you named your package folder (MyLib)
  packages = ['independentsoft.msg'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='Other/Proprietary',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Outlook .msg file format API',   # Give a short description about your library
  author = 'Independentsoft',                   # Type in your name
  author_email = 'info@independentsoft.de',      # Type in your E-Mail
  url = 'http://www.independentsoft.de',   # Provide either the link to your github or to your website
  download_url = 'http://www.independentsoft.de/msgpy',    # I explain this later on
  keywords = ['Outlook', 'msg', 'Outlook message format'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: Other/Proprietary License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
  python_requires='>=3.3',
)
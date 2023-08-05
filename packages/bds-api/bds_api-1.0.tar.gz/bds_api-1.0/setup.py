from distutils.core import setup
setup(
  name = 'bds_api',         # How you named your package folder (MyLib)
  packages = ['bds_api'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A brief python wrapper designed to access the Census Business Dynamics Statistics API',   # Give a short description about your library
  author = 'Ryan Cogburn',                   # Type in your name
  author_email = 'rncogburn@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/rncogburn/bds_api',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/rncogburn/bds_api/archive/1.0.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'requests',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)


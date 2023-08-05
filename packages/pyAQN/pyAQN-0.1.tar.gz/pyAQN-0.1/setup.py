from distutils.core import setup
setup(
  name = 'pyAQN',         # How you named your package folder (MyLib)
  packages = ['pyAQN'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python implementation of Adjusted Quantile Normalization',   # Give a short description about your library
  author = 'Shay Ben-Elazar',                   # Type in your name
  author_email = 'shaybenelazar@hotmail.com',      # Type in your E-Mail
  url = 'https://github.com/YakhiniGroup/PyAQN',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/YakhiniGroup/PyAQN/archive/v0.1.tar.gz',    # I explain this later on
  keywords = ['Quantile','Normalization'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7'
  ],
)

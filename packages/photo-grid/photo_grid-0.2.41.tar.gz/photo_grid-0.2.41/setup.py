import setuptools
setuptools.setup(name='photo_grid',
      version='0.2.41',
      description='A GUI for field segmentation',
      url='https://github.com/Poissonfish/photo_grid',
      python_requires='>=3.6',
      classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows :: Windows 10"
      ],
      author='James Chen',
      author_email='chun-peng.chen@wsu.edu',
      license='GPLv3',
      packages=['grid', 'grid.gui'],
      include_package_data=True,
      install_requires=['numpy',
                        'pandas>=0.19.2',
                        'sklearn',
                        'scipy',
                        'matplotlib',
                        'qdarkstyle',
                        'opencv-python==4.1.1.26',
                        'image',
                        'rasterio',
                        'PyQt5==5.12',
                        'tqdm'])

# Programming Language: : Python : : 3.4
# Programming Language: : Python : : 3.5

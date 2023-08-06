from setuptools import setup
files = ['plot_max/msyh.ttf']

setup(name='plot_max',
      version='0.21',
      description='high level to use matplotlib',
      url='http://github.com/pringwong',
      author='pring',
      author_email='huppid@qq.com',
      data_files=[('',['plot_max/msyh.ttf'])],
      license='None',
      packages=['plot_max'],
      zip_safe=False)

from setuptools import setup
files = ['plot_max/msyh.ttf']

setup(name='plot_max',
      version='0.22',
      description='high level to use matplotlib',
      url='http://github.com/pringwong',
      author='pring',
      include_package_data=True,
      author_email='huppid@qq.com',
      data_files=[('',['plot_max/msyh.ttf'])],
      license='None',
      packages=['plot_max'],
      zip_safe=False)

from setuptools import setup

setup(name='streamzap',
      version='0.1',
      description='Video stream detection tool using ZAP',
      keywords='analytics, video, stream, dash, hls, ZAP',
      url='http://github.com/eXpl0it3r/streamzap',
      author='Lukas Dürrenberger',
      author_email='eXpl0it3r@my-gate.net',
      license='MIT',
      packages=['streamzap'],
      install_requires=[
          'python-owasp-zap-v2.4',
          'mpegdash',
          'm3u8'
      ],
      entry_points={
          'console_scripts': ['streamzap=streamzap.command_line:main'],
      },
      zip_safe=False)

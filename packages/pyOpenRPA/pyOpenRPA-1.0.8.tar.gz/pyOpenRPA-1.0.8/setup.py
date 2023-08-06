from setuptools import setup, find_packages
import Version
def LongDescriptionRead():
    with open('README.md') as f:
        return f.read()

setup(name='pyOpenRPA',
      version=Version.Get(".."),
      description='First open source RPA platform for business',
      long_description=LongDescriptionRead(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
      ],
      keywords='OpenRPA RPA Robot Automation Robotization',
      url='https://gitlab.com/UnicodeLabs/OpenRPA',
      author='Ivan Maslov',
      author_email='Ivan.Maslov@unicodelabs.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pywinauto>=0.6.6','WMI>=1.4.9','pillow>=6.0.0','keyboard>=0.13.3','pyautogui>=0.9.44','pywin32>=224'
      ],
      include_package_data=True,
      zip_safe=False)
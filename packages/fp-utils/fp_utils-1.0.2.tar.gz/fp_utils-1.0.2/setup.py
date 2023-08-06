from distutils.core import setup

setup(
    name = 'fp_utils',
    packages = ['fp_utils'],
    version = '1.0.2',  # 
    description = 'Most commonly used Fifth Partners functions in PyPi for easy pip install. ',
    author = 'Nathan Duncan',
    author_email = 'nduncan@fifthpartners.com',
    url = 'https://github.com/fifth-partners/fp-utils',
    download_url = 'https://github.com/fifth-partners/fp-utils/archive/1.0.2.tar.gz',
    keywords = ['fifth_partners', 'utils'],
    install_requires=['google-cloud-bigquery', 'google-api-python-client','google-auth-httplib2', 'google-auth-oauthlib'],
    classifiers = [
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" 
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)


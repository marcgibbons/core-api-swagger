from setuptools import setup, find_packages, findall
from coreapi_swagger import VERSION


setup(
    name='coreapi_swagger',
    version=VERSION,
    test_suite='unittest2.collector',
    url='http://www.django-rest-framework.org',
    license='BSD',
    description='Swagger for CoreAPI',
    author='Marc Gibbons',
    author_email='marc_gibbons@rogers.com',
    packages=find_packages(),
    package_data={'': findall()},
    install_requires=['coreapi>=1.23.1', 'six>=1.10.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)

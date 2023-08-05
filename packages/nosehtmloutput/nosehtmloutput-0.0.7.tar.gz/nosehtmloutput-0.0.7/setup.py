import htmloutput.version
import setuptools

setuptools.setup(
    name="nosehtmloutput",
    version=htmloutput.version.__version__,
    author='Hewlett-Packard Development Company, L.P.',
    description="Nose plugin to produce test results in html.",
    license="Apache License, Version 2.0",
    url="https://git.openstack.org/cgit/openstack-infra/nose-html-output",
    packages=["htmloutput"],
    install_requires=['nose', 'six'],
    classifiers=[
        "Environment :: Console",
        "Topic :: Software Development :: Testing",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    entry_points={
        'nose.plugins.0.10': [
            'html-output = htmloutput.htmloutput:HtmlOutput'
        ]
    }
)

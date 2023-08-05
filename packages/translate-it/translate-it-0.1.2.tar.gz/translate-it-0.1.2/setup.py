from setuptools import setup, find_packages

requires = [
    'requests>=2.22.0',
    'lxml>=4.4.1'
]


setup(

    name='translate-it',
    version='0.1.2',
    description='translate it for me.',
    python_requires='>=3.5',
    author='wen',
    author_email='w_angzhiwen@163.com',
    url='https://github.com/suadminwen/translate',
    license='Apache 2.0',
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        'console_scripts': [
            'translate_it = translate_it.translate_it:command_line_runner'
        ]
    },
    install_requires=requires,
)

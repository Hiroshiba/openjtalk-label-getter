from setuptools import setup, find_namespace_packages

setup(
    name='openjtalk-label-getter',
    version='0.0.1',
    packages=find_namespace_packages(),
    url='https://github.com/Hiroshiba/openjtalk-label-getter',
    author='Kazuyuki Hiroshiba',
    author_email='hihokaruta@gmail.com',
    license='MIT License',
    entry_points=dict(
        console_scripts=[
            'openjtalk_label_getter=openjtalk_label_getter:main',
        ],
    ),
)

import setuptools

setuptools.setup(
    name="hg-longpath-test",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires=">=3.9",
    install_requires=[
        "mercurial>=5.8"
    ],
    extras_require=dict(
        test=['pytest', 'pytest-xdist']
    )
)

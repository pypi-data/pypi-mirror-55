from setuptools import setup


with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='git-gud',
    version='0.2.2',
    url='https://github.com/bthayer2365/git-gud/',
    description='A tool to learn git',
    author='Ben Thayer',
    author_email='ben@benthayer.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'gitgud',
        'gitgud.hooks',
        'gitgud.skills',
        'gitgud.skills.basics',
        'gitgud.skills.extras',
        'gitgud.skills.rampup',
    ],
    package_data={
        'gitgud.skills.basics': ['_*/*'],
        'gitgud.skills.extras': ['_*/*'],
        'gitgud.skills.rampup': ['_*/*'],
    },
    python_requires='>=3.0',
    install_requires=[
        'gitpython',
    ],
    entry_points={
        "console_scripts": [
            "git-gud=gitgud.__main__:main"
        ]
    }
)

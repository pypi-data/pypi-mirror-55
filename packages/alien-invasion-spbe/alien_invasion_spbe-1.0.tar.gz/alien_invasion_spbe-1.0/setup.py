from setuptools import setup

def readme():
    with open("README.md") as f:
        readme = f.read()
    return readme


setup(
    name="alien_invasion_spbe",
    version="1.0",
    description="A space invaders type game for shooting down aliens",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Javataru/python_alien_game",
    author="Jeffrey Michael Brown",
    author_email="jbrown5331@yandex.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["alien_invasion_spbe"],
    include_package_data=True,
    install_requires=["pygame"],
    entry_points={
        "console_scripts": [
            "alien-invasion-spbe=alien_invasion_spbe.alien_invasion:run_game"
        ]

    }

)
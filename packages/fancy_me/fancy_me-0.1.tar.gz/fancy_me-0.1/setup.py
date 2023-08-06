from setuptools import setup, find_packages
pkgs = ['fancy_me', "fancy_me.ws", "fancy_me.udp"]

print(pkgs)
setup(
    author="somewheve",
    version=0.1,
    name="fancy_me",
    packages=pkgs,
    author_email='somewheve@gmail.com',
    license="MIT"
)

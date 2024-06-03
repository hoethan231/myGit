from setuptools import setup

setup(name = "myGit",
      version = "1.0",
      packages = ["myGit"],
      entry_points = {
          "console_scripts" : ["myGit = myGit.cli:main"]
    })
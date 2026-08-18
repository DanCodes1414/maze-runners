from setuptools import setup


setup(
    name="mazegen",
    version="1.0.0",
    py_modules=["maze", "config", "cell", "MazeGenerator", "colours"],
    python_requires=">=3.10",
    install_requires=["pydantic"],
    author="dqureshi, dmgeorgi"
)
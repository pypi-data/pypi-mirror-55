from setuptools import find_packages, setup
install_requires = open("requirements.txt").read().splitlines()

setup(
    name="reef",
    version="0.0.1",
    url="https://srinivasreddy.dev",
    license="BSD",
    maintainer="Srinivas Reddy Thatiparthy",
    maintainer_email="thatiparthysreenivas@gmail.com",
    description=" A miniproject to test python and remote development skills.",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)

import setuptools

setuptools.setup(
    name="ssh_tunnel_boring_machine",
    version="0.1.1",
    scripts=["tbm"],
    description="A tool for managing SSH tunnels from the command line",
    url="https://github.com/dominicdoty/tbm",
    packages=setuptools.find_packages()
)
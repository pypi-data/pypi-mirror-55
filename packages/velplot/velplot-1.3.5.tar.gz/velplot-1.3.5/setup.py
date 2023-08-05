from distutils.core import setup
import os,velplot.__init__
from glob import glob

#del os.link
setup(
    name="velplot",
    version=velplot.__version__,
    author="Vincent Dumont",
    author_email="vincentdumont11@gmail.com",
    packages=["velplot"],
    requires=["numpy","matplotlib","scipy","astropy"],
    include_package_data=True,
    scripts = glob('bin/*'),
    url="https://vincentdumont.gitlab.io/velplot/",
    description="Velocity plots of quasar absorption systems",
    install_requires=[]
)

import os
import sys
import builtins
import warnings
from distutils import log
from setuptools import setup
from setuptools.command import (
    build_py,
    sdist,
)


version = "0.0.1"
version_file = os.path.join("pesummary", ".version")

python_version = sys.version_info
print("Running Python version %s.%s.%s" % python_version[:3])
if python_version < (3, 5):
    sys.exit("Python < 3.5 is not supported, aborting setup")

# tell python we're in setup.py
builtins._PESUMMARY_SETUP = True


def full_description():
    """Get the full readme
    """
    with open("README.md", "r") as f:
        readme = f.read()
    return readme


def write_version_file(version):
    """Add the version number and the git hash to the file
    'varaha.__init__.py'

    Parameters
    ----------
    version: str
        the release version of the code that you are running
    """
    from varaha.version_helper import GitInformation, PackageInformation

    git_info = GitInformation()
    packages = PackageInformation()

    with open("varaha/.version", "w") as f:
        f.writelines(["# Generated automatically by varaha\n\n"])
        f.writelines(["last_release = %s\n" % (version)])
        f.writelines(["\ngit_hash = %s\n" % (git_info.hash)])
        f.writelines(["git_author = %s\n" % (git_info.author)])
        f.writelines(["git_status = %s\n" % (git_info.status)])
        f.writelines(["git_builder = %s\n" % (git_info.builder)])
        f.writelines(["git_build_date = %s\n" % (git_info.build_date)])
        f.writelines(['git_build_packages = """%s"""' % (packages.package_info)])
    return


class _VersionedCommand(object):
    def run(self):
        log.info("generating {}".format(version_file))
        try:
            write_version_file(version)
        except Exception as exc:
            if not version_file.is_file():
                raise
            warnings.warn("failed to generate .version file, will reuse existing copy")
        super().run()


class VersionedSdist(_VersionedCommand, sdist.sdist):
    pass


class VersionedBuildPy(_VersionedCommand, build_py.build_py):
    pass


readme = full_description()

setup(
    name="varaha",
    version=version,
    author="Vaibhav Tiwari, Charlie Hoy, Stephen Fairhurst",
    author_email=(
        "vaibhav.tiwari@ligo.org, charlie.hoy@ligo.org, stephen.fairhurst@ligo.org"
    ),
    packages=["varaha", "varaha.bin"],
    url="https://git.ligo.org/charlie.hoy/varaha",
    include_package_data=True,
    download_url="https://git.ligo.org/charlie.hoy/varaha",
    license="MIT",
    description="A Fast Non-Markovian Parameter Sampler for Coalescing Compact Binaries",
    long_description=readme,
    long_description_content_type='text/markdown',
    package_data={'varaha': [version_file]},
    cmdclass={
        "sdist": VersionedSdist,
        "build_py": VersionedBuildPy,
    },
    install_requires=[
        "pycbc",
        "numpy",
        "scipy",
        "gwpy",
        "matplotlib",
        "astropy",
        "ligo-gracedb",
        "lalsuite",
        "pesummary",
        "tqdm"
    ],
    entry_points={
        'console_scripts': [
            'varaha_pipe=varaha.bin.fast_pe:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)

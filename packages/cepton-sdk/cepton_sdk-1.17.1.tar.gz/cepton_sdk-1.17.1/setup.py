import platform
import sys
import pathlib

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="cepton_sdk",
        version=open("cepton_util/VERSION").read().strip(),
        description="Cepton Python SDK",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        url="https://github.com/ceptontech/cepton_sdk_redist",
        author="Cepton Technologies",
        author_email="support@cepton.com",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python :: 3",
        ],
        keywords="cepton sdk",
        python_requires=">=3.3",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=[
            "numpy",
            "pyserial",
        ],
        extras_require={
            "capture": [
                "imageio",
                "imageio-ffmpeg",
                "netifaces",
                "pyqt5",
            ],
            "export": [
                "laspy",
                "uuid",
                "plyfile",
            ],
            "plot": [
                "pyqt5",
                "vispy",
            ],
        },
        scripts=[
            "samples/advanced/cepton_export_serial.py",
            "samples/cepton_export.py",
            "samples/cepton_list_sensors.py",
            "tools/cepton_capture.py",
            "tools/cepton_capture_gui.py",
        ]
    )

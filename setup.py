"""
setup.py
Setup script for msi compiler using cx_Freeze
Usage:
 $ python setup.py bdist_msi
 
"""
import sys
from cx_Freeze import setup, Executable

COMPANY_NAME = 'Chimera'
PRODUCT_NAME = 'Chimera Backup Agent'
VERSION = '0.1.0'
DESCRIPTION = "Runs scheduled jobs to backup files to the cloud."
EXECUTABLE = 'chimera.py'
TARGET = 'chimera.exe'

INCLUDE_FILES = [
    'README.md',
    'LICENSE',
    'app',
    'rclone/rclone.exe',
    'winservice',
    'examples',
    'jobs',
    'log',
    'config.ini'
]

# Dependencies are automatically detected, but it might need fine tuning.
PACKAGES = [
    "os",
    "sys",
    "configparser",
    "time"
]

BUILD_EXE_OPTIONS = {
    "packages": PACKAGES,
    "excludes": ["tkinter"],
    'include_files': INCLUDE_FILES
}

BDIST_MSI_OPTIONS = {
    'add_to_path': True,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (COMPANY_NAME, PRODUCT_NAME),
}

OPTIONS = {
        'build_exe': BUILD_EXE_OPTIONS,
        'bdist_msi': BDIST_MSI_OPTIONS
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

executables = [
    Executable(
        EXECUTABLE,
        base=base,
        targetName=TARGET
    )
]

setup(
    name = PRODUCT_NAME,
    version = VERSION,
    description = DESCRIPTION,
    options = OPTIONS,
    executables=executables
)
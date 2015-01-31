from pypass.recipients import Recipients
from pypass.repository import Repository
from pypass.keylist import KeyDatabase, KeyInfo
from pypass.entry import Container, PasswordEntry

from pypass.extendedgpg import ExtendedGPG, EncryptionKeys

import pypass.util

from pypass.pypass import main_entry

import pkg_resources  # part of setuptools
version = pkg_resources.require("pypass")[0].version
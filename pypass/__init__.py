from pypass.repository import Repository

from pypass.gpgdictwrapper import GPGDictWrapper
from pypass.keylist import KeyDatabase, KeyInfo
from pypass.signature import Signature

from pypass.extendedgpg import ExtendedGPG, EncryptionKeys

from pypass.entry import Container, PasswordEntry

import pypass.util
from pypass.generator import PasswordGenerator

from pypass.pypass import main_entry

import pkg_resources  # part of setuptools
version = pkg_resources.require("pypass")[0].version
#
# This file is part of pypass.  pypass is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Michael Curtis, 2015

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
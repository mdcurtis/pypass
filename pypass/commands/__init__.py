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

from pypass.commands.common import CommandInterface, EntryCommand
from pypass.commands.initcommand import InitCommand
from pypass.commands.copycommand import CopyCommand
from pypass.commands.insertcommand import InsertCommand
from pypass.commands.listcommand import ListCommand
from pypass.commands.showcommand import ShowCommand
from pypass.commands.editcommand import EditCommand
from pypass.commands.generatecommand import GenerateCommand
from pypass.commands.recipientscommand import RecipientsCommand

classes = [ InitCommand, CopyCommand, InsertCommand, 
		ListCommand, EditCommand, GenerateCommand,
		ShowCommand, RecipientsCommand ]

__all__ = [ 'CommandInterface', 'classes' ]

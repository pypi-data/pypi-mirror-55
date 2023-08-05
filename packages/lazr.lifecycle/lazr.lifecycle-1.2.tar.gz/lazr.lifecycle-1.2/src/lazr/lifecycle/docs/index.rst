..
    This file is part of lazr.lifecycle.

    lazr.lifecycle is free software: you can redistribute it and/or modify it
    under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, version 3 of the License.

    lazr.lifecycle is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
    License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with lazr.lifecycle.  If not, see <http://www.gnu.org/licenses/>.

LAZR lifecycle
**************

This package defines three "lifecycle" events that notify about object
creation, modification and deletion. The events include information about the
user responsible for the changes.

The modification event also includes information about the state of the object
before the changes.

The module also contains Snapshot support to save the state of an object for
notification, and to compute deltas between version of objects.

.. pypi description ends here

Other documents
===============

.. toctree::
   :glob:

   event
   object-delta
   snapshot
   NEWS

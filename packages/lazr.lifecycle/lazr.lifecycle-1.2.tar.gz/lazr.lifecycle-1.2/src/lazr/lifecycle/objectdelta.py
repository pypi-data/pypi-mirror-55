# Copyright 2006 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.lifecycle
#
# lazr.lifecycle is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.lifecycle is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.lifecycle.  If not, see <http://www.gnu.org/licenses/>.

__metaclass__ = type
__all__ = ['ObjectDelta']


class ObjectDelta:
    """A helper object for delta creation."""

    def __init__(self, old_obj, new_obj):
        self.old_obj = old_obj
        self.new_obj = new_obj
        self.changes = {}

    def recordNewValues(self, fields):
        """Updates changes based on changed field values."""
        for field_name in fields:
            old_val = getattr(self.old_obj, field_name, None)
            new_val = getattr(self.new_obj, field_name, None)
            if old_val != new_val:
                self.changes[field_name] = new_val

    def recordNewAndOld(self, fields):
        """Updates changes with old and new values for changed fields."""
        for field_name in fields:
            old_val = getattr(self.old_obj, field_name, None)
            new_val = getattr(self.new_obj, field_name, None)
            if old_val != new_val:
                self.changes[field_name] = { 'old' : old_val,
                                             'new' : new_val }

    def recordListAddedAndRemoved(self, field, added_name, removed_name):
        """Calculates changes in list style attributes."""
        # As much as I'd love to use sets, they are unordered
        # and any differences returned are not necessarily
        # consistant with the order they are in the underlying object.
        old_items = getattr(self.old_obj, field, [])
        new_items = getattr(self.new_obj, field, [])

        added_items = []
        for item in new_items:
            if item not in old_items:
                added_items.append(item)
        if added_items:
            self.changes[added_name] = added_items

        removed_items = []
        for item in old_items:
            if item not in new_items:
                removed_items.append(item)

        if removed_items:
            self.changes[removed_name] = removed_items

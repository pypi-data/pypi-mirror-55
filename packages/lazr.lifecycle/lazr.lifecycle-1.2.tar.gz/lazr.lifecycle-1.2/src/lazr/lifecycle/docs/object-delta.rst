Creating Object Deltas
======================

A common workflow surrounding life-cycle events involves computing the deltas
between two objects instances.  This is normally for notification emails in
order to identify what has been changed, so the appropriate information is
sent out in the email.

In order to test that the deltas, we need a simple object to test.

    >>> class TestObj(object):
    ...   def __init__(self, vars):
    ...     self.__dict__.update(vars)
    >>> old_obj = TestObj({'foo':42, 'bar':'hello', 'baz':[1,2,3], 'wiz':1})
    >>> new_obj = TestObj({'foo':42, 'bar':'world', 'baz':[2,3,4], 'wiz':2})
    >>> old_obj.foo
    42
    >>> old_obj.bar
    'hello'

And here is a simple helper function that we'll use to
print out dicts in sorted order (as pprint doesn't assure this until 2.5).

    >>> def display_delta(to_display, indent=0):
    ...   for key in sorted(to_display.keys()):
    ...     value = to_display[key]
    ...     if isinstance(value, dict):
    ...       print("%s: %s => %s" % (key, repr(value['old']), 
    ...                               repr(value['new'])))
    ...     else:
    ...       print("%s: %s" % (key, repr(to_display[key])))

The ObjectDelta instance is constructed with the old object,
and the new object instances. 

    >>> from lazr.lifecycle.objectdelta import ObjectDelta
    >>> delta = ObjectDelta(old_obj, new_obj)

The simplest case is are recording of new values.  The changes property
of the delta object just shows the field name and the new value.

    >>> delta.recordNewValues(['foo', 'bar', 'wiz'])
    >>> display_delta(delta.changes)
    bar: 'world'
    wiz: 2

An alternative to just returning the new values is to return
both the old and the new values for a field value.

     >>> delta = ObjectDelta(old_obj, new_obj)
     >>> delta.recordNewAndOld(['foo', 'bar', 'wiz'])
     >>> display_delta(delta.changes)
     bar: 'hello' => 'world'
     wiz: 1 => 2

In some cases, a list is needed to be checked for additions and removals.
Examples for this would be associated bugs, specs or brances with the
specified object.

    >>> delta = ObjectDelta(old_obj, new_obj)
    >>> delta.recordListAddedAndRemoved('baz', 'added', 'removed')
    >>> display_delta(delta.changes)
    added: [4]
    removed: [1]


Now the normal usage is to do some combination of the above, and pass
the resulting map through to the constructor for a real delta object.

    >>> class TestDelta:
    ...   def __init__(self, foo=None, bar=None, wiz=None,
    ...                baz_added=None, baz_removed=None):
    ...     self.foo = foo
    ...     self.bar = bar
    ...     self.baz_added = baz_added
    ...     self.baz_removed= baz_removed
    ...     self.wiz = wiz

    >>> obj_delta = ObjectDelta(old_obj, new_obj)
    >>> obj_delta.recordNewValues(['foo', 'bar'])
    >>> obj_delta.recordNewAndOld(['wiz'])
    >>> obj_delta.recordListAddedAndRemoved('baz', 'baz_added',
    ...                                     'baz_removed')
    >>> delta = TestDelta(**obj_delta.changes)
    >>> delta.foo
    >>> delta.bar
    'world'
    >>> delta.baz_added
    [4]
    >>> delta.baz_removed
    [1]
    >>> display_delta(delta.wiz)
    new: 2
    old: 1


.. _status_and_status_lists_toplevel:

Statuses and Status Lists
=========================

In Stalker, classes mixed with :class:`~stalker.models.mixins.StatusMixin`
needs to be created with a *suitable*
:class:`~stalker.models.status.StatusList` instance.

Because most of the *statusable* classes are going to be using the same
:class:`~stalker.models.status.Status`\ es (ex: **WIP**, **Waiting Review**,
**Completed** etc.) over and over again, it is much efficient to create those
Statuses only once and use them multiple times by grouping them in
:class:`~stalker.models.status.StatusList`\ s.

A *suitable status list* means, the
:attr:`~stalker.models.status.StatusList.target_entity_type` is set to the name
of that particular class.

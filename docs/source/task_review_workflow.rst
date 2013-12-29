.. _task_review_workflow_toplevel:

====================
Task Review Workflow
====================

Introduction
============

All tasks created in Stalker has a purpose and has an aim. It is the duty of
the task resources to accomplish that task and it is the responsibles' duty to
check if the :class:`.Task` is accomplished correctly. So Stalker presents a
way of approving or requesting a revision for a task to make everything easy
for everybody.

So lets start describing the workflow.

The Workflow
============

When a resource of a task spent his/her time reserved for a task and thinks
that this task is complete or even he/she still has time but needs some
direction, the resource (or any resource of that particular task) can request a
review.

When that happens, Stalker creates a :class:`.Review` instance and attaches it
to the task.

A :class:`.Review` instance holds the status of the review (starting from NEW),
and if some revision is requested it will also hold the description of the
revision, the extra time that the reviewer has given for the revision etc.

Lets think that a particular Task has only one responsible, and one resource.
Lets assume the resource has decided to request a review. When it is happened
Stalker creates a Review instance and assigns it to the responsible of that
Task. Then the responsible is responsible with checking if that Task is
accomplished or not. It the responsible thinks that the task is finished then
he/she sets the status of the Review to Approved (APP) or if he/she thinks that
still some work needs to be done then he/she sets the status of the Review to
Request Revision (RREV) and gives some time for the requested work.

Lets think that there are multiple responsible for a particular task. Then
when the resource request a review, then Stalker will create a Review instance
for each of the responsible. And even one of the responsible has requested a
revision the task will not be considered as completed. And when more than one
responsible request a revision, then the total amount of timing for the
revisions will be added to the task and the resource will continue to work.

Revision Counter
================

Both :class:`.Task` instances and :class:`.Review` instances have an attribute
called ``revision_number``. Each Review with the same revision_number
considered in the same set of revisions. It is only possible to have multiple
Review instances with the same revision_number value if there are more than
one responsible for a Task.

The :attr:`.Task.revision_number` starts from 0 and this represents the base or
initial revision and it is increased by 1 when one of the resources request a
review (by calling :meth:`.Task.request_review()`).

A newly created Review instance will have a revision_number which is equal to
the value of the Task.revision_number at the time it is created. But it never
will or should be 0 cause this represents the base or initial revision.

So, a Task with revision_number is 0 has no revision yet. A Task with revision
number is set to 2 has two sets of Revisions.

The best way to create revisions is to use :meth:`.Task.request_review()`. This
will ensure that there are enough :class:`.Review` instances created for each
responsible and the revision_number attribute of both ends are correctly set.
And the return value of that method should be a list of Review instances.

Each of the responsible should change the attributes of the Review instances
according to their reviews. So they both need to set the status and if they're
requesting a revision they also need to set the timing info for the revision.

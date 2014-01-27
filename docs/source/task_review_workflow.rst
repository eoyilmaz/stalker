.. _task_review_workflow_toplevel:

====================
Task Review Workflow
====================

Introduction
============

All tasks created in Stalker has a purpose and has an aim. It is the duty of
the task resources to accomplish that task and it is the responsibles' duty to
check if the :class:`.Task` is accomplished correctly. With the ``Task Review
Workflow`` Stalker presents a way of reviewing a task.

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
revision, the extra time that the reviewer has given for the revision etc. and
the desired states of all the tasks depending to the reviewed tasks.

Lets think that a particular Task has only one responsible, and one resource.
Lets assume the resource has decided to request a review. When it is happened
Stalker creates a Review instance and assigns it to the responsible of that
Task. Then the responsible is responsible for reviewing the Task. It the
responsible thinks that the task is finished then he/she sets the status of the
Review to Approved (APP) (by calling :meth:`.Review.approve()`) or if he/she
thinks that still some work needs to be done then he/she sets the status of the
Review to Request Revision (RREV) (by calling :meth:`.Review.request_revision)
and gives some time for the requested work and decides if the tasks depending
to the reviewed task should continue working or should be set on hold (if the
reviewed task was initially a task with status complete).

Lets think that there are multiple responsible for a particular task. Then
when the resource request a review, then Stalker will create a Review instance
for each of the responsible. And even if one of the responsible has requested a
revision then the task will not be considered as completed. And when more than
one responsible request a revision, then the total amount of timing for the
revisions will be added to the task and the resource will continue to work.

Depending Tasks
===============

If a revision request has been made to a completed (CMPL) task with other tasks
depending to it, there are a couple of different scenarios to follow.

Scenario A: There are no dependent tasks to the revised task or none of the
dependent tasks have started yet (all in RTS status). Then according to the
reviewers will the tasks can be set to Dependency Has Revision (DREV) which
allows the resources to continue to work or set to Waiting-For-Dependency
(WFD) which prevents the resources to work on the task.

Scenario B: There are dependent tasks and some of them has started or
completed. Again according to the reviewers will the statuses of the tasks will
follow the following table:

  +----------------+--------------+
  | Initial Status | Final Status |
  +----------------+--------------+
  | WFD            | WFD          |
  +----------------+--------------+
  | RTS            | WFD          |
  +----------------+--------------+
  | WIP            | DREV         |
  +----------------+--------------+
  | PREV           | PREV         |
  +----------------+--------------+
  | HREV           | DREV         |
  +----------------+--------------+
  | DREV           | DREV         |
  +----------------+--------------+
  | OH             | OH           |
  +----------------+--------------+
  | STOP           | STOP         |
  +----------------+--------------+
  | CMPL           | DREV         |
  +----------------+--------------+ 

When the revised task approved again and set its status to CMPL, then the
dependent task statuses will be set to their normal statuses again. The
following table shows the statuses that the tasks will have depending to their
time_logs attribute after the depending task is set to CMPL:

  +-----------------+------+------+-----+----+------+
  |                 | DREV | PREV | WFD | OH | STOP |
  +-----------------+------+------+-----+----+------+
  | Has No TimeLogs | RTS  | PREV | RTS | OH | STOP |
  +-----------------+------+------+-----+----+------+
  | Has TimeLogs    | WIP  | PREV | WIP | OH | STOP |
  +-----------------+------+------+-----+----+------+

As you see the task statuses will be restored to their original statuses except
for HREV and CMPL. HREV tasks can not be restored, because even in a normal
situation where there are no revision requested for the dependent task,
creating a new time log will set its status to WIP, and a CMPL task can not be
stored to CMPL status because there were revisions to the depending task so
there should be some work to be done to update this task, so it is restored as
WIP.

The following workflow diagram shows the status workflow, and it is a good idea
to study this to become familiar with the task statuses used in Stalker.

.. image:: ../../../docs/source/_static/images/Task_Status_Workflow.png
      :width: 637 px
      :height: 381 px
      :align: center

Revision Counter
================

Both :class:`.Task` instances and :class:`.Review` instances have an attribute
called ``review_number``. Each Review with the same review_number considered in
the same set of review. It is only possible to have multiple Review instances
with the same review_number value if their :attr:`.reviewer` attribute are
different.

The :attr:`.Task.review_number` starts from 0 and this represents the base or
initial revision and it is increased by 1 when one of the resources request a
review (by calling :meth:`.Task.request_review()`).

A newly created Review instance will have a review_number which is equal to
the value of the Task.review_number + 1 at the time it is created. But it
never will or should be 0 cause this represents the base or initial revision.

So, a Task with review_number 0 has no review yet. A Task with review number is
set to 2 has two sets of reviews.

The best way to create revisions is to use :meth:`.Task.request_review()`. This
will ensure that there are enough :class:`.Review` instances created for each
responsible and the review_number attribute of both ends are correctly set.
And the return value of that method should be a list of Review instances.

Each of the responsible should use the supplied methods (
:meth:`.Review.approve` or :meth:`.Review.request_revision`) of the Review
instances according to their reviews. So by using those actions, the
responsible users can both set the status to an appropriate value and if
they're requesting a revision they also can to set the extra timing info
they've given for the revision.

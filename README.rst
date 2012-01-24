======================
Django Roommate Search
======================

Overview
========

A django app used to search for a roommate. Each user creates a profile and can
then search other profiles to find the ideal roommate.

Requirements
============

* Django 1.3 - Django roommate search uses class based views
* `Django messages <http://code.google.com/p/django-messages/>`_
* In INSTALLED_APPS, put django roommates before django messages to use the
  override templates. These templates change django usernames to profile screen
  names for a degree of anonymity.

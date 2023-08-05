====================
djangocms-page-image
====================

This package provides two DjangoCMS extensions:

* "Page Image" is a page extension that allows you to add an image to a DjangoCMS page.
* "Teaser" is a title extension that allows you to add an image and a teaser text to each localization of a DjangoCMS page.

Dependencies
============

* django-filer >= 1.2
* Django >= 1.11
* django-cms >= 3.5


Changelog
=========

0.7.2
-----
Added copy_relations method.

0.7.1
-----
Fixed a data migration issue.

0.7.0
-----
Version 0.7.0 introduces a new title extension, called Teaser, and a migration which creates a
teaser for every existing page image extension in the site's first language (we assume that the
first language was used for previously created extensions). This allows for localized teaser texts
and also images (which might contain text).

The former "Page Image and Teaser" page extension is still available, but loses its "teaser" field
(which doesn't make too much sense in a non-localized extension anyway).

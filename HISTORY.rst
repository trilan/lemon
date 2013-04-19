History
=======

0.8.1
-----

* Fix admin menu url resolving
* Add `load url from future` for Django 1.4 compatibility

0.8.0
-----

* Update to Django 1.5

0.7.3
-----

* Hide confusing password field from user change form
* Custom admin menu items can be added now using project settings

0.7.2
-----

* Fix admin media

0.7.1
-----

* Add missing initial schemamigration

0.7
---

* Rename lemon.extradmin app to lemon
* Move all apps except extradmin to their own separate distributions
* Add ability to register custom admin sections per app using AppAdmin

0.6.2
-----

* Fix sitemap.xml data format

0.6.1
-----

* Update jQuery and jQuery UI in extradmin app
* Update doctype in admin templates
* Fix form tabs in extradmin app
* Fix change form view in ModelAdmin from extradmin app
* Fields from Publication models are added to admin change list through
  ``get_list_display`` method now
* Admin markup widget and fields can be changed for request now
* Update ModelAdmin code in extradmin app from Django 1.4

0.6.0
-----

* Update required Django version to 1.4

0.5.5
-----

* Fix sync_sitemap and sync_metatags commands

0.5.4
-----

* Add SearchIndex for pages.Page

0.5.3
-----

* Make inline admin class used in MetatagsSite cutomizable

0.5.2
-----

* Update logos
* Fix app titles in app dashboard widget

0.5.1
-----

* Fix handling of the _db attribute on the PublicationManager in get_query_set
* Fix robots.txt template

0.5
---

* First public release!

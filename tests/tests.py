# -*- coding: utf-8 -*-
# Copyright (C) 1998-2010 by the Free Software Foundation, Inc.
#
# This file is part of GNU Mailman.
#
# GNU Mailman is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# GNU Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# GNU Mailman.  If not, see <http://www.gnu.org/licenses/>.

"""
==============================
Test suite for the Mailman UI.
==============================

This document both acts as a test for all the functions implemented
in the UI as well as documenting what has been done.

    >>> from setup import setup_mm, Testobject, teardown_mm
    >>> testobject = setup_mm(Testobject())

Getting Started
===============

To start the test, import the django test client.

    >>> from django.test.client import Client

Then instantiate a test client.

    >>> c = Client()

Go to the start page listing all lists.

    >>> response = c.get('/',)

Make sure the load was a success by checking the status code.

    >>> response.status_code
    200

Check that login is required for a couple of pages
=================
Try to access some of the admin Pages. Accessing these pages
redirects to a login page since we need admin authority to view and use them
#TODO - ACL tests will be implemented for each site at a central place at later stages of development.
Please be aware that this test only checks for authentification ONCE.

    >>> response = c.get('/domains/')

Check that Http Redirect is returned

    >>> from django.http import HttpResponseRedirect
    >>> print type(response) == HttpResponseRedirect
    True

User + Login
===================
For authentification we do need to setup a test user into the system.
This including the login will be checked here:
    
    >>> #c.... adduser() #TODO

    Check our own login form, which should redirect the user to a usable page after every successful login
    Login was successful if we get a return object to either the list index or a specified url
    >>> response = c.post('/accounts/login/',
    ...                   {"user": "james@example.com",
    ...                   "password": "james"})
    >>> print type(response) == HttpResponseRedirect
    True
    
    Check user login directly via our own Auth Framework which will save the Login Cookie which is needed for further testing
    >>> c.login(username='james@example.com', password='james')
    True

Domains Page
===================
Hence, we log in as an admin on the login page we get as a response 
to our call.    

    >>> response = c.get('/domains/')
    >>> print "Add a new Domain" in response.content
    True
    >>> print response

Finishing Test
===============

    >>> teardown_mm(testobject)    
"""

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
Functionality and Test
==============================

This document both acts as a test for all the functions implemented
in the UI as well as documenting what can be done

Test Pre Requirements
=====================

* We've created a special Testobject which will run it's own instance of Mailman3 with a new empty Database.

    >>> from setup import setup_mm, Testobject, teardown_mm
    >>> testobject = setup_mm(Testobject())

    .. note:: 
        You need to stop all Mailman3 instances before running the tests

* Modules needed
    As we can't make sure that you're running the same language as we did we made sure that each test below is executed using the exact same translation mechanism as we use to Display you Status Messages and other GUI Texts.

    Import Translation Module to check success messages
        >>> from django.utils.translation import gettext as _
    
    Import HTTPRedirectObject to check whether a response redirects
        >>> from django.http import HttpResponseRedirect

Getting Started
===============

Starting the test module we do use a special Django Test Client which needs to be imported first.

    >>> from django.test.client import Client
    >>> c = Client()

Once this is created we can try accessing our first Page and check that this was done successful

    >>> response = c.get('/lists/',)
    >>> response.status_code
    200

Login Required
==================================================

As described within the installation instructions we *already* started using authentification. The easiest way testing it is that we simply load a page which is restricted to some users only.
This was done using Django's @login_required Decorator in front of the View.
One of the pages which requires a Login is the Domain Administration, if we can load the page without a redirect to the Login page, you're either already logged in or something went wrong.

    >>> response = c.get('/domains/')
    >>> print type(response) == HttpResponseRedirect
    True

Login of a User
===============

We've decided to write our own Authentification Backend to use with Django.
This will handle all @login_required .authenticate() .login() requests.

As we do not have the Authenticating Part which connects Both Mailman and the WebUI we had to hardcode usernames and permissions into the file (auth/restbackend.py)
For more information what we're planning to implement here take a look at the Acknowledgements.

    .. note::
        If you're planning to expand this feel free to use this wonderful resource:
        https://docs.djangoproject.com/en/dev/topics/auth/

Once the new middleware is in place we will need to create a user first. At the moment the user is automaticly created upon success of the login procedure.
    
    >>> #c.... adduser() #TODO add user

Users will have to use the Login form which is located at (/accounts/login/) in order to authenticate themself. The Login / Logout button is linked in the bottom left corner of each page as well.

After each successful login users should be redirected either to the site which they requested before - stored in a GET Value named next - or get the List index. Only if they've used a faulty login they should stay on the Login Page to try again.
    
    >>> response = c.post('/accounts/login/',
    ...                   {"user": "james@example.com",
    ...                   "password": "james"})
    
    >>> print type(response) == HttpResponseRedirect
    True
    
Unfortuneatly the Test Client requires to use the Login directly because it does handle each request seperately. For this reason we have to use the following part in the Tests only to authenticate a user.
Each successful Login will return True and write the users object into the request context, which allows simple checks whether there is a user logged in and what his name is.

    >>> c.login(username='katie@example.com', password='katie')
    True
    
Permissions
===========
Check that only James does have the permission to get the domains administration
#TODO - ACL is hardcoded in auth backend : permission domain_admin → == james@...
    
    >>> response = c.get('/domains/')
    >>> print type(response) == HttpResponseRedirect
    True
    
    >>> c.logout() #katie

    >>> c.login(username='james@example.com', password='james') #now Domains should work - see tests below
    True

Create a New Domain
===================
Check the content to see that we came to the create page after 
logging in.

    >>> response = c.get('/domains/')
    
Then we check that everything went well.
    >>> response.status_code
    200
    >>> print "Domain Index" in response.content #TODO - change heading
    True
    
Check the button which should allow creation of a new domains
    >>> '<li class="mm_new_domain"><a href="/domains/new/">New Domain</a></li>' in response.content
    True

Now go to the Domains creation page
    >>> response = c.get('/domains/new/')

Then we check that everything went well.

    >>> response.status_code
    200
    >>> print "Add a new Domain" in response.content #TODO - change heading
    True

    
and create a new Domain called 'mail.example.com'.    
Check that the new Domain exists in the list of existing domains which is above new_domain form
    >>> response = c.post('/domains/new/',
    ...                   {"mail_host": "mail.example.com",
    ...                    "web_host": "example.com",
    ...                    "description": "doctest testing domain"})  
    >>> response = c.get('/domains/')
        
Then we check that everything went well.
    >>> response.status_code
    200
    >>> print "doctest testing domain" in response.content
    True

Create a New List
=================

Try to access the list index
    >>> response = c.get('/lists/')
    
Then we check that everything went well.
    >>> response.status_code
    200
    
    >>> "All available Lists" in response.content
    True

Try to create a new list. 
And check the content to see that we came to the create page after 
logging in.

    >>> response = c.get('/lists/new/')
    
Then we check that everything went well.
    >>> response.status_code
    200
    
    >>> print "Create a new List on" in response.content
    True

Now create a new list called 'new_list'.
We should end up on a redirect
    >>> response = c.post('/lists/new/',
    ...                   {"listname": "new_list1",
    ...                    "mail_host": "mail.example.com",
    ...                    "list_owner": "james@example.com",
    ...                    "description": "doctest testing list",
    ...                    "advertised": "True",    
    ...                    "languages": "English (USA)"})    
    >>> print type(response) == HttpResponseRedirect
    True
    
List index page should now include the realname of the list

    >>> response = c.get('/lists/',HTTP_HOST='example.com')

Then we check that everything went well.
    >>> response.status_code
    200
    >>> "New_list1" in response.content
    True

List Summary
============

Four options appear on this page. The first one is to subscribe, 
2. to view archives
3. to edit the list settings #at least if you do have permission to do so
4. to unsubscribe

    >>> response = c.get('/lists/new_list1%40mail.example.com/',)    

Then we check that everything went well.
    >>> response.status_code
    200
    >>> "Subscribe" in response.content
    True
    >>> "Archives" in response.content
    True
    >>> "Edit Options" in response.content
    True
    >>> "Unsubscribe" in response.content
    True
    
Subscriptions   
=============

Get the Subscriptions Page and check that the form was prefilled with the users E-Mail
    >>> url = '/subscriptions/new_list1%40mail.example.com/subscribe'
    >>> response = c.get(url)

Then we check that everything went well.
    >>> response.status_code
    200
    >>> "james@example.com" in response.content
    True
    
Now subscribe James and Katie and check that you get redirected to List Summary which should now have an additional Button allowing to modify your user options.
    
    >>> response = c.post(url,
    ...                   {"email": "james@example.com",
    ...                   "real_name": "James Watt",
    ...                   "name": "subscribe",
    ...                   "fqdn_listname": "new_list1@mail.example.com"})
    >>> response = c.post(url,
    ...                   {"email": "katie@example.com",
    ...                   "real_name": "Katie Doe",
    ...                   "name": "subscribe",
    ...                   "fqdn_listname": "new_list1@mail.example.com"})   
    >>> print (_('Subscribed')+' katie@example.com') in response.content
    True
    
The logged in user (james@example.com) can now modify his own membership using a button which is displayed in list_summary   
    >>> response = c.get('/lists/new_list1%40mail.example.com/')
    >>> "mm_membership" in response.content
    True
    
Using the same subscription page we can unsubscribe as well.    
    >>> response = c.post('/subscriptions/new_list1%40mail.example.com/unsubscribe',
    ...                   {"email": "katie@example.com",
    ...                   "name": "unsubscribe",
    ...                   "fqdn_listname": "new_list1@mail.example.com"})
    >>> print (_('Unsubscribed')+' katie@example.com') in response.content
    True
    
Mass Subscribe Users (within settings)
======================================

Now we want to mass subscribe a few users to the list. Therefore, 
go to the mass subscription page.

    >>> url = '/subscriptions/new_list1%40mail.example.com/mass_subscribe/'
    >>> response = c.get(url)

Check that everything went well by making sure the status code 
was correct.

    >>> response.status_code
    200

Try mass subscribing the users 'liza@example.com' and 
'george@example.com'. Each address should be provided on a separate 
line so add '\\n' between the names to indicate that this was done 
(we're on a Linux machine which is why the letter 'n' was used and 
the double '\\' instead of a single one is to escape the string 
parsing of Python).

    >>> url = '/subscriptions/new_list1%40mail.example.com/mass_subscribe/'
    >>> response = c.post(url,
    ...                   {"emails": "liza@example.com\\ngeorge@example.com"})

If everything was successful, we shall get a positive response from 
the page. We'll check that this was the case.
    
    >>> print _("The mass subscription was successful.") in response.content
    True
    
Change the Memebership Settings
===============================

Now let's go to the membership settings page. Once we go there we 
should get a list of all the available lists.

    >>> response = c.get('/membership_settings/new_list1%40mail.example.com/')

Check that we came to the right place...

    >>> print "Membership Settings" in response.content
    True

...and select the list 'test-one@example.com'.

    >>> response = c.get('/membership_settings/new_list1%40mail.example.com/')

Lets make sure we got to the right page.

    >>> print ("Membership Settings" in response.content) and ("for new_list1@mail.example.com" in response.content)
    True
    
Delete the List
===============

Finally, let's delete the list.
We start by checking that the list is really there (for reference).

    >>> response = c.get('/lists/',HTTP_HOST='example.com')
    >>> print "New_list1" in response.content
    True

Trying to delete the List we have to confirm this action
    >>> response = c.get('/delete_list/new_list1%40mail.example.com/',)
    >>> print "Please confirm" in response.content
    True

Confirmed by pressing the button which requests the same page using POST
    >>> response = c.post('/delete_list/new_list1%40mail.example.com/',)

...and check that it's been deleted.
    >>> response = c.get('/lists/',HTTP_HOST='example.com')
    >>> print "new_list1%40example.com" in response.content
    False

So far this is what you can do in the UI. More tests can be added 
here later.    
    
Finishing Test
==============

    >>> teardown_mm(testobject)    
"""

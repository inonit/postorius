# -*- coding: utf-8 -*-
# Copyright (C) 1998-2012 by the Free Software Foundation, Inc.
#
# This file is part of Postorius.
#
# Postorius is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Postorius is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Postorius.  If not, see <http://www.gnu.org/licenses/>.


from django.shortcuts import render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.views.generic import TemplateView

from postorius.models import (Domain, List, Member, MailmanUser,
                              MailmanApiError, Mailman404Error)
from postorius import utils


class MailingListView(TemplateView):
    """A generic view for everything based on a mailman.client
    list object.

    Sets self.mailing_list to list object if fqdn_listname in **kwargs.
    """

    def _get_list(self, fqdn_listname):
        return List.objects.get_or_404(fqdn_listname=fqdn_listname)

    def dispatch(self, request, *args, **kwargs):
        # get the list object.
        if 'fqdn_listname' in kwargs:
            try:
                self.mailing_list = self._get_list(kwargs['fqdn_listname'])
            except MailmanApiError:
                return utils.render_api_error(request)
        # set the template
        if 'template' in kwargs:
            self.template = kwargs['template']
        return super(MailingListView, self).dispatch(request, *args, **kwargs)


class MailmanUserView(TemplateView):
    """A generic view for everything based on a mailman.client
    user object.

    Sets self.mm_user to list object if user_id in **kwargs.
    """

    def _get_first_address(self, user_obj):
        for address in user_obj.addresses:
            return address

    def _get_user(self, user_id):
        user_obj = MailmanUser.objects.get_or_404(address=user_id)
        # replace display_name with first address if display_name is not set
        if user_obj.display_name == 'None' or user_obj.display_name is None:
            user_obj.display_name = ''
        user_obj.first_address = self._get_first_address(user_obj)
        return user_obj

    def dispatch(self, request, *args, **kwargs):
        # get the user object.
        if 'user_id' in kwargs:
            try:
                self.mm_user = self._get_user(kwargs['user_id'])
            except MailmanApiError:
                return utils.render_api_error(request)
        # set the template
        if 'template' in kwargs:
            self.template = kwargs['template']
        return super(MailmanUserView, self).dispatch(request, *args, **kwargs)

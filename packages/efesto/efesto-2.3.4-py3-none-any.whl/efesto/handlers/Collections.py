#   Copyright (C) 2018  Jacopo Cascioli
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*
from falcon import HTTP_501

from .BaseHandler import BaseHandler
from ..Siren import Siren
from ..exceptions import BadRequest


class Collections(BaseHandler):

    def query(self, params):
        self.model.q = self.model.select()
        for key, value in params.items():
            self.model.query(key, value)

    def page(self, params):
        self._page = int(params.pop('page', 1))

    def items(self, params):
        self._items = int(params.pop('items', 20))

    def order(self, params):
        """
        Sets _order to the requested order, or leaves it to the default value.
        """
        order = params.pop('_order', None)
        if order is None:
            return None

        direction = 'asc'
        if order[0] == '-':
            order = order[1:]
            direction = 'desc'
        column = getattr(self.model, order)
        if column is None:
            return None
        self._order = getattr(column, direction)()

    @staticmethod
    def apply_owner(user, payload):
        if 'owner_id' in payload:
            return None
        payload['owner_id'] = user.id

    def process_params(self, params):
        """
        Processes the parameters of a request
        """
        self.page(params)
        self.items(params)
        self.order(params)
        self.query(params)

    def get_data(self, user):
        """
        Gets data performing a read query with the current user.
        """
        return user.do('read', self.model.q, self.model)

    def paginate_data(self, data):
        """
        Paginate data
        """
        query = data.order_by(self._order).paginate(self._page, self._items)
        return list(query.execute())

    def on_get(self, request, response, **params):
        """
        Executes a get request
        """
        user = params['user']
        self.process_params(request.params)
        embeds = self.embeds(request.params)
        data = self.get_data(user)
        body = Siren(self.model, self.paginate_data(data), request.path,
                     page=self._page, total=data.count())
        response.body = body.encode(includes=embeds)

    def on_post(self, request, response, **params):
        self.apply_owner(params['user'], request.payload)
        item = self.model.write(**request.payload)
        if item is None:
            raise BadRequest('write_error', request.payload)
        body = Siren(self.model, item, request.path)
        response.body = body.encode()

    def on_patch(self, request, response, **params):
        response.status = HTTP_501

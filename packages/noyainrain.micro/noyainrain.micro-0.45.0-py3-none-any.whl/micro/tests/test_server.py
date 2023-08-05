# micro
# Copyright (C) 2018 micro contributors
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# Lesser General Public License as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=missing-docstring; test module

import http.client
import json

from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test

from micro.server import (CollectionEndpoint, Server, make_orderable_endpoints,
                          make_trashable_endpoints)
from micro.test import ServerTestCase, CatApp

class ServerTest(ServerTestCase):
    def setUp(self):
        super().setUp()
        self.app = CatApp(redis_url='15')
        self.app.r.flushdb()
        handlers = [
            (r'/api/cats$', CollectionEndpoint, {'get_collection': lambda: self.app.cats}),
            *make_orderable_endpoints(r'/api/cats', lambda: self.app.cats),
            *make_trashable_endpoints(r'/api/cats/([^/]+)', lambda i: self.app.cats[i])
        ]
        self.server = Server(self.app, handlers, client_path='hello',
                             client_modules_path='node_modules', port=16160)
        self.server.start()
        self.staff_member = self.app.login()
        self.user = self.app.login()
        self.client_user = self.user

    @gen_test
    async def test_availability(self):
        # UI
        await self.request('/')
        await self.request('/manifest.webmanifest')
        await self.request(
            '/log-client-error', method='POST',
            body='{"type": "Error", "stack": "micro.UI.prototype.createdCallback", "url": "/"}')

        # API
        await self.request('/api/login', method='POST', body='')
        await self.request('/api/users/' + self.user.id)
        await self.request('/api/users/' + self.user.id, method='POST', body='{"name": "Happy"}')
        await self.request('/api/users/{}'.format(self.app.user.id), method='PATCH',
                           body='{"op": "disable_notifications"}')
        await self.request('/api/settings')
        await self.request('/api/analytics/referrals', method='POST',
                           body='{"url": "https://example.org/"}')

        # API (generic)
        cat = self.app.cats.create()
        await self.request('/api/cats/move', method='POST',
                           body='{{"item_id": "{}", "to_id": null}}'.format(cat.id))
        await self.request('/api/cats/{}/trash'.format(cat.id), method='POST', body='')
        await self.request('/api/cats/{}/restore'.format(cat.id), method='POST', body='')

        # API (as staff member)
        self.client_user = self.staff_member
        await self.request(
            '/api/settings', method='POST',
            body='{"title": "CatzApp", "icon": "http://example.org/static/icon.svg"}')
        await self.request('/api/activity/v2')
        await self.request('/api/activity/v2', method='PATCH', body='{"op": "subscribe"}')
        await self.request('/api/activity/v2', method='PATCH', body='{"op": "unsubscribe"}')
        await self.request('/api/analytics/stats/users')
        await self.request('/api/analytics/referrals')

    @gen_test
    def test_endpoint_request(self):
        response = yield self.request('/api/users/' + self.user.id)
        user = json.loads(response.body.decode())
        self.assertEqual(user.get('__type__'), 'User')
        self.assertEqual(user.get('id'), self.user.id)

    @gen_test
    def test_endpoint_request_invalid_body(self):
        with self.assertRaises(HTTPClientError) as cm:
            yield self.request('/api/users/' + self.user.id, method='POST', body='foo')
        e = cm.exception
        self.assertEqual(e.code, http.client.BAD_REQUEST)

    @gen_test
    def test_endpoint_request_key_error(self):
        with self.assertRaises(HTTPClientError) as cm:
            yield self.request('/api/users/foo')
        self.assertEqual(cm.exception.code, http.client.NOT_FOUND)

    @gen_test
    def test_endpoint_request_input_error(self):
        with self.assertRaises(HTTPClientError) as cm:
            yield self.request('/api/users/' + self.user.id, method='POST', body='{"name": 42}')
        self.assertEqual(cm.exception.code, http.client.BAD_REQUEST)
        error = json.loads(cm.exception.response.body.decode())
        self.assertEqual(error.get('__type__'), 'InputError')

    @gen_test
    def test_endpoint_request_value_error(self):
        with self.assertRaises(HTTPClientError) as cm:
            yield self.request('/api/settings', method='POST',
                               body='{"provider_description": {"en": " "}}')
        self.assertEqual(cm.exception.code, http.client.BAD_REQUEST)
        self.assertIn('provider_description_bad_type', cm.exception.response.body.decode())

    @gen_test
    async def test_collection_endpoint_get(self):
        self.app.cats.create(name='Happy')
        self.app.cats.create(name='Grumpy')
        self.app.cats.create(name='Long')
        response = await self.request('/api/cats?slice=1:')
        cats = json.loads(response.body.decode())
        self.assertEqual(cats.get('count'), 3)
        self.assertEqual([cat.get('name') for cat in cats.get('items', [])], ['Grumpy', 'Long'])
        self.assertEqual(cats.get('slice'), [1, 3])

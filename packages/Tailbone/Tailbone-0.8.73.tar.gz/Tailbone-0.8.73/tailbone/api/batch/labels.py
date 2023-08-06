# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2019 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Tailbone Web API - Label Batches
"""

from __future__ import unicode_literals, absolute_import

import six

from rattail.db import model
from rattail.time import localtime

from cornice import resource

from tailbone.api import APIMasterView


class LabelBatchViews(APIMasterView):

    model_class = model.LabelBatch

    def pretty_datetime(self, dt):
        if not dt:
            return ""
        return dt.strftime('%Y-%m-%d @ %I:%M %p')

    def normalize(self, batch):

        created = batch.created
        created = localtime(self.rattail_config, created, from_utc=True)
        created = self.pretty_datetime(created)

        executed = batch.executed
        if executed:
            executed = localtime(self.rattail_config, executed, from_utc=True)
            executed = self.pretty_datetime(executed)

        return {
            'uuid': batch.uuid,
            '_str': six.text_type(batch),
            'id': batch.id,
            'id_str': batch.id_str,
            'description': batch.description,
            'notes': batch.notes,
            'rowcount': batch.rowcount,
            'created': created,
            'created_by_uuid': batch.created_by.uuid,
            'created_by_display': six.text_type(batch.created_by),
            'complete': batch.complete,
            'executed': executed,
            'executed_by_uuid': batch.executed_by_uuid,
            'executed_by_display': six.text_type(batch.executed_by or ''),
        }

    def collection_get(self):
        return self._collection_get()

    def collection_post(self):
        return self._collection_post()

    def update_object(self, batch, data):

        # assign some default values for new batch
        if not batch.uuid:
            batch.created_by_uuid = self.request.user.uuid
            if batch.rowcount is None:
                batch.rowcount = 0

        return super(LabelBatchViews, self).update_object(batch, data)

    def get(self):
        return self._get()

    # @view(permission='labels.batch.edit')
    # def post(self):
    #     return self._post()

    @classmethod
    def defaults(cls, config):

        # label batches
        resource.add_view(cls.collection_get, permission='labels.batch.list')
        resource.add_view(cls.collection_post, permission='labels.batch.create')
        resource.add_view(cls.get, permission='labels.batch.view')
        batch_resource = resource.add_resource(cls, collection_path='/label-batches', path='/label-batch/{uuid}')
        config.add_cornice_resource(batch_resource)


class LabelBatchRowViews(APIMasterView):

    model_class = model.LabelBatchRow

    def normalize(self, row):
        batch = row.batch
        return {
            'uuid': row.uuid,
            '_str': six.text_type(row),
            '_parent_str': six.text_type(batch),
            '_parent_uuid': batch.uuid,
            'batch_uuid': batch.uuid,
            'batch_id': batch.id,
            'batch_id_str': batch.id_str,
            'batch_description': batch.description,
            'sequence': row.sequence,
            'item_id': row.item_id,
            'description': row.description,
            'status_code': row.status_code,
            'status_display': row.STATUS.get(row.status_code, six.text_type(row.status_code)),
        }

    def collection_get(self):
        return self._collection_get()

    def get(self):
        return self._get()

    @classmethod
    def defaults(cls, config):

        # label batch rows
        resource.add_view(cls.collection_get, permission='labels.batch.view')
        resource.add_view(cls.get, permission='labels.batch.view')
        rows_resource = resource.add_resource(cls, collection_path='/label-batch-rows', path='/label-batch-row/{uuid}')
        config.add_cornice_resource(rows_resource)


def includeme(config):
    LabelBatchViews.defaults(config)
    LabelBatchRowViews.defaults(config)

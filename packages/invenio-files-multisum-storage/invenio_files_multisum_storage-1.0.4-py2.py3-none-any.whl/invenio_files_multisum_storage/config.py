# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio Files Multi-Checksum Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from invenio_indexer.api import RecordIndexer
from invenio_records_rest.utils import allow_all, check_elasticsearch
from invenio_search import RecordsSearch

RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        default_endpoint_prefix=True,
        search_class=RecordsSearch,
        indexer_class=RecordIndexer,
        search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('invenio_files_multisum_storage.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('invenio_files_multisum_storage.serializers'
                                 ':json_v1_search'),
        },
        record_loaders={
            'application/json': ('invenio_files_multisum_storage.loaders'
                                 ':json_v1'),
        },
        list_route='/records/',
        item_route='/records/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        # TODO: Redefine these permissions to cover your auth needs
        create_permission_factory_imp=allow_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
    ),
}
"""REST API for invenio-files-multisum-storage."""

RECORDS_UI_ENDPOINTS = {
    'recid': {
        'pid_type': 'recid',
        'route': '/records/<pid_value>',
        'template': 'invenio_files_multisum_storage/record.html',
    },
}
"""Records UI for invenio-files-multisum-storage."""

SEARCH_UI_JSTEMPLATE_RESULTS = 'templates/invenio_files_multisum_storage/results.html'
"""Result list template."""

PIDSTORE_RECID_FIELD = 'id'

INVENIO_FILES_MULTISUM_STORAGE_ENDPOINTS_ENABLED = True
"""Enable/disable automatic endpoint registration."""

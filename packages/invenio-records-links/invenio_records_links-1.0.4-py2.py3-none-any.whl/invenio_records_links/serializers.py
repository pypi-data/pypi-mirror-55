import json

from elasticsearch_dsl.query import Term, Ids
from flask import current_app
from invenio_pidstore import current_pidstore
from invenio_records_rest.links import default_links_factory
from invenio_records_rest.serializers.base import PreprocessorMixin
from invenio_records_rest.utils import obj_or_import_string
from invenio_search import RecordsSearch, current_search
from invenio_search.utils import schema_to_index


class LinkedObjectSerializerMixin(PreprocessorMixin):
    other_side_rest_endpoint = None
    """
    endpoint key from RECORDS_REST_ENDPOINTS
    """

    other_side_link_property = None
    """
    property on the other side that links to this side property
    """

    other_side_search = None
    """
    used to override search_class from RECORDS_REST_ENDPOINTS.
    redefine as property to return search class instance.
    
    If not defined, the default search class from the other side 
    will be used
    """

    this_side_property = '_id'
    """
    this side property - if it is _id, it is the internal invenio record id,
    otherwise it is a value of a metadatum from this record
    """

    other_side_serializer = None
    """
    returns a type / instance of other side serializer. If not supplied, returns directly an array of hits
    """

    output_property = 'linked_resources'
    """
    name of the property to which the linked resources should be serialized
    """

    def preprocess_record(self, pid, record, links_factory=None, **kwargs):
        ret = super().preprocess_record(pid, record, links_factory=links_factory, **kwargs)

        if self.this_side_property == '_id':
            query = Ids(pid.object_uuid)
        else:
            query = Term(**{self.other_side_link_property: record[self.this_side_property]})

        rest_configuration = current_app.config['RECORDS_REST_ENDPOINTS'][self.other_side_rest_endpoint]

        if self.other_side_search:
            search = self.other_side_search(rest_configuration.get('search_index'))
        else:
            search = obj_or_import_string(rest_configuration.get('search_class', None), default=RecordsSearch)(
                     index=rest_configuration.get('search_index')
                 )

        search_result = search.params(version=True).query(query).execute().to_dict()

        _serializer = self.other_side_serializer

        if _serializer:
            serializer = lambda *args, **kwargs: json.loads(_serializer.serialize_search(*args, **kwargs))
        else:
            serializer = lambda pid_fetcher, search_result, links, item_links_factory: search_result

        pid_fetcher = current_pidstore.fetchers[rest_configuration.get('pid_fetcher')]

        links_factory = obj_or_import_string(
            rest_configuration.get('links_factory_imp'), default=default_links_factory
        )

        ret[self.output_property] = serializer(
            pid_fetcher=pid_fetcher,
            search_result=search_result,
            links={},
            item_links_factory=links_factory,
        )['hits']['hits']

        return ret

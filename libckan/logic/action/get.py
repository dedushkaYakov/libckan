__author__ = 'dgraziotin'

from libckan import request
from libckan.model import response
from libckan.model import package

#TODO not completely satisfied with this design
class Package(request.Api, package.Package):
    def search(self, q='*:*', fq='', rows=20, sort='score desc, name asc', start=0, qf='',
               facet=True, facet_mincount='', facet_limit='', facet_field=''):
        """
        Searches for packages satisfying a given search criteria.

        This action accepts solr search query parameters (details below), and
        returns a dictionary of results, including dictized datasets that match
        the search criteria, a search count and also facet information.

        **Solr Parameters:**

        For more in depth treatment of each paramter, please read the `Solr
        Documentation <http://wiki.apache.org/solr/CommonQueryParameters>`_.

        This action accepts a *subset* of solr's search query parameters:

        :param q: the solr query.  Optional.  Default: `"*:*"`
        :type q: string
        :param fq: any filter queries to apply.  Note: `+site_id:{ckan_site_id}`
            is added to this string prior to the query being executed.
        :type fq: string
        :param rows: the number of matching rows to return.
        :type rows: int
        :param sort: sorting of the search results.  Optional.  Default:
            "score desc, name asc".  As per the solr documentation, this is a
            comma-separated string of field names and sort-orderings.
        :type sort: string
        :param start: the offset in the complete result for where the set of
            returned datasets should begin.
        :type start: int
        :param qf: the dismax query fields to search within, including boosts.  See
            the `Solr Dismax Documentation
            <http://wiki.apache.org/solr/DisMaxQParserPlugin#qf_.28Query_Fields.29>`_
            for further details.
        :type qf: string
        :param facet: whether to enable faceted results.  Default: "true".
        :type facet: string
        :param facet.mincount: the minimum counts for facet fields should be
            included in the results.
        :type facet.mincount: int
        :param facet.limit: the maximum number of constraint counts that should be
            returned for the facet fields. A negative value means unlimited
        :type facet.limit: int
        :param facet.field: the fields to facet upon.  Default empty.  If empty,
            then the returned facet information is empty.
        :type facet.field: list of strings

        **Results:**

        The result of this action is a dict with the following keys:

        :rtype: A dictionary with the following
        """

        args = self._sanitize(locals())
        api_call_dict = self.request(action='package_search', data=args)
        resp = response.Response.from_dict(api_call_dict)

        for i in range(0, len(resp.result['results'])):
            pkg_obj = self.from_dict(resp.result['results'][i])
            resp.result['results'][i] = pkg_obj
        return resp

    def _sanitize(self, params):
        for key in params.keys():
            if not params[key] or key=='self':
                del params[key]

        for key in params.keys():
            if key.startswith('facet_'):
                new_key = key.replace('_', '.')
                params[new_key] = params[key]
                del params[key]
            if key == 'facet':
                params[key] = str(params[key]).lower()

        return params
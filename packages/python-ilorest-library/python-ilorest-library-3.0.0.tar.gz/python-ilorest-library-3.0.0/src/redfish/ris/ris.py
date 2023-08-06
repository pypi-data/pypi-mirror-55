###
# Copyright 2019 Hewlett Packard Enterprise, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###
# -*- coding: utf-8 -*-
"""RIS implementation"""

#---------Imports---------

import re
import sys
import weakref
import logging

from collections import (OrderedDict, defaultdict)

#Added for py3 compatibility
import six

from six.moves.urllib.parse import urlparse, urlunparse

import jsonpath_rw
import jsonpointer

from jsonpointer import set_pointer

from redfish.ris.sharedtypes import Dictable
from redfish.rest.containers import RestRequest, StaticRestResponse
#---------End of imports---------

#---------Debug logger---------

LOGGER = logging.getLogger(__name__)

#---------End of debug logger---------

class BiosUnregisteredError(Exception):
    """Raised when BIOS has not been registered correctly in iLO"""
    pass

class SchemaValidationError(Exception):
    """Schema Validation Class Error"""
    pass

class SessionExpired(Exception):
    """Raised when session has expired"""
    pass

class RisMonolithMemberBase(Dictable):
    """RIS monolith member base class"""
    pass

class RisInstanceNotFoundError(Exception):
    """Raised when attempting to select an instance that does not exist"""
    pass

class RisMonolithMemberv100(RisMonolithMemberBase):
    """Wrapper around RestResponse that adds the monolith data"""
    def __init__(self, restresp=None, isredfish=True):
        self._resp = restresp
        self._patches = list()
        self._typestring = '@odata.type' if isredfish else 'Type'
        self.modified = False
        self.defpath = self.deftype = self.defetag = self._type = None
        self.__bool__ = self.__nonzero__

    @property
    def type(self):
        """Return type from monolith"""
        try:
            if self and self._typestring in self._resp.dict:
                return self._resp.dict[self._typestring]
            #Added for object type
            elif self and 'type' in self._resp.dict:
                return self._resp.dict['type']
        except ValueError:
            return None
        return None

    @property
    def maj_type(self):
        """Return maj type from monolith"""
        if self.type:
            if '.' in self.type:
                types = ".".join(self.type.split(".", 2)[:2])
                retval = types[1:] if types.startswith('#') else types
            else:
                retval = self.type
            return retval
        return self.deftype

    def __nonzero__(self):
        """Defining the bool value for the class"""
        return True if self._resp else False

    @property
    def resp(self):
        """Return resp from monolith"""
        return self._resp

    @property
    def path(self):
        """Return path from monolith"""
        return self._resp.request.path if self else self.defpath

    @property
    def patches(self):
        """Return patches from monolith"""
        return self._patches

    @patches.setter
    def patches(self, val):
        """Set patches from monolith"""
        self._patches = val

    @property
    def dict(self):
        """Return dict from monolith"""
        return self._resp.dict

    @property
    def etag(self):
        """Get the etag of the response"""
        return self.defetag if not self.resp else self.resp.\
            getheader('etag') if 'etag' in self.resp.getheaders()\
            else self.resp.getheader('ETag')

    def popdefs(self, typename, pathval, etagval):
        """Populate the default values in the class"""
        self.defetag = etagval
        self.deftype = typename
        self.defpath = pathval

    def to_dict(self):
        """Convert monolith to dict"""
        result = OrderedDict()
        if self.maj_type:
            result['Type'] = self.type

            if self and self.maj_type == 'Collection.1' and 'MemberType' in self._resp.dict:
                result['MemberType'] = self._resp.dict['MemberType']

            result['links'] = OrderedDict()
            result['links']['href'] = ''
            result['ETag'] = self.etag

            if self:
                result['Content'] = self._resp.dict
                result['Status'] = self._resp.status
                result['Headers'] = self._resp.getheaders()
            result['OriginalUri'] = self.path
            result['Patches'] = self._patches
            result['modified'] = self.modified
            result['MajType'] = self.maj_type

        return result

    def load_from_dict(self, src):
        """Load variables from dict monolith

        :param src: source to load from
        :type src: dict
        """
        if 'Type' in src:
            self._type = src['Type']
            if 'Content' in src:
                restreq = RestRequest(method='GET', path=src['OriginalUri'])
                src['restreq'] = restreq
                self._resp = StaticRestResponse(**src)
            self.deftype = src['MajType']
            self.defpath = src['OriginalUri']
            self.defetag = src['ETag']
            self._patches = src['Patches']
            self.modified = src['modified']

class RisMonolith(Dictable):
    """Monolithic cache of RIS data"""
    def __init__(self, client, typepath):
        """Initialize RisMonolith

        :param client: client to utilize
        :type client: RmcClient object
        Client is saved as a weakref, using it requires brackets and will not survive if the client
        used in init is removed

        """
        self._client = weakref.ref(client)
        self.name = "Monolithic output of RIS Service"
        self._visited_urls = list()
        self._current_location = '/'
        self._type = None
        self._name = None
        self.progress = 0
        self.is_redfish = self._client().is_redfish
        self.typesadded = defaultdict(set)
        self.paths = dict()
        self.ctree = defaultdict(set)
        self.colltypes = defaultdict(set)

        self.typepath = typepath
        self.collstr = self.typepath.defs.collectionstring
        self.etagstr = 'ETag'
        if self.is_redfish:
            self._resourcedir = '/redfish/v1/ResourceDirectory/'
        else:
            self._resourcedir = '/rest/v1/ResourceDirectory'

    @property
    def type(self):
        """Return monolith version type"""
        return "Monolith.1.0.0"

    @property
    def visited_urls(self):
        """Return the visited URLS"""
        return list(set(self._visited_urls)|set(self.paths.keys()))

    @visited_urls.setter
    def visited_urls(self, visited_urls):
        """Set visited URLS to given list."""
        self._visited_urls = visited_urls

    @property
    def types(self):
        """Returns list of types of members in monolith
        :rtype: list
        """
        return list(self.typesadded.keys())

    @types.setter
    def types(self, member):
        """Adds a member to monolith

        :param member: Member created based on response.
        :type member: RisMonolithMemberv100.
        """
        self.typesadded[member.maj_type].add(member.path)
        patches = []
        if member.path in list(self.paths.keys()):
            patches = self.paths[member.path].patches
        self.paths[member.path] = member
        self.paths[member.path].patches.extend([patch for patch in patches])

    def path(self, path):
        """Provide the response of requested path

        :param path: path of response requested
        :type path: str.
        :rtype: RestResponse
        """
        try:
            return self.paths[path]
        except:
            return None

    def update_progress(self):
        """Simple function to increment the dot progress"""
        if self.progress % 6 == 0:
            sys.stdout.write('.')

    def load(self, path=None, includelogs=False, init=False, \
            crawl=True, loadtype='href', loadcomplete=False, rel=False):
        """Walk entire RIS model and cache all responses in self.

        :param path: path to start load from.
        :type path: str.
        :param includelogs: flag to determine if logs should be downloaded also.
        :type includelogs: boolean.
        :param init: flag to determine if first run of load.
        :type init: boolean.
        :param crawl: flag to determine if load should traverse found links.
        :type crawl: boolean.
        :param loadtype: flag to determine if load is meant for only href items.
        :type loadtype: str.
        :param loadcomplete: flag to download the entire monolith
        :type loadcomplete: boolean
        :param rel: flag to reload the path specified
        :type rel: boolean

        """
        if init:
            if LOGGER.getEffectiveLevel() == 40:
                sys.stdout.write("Discovering data...")
            else:
                LOGGER.info("Discovering data...")
            self.name = self.name + ' at %s' % self._client().base_url

        selectivepath = path
        if not selectivepath:
            selectivepath = self._client().default_prefix

        self._load(selectivepath, crawl=crawl, includelogs=includelogs,\
             init=init, loadtype=loadtype, loadcomplete=loadcomplete, rel=rel)

        if init:
            if LOGGER.getEffectiveLevel() == 40:
                sys.stdout.write("Done\n")
            else:
                LOGGER.info("Done\n")

    def _load(self, path, crawl=True, originaluri=None, includelogs=False,\
                        init=True, loadtype='href', loadcomplete=False, \
                                                rel=False, prevpath=None):
        """Helper function to main load function.

        :param path: path to start load from.
        :type path: str.
        :param crawl: flag to determine if load should traverse found links.
        :type crawl: boolean.
        :param originaluri: variable to assist in determining originating path.
        :type originaluri: str.
        :param includelogs: flag to determine if logs should be downloaded also.
        :type includelogs: boolean.
        :param init: flag to determine if first run of load.
        :type init: boolean.
        :param loadtype: flag to determine if load is meant for only href items.
        :type loadtype: str.
        :param loadcomplete: flag to download the entire monolith
        :type loadcomplete: boolean

        """

        if path.endswith("?page=1") and not loadcomplete:
            return
        elif not includelogs and not crawl:
            if "/Logs" in path:
                return

        #TODO: need to find a better way to support non ascii characters
        path = path.replace("|", "%7C")
        #remove fragments
        newpath = urlparse(path)
        newpath = list(newpath[:])
        newpath[-1] = ''
        path = urlunparse(tuple(newpath))

        if prevpath and prevpath != path:
            self.ctree[prevpath].update([path])
        if not rel:
            if path.lower() in self.visited_urls:
                return
        LOGGER.debug('_loading %s', path)

        resp = self._client().get(path)

        if resp.status != 200 and path.lower() == self.typepath.defs.biospath:
            raise BiosUnregisteredError()
        elif resp.status == 401:
            raise SessionExpired("Invalid session. Please logout and "\
                                    "log back in or include credentials.")
        elif resp.status not in (201, 200):
            self.removepath(path)
            return

        if loadtype == "ref":
            try:
                if resp.status in (201, 200):
                    self.update_member(resp=resp, path=path, init=init)
                self.parse_schema(resp)
            except jsonpointer.JsonPointerException:
                raise SchemaValidationError()

        self.update_member(resp=resp, path=path, init=init)

        fpath = lambda pa, path: path if pa.endswith(self.typepath.defs.hrefstring) and \
            pa.startswith((self.collstr, 'Entries')) else None

        if loadtype == 'href':
            #follow all the href attributes
            if self.is_redfish:
                jsonpath_expr = jsonpath_rw.parse("$..'@odata.id'")
            else:
                jsonpath_expr = jsonpath_rw.parse('$..href')
            matches = jsonpath_expr.find(resp.dict)

            if 'links' in resp.dict and 'NextPage' in resp.dict['links']:
                if originaluri:
                    next_link_uri = originaluri + '?page=' + \
                                    str(resp.dict['links']['NextPage']['page'])
                    href = '%s' % next_link_uri

                    self._load(href, originaluri=originaluri, \
                               includelogs=includelogs, crawl=crawl, \
                               init=init, prevpath=None, loadcomplete=loadcomplete)
                else:
                    next_link_uri = path + '?page=' + \
                                    str(resp.dict['links']['NextPage']['page'])

                    href = '%s' % next_link_uri
                    self._load(href, originaluri=path, includelogs=includelogs,\
                        crawl=crawl, init=init, prevpath=None, loadcomplete=loadcomplete)

            matchrdirpath = next((match for match in matches if match.value == \
                                                    self._resourcedir), None)
            if not matchrdirpath and crawl:
                for match in matches:
                    if path == "/rest/v1" and not loadcomplete:
                        if str(match.full_path) == "links.Schemas.href" or \
                                str(match.full_path) == "links.Registries.href":
                            continue
                    elif not loadcomplete:
                        if str(match.full_path) == "Registries.@odata.id" or \
                                str(match.full_path) == "JsonSchemas.@odata.id":
                            continue

                    if match.value == path:
                        continue
                    elif not isinstance(match.value, six.string_types):
                        continue

                    href = '%s' % match.value
                    self._load(href, crawl=crawl, \
                       originaluri=originaluri, includelogs=includelogs, \
                       init=init, prevpath=fpath(str(match.full_path), path), \
                       loadcomplete=loadcomplete)
            elif crawl:
                href = '%s' % matchrdirpath.value
                self._load(href, crawl=crawl, originaluri=originaluri, \
                    includelogs=includelogs, init=init, prevpath=path, loadcomplete=loadcomplete)
            if loadcomplete:
                if path == '/rest/v1':
                    schemamatch = jsonpath_rw.parse('$..extref')
                else:
                    schemamatch = jsonpath_rw.parse('$..Uri')
                smatches = schemamatch.find(resp.dict)
                matches = matches + smatches
                for match in matches:
                    if isinstance(match.value, six.string_types):
                        self._load(match.value, crawl=crawl, originaluri=originaluri,\
                        includelogs=includelogs, init=init, loadcomplete=loadcomplete,\
                                     prevpath=fpath(str(match.full_path), path))

    def parse_schema(self, resp):
        """Function to get and replace schema $ref with data

        :param resp: response data containing ref items.
        :type resp: str.

        """
        #pylint: disable=maybe-no-member
        if not self.typepath.gencompany:
            return self.parse_schema_gen(resp)
        jsonpath_expr = jsonpath_rw.parse('$.."$ref"')
        matches = jsonpath_expr.find(resp.dict)
        respcopy = resp.dict
        typeregex = '([#,@].*?\.)'
        if matches:
            for match in matches:
                fullpath = str(match.full_path)
                jsonfile = match.value.split('#')[0]
                jsonpath = match.value.split('#')[1]
                listmatch = None
                found = None

                if 'redfish.dmtf.org' in jsonfile:
                    if 'odata' in jsonfile:
                        jsonpath = jsonpath.replace(jsonpath.split('/')[-1], \
                                            'odata' + jsonpath.split('/')[-1])
                    jsonfile = 'Resource.json'

                found = re.search(typeregex, fullpath)
                if found:
                    repitem = fullpath[found.regs[0][0]:found.regs[0][1]]
                    schemapath = '/' + fullpath.replace(repitem, '~').\
                                        replace('.', '/').replace('~', repitem)
                else:
                    schemapath = '/' + fullpath.replace('.', '/')

                if '.json' in jsonfile:
                    itempath = schemapath

                    if self.is_redfish:
                        if resp.request.path[-1] == '/':
                            newpath = '/'.join(resp.request.path.split('/')\
                                                [:-2]) + '/' + jsonfile + '/'
                        else:
                            newpath = '/'.join(resp.request.path.split('/')\
                                                [:-1]) + '/' + jsonfile + '/'
                    else:
                        newpath = '/'.join(resp.request.path.split('/')[:-1]) \
                                                                + '/' + jsonfile

                    if 'href.json' in newpath:
                        continue

                    if newpath.lower() not in self.visited_urls:
                        self.load(newpath, crawl=False, includelogs=False, \
                                                init=False, loadtype='ref')

                    instance = list()

                    #deprecated type "string" for Type.json
                    if 'string' in self.types:
                        for item in self.iter('string'):
                            instance.append(item)
                    if 'object' in self.types:
                        for item in self.iter('object'):
                            instance.append(item)

                    for item in instance:
                        if jsonfile in item.path:
                            if 'anyOf' in fullpath:
                                break

                            dictcopy = item.dict
                            listmatch = re.search('[[][0-9]+[]]', itempath)

                            if listmatch:
                                start = listmatch.regs[0][0]
                                end = listmatch.regs[0][1]

                                newitempath = [itempath[:start], itempath[end:]]
                                start = jsonpointer.JsonPointer(newitempath[0])
                                end = jsonpointer.JsonPointer(newitempath[1])

                                del start.parts[-1], end.parts[-1]
                                vals = start.resolve(respcopy)

                                count = 0

                                for val in vals:
                                    try:
                                        if '$ref' in six.iterkeys(end.resolve(val)):
                                            end.resolve(val).pop('$ref')
                                            end.resolve(val).update(dictcopy)
                                            replace_pointer = jsonpointer.\
                                                JsonPointer(end.path + jsonpath)

                                            data = replace_pointer.resolve(val)
                                            set_pointer(val, end.path, data)
                                            start.resolve(respcopy)[count].\
                                                                    update(val)

                                            break
                                    except:
                                        count += 1
                            else:
                                itempath = jsonpointer.JsonPointer(itempath)
                                del itempath.parts[-1]

                                if '$ref' in six.iterkeys(itempath.resolve(respcopy)):
                                    itempath.resolve(respcopy).pop('$ref')
                                    itempath.resolve(respcopy).update(dictcopy)
                                    break

                if jsonpath:
                    if 'anyOf' in fullpath:
                        continue

                    if not jsonfile:
                        replacepath = jsonpointer.JsonPointer(jsonpath)
                        schemapath = schemapath.replace('/$ref', '')
                        if re.search('\[\d]', schemapath):
                            schemapath = schemapath.translate(None, '[]')
                        schemapath = jsonpointer.JsonPointer(schemapath)
                        data = replacepath.resolve(respcopy)

                        if '$ref' in schemapath.resolve(respcopy):
                            schemapath.resolve(respcopy).pop('$ref')
                            schemapath.resolve(respcopy).update(data)

                    else:
                        if not listmatch:
                            schemapath = schemapath.replace('/$ref', '')
                            replacepath = schemapath + jsonpath
                            replace_pointer = jsonpointer.JsonPointer(replacepath)
                            data = replace_pointer.resolve(respcopy)
                            set_pointer(respcopy, schemapath, data)

            resp.loaddict(respcopy)
        else:
            resp.loaddict(respcopy)

    def parse_schema_gen(self, resp):
        """Redfish general function to get and replace schema $ref with data

        :param resp: response data containing ref items.
        :type resp: str.

        """
        #pylint: disable=maybe-no-member
        getval = lambda inmat: getval(inmat.left) + '/' + str(inmat.right) \
                            if hasattr(inmat, 'left') else str(inmat)
        respcopy = resp.dict
        jsonpath_expr = jsonpath_rw.parse('$.."anyOf"')
        while True:
            matches = jsonpath_expr.find(respcopy)
            if not matches:
                break
            match = matches[0]
            newval = None
            schlist = match.value
            schlist = [ele for ele in list(schlist) if ele != {"type":"null"}]
            norefsch = [ele for ele in list(schlist) if isinstance(ele, dict) and \
                                                                                len(ele.keys()) > 1]
            if norefsch:
                newval = norefsch[0]
            else:
                newsc = [ele for ele in list(schlist) if not ele["$ref"].split('#')[0]]
                newval = newsc[0] if newsc else None
                if not newval:
                    schlist = [ele["$ref"] for ele in list(schlist) if "$ref" in ele.keys() and \
                       (ele["$ref"].split('#')[0].endswith('.json') and 'odata' not in \
                       ele["$ref"].split('#')[0])]
                    maxsch = max(schlist)
                    newval = {"$ref":maxsch}

            itempath = '/' + getval(match.full_path)
            if re.search('\[\d+]', itempath):
                itempath = itempath.translate(None, '[]')
            itempath = jsonpointer.JsonPointer(itempath)
            del itempath.parts[-1]
            if 'anyOf' in six.iterkeys(itempath.resolve(respcopy)):
                itempath.resolve(respcopy).pop('anyOf')
                itempath.resolve(respcopy).update(newval)

        jsonpath_expr = jsonpath_rw.parse('$.."$ref"')
        matches = jsonpath_expr.find(respcopy)
        if matches:
            for _, match in enumerate(matches):
                jsonfile = match.value.split('#')[0]
                jsonfile = '' if jsonfile.lower() == resp.request.path.lower() else jsonfile
                jsonpath = match.value.split('#')[1]

                schemapath = '/' + getval(match.full_path)
                if jsonfile:
                    itempath = schemapath
                    if '/' not in jsonfile:
                        inds = -2 if resp.request.path[-1] == '/' else -1
                        jsonfile = '/'.join(resp.request.path.split('/')[:inds]) \
                                    + '/' + jsonfile + '/'
                    if jsonfile not in self.paths:
                        self.load(jsonfile, crawl=False, includelogs=False, \
                                                init=False, loadtype='ref')
                    item = self.paths[jsonfile] if jsonfile in self.paths else None

#                     if not item:
#                         if not 'anyOf' in schemapath:
#                             raise "We got a situation :|"
#                         continue
                    if re.search('\[\d+]', itempath):
                        itempath = itempath.translate(None, '[]')
                    itempath = jsonpointer.JsonPointer(itempath)
                    del itempath.parts[-1]
                    if '$ref' in six.iterkeys(itempath.resolve(respcopy)):
                        itempath.resolve(respcopy).pop('$ref')
                        itempath.resolve(respcopy).update(item.dict)

                if jsonpath:
                    schemapath = schemapath.replace('/$ref', '')
                    if re.search('\[\d+]', schemapath):
                        schemapath = schemapath.translate(None, '[]')
                    if not jsonfile:
                        replacepath = jsonpointer.JsonPointer(jsonpath)
                        schemapath = jsonpointer.JsonPointer(schemapath)
                        data = replacepath.resolve(respcopy)
                        if '$ref' in schemapath.resolve(respcopy):
                            schemapath.resolve(respcopy).pop('$ref')
                            schemapath.resolve(respcopy).update(data)
                    else:
                        replacepath = schemapath + jsonpath
                        replace_pointer = jsonpointer.\
                                                    JsonPointer(replacepath)
                        data = replace_pointer.resolve(respcopy)
                        set_pointer(respcopy, schemapath, data)

            resp.loaddict(respcopy)
        else:
            resp.loaddict(respcopy)

    def update_member(self, member=None, resp=None, path=None, init=True):
        """Adds member to this monolith. If the member already exists the
        data is updated in place.

        :param member: Ris monolith member object made by branch worker.
        :type member: RisMonolithMemberv100.
        :param resp: response received.
        :type resp: str.
        :param path: path correlating to the response.
        :type path: str.
        :param init: flag to determine if progress bar should be updated.
        :type init: boolean.

        """
        if not member and resp and path:
            self._visited_urls.append(path.lower())

            member = RisMonolithMemberv100(resp, self.is_redfish)
            if not member:#Assuming for lack of member and not member.type
                return
            if not member.type:
                member.deftype = 'object'#Hack for general schema with no type

        self.types = member

        if init:
            self.progress += 1
            if LOGGER.getEffectiveLevel() == 40:
                self.update_progress()

    def load_from_dict(self, src):
        """Load data to monolith from dict

        :param src: data receive from rest operation.
        :type src: str.

        """
        self._type = src['Type']
        self._name = src['Name']
        self.typesadded = defaultdict(set, {ki:set(val) for ki, val in src['typepath'].iteritems()})
        self.ctree = defaultdict(set, {ki:set(val) for ki, val in src['ctree'].iteritems()})
        self.colltypes = defaultdict(set, {ki:set(val) for ki, val in src['colls'].iteritems()})
        for _, resp in list(src['resps'].items()):
            member = RisMonolithMemberv100(None, self.is_redfish)
            member.load_from_dict(resp)
            self.update_member(member=member, init=False)
        return

    def to_dict(self):
        """Convert data to dict from monolith"""
        result = OrderedDict()
        result['Type'] = self.type
        result['Name'] = self.name
        result["typepath"] = self.typesadded
        result['ctree'] = self.ctree
        result['colls'] = self.colltypes
        result["resps"] = {x:v.to_dict() for x, v in list(self.paths.items())}
        return result

    @property
    def location(self):
        """Return current location"""
        return self._current_location

    @location.setter
    def location(self, newval):
        """Set current location"""
        self._current_location = newval

    def iter(self, typeval=None):
        """Returns each member of monolith

        :rtype: RisMonolithMemberv100
        """
        if not typeval:
            for _, val in self.paths.items():
                yield val
        else:
            for typename in self.gettypename(typeval):
                for item in self.typesadded[typename]:
                    yield self.paths[item]

    def itertype(self, typeval):
        """Returns member of given type in monolith

        :param typeval: type name of the requested response.
        :type typeval: str.

        :rtype: RisMonolithMemberv100
        """
        typeiter = self.gettypename(typeval)
        types = next(typeiter, None)
        if types:
            while types:
                for item in self.typesadded[types]:
                    yield self.paths[item]
                types = next(typeiter, None)
        else:
            raise RisInstanceNotFoundError("Unable to locate instance for" \
                                                            " '%s'" % typeval)

    def typecheck(self, types):
        """Check if a member of given type exists

        :param types: type name of the requested response.
        :type types: str.

        :rtype: bool.
        """
        if any(types in val for val in self.types):
            return True
        return False

    def gettypename(self, types):
        """Get the maj_type name of given type

        :param types: type name of the requested response.
        :type types: str.
        """
        types = types[1:] if types[0] in ("#", u"#") else types
        return iter((xt for xt in self.types if xt and types.lower() in xt.lower()))

    def markmodified(self, opath, path=None, modpaths=None):
        """Mark the paths to be modifed which are connected to current path.

        :param opath: original path which has been modified
        :type path: str
        :param path: path which has been modified
        :type path: str
        :param modpaths: paths in a list which has to be modified
        :type modpaths: set
        """
        modpaths = set() if modpaths is None else modpaths
        path = path if path else opath
        if not path:
            return
        modpaths.update(self.ctree[path] if path in self.ctree else set())
        self.paths[path].modified = True
        for npath in [unmodpath for unmodpath in modpaths if unmodpath \
                                        in self.paths and not self.paths[unmodpath].modified]:
            self.markmodified(opath, path=npath, modpaths=modpaths)
        return modpaths

    def checkmodified(self, opath, path=None, modpaths=None):
        """Check if the path or its children are modified.

        :param path: path which is to be checked if modified
        :type path: str
        """
        #return [paths for paths in self.ctree[path] if self.paths[paths].modified]
        modpaths = set() if modpaths is None else modpaths
        path = path if path else opath
        newpaths = set()
        if not path:
            return
        if path in self.paths and self.paths[path].modified:
            newpaths = set([conn for conn in self.ctree[path] if conn in \
                 self.paths and self.paths[path].modified]) - modpaths
            modpaths.update(newpaths|set([path]))
        for npath in [unmodpath for unmodpath in newpaths]:
            self.checkmodified(opath, path=npath, modpaths=modpaths)
        return modpaths

    def removepath(self, path):
        """Remove a given path from the cache

        :param path: path which is to be checked if modified
        :type path: str
        """
        if path in self._visited_urls:
            self._visited_urls.remove(path)
        if not path in self.paths:
            return
        if path in self.typesadded[self.paths[path].maj_type]:
            self.typesadded[self.paths[path].maj_type].remove(path)
        if not self.typesadded[self.paths[path].maj_type]:
            del self.typesadded[self.paths[path].maj_type]
        del self.paths[path]
        if path in self.ctree:
            del self.ctree[path]
        _ = [self.ctree[paths].remove(path) for paths in self.ctree if path in self.ctree[paths]]

    def populatecollections(self):
        """Populate the collections type and types depending on resourcedirectory"""
        if not self._resourcedir in self.paths:
            return
        self.colltypes = defaultdict(set)
        alltypes = []
        colls = []
        for item in self.paths[self._resourcedir].dict["Instances"]:
            #Fix for incorrect RDir instances.
            if not self.typepath.defs.typestring in item or item[self.typepath.defs.hrefstring] \
                                                                                    in self.paths:
                continue
            typename = ".".join(item[self.typepath.defs.typestring].split(".", 2)[:2])\
                                                                                    .split('#')[-1]
            _ = [alltypes.append(typename) if not 'Collection' in typename else None]
            _ = [colls.append(typename) if 'Collection' in typename else None]
            member = RisMonolithMemberv100(None, self.is_redfish)
            member.popdefs(typename, item[self.typepath.defs.hrefstring], item[self.etagstr])
            self.update_member(member=member, init=False)
        for coll in colls:
            collname = coll.split('Collection')[0].split('#')[-1]
            typename = next((name for name in alltypes if name.startswith(collname)), None)
            colltype = ".".join(coll.split(".", 2)[:2]).split('#')[-1]
            self.colltypes[typename].add(colltype)

    def capture(self, redmono=False):
        """Build and return the entire monolith

        :param redmono: Flag to return reduced monolith or not
        :type redmono: bool.
        """
        self.load(includelogs=True, crawl=True, loadcomplete=True, rel=True, init=True)
        return self.to_dict() if not redmono else {x:{"Headers":v.resp.getheaders(), \
                "Response":v.resp.dict} for x, v in list(self.paths.items()) if v}

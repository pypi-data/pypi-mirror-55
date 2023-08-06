#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright - See LICENSE for details
# Authors: Guannan Ma @mythmgn
"""
:description:
    amis proxy center
"""

import copy


__all__ = [
    'SimpleRender', 'Table',
    'Divider', 'Echarts', 'Tabs'
]


class SimpleRender(object):
    """
    amis formatter
    """
    AMIS_DATA = {
        'status': 0,
        'msg': 'ok'
    }

    def _new_data(self):
        """return new amis json data"""
        data = copy.deepcopy(self.AMIS_DATA)
        return data

    def nav(self, items, default_value):
        """
        :param items:
            should be like
            [ {'label': 'xxx', 'active':'xxx'},
            {'label': 'yyy', 'active': 'False'}]
        """
        data = self._new_data()
        data['data'] = {}
        data['data']['links'] = items
        data['data']['value'] = default_value
        return data

    def table(self, headers, rows, data_name=None, count=None):
        """
        return amis data for table
        """
        data = copy.deepcopy(self.AMIS_DATA)
        items = []
        for i in range(0, len(rows)):
            item = {}
            for colindex in range(0, len(headers)):
                item[headers[colindex]] = rows[i][colindex]
            items.append(item)
        data['data'] = {}
        tbl_dict = None
        if data_name is None:
            data['data'] = items
            tbl_dict = data
        else:
            data['data'][data_name] = items
            tbl_dict = data['data']
        if count is not None:
            tbl_dict['count'] = count
        return data

    def crud(self, headers, rows, count, data_name=None):
        """
        crud
        """
        data = copy.deepcopy(self.AMIS_DATA)
        items = []
        for i in range(0, len(rows)):
            item = {}
            for colindex in range(0, len(headers)):
                item[headers[colindex]] = rows[i][colindex]
            items.append(item)
        data['data'] = {}
        crud_dic = None
        if data_name is None:
            data['data']['rows'] = items
            crud_dic = data['data']
        else:
            data['data'][data_name] = {}
            data['data'][data_name]['rows'] = items
            crud_dic = data['data'][data_name]
        crud_dic['count'] = count
        return data

    def raw_json(self, datadict):
        """
        return raw json dict for amis
        """
        data = copy.deepcopy(self.AMIS_DATA)
        data['data'] = datadict
        return data


class BaseRender(object):
    """
    Amis Base Render
    """
    def __init__(self, schema_url, obj_type):
        """
        """
        self._schema_url = schema_url
        self._type = obj_type
        self._rawdata = {
            'type': obj_type
        }
        if schema_url is not None:
            self._rawdata['$schema'] = self._schema_url

    def render(self):
        """
        render json string
        """
        renderdict = {
            'status':0,
            'msg':'',
            'data': self._rawdata
        }
        return renderdict

    def default_fill(self, kvs):
        """
        fill the object with default attribute(key/value)
        """
        if kvs is not None:
            self._rawdata.update(kvs)

    def set_attr(self, key, value):
        """
        set attr for the table
        """
        self._rawdata[key] = value

    @property
    def jsondict(self):
        """
        return jsondict of this component
        """
        return self._rawdata


class Table(BaseRender):
    """
    amis table
    """
    def __init__(self):
        """
        """
        BaseRender.__init__(
            self, 'https://houtai.baidu.com/v2/schemas/table.json#',
            'table'
        )
        self.default_fill({
            'affixHeader': True,
            'columnsTogglable': 'auto',
            'placeholder': 'no avaliable data',
            'className': 'panel-default',
            'tableClassName': 'table-db table-striped',
            'headerClassName': 'crud-table-header',
            'footerClassName': 'crud-table-footer',
            'toolbarClassName': 'crud-table-toolbar'
        })
        self._rawdata['data'] = {'items':[]}
        self._rawdata['columns'] = []

    def set_title(self, title):
        """
        set title for the table
        """
        self._rawdata['title'] = title

    def add_column(self, col_type, label, name):
        """
        add column into amis table
        """
        self._rawdata['columns'].append({
            'label': label,
            'type': col_type,
            'name': name
        })

    def set_columns(self, column_list):
        """
        set columns
        """
        self._rawdata['columns'] = []
        self._rawdata['columns'].extend(column_list)

    def clear_columns(self):
        """
        clear columns of the table
        """
        self._rawdata['columns'] = []

    def set_rows(self, rows):
        """
        set rows for the table

        :param rows:
            [{'col_name_1': xxx, 'col_name_2': xxx,...}, ...]
        """
        self._rawdata['data']['items'] = rows


class Divider(BaseRender):
    """
    amis separator
    """
    def __init__(self, **kwargs):
        """
        amis separator
        """
        BaseRender.__init__(
            self, None,
            'divider'
        )
        self.default_fill(kwargs)


class Echarts(BaseRender):
    """
    echarts in amis
    """
    def __init__(self, tabnum=1, **kwargs):
        BaseRender.__init__(
            self, None,
            'chart'
        )
        # self._tabnum = tabnum
        # self._tabs = [{} for _ in range(self._tabnum)]
        if kwargs is not None:
            for key, value in kwargs:
                self.set_attr(key, value)

    def config(self, jsondict):
        """
        :param jsondict should be a json dict which configure echarts.
        """
        self._rawdata['config'] = jsondict


class Tabs(BaseRender):
    """
    amis tabs
    """
    def __init__(self, **kwargs):
        BaseRender.__init__(
            self, 'https://houtai.baidu.com/v2/schemas/tabs.json#',
            'tabs'
        )
        self._rawdata['tabs'] = []
        if kwargs is not None:
            for key, value in kwargs:
                self.set_attr(key, value)

    def count(self):
        """return tabs num of the AmisTabs"""
        return len(self._rawdata['tabs'])

    def add_tab(self, title):
        """
        :param bodydict:
            should be a sub-class object of BaseRender
        """
        tempdict = {'title': title, 'body': []}
        self._rawdata['tabs'].append(tempdict)

    def set_tab(self, tabindex, title, bodydict):
        """
        set tab with tabindex
        """
        if tabindex >= len(self._rawdata['tabs']):
            raise ValueError('tabindex out of boundary')
        self._rawdata['tabs'][tabindex]['title'] = title
        self._rawdata['tabs'][tabindex]['body'] = bodydict

    def add_component(self, tabindex, component):
        """
        :param tabindex
            should be less than (tabnum - 1)
        """
        if not isinstance(component, BaseRender):
            raise TypeError('is not supported amis component')
        self._rawdata['tabs'][tabindex]['body'].append(
            component.jsondict
        )

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent

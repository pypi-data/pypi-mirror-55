# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 17:11
# @Author  : floatsliang
# @File    : parser.py
import json
from typing import List, Tuple, Dict
from datetime import datetime, date


def _serialize(val):
    if isinstance(val, dict):
        val = u"'{}'".format(json.dumps(val))
    elif isinstance(val, (datetime, date)):
        val = u"'{}'".format(str(val))
    else:
        val = u"'{}'".format(val)
    return val


def parse_labels(labels: List[str], div=':') -> str:
    parsed_labels = []
    for label in labels:
        parsed_labels.append(label)
    return ':' + div.join(parsed_labels) if parsed_labels else ''


def parse_fields(fields: List[str]) -> str:
    for idx, field in enumerate(fields):
        if '__' in field:
            fields[idx] = field.replace('__', '.', 1)
        else:
            pass
    return ', '.join(fields)


def parse_order_by(order_by: List[List or Tuple]) -> str:
    order_bys = []
    for field, order in order_by:
        if '__' in field:
            field = field.replace('__', '.', 1)
        elif '.' in field:
            pass
        else:
            raise Exception(u'ERROR: expected order by property format: '
                            u'[node].[property] or [node]__[property], got {}'.format(field))
        order_bys.append(u'{} {}'.format(field, order))
    if order_bys:
        return 'ORDER BY {}'.format(','.join(order_bys))
    else:
        return ''


def parse_terms(terms: Dict) -> str:
    filters = []
    for field, term in terms.items():
        if '__' in field:
            field = field.replace('__', '.', 1)
        elif '.' in field:
            pass
        else:
            raise Exception(u'ERROR: expected where filter property format: '
                            u'[node].[property] or [node]__[property], got {}'.format(field))
        if isinstance(term, (list, tuple)):
            op = term[1].strip()
            if len(term) == 3:
                relation = u' {} '.format(term[2].strip()).upper()
            else:
                relation = ' AND '
            values = term[0]
            if op.lower() == 'in':
                if isinstance(values, (list, tuple)):
                    values = [_serialize(val) for val in values if val is not None]
                    if values:
                        filters.append(u'{} IN [{}]'.format(field, ', '.join(values)))
                else:
                    if values is not None:
                        values = _serialize(values)
                        filters.append(u'{} = {}'.format(field, values))
            elif op.lower() == 'join':
                if isinstance(values, (list, tuple)):
                    values = [val.replace('__', '.', 1) for val in values if val is not None]
                    if values:
                        filters.append(u'({})'.format(
                            relation.join([u'{} = {}'.format(field, val) for val in values])))
                else:
                    if values is not None:
                        filters.append(u'{} = {}'.format(field, values.replace('__', '.', 1)))
            else:
                if isinstance(values, (list, tuple)):
                    values = [_serialize(val) for val in values if val is not None]
                    if values:
                        filters.append(u'({})'.format(
                            relation.join([u'{} {} {}'.format(field, op, val) for val in values])))
                else:
                    if values is not None:
                        values = _serialize(values)
                        filters.append(u'{} {} {}'.format(field, op, values))
        else:
            if term is not None:
                term = _serialize(term)
                filters.append(u'{}={}'.format(field, term))
    filters = ' AND '.join(filters)
    return filters


def parse_properties(properties: Dict, eq=':') -> str:
    property_list = []
    for key, val in properties.items():
        if val is not None:
            if '__' in key:
                key = key.replace('__', '.', 1)
            elif '.' not in key and eq != ':':
                raise Exception('ERROR: expected property name format: '
                                '[node].[property] or [node]__[property], got {}'.format(key))
            property_list.append(u'{}{}{}'.format(key, eq, _serialize(val)))
    properties = ', '.join(property_list)
    return properties

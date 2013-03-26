from __future__ import unicode_literals
import warnings

from django.utils.safestring import mark_safe

import django_tables2 as tables
from django_tables2.utils import AttributeDict
from django_tables2.columns.base import Column, library

import settings
import master_checkbox.settings

class Meta():
    orderable=False
    attrs = {
        "class":settings.TABLE_CLASS,
    }

class Datatable(tables.Table):

    def _get_table_filter(self):
        """a datatables based filter for the given table
        
        the filter is itself a table
        """

        id = self.__class__.Meta.attrs['id']

        class TableFilter(tables.Table):

            target = tables.Column()

            find = TextColumn(
                attrs={
                    'td__input':{settings.FILTER_TABLE_FIND_ATTR:id},
                }
            )
            
            regex = MasterCheckBoxColumn(
                "regex",
                th__before_input='regex',
                attrs={
                    'td__input':{settings.FILTER_TABLE_REGEX_ATTR:id},
                }
            )

            smart = MasterCheckBoxColumn(
                "smart",
                th__before_input='smart',
                attrs={
                    'td__input':{settings.FILTER_TABLE_SMART_ATTR:id},
                }
            )

            class Meta():
                orderable=False

        data = [
            {'target':'global', },
        ]

        return TableFilter(data)


    def __init__(self,*args,**kwargs):
        super(Datatable,self).__init__(*args,**kwargs)
        self.filter = self._get_table_filter()

class MasterCheckBoxColumn(tables.CheckBoxColumn):
    """sortable checkbox column with a box to select/deselect all at once

    :param master_group: passed as
        attrs["th__input"][master_checkbox.settings.SLAVE_GROUP_ATTR]
        and
        attrs["td__input"][master_checkbox.settings.MASTER_GROUP_ATTR]
        to django_tables2.CheckBoxColumn.__init__()
    :type master_group: str
    :param form: passed as attrs["td__input"]["form"] to django_tables2.CheckBoxColumn.__init__()
    :type form: str
    :param name: passed as attrs["td__input"]["name"] to django_tables2.CheckBoxColumn.__init__()
    :type name: str

    :example:

        import django_tables2_datatables as dtd_tables
    
        class SomeTable(tables.Table):

            selection = dtd_tables.MasterCheckBoxColumn(
                    "master-group",        #<th><input settings.MASTER_GROUP_ATTR="$master_group">, <td><input settings.SLAVE_OF_ATTR="$master_group">
                    name="name",           #<td><input name="$name">
                    form="form",           #<td><input form="$form">
                    accessor="groupname",  #see django_tables2.ChekBoxColumn
                )
    """

    def __init__(
                self,
                master_group='select-group',
                *args,
                **kwargs
            ):

        attrs = kwargs.get('attrs',{})

        attrs["th"] = attrs.get("th",{})
        attrs["th"]["class"] = attrs["th"].get("class","") + ' ' + settings.FILTER_CHECKBOX_CLASS

        attrs["th__input"] = attrs.get("th__input",{})
        attrs["th__input"][master_checkbox.settings.MASTER_GROUP_ATTR] = master_group

        attrs["td__input"] = attrs.get("td__input",{})
        attrs["td__input"][master_checkbox.settings.SLAVE_GROUP_ATTR] = master_group

        form = kwargs.pop("form",None)
        if form:
            attrs["td__input"]["form"] = form

        name = kwargs.pop("name",None)
        if name:
            attrs["td__input"]["name"] = name

        kwargs['attrs'] = attrs

        kwargs['empty_values'] = kwargs.get('empty_values',())

        super(MasterCheckBoxColumn,self).__init__(*args,**kwargs)

class LinkColumn(tables.LinkColumn):
    """column of links. search and sort ignore the anchor tag"""

    def __init__(
                self,
                *args,
                **kwargs
            ):

        attrs = kwargs.get('attrs',{})
        attrs["th"] = attrs.get("th",{})
        attrs["th"]["class"] = attrs["th"].get("class","") + ' ' + settings.FILTER_HTML_CLASS
        kwargs['attrs'] = attrs

        super(LinkColumn,self).__init__(*args,**kwargs)


@library.register
class TextColumn(Column):
    """text input elements

    TODO factor out with CheckBoxColumn and pull request
    """
    def __init__(self, attrs=None, **extra):
        valid = set(("input", "th__input", "td__input", "th", "td", "cell"))
        if attrs and not set(attrs) & set(valid):
            warnings.warn('attrs keys must be one of %s, interpreting as {"td__input": %s}'
                          % (', '.join(valid), attrs), DeprecationWarning)
            attrs = {"td__input": attrs}
        if "header_attrs" in extra:
            warnings.warn('header_attrs argument is deprecated, '
                          'use attrs={"th__input": ...} instead',
                          DeprecationWarning)
            attrs.setdefault('th__input', {}).update(extra.pop('header_attrs'))

        kwargs = {b'orderable': False, b'attrs': attrs}
        kwargs.update(extra)
        kwargs['empty_values'] = kwargs.get('empty_values',())
        super(TextColumn, self).__init__(**kwargs)

    def render(self, value, bound_column):  # pylint: disable=W0221
        default = {
            'type': 'text',
            'name': bound_column.name,
        }
        general = self.attrs.get('input')
        specific = self.attrs.get('td__input')
        attrs = AttributeDict(default, **(specific or general or {}))
        return mark_safe('<input %s/>' % attrs.as_html())

from django.conf import settings

#TODO IMPLEMENT
#CLASS_PREFIX = getattr(settings,
        #'DATATABLE_CLASS_PREFIX',
        #'datatable',
    #)

#CLASS_SEPARATOR = getattr(settings,
        #'DATATABLE_CLASS_SEPARATOR',
        #'_',
    #)

#ATTR_PREFIX = getattr(settings,
        #'DATATABLE_ATTR_PREFIX',
        #'datatable',
    #)

#ATTR_SEPARATOR = getattr(settings,
        #'DATATABLE_ATTR_SEPARATOR',
        #'_',
    #)

#<th class="CHECKBOX_CLASS ...">
FILTER_HTML_CLASS = getattr(settings,
    'DATATABLE_FILTER_HTML_CLASS',
    'datatable_filter_html',
)

#<th class="CHECKBOX_CLASS ...">
FILTER_CHECKBOX_CLASS = getattr(settings,
    'DATATABLE_FILTER_CHECKBOX_CLASS',
    'datatable_filter_checkbox',
)


FILTER_TABLE_FIND_ATTR = getattr(settings,
    'DATATABLE_FILTER_TARGET_TABLE_ATTR',
    'datatable_filter_target',
)

FILTER_TABLE_REGEX_ATTR = getattr(settings,
    'DATATABLE_FILTER_REGEX_CLASS',
    'datatable_filter_regex'
)

FILTER_TABLE_SMART_ATTR = getattr(settings,
    'DATATABLE_FILTER_SMART_CLASS',
    'datatable_filter_smart'
)

FILTER_COL_FIND_ATTR = getattr(settings,
    'DATATABLE_FILTER_COL_FIND_CLASS',
    'datatable_filter_col_find'
)

FILTER_COL_REGEX_ATTR = getattr(settings,
    'DATATABLE_FILTER_COL_REGEX_CLASS',
    'datatable_filter_col_regex'
)

FILTER_COL_SMART_ATTR = getattr(settings,
    'DATATABLE_FILTER_COL_SMART_CLASS',
    'datatable_filter_col_smart'
)

#<th class="HTML_CLASS ...">
FILTER_HTML_CLASS = getattr(settings,
    'DATATABLE_HTML_CLASS',
    'html',
)

TABLE_CLASS = getattr(settings,
    'DATATABLE_TABLE_CLASS',
    'datatable',
)

CONTEXT = {
    'datatable_table_class': TABLE_CLASS,
    'datatable_filter_table_find_attr': FILTER_TABLE_FIND_ATTR,
    'datatable_filter_table_regex_attr': FILTER_TABLE_REGEX_ATTR,
    'datatable_filter_table_smart_attr': FILTER_TABLE_SMART_ATTR,
    'datatable_filter_col_find_attr': FILTER_COL_FIND_ATTR,
    'datatable_filter_col_regex_attr': FILTER_COL_REGEX_ATTR,
    'datatable_filter_col_smart_attr': FILTER_COL_SMART_ATTR,
    'datatable_filter_html_class': FILTER_HTML_CLASS,
    'datatable_filter_checkbox_class': FILTER_CHECKBOX_CLASS,
}



from settings import *

def processor(request):

    return {
            'datatable_table_class' : TABLE_CLASS,
            'datatable_filter_target_table_attr' : FILTER_TARGET_TABLE_ATTR,
            'datatable_filter_target_col_attr' : FILTER_TARGET_COL_ATTR,
            'datatable_filter_find_class' : FILTER_FIND_CLASS,
            'datatable_filter_regex_class' : FILTER_REGEX_CLASS,
            'datatable_filter_smart_class' : FILTER_SMART_CLASS,
            'datatable_filter_col_find_class' : FILTER_COL_FIND_CLASS,
            'datatable_filter_col_regex_class' : FILTER_COL_REGEX_CLASS,
            'datatable_filter_col_smart_class' : FILTER_COL_SMART_CLASS,
            'datatable_filter_html_class' : FILTER_HTML_CLASS,
            'datatable_filter_checkbox_class' : FILTER_CHECKBOX_CLASS,
        }



from django import template

register = template.Library()

# TAGS FOR PASSING ID TO HTML ELEMENTS
@register.simple_tag
def modal_id():
    return "ajax-modal"

@register.simple_tag
def table_id():
    return "ajax-table"

@register.simple_tag
def form_id():
    return "ajax-filter"

@register.simple_tag
def message_id():
    return "ajax-message"

@register.simple_tag
def pagination_id():
    return "ajax-pagination"

# TAGS TO RENDER ELEMENTS
@register.inclusion_tag('partials/modal.html')
def ajax_modal():
    return {}

@register.inclusion_tag('partials/message.html')
def ajax_message():
    return {}

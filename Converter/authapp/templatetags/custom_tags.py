from django import template
import datetime
register = template.Library()

# def modify_name(value, arg):
#     if arg == "first_name":
#         return value.split(" ")[0]
#     if arg == "last_name":
#         return value.split(" ")[-1]
#     return value
    
# register.filter('modify_name', modify_name)




@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)
from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def int_range(tot, shift=0):
    if not tot:
        return None
    return range(0 + int(shift), int(tot) + int(shift))


@register.filter
def sub(number, subtract):
    try:
        number + 1
        try:
            subtract = float(subtract)
        except:
            return number
        return number - subtract
    except:
        return number


@register.filter
def dk(dictionary, dict_key):
    if not dictionary:
        return None
    element = None
    if dictionary:
        if dict_key in dictionary.keys():
            return dictionary[dict_key]
        if str(dict_key) in dictionary.keys():
            return dictionary[str(dict_key)]
    return element


@register.filter
def listsort(list_to_sort):
    sorted_list = None
    if isinstance(list_to_sort, (list, set, tuple)):
        sorted_list = sorted(list_to_sort)
    elif isinstance(list_to_sort, dict):
        sorted_list = sorted(list_to_sort.keys())
    return sorted_list


@register.filter
def sorteddictitems(dict_to_sort):
    sorted_list = []
    for k in sorted(dict_to_sort.keys()):
        sorted_list.append((k, dict_to_sort[k]))
    return sorted_list


@register.filter
def obj_to_dict(obj):
    dictionary = None
    if obj:
        try:
            dictionary = vars(obj)
        except:
            dictionary = {}
    return dictionary


@register.filter
def timedelta_dict_to_string(t_dict):
    res = ''
    if t_dict['days']:
        res += '%s days ' % t_dict['days']
    if t_dict['hours']:
        res += '%s hours ' % t_dict['hours']
    if t_dict['minutes']:
        res += '%s min ' % t_dict['minutes']
    if t_dict['seconds']:
        res += '%s sec' % t_dict['seconds']
    if res == '':
        res = '0 sec'
    return res.strip()


@register.filter
def hours_to_timedelta(hours_str):
    from datetime import timedelta
    hours_array = hours_str.split(':')
    try:
        time = str(timedelta(hours=int(hours_array[0]),
                             minutes=int(hours_array[1]),
                             seconds=int(hours_array[2])))
        time = time.replace(', 0:00:00', '')
    except:
        time = ''
    return time


@register.filter
def hours_to_seconds(hours_str):
    hours_array = hours_str.split(':')
    try:
        time = int(hours_array[0]) * 60 * 60 + \
                int(hours_array[1]) * 60 + \
                int(hours_array[2])
    except:
        time = 0
    return time


@register.simple_tag
def generate_uuid4():
    import uuid
    return uuid.uuid4()


@register.simple_tag
def obj_method(obj, method_name, *args):
    try:
        value = getattr(obj, method_name)(*args)
    except Exception as e:
        value = e
    return value


@register.filter(name='in_group')
def in_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()

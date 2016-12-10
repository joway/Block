import markdown2
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from . import register


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def markup(value):
    modified = value.replace('```', '  ')
    return mark_safe(markdown2.markdown(modified)
                     )

from django.template import Library, Node, Variable
from re import split

register = Library()


class AddGetParameter(Node):
    def __init__(self, values):
        self.values = values

    def render(self, context):
        req = Variable('request').resolve(context)
        params = req.GET.copy()
        for key, value in self.values.items():
            params[key] = str(Variable(value).resolve(context))
        return f'?{params.urlencode()}'


@register.tag
def add_get(parser, token):
    try:
        contents = split(r'\s+', token.contents, 2)[1]
        pairs = split(r',', contents)
    except:
        pairs = []
    values = {}
    for pair in pairs:
        s = split('=', pair, 2)
        values[s[0]] = s[1]
    return AddGetParameter(values)

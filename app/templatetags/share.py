from django import template
from django.template.loader import get_template
from django.template import Context
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import stringfilter

register = template.Library()

class ShareNode(template.Node):
	def __init__(self, obj):
		self.obj = obj
		
	def render(self, context):
		resolved = self.obj.resolve(context)
		
		try:
			getattr(resolved, 'get_share_url')
			getattr(resolved, 'get_share_description')
		except:
			raise template.TemplateSyntaxError, 'Parameter must be an object with a "get_share_url" and a "get_share_description" method.'
		
		return get_template('share_links.html').render(Context({
			'url': resolved.get_share_url(),
			'content': resolved.get_share_description(),
			'title': getattr(resolved, 'get_share_title', lambda: None)()											
		}))
	
@register.tag
def get_share_links(parser, token):
	obj = token.split_contents()[1]
	
	try:
		obj = template.Variable(obj)
	except:
		raise template.TemplateSyntaxError, 'Unable to resolve %s.' % obj
	
	return ShareNode(obj)

@register.filter(name="plus_spaces")
def plus_spaces(value, *args):
	return value.replace(' ', '+').replace('%20', '+')
plus_spaces.is_safe = True
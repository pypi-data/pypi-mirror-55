"""
Copyright 2019 Zakru

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from .requests import requestList, request, ObjectFromDict

def getIngredientNames():
	"""Gets a :class:`list` of :class:`str` objects containing all
	ingredient names from the Wynncraft API. Uses
	https://docs.wynncraft.com/Ingredient-API/#list.
	
	:returns: A list of all ingredient names as :class:`str`
	:rtype: :class:`list`
	"""
	return requestList('https://api.wynncraft.com/v2/ingredient/list')

def getIngredient(name):
	"""Gets an Ingredient as an
	:class:`ObjectFromDict <wynn.requests.ObjectFromDict>` object from
	the Wynncraft API. Uses
	https://docs.wynncraft.com/Ingredient-API/#get.
	
	:param name: The name of the Ingredient
	:type name: :class:`str`
	
	:returns: The Ingredient returned by the API
	:rtype: :class:`ObjectFromDict <wynn.requests.ObjectFromDict>`
	"""
	return ObjectFromDict(request(
		'https://api.wynncraft.com/v2/ingredient/get/{0}',
		n.replace(' ', '_')
		))

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

from .requests import requestList, requestObject, ObjectFromDict


def getRecipeIDs():
    """Gets a :class:`list` of :class:`str` objects containing all
    recipe IDs from the Wynncraft API.

    :returns: A list of all recipeIDs as :class:`str`
    :rtype: :class:`list`
    """
    return requestList('https://api.wynncraft.com/v2/recipe/list')


def getRecipe(id):
    """Gets a Recipe as an
    :class:`ObjectFromDict <wynn.requests.ObjectFromDict>` object from
    the Wynncraft API.

    Format: https://docs.wynncraft.com/Recipe-API/#recipe-object

    :param name: The ID of the Recipe
    :type name: :class:`str`

    :returns: The Recipe returned by the API
    :rtype: :class:`ObjectFromDict <wynn.requests.ObjectFromDict>`
    """
    return ObjectFromDict(requestObject(
        'https://api.wynncraft.com/v2/recipe/get/{0}',
        id
        ))

def searchRecipes(query, args):
    """Searches for recipes from the Wynncraft API. See
    https://docs.wynncraft.com/Recipe-API/#search for query
    format.

    :param query: See above link
    :type query: :class:`str`
    :param args: See above link
    :type args: :class:`str`

    :returns: A list of recipes as
       :class:`ObjectFromDict <wynn.requests.ObjectFromDict>`
    :rtype: :class:`list`
    """
    return map(ObjectFromDict, requestList(
        'https://api.wynncraft.com/v2/recipe/search/{0}/{1}',
        query, args,
        ))

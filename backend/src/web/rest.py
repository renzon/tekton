# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton.gae.middleware.json_middleware import JsonResponse, JsonUnsecureResponse


def items():
    return JsonResponse({'data': [1, 2, 3]})

def unsecure():
    return JsonUnsecureResponse({'data': [1, 2, 3]})
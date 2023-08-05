#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from xoeuf import api, fields, models
from xoeuf.models.extensions import get_ref


class FooBar(models.Model):
    _name = "test_xoeuf_models.foobar"
    name = fields.Text()

    @api.model
    def get_ref(self, ref):
        return get_ref(self, ref)

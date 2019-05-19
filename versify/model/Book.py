#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Book:
    def __init__(self, testament, name, code, position):
        self.testament = testament
        self.name = name
        self.code = code
        self.position = position
        self.chapters = []

    def get_chapters(self):
        return self.chapters

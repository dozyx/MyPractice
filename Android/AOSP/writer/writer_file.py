#!/usr/bin/env python
# -*- coding: utf-8 -*-

file_object = open('default.xml')

change_content = ''
while 1:
    line = file_object.readline()
    if not line.__contains__('clone-depth'):
        try:
            endpos = line.index("/>")
            line = line[0:endpos] + ' clone-depth="1"' + line[endpos: line.__len__()]
            pass
        except Exception, e:
            pass

    change_content += line
    if not line:
        break
    pass  # do something

print change_content
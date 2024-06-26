# -*- coding: UTF-8 -*-
#
# Copyright (c) 2009-2010 Ars Aperta, Itaapy, Pierlis, Talend.
#
# Authors: Hervé Cauwelier <herve@itaapy.com>
#          David Versmisse <david.versmisse@itaapy.com>
#
# This file is part of Lpod (see: http://lpod-project.net).
# Lpod is free software; you can redistribute it and/or modify it under
# the terms of either:
#
# a) the GNU General Public License as published by the Free Software
#    Foundation, either version 3 of the License, or (at your option)
#    any later version.
#    Lpod is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with Lpod.  If not, see <http://www.gnu.org/licenses/>.
#
# b) the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#

# Import from the Standard Library
from datetime import date, time, timedelta
from os import mkdir
from os.path import exists
from sys import version_info

# Import from PIL
from PIL import Image

# Import from lpod
from lpod.document import odf_new_document
from lpod.paragraph import odf_create_paragraph
from lpod.heading import odf_create_heading
from lpod.frame import odf_create_frame
from lpod.image import odf_create_image
from lpod.style import odf_create_style, rgb2hex
from lpod.variable import odf_create_variable_decl
from lpod.variable import odf_create_variable_set, odf_create_variable_get
from lpod.variable import odf_create_user_field_decl
from lpod.variable import odf_create_user_field_get
from lpod.variable import odf_create_page_number_variable
from lpod.variable import odf_create_page_count_variable
from lpod.variable import odf_create_date_variable, odf_create_time_variable
from lpod.variable import odf_create_chapter_variable
from lpod.variable import odf_create_filename_variable
from lpod.table import odf_create_table
from lpod import __version__, __installation_path__


# Hello messages
print('lpod installation test')
print(' Version           : %s' %  __version__)
print(' Installation path : %s' % __installation_path__)
print()
print('Generating test_output/use_case2.odt ...')

# Go
document = odf_new_document('text')
body = document.get_body()

# 0- The image
# ------------
image = Image.open('samples/image.png')
width, height = image.size
paragraph = odf_create_paragraph(style="Standard")
# 72 ppp
frame = odf_create_frame('frame1', 'Graphics',
                         str(width / 72.0) + 'in',
                         str(height / 72.0) + 'in')
internal_name = 'Pictures/image.png'
image = odf_create_image(internal_name)
frame.append(image)
paragraph.append(frame)
body.append(paragraph)

# And store the data
container = document.container
container.set_part(internal_name, open('samples/image.png').read())


# 1- Congratulations (=> style on paragraph)
# ------------------------------------------
heading = odf_create_heading(1, text='Congratulations !')
body.append(heading)

# The style
style = odf_create_style('paragraph', "style1", parent="Standard",
        area='text', color=rgb2hex('blue'), background_color=rgb2hex('red'))
document.insert_style(style)

# The paragraph
text =  'This document has been generated by the lpOD installation test.'
paragraph = odf_create_paragraph(text, style="style1")
body.append(paragraph)


# 2- Your environment (=> a table)
# --------------------------------
heading = odf_create_heading(1, text='Your environment')
body.append(heading)

data = []

# lpOD Version
data.append(['lpOD library version', __version__])

# Python version
data.append(['Python version', '%d.%d.%d' % version_info[:3]])

# Creation / Insertion
table = odf_create_table('table1', width=2, height=2, style="Standard")
table.set_values(data)
body.append(table)


# 3- Description (=> footnote & => highlight)
# -------------------------------------------

heading = odf_create_heading(1, text='Description')
body.append(heading)

# A paragraph with a note
text = 'The lpOD project is made to generate easily OpenDocuments.'
paragraph = odf_create_paragraph(text, style="Standard")
paragraph.insert_note(after="lpOD project", note_id='note1',
    citation='1', body='http://lpod-project.net/')
body.append(paragraph)

# A paragraph with a highlighted word

# The style
style = odf_create_style('text', "style2", parent="Standard", area='text',
        background_color=rgb2hex('yellow'))
document.insert_style(style)

# The paragraph
text = ('The office document file format OpenDocument Format (ODF) '
        'is an ISO standard ISO 26300 used by many applications.')
paragraph = odf_create_paragraph(text, "Standard")
paragraph.set_span("style2", regex="ISO standard")
body.append(paragraph)


# 4- A variable
# -------------

# A variable "spam" with the value 42
variable_set = odf_create_variable_set('spam', 42)
value_type = variable_set.get_attribute('office:value-type')
variable_decl = odf_create_variable_decl('spam', value_type)

# Insert
heading = odf_create_heading(1, text='A variable')
body.append(heading)

decl = body.get_variable_decls()
decl.append(variable_decl)

text = 'Set of spam.'
paragraph = odf_create_paragraph(text, style="Standard")
body.append(paragraph)
paragraph._insert_between(variable_set, "Set", "spam.")

text = 'The value of spam is: '
value = body.get_variable_set_value('spam')
variable_get = odf_create_variable_get('spam', value)
paragraph = odf_create_paragraph(text, style="Standard")
body.append(paragraph)
paragraph.insert_variable(variable_get, "is: ")


# 5- An user field
# ----------------

# An user field "pi5" with the value 3.14159
user_field_decl = odf_create_user_field_decl('pi5', value=3.14159)

# Insert
heading = odf_create_heading(1, text='An user field')
body.append(heading)

decl = body.get_user_field_decls()
decl.append(user_field_decl)

text = 'The value of pi5 is: '
value = body.get_user_field_value('pi5')
user_field_get = odf_create_user_field_get('pi5', value)
paragraph = odf_create_paragraph(text, style="Standard")
body.append(paragraph)
paragraph._insert_between(user_field_get, "The", "is: ")


# 6- Page number
# --------------

heading = odf_create_heading(1, text='Page number')
body.append(heading)

text1 = 'The current page is: '
text2 = 'The previous page is: '
text3 = 'The next page is: '
text4 = 'The total page number is: '

paragraph = odf_create_paragraph(text1, style="Standard")
body.append(paragraph)
paragraph.insert_variable(odf_create_page_number_variable(), "is: ")

paragraph = odf_create_paragraph(text2, style="Standard")
body.append(paragraph)
paragraph.insert_variable(odf_create_page_number_variable(select_page='previous'),
        "is: ")

paragraph = odf_create_paragraph(text3, style="Standard")
body.append(paragraph)
paragraph.insert_variable(odf_create_page_number_variable(select_page='next'),
        "is: ")

paragraph = odf_create_paragraph(text4, style="Standard")
body.append(paragraph)
paragraph.insert_variable(odf_create_page_count_variable(), "is: ")


# 7- Date
# -------

heading = odf_create_heading(1, text='Date insertion')
body.append(heading)

text1 = 'A fixed date: '
text2 = 'Today: '

paragraph = odf_create_paragraph(text1, style="Standard")
body.append(paragraph)
paragraph.insert_variable(odf_create_date_variable(date(2009, 7, 20),
    fixed=True), "date: ")

paragraph = odf_create_paragraph(text2, style="Standard")
body.append(paragraph)
paragraph.insert_variable(odf_create_date_variable(date(2009, 7, 20)),
    "Today: ")


# 8- Time
# --------

heading = odf_create_heading(1, text='Time insertion')
body.append(heading)

text1 = 'A fixed time: '
text2 = 'Now: '
text3 = 'In 1 hour: '

paragraph = odf_create_paragraph(text1, style="Standard")
body.append(paragraph)
paragraph.insert_variable(odf_create_time_variable(time(19, 30), fixed=True),
        "time: ")

paragraph = odf_create_paragraph(text2, style="Standard")
body.append(paragraph)
paragraph.insert_variable(odf_create_time_variable(time(19, 30)), "Now: ")

paragraph = odf_create_paragraph(text3, style="Standard")
body.append(paragraph)
paragraph.insert_variable(odf_create_time_variable(time(19, 30),
    time_adjust=timedelta(hours=1)), "hour: ")


# 9- Chapter
# -----------

heading = odf_create_heading(1, text='Chapter')
body.append(heading)

text = 'The current chapter is: '

paragraph = odf_create_paragraph(text, style="Standard")
body.append(paragraph)
paragraph.insert_variable(odf_create_chapter_variable(display='number-and-name'),
        "is: ")


# 10- Filename
# ------------

heading = odf_create_heading(1, text='Filename')
body.append(heading)

text = 'The current file name is: '

paragraph = odf_create_paragraph(text, style="Standard")
body.append(paragraph)
paragraph._insert_between(odf_create_filename_variable(), "The", "is: ")




# Save
# ----

if not exists('test_output'):
    mkdir('test_output')
document.save('test_output/use_case2.odt', pretty=True)

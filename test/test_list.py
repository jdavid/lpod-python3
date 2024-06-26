# -*- coding: UTF-8 -*-
#
# Copyright (c) 2009-2010 Ars Aperta, Itaapy, Pierlis, Talend.
#
# Authors: Romain Gauthier <romain@itaapy.com>
#          Hervé Cauwelier <herve@itaapy.com>
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
from unittest import TestCase, main

# Import from lpod
from lpod.const import ODF_CONTENT
from lpod.document import odf_get_document
from lpod.list import odf_create_list, odf_create_list_item
from lpod.utils import convert_unicode


class TestList(TestCase):

    def setUp(self):
        self.document = document = odf_get_document('samples/list.odt')
        self.content = document.get_part(ODF_CONTENT)


    def tearDown(self):
        del self.content
        del self.document


    def test_create_item(self):
        item = odf_create_list_item()
        expected = '<text:list-item/>'
        self.assertEqual(item.serialize(), expected)


    def test_create_list(self):
        item = odf_create_list_item()
        a_list = odf_create_list(['你好 Zoé'])
        expected = (('<text:list>'
                       '<text:list-item>'
                         '<text:p>%s</text:p>'
                       '</text:list-item>'
                     '</text:list>') % convert_unicode('你好 Zoé'))
        self.assertEqual(a_list.serialize(), expected)


    def test_insert_list(self):
        content = self.content
        clone = content.clone()
        item = odf_create_list_item()
        a_list = odf_create_list(style='a_style')
        a_list.append(item)
        body = clone.get_body()
        body.append(a_list)

        expected = ('<text:list text:style-name="a_style">'
                    '<text:list-item/>'
                    '</text:list>')
        self.assertEqual(a_list.serialize(), expected)


    def test_insert_item(self):
        breakfast = odf_create_list()
        breakfast.insert_item('spam', 1)
        breakfast.insert_item('eggs', 2)
        item = odf_create_list_item('ham')
        breakfast.insert_item(item, -1)

        expected = ('<text:list>'
                      '<text:list-item>'
                        '<text:p>spam</text:p>'
                      '</text:list-item>'
                      '<text:list-item>'
                        '<text:p>ham</text:p>'
                      '</text:list-item>'
                      '<text:list-item>'
                        '<text:p>eggs</text:p>'
                      '</text:list-item>'
                    '</text:list>')
        # TODO Use the true list element in the body of the document instead of
        # the element just created.
        self.assertEqual(breakfast.serialize(), expected)


    def test_append_item(self):
        breakfast = odf_create_list()
        breakfast.append_item('spam')
        breakfast.append_item('ham')
        item = odf_create_list_item('eggs')
        breakfast.append_item(item)

        expected = ('<text:list>'
                      '<text:list-item>'
                        '<text:p>spam</text:p>'
                      '</text:list-item>'
                      '<text:list-item>'
                        '<text:p>ham</text:p>'
                      '</text:list-item>'
                      '<text:list-item>'
                        '<text:p>eggs</text:p>'
                      '</text:list-item>'
                    '</text:list>')
        # TODO Use the true list element in the body of the document instead of
        # the element just created.
        self.assertEqual(breakfast.serialize(), expected)


    def test_insert_sub_item(self):
        spam = odf_create_list(['spam'])
        ham = odf_create_list(['ham'])
        eggs = odf_create_list(['eggs'])

        spam.insert_item(ham, 1)
        ham.insert_item(eggs, 1)

        expected = ('<text:list>'
                      '<text:list-item>'
                        '<text:p>spam</text:p>'
                      '</text:list-item>'
                      '<text:list-item>'
                        '<text:list>'
                          '<text:list-item>'
                            '<text:p>ham</text:p>'
                          '</text:list-item>'
                          '<text:list-item>'
                            '<text:list>'
                              '<text:list-item>'
                                '<text:p>eggs</text:p>'
                              '</text:list-item>'
                            '</text:list>'
                          '</text:list-item>'
                        '</text:list>'
                      '</text:list-item>'
                    '</text:list>')
        # TODO Use the true list element in the body of the document instead of
        # the element just created.
        self.assertEqual(spam.serialize(), expected)


    def test_append_sub_item(self):
        spam = odf_create_list(['spam'])
        ham = odf_create_list(['ham'])
        eggs = odf_create_list(['eggs'])

        spam.append_item(ham)
        ham.append_item(eggs)

        expected = ('<text:list>'
                      '<text:list-item>'
                        '<text:p>spam</text:p>'
                      '</text:list-item>'
                      '<text:list-item>'
                        '<text:list>'
                          '<text:list-item>'
                            '<text:p>ham</text:p>'
                          '</text:list-item>'
                          '<text:list-item>'
                            '<text:list>'
                              '<text:list-item>'
                                '<text:p>eggs</text:p>'
                              '</text:list-item>'
                            '</text:list>'
                          '</text:list-item>'
                        '</text:list>'
                      '</text:list-item>'
                    '</text:list>')
        # TODO Use the true list element in the body of the document instead of
        # the element just created.
        self.assertEqual(spam.serialize(), expected)


    def test_nested_list(self):
        breakfast = odf_create_list()
        spam = odf_create_list_item('spam')
        ham = odf_create_list_item('ham')
        eggs = odf_create_list_item('eggs')
        # First way: a list in an item, right next to a paragraph
        spam.append(odf_create_list(['thé', 'café', 'chocolat']))
        breakfast.append_item(spam)
        breakfast.append_item(ham)
        breakfast.append_item(eggs)
        # Second way: a list as an item
        breakfast.append_item(breakfast.clone())

        expected = ('<text:list>\n'
                    '  <text:list-item>\n'
                    '    <text:p>spam</text:p>\n'
                    '    <text:list>\n'
                    '      <text:list-item>\n'
                    '        <text:p>th&#233;</text:p>\n'
                    '      </text:list-item>\n'
                    '      <text:list-item>\n'
                    '        <text:p>caf&#233;</text:p>\n'
                    '      </text:list-item>\n'
                    '      <text:list-item>\n'
                    '        <text:p>chocolat</text:p>\n'
                    '      </text:list-item>\n'
                    '    </text:list>\n'
                    '  </text:list-item>\n'
                    '  <text:list-item>\n'
                    '    <text:p>ham</text:p>\n'
                    '  </text:list-item>\n'
                    '  <text:list-item>\n'
                    '    <text:p>eggs</text:p>\n'
                    '  </text:list-item>\n'
                    '  <text:list-item>\n'
                    '    <text:list>\n'
                    '      <text:list-item>\n'
                    '        <text:p>spam</text:p>\n'
                    '        <text:list>\n'
                    '          <text:list-item>\n'
                    '            <text:p>th&#233;</text:p>\n'
                    '          </text:list-item>\n'
                    '          <text:list-item>\n'
                    '            <text:p>caf&#233;</text:p>\n'
                    '          </text:list-item>\n'
                    '          <text:list-item>\n'
                    '            <text:p>chocolat</text:p>\n'
                    '          </text:list-item>\n'
                    '        </text:list>\n'
                    '      </text:list-item>\n'
                    '      <text:list-item>\n'
                    '        <text:p>ham</text:p>\n'
                    '      </text:list-item>\n'
                    '      <text:list-item>\n'
                    '        <text:p>eggs</text:p>\n'
                    '      </text:list-item>\n'
                    '    </text:list>\n'
                    '  </text:list-item>\n'
                    '</text:list>\n')
        # TODO Use the true list element in the body of the document instead of
        # the element just created.
        self.assertEqual(breakfast.serialize(pretty=True), expected)


    def test_insert_before(self):
        breakfast = odf_create_list()
        breakfast.append_item('spam')
        eggs = odf_create_list_item('eggs')
        breakfast.append_item(eggs)
        ham = odf_create_list_item('ham')
        breakfast.insert_item(ham, before=eggs)

        expected = ('<text:list>'
                      '<text:list-item>'
                        '<text:p>spam</text:p>'
                      '</text:list-item>'
                      '<text:list-item>'
                        '<text:p>ham</text:p>'
                      '</text:list-item>'
                      '<text:list-item>'
                        '<text:p>eggs</text:p>'
                      '</text:list-item>'
                    '</text:list>')
        # TODO use the true list element in the body of the document instead of
        # the element just created.
        self.assertEqual(breakfast.serialize(), expected)


    def test_insert_after(self):
        breakfast = odf_create_list()
        breakfast.append_item('spam')
        ham = odf_create_list_item('ham')
        breakfast.append_item(ham)
        eggs = odf_create_list_item('eggs')
        breakfast.insert_item(eggs, after=ham)

        expected = ('<text:list>'
                      '<text:list-item>'
                        '<text:p>spam</text:p>'
                      '</text:list-item>'
                      '<text:list-item>'
                        '<text:p>ham</text:p>'
                      '</text:list-item>'
                      '<text:list-item>'
                        '<text:p>eggs</text:p>'
                      '</text:list-item>'
                    '</text:list>')
        # TODO use the true list element in the body of the document instead of
        # the element just created.
        self.assertEqual(breakfast.serialize(), expected)


    def test_get_item_by_content(self):
        # Create the items
        spam = odf_create_list_item('spam')
        ham = odf_create_list_item('ham')
        eggs = odf_create_list_item('eggs')
        # Create the corresponding lists
        spam_list = odf_create_list()
        ham_list = odf_create_list()
        eggs_list = odf_create_list()
        # Fill the lists
        spam_list.append_item(spam)
        ham_list.append_item(ham)
        eggs_list.append_item(eggs)
        # Create the final nested list (spam_list)
        spam.append(ham_list)
        ham.append(eggs_list)

        item = spam_list.get_item(content=r'spam')
        expected = ('<text:list-item>\n'
                    '  <text:p>spam</text:p>\n'
                    '  <text:list>\n'
                    '    <text:list-item>\n'
                    '      <text:p>ham</text:p>\n'
                    '      <text:list>\n'
                    '        <text:list-item>\n'
                    '          <text:p>eggs</text:p>\n'
                    '        </text:list-item>\n'
                    '      </text:list>\n'
                    '    </text:list-item>\n'
                    '  </text:list>\n'
                    '</text:list-item>\n')
        self.assertEqual(item.serialize(pretty=True), expected)
        item = spam_list.get_item(content=r'ham')
        expected = ('<text:list-item>\n'
                    '  <text:p>ham</text:p>\n'
                    '  <text:list>\n'
                    '    <text:list-item>\n'
                    '      <text:p>eggs</text:p>\n'
                    '    </text:list-item>\n'
                    '  </text:list>\n'
                    '</text:list-item>\n')
        self.assertEqual(item.serialize(pretty=True), expected)
        item = spam_list.get_item(content=r'eggs')
        expected = ('<text:list-item>\n'
                    '  <text:p>eggs</text:p>\n'
                    '</text:list-item>\n')
        self.assertEqual(item.serialize(pretty=True), expected)


    def test_get_formatted_text(self):
        # Create the items
        spam = odf_create_list_item('In this picture, there are 47 people;\n'
                                    'none of them can be seen.')
        ham = odf_create_list_item('In this film, we hope to show you the\n'
                                   'value of not being seen.\n')
        eggs = odf_create_list_item('Here is Mr. Bagthorpe of London, '
                                    'SE14.\n')
        foo = odf_create_list_item('He cannot be seen.')
        bar = odf_create_list_item('Now I am going to ask him to stand up.')
        baz = odf_create_list_item('Mr. Bagthorpe, will you stand up please?')
        # Create the lists
        how_not_to_be_seen1 = odf_create_list()
        how_not_to_be_seen2 = odf_create_list()
        how_not_to_be_seen3 = odf_create_list()
        # Fill the lists
        # First list
        how_not_to_be_seen1.append_item(spam)
        # Second list
        how_not_to_be_seen2.append_item(ham)
        how_not_to_be_seen2.append_item(eggs)
        how_not_to_be_seen2.append_item(foo)
        # Third list
        how_not_to_be_seen3.append_item(bar)
        how_not_to_be_seen3.append_item(baz)
        # Create the final nested list (how_not_to_be_seen1)
        spam.append(how_not_to_be_seen2)
        foo.append(how_not_to_be_seen3)

        # Initialize an empty fake context
        context = {'document': None,
                   'footnotes': [],
                   'endnotes': [],
                   'annotations': [],
                   'rst_mode': False}
        expected = ('- In this picture, there are 47 people;\n'
                    '  none of them can be seen.\n'
                    '  \n'
                    '  - In this film, we hope to show you the\n'
                    '    value of not being seen.\n'
                    '  - Here is Mr. Bagthorpe of London, SE14.\n'
                    '  - He cannot be seen.\n'
                    '    \n'
                    '    - Now I am going to ask him to stand up.\n'
                    '    - Mr. Bagthorpe, will you stand up please?\n')
        self.assertEqual(how_not_to_be_seen1.get_formatted_text(context),
                         expected)



if __name__ == '__main__':
    main()

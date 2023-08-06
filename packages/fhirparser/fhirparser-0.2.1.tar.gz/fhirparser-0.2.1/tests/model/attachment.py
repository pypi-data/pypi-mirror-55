#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Attachment) on 2019-11-06.
#  2019, SMART Health IT.


from . import element

class Attachment(element.Element):
    """ Content in a format defined elsewhere.
    
    For referring to data content defined in other formats.
    """
    
    resource_type = "Attachment"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.contentType = None
        """ Mime type of the content, with charset etc..
        Type `str`. """
        
        self.language = None
        """ Human language of the content (BCP-47).
        Type `str`. """
        
        self.data = None
        """ Data inline, base64ed.
        Type `str`. """
        
        self.url = None
        """ Uri where the data can be found.
        Type `str`. """
        
        self.size = None
        """ Number of bytes of content (if url provided).
        Type `int`. """
        
        self.hash = None
        """ Hash of the data (sha-1, base64ed).
        Type `str`. """
        
        self.title = None
        """ Label to display in place of the data.
        Type `str`. """
        
        self.creation = None
        """ Date attachment was first created.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(Attachment, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Attachment, self).elementProperties()
        js.extend([
            ("contentType", "contentType", str, False, None, False),
            ("language", "language", str, False, None, False),
            ("data", "data", str, False, None, False),
            ("url", "url", str, False, None, False),
            ("size", "size", int, False, None, False),
            ("hash", "hash", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("creation", "creation", fhirdate.FHIRDate, False, None, False),
        ])
        return js


from . import fhirdate

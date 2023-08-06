#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Contributor) on 2019-11-06.
#  2019, SMART Health IT.


from . import element

class Contributor(element.Element):
    """ Contributor information.
    
    A contributor to the content of a knowledge asset, including authors,
    editors, reviewers, and endorsers.
    """
    
    resource_type = "Contributor"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ author | editor | reviewer | endorser.
        Type `str`. """
        
        self.name = None
        """ Who contributed the content.
        Type `str`. """
        
        self.contact = None
        """ Contact details of the contributor.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        super(Contributor, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Contributor, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("name", "name", str, False, None, True),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
        ])
        return js


from . import contactdetail

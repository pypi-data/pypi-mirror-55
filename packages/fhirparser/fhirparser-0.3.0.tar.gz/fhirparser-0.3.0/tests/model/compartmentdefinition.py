#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/CompartmentDefinition) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class CompartmentDefinition(domainresource.DomainResource):
    """ Compartment Definition for a resource.
    
    A compartment definition that defines how resources are accessed on a
    server.
    """
    
    resource_type = "CompartmentDefinition"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.url = None
        """ Canonical identifier for this compartment definition, represented
        as a URI (globally unique).
        Type `str`. """
        
        self.version = None
        """ Business version of the compartment definition.
        Type `str`. """
        
        self.name = None
        """ Name for this compartment definition (computer friendly).
        Type `str`. """
        
        self.status = None
        """ draft | active | retired | unknown.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
        self.date = None
        """ Date last changed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.publisher = None
        """ Name of the publisher (organization or individual).
        Type `str`. """
        
        self.contact = None
        """ Contact details for the publisher.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Natural language description of the compartment definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this compartment definition is defined.
        Type `str`. """
        
        self.code = None
        """ Patient | Encounter | RelatedPerson | Practitioner | Device.
        Type `str`. """
        
        self.search = None
        """ Whether the search syntax is supported.
        Type `bool`. """
        
        self.resource = None
        """ How a resource is related to the compartment.
        List of `CompartmentDefinitionResource` items (represented as `dict` in JSON). """
        
        super(CompartmentDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CompartmentDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, True),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, True),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("code", "code", str, False, None, True),
            ("search", "search", bool, False, None, True),
            ("resource", "resource", CompartmentDefinitionResource, True, None, False),
        ])
        return js


from . import backboneelement

class CompartmentDefinitionResource(backboneelement.BackboneElement):
    """ How a resource is related to the compartment.
    
    Information about how a resource is related to the compartment.
    """
    
    resource_type = "CompartmentDefinitionResource"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.code = None
        """ Name of resource type.
        Type `str`. """
        
        self.param = None
        """ Search Parameter Name, or chained parameters.
        List of `str` items. """
        
        self.documentation = None
        """ Additional documentation about the resource and compartment.
        Type `str`. """
        
        super(CompartmentDefinitionResource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CompartmentDefinitionResource, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("param", "param", str, True, None, False),
            ("documentation", "documentation", str, False, None, False),
        ])
        return js


from . import contactdetail
from . import fhirdate
from . import usagecontext

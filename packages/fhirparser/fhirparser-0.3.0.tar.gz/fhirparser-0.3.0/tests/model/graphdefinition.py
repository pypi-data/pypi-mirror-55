#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/GraphDefinition) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class GraphDefinition(domainresource.DomainResource):
    """ Definition of a graph of resources.
    
    A formal computable definition of a graph of resources - that is, a
    coherent set of resources that form a graph by following references. The
    Graph Definition resource defines a set and makes rules about the set.
    """
    
    resource_type = "GraphDefinition"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.url = None
        """ Canonical identifier for this graph definition, represented as a
        URI (globally unique).
        Type `str`. """
        
        self.version = None
        """ Business version of the graph definition.
        Type `str`. """
        
        self.name = None
        """ Name for this graph definition (computer friendly).
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
        """ Natural language description of the graph definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for graph definition (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this graph definition is defined.
        Type `str`. """
        
        self.start = None
        """ Type of resource at which the graph starts.
        Type `str`. """
        
        self.profile = None
        """ Profile on base resource.
        Type `str`. """
        
        self.link = None
        """ Links this graph makes rules about.
        List of `GraphDefinitionLink` items (represented as `dict` in JSON). """
        
        super(GraphDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(GraphDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, True),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("start", "start", str, False, None, True),
            ("profile", "profile", str, False, None, False),
            ("link", "link", GraphDefinitionLink, True, None, False),
        ])
        return js


from . import backboneelement

class GraphDefinitionLink(backboneelement.BackboneElement):
    """ Links this graph makes rules about.
    """
    
    resource_type = "GraphDefinitionLink"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.path = None
        """ Path in the resource that contains the link.
        Type `str`. """
        
        self.sliceName = None
        """ Which slice (if profiled).
        Type `str`. """
        
        self.min = None
        """ Minimum occurrences for this link.
        Type `int`. """
        
        self.max = None
        """ Maximum occurrences for this link.
        Type `str`. """
        
        self.description = None
        """ Why this link is specified.
        Type `str`. """
        
        self.target = None
        """ Potential target for the link.
        List of `GraphDefinitionLinkTarget` items (represented as `dict` in JSON). """
        
        super(GraphDefinitionLink, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(GraphDefinitionLink, self).elementProperties()
        js.extend([
            ("path", "path", str, False, None, False),
            ("sliceName", "sliceName", str, False, None, False),
            ("min", "min", int, False, None, False),
            ("max", "max", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("target", "target", GraphDefinitionLinkTarget, True, None, False),
        ])
        return js


class GraphDefinitionLinkTarget(backboneelement.BackboneElement):
    """ Potential target for the link.
    """
    
    resource_type = "GraphDefinitionLinkTarget"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ Type of resource this link refers to.
        Type `str`. """
        
        self.params = None
        """ Criteria for reverse lookup.
        Type `str`. """
        
        self.profile = None
        """ Profile for the target resource.
        Type `str`. """
        
        self.compartment = None
        """ Compartment Consistency Rules.
        List of `GraphDefinitionLinkTargetCompartment` items (represented as `dict` in JSON). """
        
        self.link = None
        """ Additional links from target resource.
        List of `GraphDefinitionLink` items (represented as `dict` in JSON). """
        
        super(GraphDefinitionLinkTarget, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(GraphDefinitionLinkTarget, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("params", "params", str, False, None, False),
            ("profile", "profile", str, False, None, False),
            ("compartment", "compartment", GraphDefinitionLinkTargetCompartment, True, None, False),
            ("link", "link", GraphDefinitionLink, True, None, False),
        ])
        return js


class GraphDefinitionLinkTargetCompartment(backboneelement.BackboneElement):
    """ Compartment Consistency Rules.
    """
    
    resource_type = "GraphDefinitionLinkTargetCompartment"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.use = None
        """ condition | requirement.
        Type `str`. """
        
        self.code = None
        """ Patient | Encounter | RelatedPerson | Practitioner | Device.
        Type `str`. """
        
        self.rule = None
        """ identical | matching | different | custom.
        Type `str`. """
        
        self.expression = None
        """ Custom rule, as a FHIRPath expression.
        Type `str`. """
        
        self.description = None
        """ Documentation for FHIRPath expression.
        Type `str`. """
        
        super(GraphDefinitionLinkTargetCompartment, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(GraphDefinitionLinkTargetCompartment, self).elementProperties()
        js.extend([
            ("use", "use", str, False, None, True),
            ("code", "code", str, False, None, True),
            ("rule", "rule", str, False, None, True),
            ("expression", "expression", str, False, None, False),
            ("description", "description", str, False, None, False),
        ])
        return js


from . import codeableconcept
from . import contactdetail
from . import fhirdate
from . import usagecontext

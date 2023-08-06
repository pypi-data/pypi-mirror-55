#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/OperationDefinition) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class OperationDefinition(domainresource.DomainResource):
    """ Definition of an operation or a named query.
    
    A formal computable definition of an operation (on the RESTful interface)
    or a named query (using the search interaction).
    """
    
    resource_type = "OperationDefinition"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.url = None
        """ Canonical identifier for this operation definition, represented as
        a URI (globally unique).
        Type `str`. """
        
        self.version = None
        """ Business version of the operation definition.
        Type `str`. """
        
        self.name = None
        """ Name for this operation definition (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this operation definition (human friendly).
        Type `str`. """
        
        self.status = None
        """ draft | active | retired | unknown.
        Type `str`. """
        
        self.kind = None
        """ operation | query.
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
        """ Natural language description of the operation definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for operation definition (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this operation definition is defined.
        Type `str`. """
        
        self.affectsState = None
        """ Whether content is changed by the operation.
        Type `bool`. """
        
        self.code = None
        """ Name used to invoke the operation.
        Type `str`. """
        
        self.comment = None
        """ Additional information about use.
        Type `str`. """
        
        self.base = None
        """ Marks this as a profile of the base.
        Type `str`. """
        
        self.resource = None
        """ Types this operation applies to.
        List of `str` items. """
        
        self.system = None
        """ Invoke at the system level?.
        Type `bool`. """
        
        self.type = None
        """ Invoke at the type level?.
        Type `bool`. """
        
        self.instance = None
        """ Invoke on an instance?.
        Type `bool`. """
        
        self.inputProfile = None
        """ Validation information for in parameters.
        Type `str`. """
        
        self.outputProfile = None
        """ Validation information for out parameters.
        Type `str`. """
        
        self.parameter = None
        """ Parameters for the operation/query.
        List of `OperationDefinitionParameter` items (represented as `dict` in JSON). """
        
        self.overload = None
        """ Define overloaded variants for when  generating code.
        List of `OperationDefinitionOverload` items (represented as `dict` in JSON). """
        
        super(OperationDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, True),
            ("title", "title", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("kind", "kind", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("affectsState", "affectsState", bool, False, None, False),
            ("code", "code", str, False, None, True),
            ("comment", "comment", str, False, None, False),
            ("base", "base", str, False, None, False),
            ("resource", "resource", str, True, None, False),
            ("system", "system", bool, False, None, True),
            ("type", "type", bool, False, None, True),
            ("instance", "instance", bool, False, None, True),
            ("inputProfile", "inputProfile", str, False, None, False),
            ("outputProfile", "outputProfile", str, False, None, False),
            ("parameter", "parameter", OperationDefinitionParameter, True, None, False),
            ("overload", "overload", OperationDefinitionOverload, True, None, False),
        ])
        return js


from . import backboneelement

class OperationDefinitionOverload(backboneelement.BackboneElement):
    """ Define overloaded variants for when  generating code.
    
    Defines an appropriate combination of parameters to use when invoking this
    operation, to help code generators when generating overloaded parameter
    sets for this operation.
    """
    
    resource_type = "OperationDefinitionOverload"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.parameterName = None
        """ Name of parameter to include in overload.
        List of `str` items. """
        
        self.comment = None
        """ Comments to go on overload.
        Type `str`. """
        
        super(OperationDefinitionOverload, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationDefinitionOverload, self).elementProperties()
        js.extend([
            ("parameterName", "parameterName", str, True, None, False),
            ("comment", "comment", str, False, None, False),
        ])
        return js


class OperationDefinitionParameter(backboneelement.BackboneElement):
    """ Parameters for the operation/query.
    
    The parameters for the operation/query.
    """
    
    resource_type = "OperationDefinitionParameter"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.name = None
        """ Name in Parameters.parameter.name or in URL.
        Type `str`. """
        
        self.use = None
        """ in | out.
        Type `str`. """
        
        self.min = None
        """ Minimum Cardinality.
        Type `int`. """
        
        self.max = None
        """ Maximum Cardinality (a number or *).
        Type `str`. """
        
        self.documentation = None
        """ Description of meaning/use.
        Type `str`. """
        
        self.type = None
        """ What type this parameter has.
        Type `str`. """
        
        self.targetProfile = None
        """ If type is Reference | canonical, allowed targets.
        List of `str` items. """
        
        self.searchType = None
        """ number | date | string | token | reference | composite | quantity |
        uri | special.
        Type `str`. """
        
        self.binding = None
        """ ValueSet details if this is coded.
        Type `OperationDefinitionParameterBinding` (represented as `dict` in JSON). """
        
        self.referencedFrom = None
        """ References to this parameter.
        List of `OperationDefinitionParameterReferencedFrom` items (represented as `dict` in JSON). """
        
        self.part = None
        """ Parts of a nested Parameter.
        List of `OperationDefinitionParameter` items (represented as `dict` in JSON). """
        
        super(OperationDefinitionParameter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationDefinitionParameter, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("use", "use", str, False, None, True),
            ("min", "min", int, False, None, True),
            ("max", "max", str, False, None, True),
            ("documentation", "documentation", str, False, None, False),
            ("type", "type", str, False, None, False),
            ("targetProfile", "targetProfile", str, True, None, False),
            ("searchType", "searchType", str, False, None, False),
            ("binding", "binding", OperationDefinitionParameterBinding, False, None, False),
            ("referencedFrom", "referencedFrom", OperationDefinitionParameterReferencedFrom, True, None, False),
            ("part", "part", OperationDefinitionParameter, True, None, False),
        ])
        return js


class OperationDefinitionParameterReferencedFrom(backboneelement.BackboneElement):
    """ References to this parameter.
    
    Identifies other resource parameters within the operation invocation that
    are expected to resolve to this resource.
    """
    
    resource_type = "OperationDefinitionParameterReferencedFrom"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.source = None
        """ Referencing parameter.
        Type `str`. """
        
        self.sourceId = None
        """ Element id of reference.
        Type `str`. """
        
        super(OperationDefinitionParameterReferencedFrom, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationDefinitionParameterReferencedFrom, self).elementProperties()
        js.extend([
            ("source", "source", str, False, None, True),
            ("sourceId", "sourceId", str, False, None, False),
        ])
        return js


class OperationDefinitionParameterBinding(backboneelement.BackboneElement):
    """ ValueSet details if this is coded.
    
    Binds to a value set if this parameter is coded (code, Coding,
    CodeableConcept).
    """
    
    resource_type = "OperationDefinitionParameterBinding"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.strength = None
        """ required | extensible | preferred | example.
        Type `str`. """
        
        self.valueSet = None
        """ Source of value set.
        Type `str`. """
        
        super(OperationDefinitionParameterBinding, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationDefinitionParameterBinding, self).elementProperties()
        js.extend([
            ("strength", "strength", str, False, None, True),
            ("valueSet", "valueSet", str, False, None, True),
        ])
        return js


from . import codeableconcept
from . import contactdetail
from . import fhirdate
from . import usagecontext

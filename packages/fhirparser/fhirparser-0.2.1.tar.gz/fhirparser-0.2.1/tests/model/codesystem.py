#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/CodeSystem) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class CodeSystem(domainresource.DomainResource):
    """ Declares the existence of and describes a code system or code system
    supplement.
    
    The CodeSystem resource is used to declare the existence of and describe a
    code system or code system supplement and its key properties, and
    optionally define a part or all of its content.
    """
    
    resource_type = "CodeSystem"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.url = None
        """ Canonical identifier for this code system, represented as a URI
        (globally unique) (Coding.system).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the code system (business identifier).
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the code system (Coding.version).
        Type `str`. """
        
        self.name = None
        """ Name for this code system (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this code system (human friendly).
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
        """ Natural language description of the code system.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for code system (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this code system is defined.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.caseSensitive = None
        """ If code comparison is case sensitive.
        Type `bool`. """
        
        self.valueSet = None
        """ Canonical reference to the value set with entire code system.
        Type `str`. """
        
        self.hierarchyMeaning = None
        """ grouped-by | is-a | part-of | classified-with.
        Type `str`. """
        
        self.compositional = None
        """ If code system defines a compositional grammar.
        Type `bool`. """
        
        self.versionNeeded = None
        """ If definitions are not stable.
        Type `bool`. """
        
        self.content = None
        """ not-present | example | fragment | complete | supplement.
        Type `str`. """
        
        self.supplements = None
        """ Canonical URL of Code System this adds designations and properties
        to.
        Type `str`. """
        
        self.count = None
        """ Total concepts in the code system.
        Type `int`. """
        
        self.filter = None
        """ Filter that can be used in a value set.
        List of `CodeSystemFilter` items (represented as `dict` in JSON). """
        
        self.property = None
        """ Additional information supplied about each concept.
        List of `CodeSystemProperty` items (represented as `dict` in JSON). """
        
        self.concept = None
        """ Concepts in the code system.
        List of `CodeSystemConcept` items (represented as `dict` in JSON). """
        
        super(CodeSystem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystem, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("caseSensitive", "caseSensitive", bool, False, None, False),
            ("valueSet", "valueSet", str, False, None, False),
            ("hierarchyMeaning", "hierarchyMeaning", str, False, None, False),
            ("compositional", "compositional", bool, False, None, False),
            ("versionNeeded", "versionNeeded", bool, False, None, False),
            ("content", "content", str, False, None, True),
            ("supplements", "supplements", str, False, None, False),
            ("count", "count", int, False, None, False),
            ("filter", "filter", CodeSystemFilter, True, None, False),
            ("property", "property", CodeSystemProperty, True, None, False),
            ("concept", "concept", CodeSystemConcept, True, None, False),
        ])
        return js


from . import backboneelement

class CodeSystemConcept(backboneelement.BackboneElement):
    """ Concepts in the code system.
    
    Concepts that are in the code system. The concept definitions are
    inherently hierarchical, but the definitions must be consulted to determine
    what the meanings of the hierarchical relationships are.
    """
    
    resource_type = "CodeSystemConcept"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.code = None
        """ Code that identifies concept.
        Type `str`. """
        
        self.display = None
        """ Text to display to the user.
        Type `str`. """
        
        self.definition = None
        """ Formal definition.
        Type `str`. """
        
        self.designation = None
        """ Additional representations for the concept.
        List of `CodeSystemConceptDesignation` items (represented as `dict` in JSON). """
        
        self.property = None
        """ Property value for the concept.
        List of `CodeSystemConceptProperty` items (represented as `dict` in JSON). """
        
        self.concept = None
        """ Child Concepts (is-a/contains/categorizes).
        List of `CodeSystemConcept` items (represented as `dict` in JSON). """
        
        super(CodeSystemConcept, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystemConcept, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("display", "display", str, False, None, False),
            ("definition", "definition", str, False, None, False),
            ("designation", "designation", CodeSystemConceptDesignation, True, None, False),
            ("property", "property", CodeSystemConceptProperty, True, None, False),
            ("concept", "concept", CodeSystemConcept, True, None, False),
        ])
        return js


class CodeSystemProperty(backboneelement.BackboneElement):
    """ Additional information supplied about each concept.
    
    A property defines an additional slot through which additional information
    can be provided about a concept.
    """
    
    resource_type = "CodeSystemProperty"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.code = None
        """ Identifies the property on the concepts, and when referred to in
        operations.
        Type `str`. """
        
        self.uri = None
        """ Formal identifier for the property.
        Type `str`. """
        
        self.description = None
        """ Why the property is defined, and/or what it conveys.
        Type `str`. """
        
        self.type = None
        """ code | Coding | string | integer | boolean | dateTime | decimal.
        Type `str`. """
        
        super(CodeSystemProperty, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystemProperty, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("uri", "uri", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("type", "type", str, False, None, True),
        ])
        return js


class CodeSystemFilter(backboneelement.BackboneElement):
    """ Filter that can be used in a value set.
    
    A filter that can be used in a value set compose statement when selecting
    concepts using a filter.
    """
    
    resource_type = "CodeSystemFilter"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.code = None
        """ Code that identifies the filter.
        Type `str`. """
        
        self.description = None
        """ How or why the filter is used.
        Type `str`. """
        
        self.operator = None
        """ = | is-a | descendent-of | is-not-a | regex | in | not-in |
        generalizes | exists.
        List of `str` items. """
        
        self.value = None
        """ What to use for the value.
        Type `str`. """
        
        super(CodeSystemFilter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystemFilter, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("description", "description", str, False, None, False),
            ("operator", "operator", str, True, None, True),
            ("value", "value", str, False, None, True),
        ])
        return js


class CodeSystemConceptProperty(backboneelement.BackboneElement):
    """ Property value for the concept.
    
    A property value for this concept.
    """
    
    resource_type = "CodeSystemConceptProperty"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.code = None
        """ Reference to CodeSystem.property.code.
        Type `str`. """
        
        self.valueCode = None
        """ Value of the property for this concept.
        Type `str`. """
        
        self.valueCoding = None
        """ Value of the property for this concept.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.valueString = None
        """ Value of the property for this concept.
        Type `str`. """
        
        self.valueInteger = None
        """ Value of the property for this concept.
        Type `int`. """
        
        self.valueBoolean = None
        """ Value of the property for this concept.
        Type `bool`. """
        
        self.valueDateTime = None
        """ Value of the property for this concept.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueDecimal = None
        """ Value of the property for this concept.
        Type `float`. """
        
        super(CodeSystemConceptProperty, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystemConceptProperty, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("valueCode", "valueCode", str, False, "value", True),
            ("valueCoding", "valueCoding", coding.Coding, False, "value", True),
            ("valueString", "valueString", str, False, "value", True),
            ("valueInteger", "valueInteger", int, False, "value", True),
            ("valueBoolean", "valueBoolean", bool, False, "value", True),
            ("valueDateTime", "valueDateTime", fhirdate.FHIRDate, False, "value", True),
            ("valueDecimal", "valueDecimal", float, False, "value", True),
        ])
        return js


class CodeSystemConceptDesignation(backboneelement.BackboneElement):
    """ Additional representations for the concept.
    
    Additional representations for the concept - other languages, aliases,
    specialized purposes, used for particular purposes, etc.
    """
    
    resource_type = "CodeSystemConceptDesignation"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.language = None
        """ Human language of the designation.
        Type `str`. """
        
        self.use = None
        """ Details how this designation would be used.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.value = None
        """ The text value for this designation.
        Type `str`. """
        
        super(CodeSystemConceptDesignation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystemConceptDesignation, self).elementProperties()
        js.extend([
            ("language", "language", str, False, None, False),
            ("use", "use", coding.Coding, False, None, False),
            ("value", "value", str, False, None, True),
        ])
        return js


from . import codeableconcept
from . import coding
from . import contactdetail
from . import fhirdate
from . import identifier
from . import usagecontext

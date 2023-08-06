#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ValueSet) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class ValueSet(domainresource.DomainResource):
    """ A set of codes drawn from one or more code systems.
    
    A ValueSet resource instance specifies a set of codes drawn from one or
    more code systems, intended for use in a particular context. Value sets
    link between [CodeSystem](codesystem.html) definitions and their use in
    [coded elements](terminologies.html).
    """
    
    resource_type = "ValueSet"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.url = None
        """ Canonical identifier for this value set, represented as a URI
        (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the value set (business identifier).
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the value set.
        Type `str`. """
        
        self.name = None
        """ Name for this value set (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this value set (human friendly).
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
        """ Natural language description of the value set.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for value set (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.immutable = None
        """ Indicates whether or not any change to the content logical
        definition may occur.
        Type `bool`. """
        
        self.purpose = None
        """ Why this value set is defined.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.compose = None
        """ Content logical definition of the value set (CLD).
        Type `ValueSetCompose` (represented as `dict` in JSON). """
        
        self.expansion = None
        """ Used when the value set is "expanded".
        Type `ValueSetExpansion` (represented as `dict` in JSON). """
        
        super(ValueSet, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ValueSet, self).elementProperties()
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
            ("immutable", "immutable", bool, False, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("compose", "compose", ValueSetCompose, False, None, False),
            ("expansion", "expansion", ValueSetExpansion, False, None, False),
        ])
        return js


from . import backboneelement

class ValueSetExpansion(backboneelement.BackboneElement):
    """ Used when the value set is "expanded".
    
    A value set can also be "expanded", where the value set is turned into a
    simple collection of enumerated codes. This element holds the expansion, if
    it has been performed.
    """
    
    resource_type = "ValueSetExpansion"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.identifier = None
        """ Identifies the value set expansion (business identifier).
        Type `str`. """
        
        self.timestamp = None
        """ Time ValueSet expansion happened.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.total = None
        """ Total number of codes in the expansion.
        Type `int`. """
        
        self.offset = None
        """ Offset at which this resource starts.
        Type `int`. """
        
        self.parameter = None
        """ Parameter that controlled the expansion process.
        List of `ValueSetExpansionParameter` items (represented as `dict` in JSON). """
        
        self.contains = None
        """ Codes in the value set.
        List of `ValueSetExpansionContains` items (represented as `dict` in JSON). """
        
        super(ValueSetExpansion, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ValueSetExpansion, self).elementProperties()
        js.extend([
            ("identifier", "identifier", str, False, None, False),
            ("timestamp", "timestamp", fhirdate.FHIRDate, False, None, True),
            ("total", "total", int, False, None, False),
            ("offset", "offset", int, False, None, False),
            ("parameter", "parameter", ValueSetExpansionParameter, True, None, False),
            ("contains", "contains", ValueSetExpansionContains, True, None, False),
        ])
        return js


class ValueSetCompose(backboneelement.BackboneElement):
    """ Content logical definition of the value set (CLD).
    
    A set of criteria that define the contents of the value set by including or
    excluding codes selected from the specified code system(s) that the value
    set draws from. This is also known as the Content Logical Definition (CLD).
    """
    
    resource_type = "ValueSetCompose"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.lockedDate = None
        """ Fixed date for references with no specified version (transitive).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.inactive = None
        """ Whether inactive codes are in the value set.
        Type `bool`. """
        
        self.include = None
        """ Include one or more codes from a code system or other value set(s).
        List of `ValueSetComposeInclude` items (represented as `dict` in JSON). """
        
        self.exclude = None
        """ Explicitly exclude codes from a code system or other value sets.
        List of `ValueSetComposeInclude` items (represented as `dict` in JSON). """
        
        super(ValueSetCompose, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ValueSetCompose, self).elementProperties()
        js.extend([
            ("lockedDate", "lockedDate", fhirdate.FHIRDate, False, None, False),
            ("inactive", "inactive", bool, False, None, False),
            ("include", "include", ValueSetComposeInclude, True, None, True),
            ("exclude", "exclude", ValueSetComposeInclude, True, None, False),
        ])
        return js


class ValueSetComposeInclude(backboneelement.BackboneElement):
    """ Include one or more codes from a code system or other value set(s).
    """
    
    resource_type = "ValueSetComposeInclude"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.system = None
        """ The system the codes come from.
        Type `str`. """
        
        self.version = None
        """ Specific version of the code system referred to.
        Type `str`. """
        
        self.concept = None
        """ A concept defined in the system.
        List of `ValueSetComposeIncludeConcept` items (represented as `dict` in JSON). """
        
        self.filter = None
        """ Select codes/concepts by their properties (including relationships).
        List of `ValueSetComposeIncludeFilter` items (represented as `dict` in JSON). """
        
        self.valueSet = None
        """ Select the contents included in this value set.
        List of `str` items. """
        
        super(ValueSetComposeInclude, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ValueSetComposeInclude, self).elementProperties()
        js.extend([
            ("system", "system", str, False, None, False),
            ("version", "version", str, False, None, False),
            ("concept", "concept", ValueSetComposeIncludeConcept, True, None, False),
            ("filter", "filter", ValueSetComposeIncludeFilter, True, None, False),
            ("valueSet", "valueSet", str, True, None, False),
        ])
        return js


class ValueSetComposeIncludeFilter(backboneelement.BackboneElement):
    """ Select codes/concepts by their properties (including relationships).
    
    Select concepts by specify a matching criterion based on the properties
    (including relationships) defined by the system, or on filters defined by
    the system. If multiple filters are specified, they SHALL all be true.
    """
    
    resource_type = "ValueSetComposeIncludeFilter"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.property = None
        """ A property/filter defined by the code system.
        Type `str`. """
        
        self.op = None
        """ = | is-a | descendent-of | is-not-a | regex | in | not-in |
        generalizes | exists.
        Type `str`. """
        
        self.value = None
        """ Code from the system, or regex criteria, or boolean value for
        exists.
        Type `str`. """
        
        super(ValueSetComposeIncludeFilter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ValueSetComposeIncludeFilter, self).elementProperties()
        js.extend([
            ("property", "property", str, False, None, True),
            ("op", "op", str, False, None, True),
            ("value", "value", str, False, None, True),
        ])
        return js


class ValueSetComposeIncludeConcept(backboneelement.BackboneElement):
    """ A concept defined in the system.
    
    Specifies a concept to be included or excluded.
    """
    
    resource_type = "ValueSetComposeIncludeConcept"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.code = None
        """ Code or expression from system.
        Type `str`. """
        
        self.display = None
        """ Text to display for this code for this value set in this valueset.
        Type `str`. """
        
        self.designation = None
        """ Additional representations for this concept.
        List of `ValueSetComposeIncludeConceptDesignation` items (represented as `dict` in JSON). """
        
        super(ValueSetComposeIncludeConcept, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ValueSetComposeIncludeConcept, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("display", "display", str, False, None, False),
            ("designation", "designation", ValueSetComposeIncludeConceptDesignation, True, None, False),
        ])
        return js


class ValueSetComposeIncludeConceptDesignation(backboneelement.BackboneElement):
    """ Additional representations for this concept.
    
    Additional representations for this concept when used in this value set -
    other languages, aliases, specialized purposes, used for particular
    purposes, etc.
    """
    
    resource_type = "ValueSetComposeIncludeConceptDesignation"
    
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
        """ Types of uses of designations.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.value = None
        """ The text value for this designation.
        Type `str`. """
        
        super(ValueSetComposeIncludeConceptDesignation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ValueSetComposeIncludeConceptDesignation, self).elementProperties()
        js.extend([
            ("language", "language", str, False, None, False),
            ("use", "use", coding.Coding, False, None, False),
            ("value", "value", str, False, None, True),
        ])
        return js


class ValueSetExpansionContains(backboneelement.BackboneElement):
    """ Codes in the value set.
    
    The codes that are contained in the value set expansion.
    """
    
    resource_type = "ValueSetExpansionContains"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.system = None
        """ System value for the code.
        Type `str`. """
        
        self.abstract = None
        """ If user cannot select this entry.
        Type `bool`. """
        
        self.inactive = None
        """ If concept is inactive in the code system.
        Type `bool`. """
        
        self.version = None
        """ Version in which this code/display is defined.
        Type `str`. """
        
        self.code = None
        """ Code - if blank, this is not a selectable code.
        Type `str`. """
        
        self.display = None
        """ User display for the concept.
        Type `str`. """
        
        self.designation = None
        """ Additional representations for this item.
        List of `ValueSetComposeIncludeConceptDesignation` items (represented as `dict` in JSON). """
        
        self.contains = None
        """ Codes contained under this entry.
        List of `ValueSetExpansionContains` items (represented as `dict` in JSON). """
        
        super(ValueSetExpansionContains, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ValueSetExpansionContains, self).elementProperties()
        js.extend([
            ("system", "system", str, False, None, False),
            ("abstract", "abstract", bool, False, None, False),
            ("inactive", "inactive", bool, False, None, False),
            ("version", "version", str, False, None, False),
            ("code", "code", str, False, None, False),
            ("display", "display", str, False, None, False),
            ("designation", "designation", ValueSetComposeIncludeConceptDesignation, True, None, False),
            ("contains", "contains", ValueSetExpansionContains, True, None, False),
        ])
        return js


class ValueSetExpansionParameter(backboneelement.BackboneElement):
    """ Parameter that controlled the expansion process.
    
    A parameter that controlled the expansion process. These parameters may be
    used by users of expanded value sets to check whether the expansion is
    suitable for a particular purpose, or to pick the correct expansion.
    """
    
    resource_type = "ValueSetExpansionParameter"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.name = None
        """ Name as assigned by the client or server.
        Type `str`. """
        
        self.valueString = None
        """ Value of the named parameter.
        Type `str`. """
        
        self.valueBoolean = None
        """ Value of the named parameter.
        Type `bool`. """
        
        self.valueInteger = None
        """ Value of the named parameter.
        Type `int`. """
        
        self.valueDecimal = None
        """ Value of the named parameter.
        Type `float`. """
        
        self.valueUri = None
        """ Value of the named parameter.
        Type `str`. """
        
        self.valueCode = None
        """ Value of the named parameter.
        Type `str`. """
        
        self.valueDateTime = None
        """ Value of the named parameter.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(ValueSetExpansionParameter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ValueSetExpansionParameter, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("valueString", "valueString", str, False, "value", False),
            ("valueBoolean", "valueBoolean", bool, False, "value", False),
            ("valueInteger", "valueInteger", int, False, "value", False),
            ("valueDecimal", "valueDecimal", float, False, "value", False),
            ("valueUri", "valueUri", str, False, "value", False),
            ("valueCode", "valueCode", str, False, "value", False),
            ("valueDateTime", "valueDateTime", fhirdate.FHIRDate, False, "value", False),
        ])
        return js


from . import codeableconcept
from . import coding
from . import contactdetail
from . import fhirdate
from . import identifier
from . import usagecontext

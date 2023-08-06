#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ObservationDefinition) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class ObservationDefinition(domainresource.DomainResource):
    """ Definition of an observation.
    
    Set of definitional characteristics for a kind of observation or
    measurement produced or consumed by an orderable health care service.
    """
    
    resource_type = "ObservationDefinition"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.category = None
        """ Category of observation.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.code = None
        """ Type of observation (code / type).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Business identifier for this ObservationDefinition instance.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.permittedDataType = None
        """ Quantity | CodeableConcept | string | boolean | integer | Range |
        Ratio | SampledData | time | dateTime | Period.
        List of `str` items. """
        
        self.multipleResultsAllowed = None
        """ Multiple results allowed.
        Type `bool`. """
        
        self.method = None
        """ Method used to produce the observation.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.preferredReportName = None
        """ Preferred report name.
        Type `str`. """
        
        self.quantitativeDetails = None
        """ Characteristics of quantitative results.
        Type `ObservationDefinitionQuantitativeDetails` (represented as `dict` in JSON). """
        
        self.qualifiedInterval = None
        """ Qualified range for continuous and ordinal observation results.
        List of `ObservationDefinitionQualifiedInterval` items (represented as `dict` in JSON). """
        
        self.validCodedValueSet = None
        """ Value set of valid coded values for the observations conforming to
        this ObservationDefinition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.normalCodedValueSet = None
        """ Value set of normal coded values for the observations conforming to
        this ObservationDefinition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.abnormalCodedValueSet = None
        """ Value set of abnormal coded values for the observations conforming
        to this ObservationDefinition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.criticalCodedValueSet = None
        """ Value set of critical coded values for the observations conforming
        to this ObservationDefinition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ObservationDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ObservationDefinition, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("permittedDataType", "permittedDataType", str, True, None, False),
            ("multipleResultsAllowed", "multipleResultsAllowed", bool, False, None, False),
            ("method", "method", codeableconcept.CodeableConcept, False, None, False),
            ("preferredReportName", "preferredReportName", str, False, None, False),
            ("quantitativeDetails", "quantitativeDetails", ObservationDefinitionQuantitativeDetails, False, None, False),
            ("qualifiedInterval", "qualifiedInterval", ObservationDefinitionQualifiedInterval, True, None, False),
            ("validCodedValueSet", "validCodedValueSet", fhirreference.FHIRReference, False, None, False),
            ("normalCodedValueSet", "normalCodedValueSet", fhirreference.FHIRReference, False, None, False),
            ("abnormalCodedValueSet", "abnormalCodedValueSet", fhirreference.FHIRReference, False, None, False),
            ("criticalCodedValueSet", "criticalCodedValueSet", fhirreference.FHIRReference, False, None, False),
        ])
        return js


from . import backboneelement

class ObservationDefinitionQualifiedInterval(backboneelement.BackboneElement):
    """ Qualified range for continuous and ordinal observation results.
    
    Multiple  ranges of results qualified by different contexts for ordinal or
    continuous observations conforming to this ObservationDefinition.
    """
    
    resource_type = "ObservationDefinitionQualifiedInterval"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.category = None
        """ reference | critical | absolute.
        Type `str`. """
        
        self.range = None
        """ The interval itself, for continuous or ordinal observations.
        Type `Range` (represented as `dict` in JSON). """
        
        self.context = None
        """ Range context qualifier.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.appliesTo = None
        """ Targetted population of the range.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.gender = None
        """ male | female | other | unknown.
        Type `str`. """
        
        self.age = None
        """ Applicable age range, if relevant.
        Type `Range` (represented as `dict` in JSON). """
        
        self.gestationalAge = None
        """ Applicable gestational age range, if relevant.
        Type `Range` (represented as `dict` in JSON). """
        
        self.condition = None
        """ Condition associated with the reference range.
        Type `str`. """
        
        super(ObservationDefinitionQualifiedInterval, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ObservationDefinitionQualifiedInterval, self).elementProperties()
        js.extend([
            ("category", "category", str, False, None, False),
            ("range", "range", range.Range, False, None, False),
            ("context", "context", codeableconcept.CodeableConcept, False, None, False),
            ("appliesTo", "appliesTo", codeableconcept.CodeableConcept, True, None, False),
            ("gender", "gender", str, False, None, False),
            ("age", "age", range.Range, False, None, False),
            ("gestationalAge", "gestationalAge", range.Range, False, None, False),
            ("condition", "condition", str, False, None, False),
        ])
        return js


class ObservationDefinitionQuantitativeDetails(backboneelement.BackboneElement):
    """ Characteristics of quantitative results.
    
    Characteristics for quantitative results of this observation.
    """
    
    resource_type = "ObservationDefinitionQuantitativeDetails"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.customaryUnit = None
        """ Customary unit for quantitative results.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.unit = None
        """ SI unit for quantitative results.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.conversionFactor = None
        """ SI to Customary unit conversion factor.
        Type `float`. """
        
        self.decimalPrecision = None
        """ Decimal precision of observation quantitative results.
        Type `int`. """
        
        super(ObservationDefinitionQuantitativeDetails, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ObservationDefinitionQuantitativeDetails, self).elementProperties()
        js.extend([
            ("customaryUnit", "customaryUnit", codeableconcept.CodeableConcept, False, None, False),
            ("unit", "unit", codeableconcept.CodeableConcept, False, None, False),
            ("conversionFactor", "conversionFactor", float, False, None, False),
            ("decimalPrecision", "decimalPrecision", int, False, None, False),
        ])
        return js


from . import codeableconcept
from . import fhirreference
from . import identifier
from . import range

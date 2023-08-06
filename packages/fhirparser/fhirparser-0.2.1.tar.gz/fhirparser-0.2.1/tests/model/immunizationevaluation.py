#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ImmunizationEvaluation) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class ImmunizationEvaluation(domainresource.DomainResource):
    """ Immunization evaluation information.
    
    Describes a comparison of an immunization event against published
    recommendations to determine if the administration is "valid" in relation
    to those  recommendations.
    """
    
    resource_type = "ImmunizationEvaluation"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.identifier = None
        """ Business identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ completed | entered-in-error.
        Type `str`. """
        
        self.patient = None
        """ Who this evaluation is for.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ Date evaluation was performed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.authority = None
        """ Who is responsible for publishing the recommendations.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.targetDisease = None
        """ Evaluation target disease.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.immunizationEvent = None
        """ Immunization being evaluated.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.doseStatus = None
        """ Status of the dose relative to published recommendations.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.doseStatusReason = None
        """ Reason for the dose status.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Evaluation notes.
        Type `str`. """
        
        self.series = None
        """ Name of vaccine series.
        Type `str`. """
        
        self.doseNumberPositiveInt = None
        """ Dose number within series.
        Type `int`. """
        
        self.doseNumberString = None
        """ Dose number within series.
        Type `str`. """
        
        self.seriesDosesPositiveInt = None
        """ Recommended number of doses for immunity.
        Type `int`. """
        
        self.seriesDosesString = None
        """ Recommended number of doses for immunity.
        Type `str`. """
        
        super(ImmunizationEvaluation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImmunizationEvaluation, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("authority", "authority", fhirreference.FHIRReference, False, None, False),
            ("targetDisease", "targetDisease", codeableconcept.CodeableConcept, False, None, True),
            ("immunizationEvent", "immunizationEvent", fhirreference.FHIRReference, False, None, True),
            ("doseStatus", "doseStatus", codeableconcept.CodeableConcept, False, None, True),
            ("doseStatusReason", "doseStatusReason", codeableconcept.CodeableConcept, True, None, False),
            ("description", "description", str, False, None, False),
            ("series", "series", str, False, None, False),
            ("doseNumberPositiveInt", "doseNumberPositiveInt", int, False, "doseNumber", False),
            ("doseNumberString", "doseNumberString", str, False, "doseNumber", False),
            ("seriesDosesPositiveInt", "seriesDosesPositiveInt", int, False, "seriesDoses", False),
            ("seriesDosesString", "seriesDosesString", str, False, "seriesDoses", False),
        ])
        return js


from . import codeableconcept
from . import fhirdate
from . import fhirreference
from . import identifier

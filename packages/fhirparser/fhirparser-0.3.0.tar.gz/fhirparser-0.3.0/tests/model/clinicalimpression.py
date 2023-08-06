#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ClinicalImpression) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class ClinicalImpression(domainresource.DomainResource):
    """ A clinical assessment performed when planning treatments and management
    strategies for a patient.
    
    A record of a clinical assessment performed to determine what problem(s)
    may affect the patient and before planning the treatments or management
    strategies that are best to manage a patient's condition. Assessments are
    often 1:1 with a clinical consultation / encounter,  but this varies
    greatly depending on the clinical workflow. This resource is called
    "ClinicalImpression" rather than "ClinicalAssessment" to avoid confusion
    with the recording of assessment tools such as Apgar score.
    """
    
    resource_type = "ClinicalImpression"
    
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
        """ in-progress | completed | entered-in-error.
        Type `str`. """
        
        self.statusReason = None
        """ Reason for current status.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.code = None
        """ Kind of assessment performed.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Why/how the assessment was performed.
        Type `str`. """
        
        self.subject = None
        """ Patient or group assessed.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter created as part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.effectiveDateTime = None
        """ Time of assessment.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ Time of assessment.
        Type `Period` (represented as `dict` in JSON). """
        
        self.date = None
        """ When the assessment was documented.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.assessor = None
        """ The clinician performing the assessment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.previous = None
        """ Reference to last assessment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.problem = None
        """ Relevant impressions of patient state.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.investigation = None
        """ One or more sets of investigations (signs, symptoms, etc.).
        List of `ClinicalImpressionInvestigation` items (represented as `dict` in JSON). """
        
        self.protocol = None
        """ Clinical Protocol followed.
        List of `str` items. """
        
        self.summary = None
        """ Summary of the assessment.
        Type `str`. """
        
        self.finding = None
        """ Possible or likely findings and diagnoses.
        List of `ClinicalImpressionFinding` items (represented as `dict` in JSON). """
        
        self.prognosisCodeableConcept = None
        """ Estimate of likely outcome.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.prognosisReference = None
        """ RiskAssessment expressing likely outcome.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.supportingInfo = None
        """ Information supporting the clinical impression.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments made about the ClinicalImpression.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(ClinicalImpression, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClinicalImpression, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("statusReason", "statusReason", codeableconcept.CodeableConcept, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", str, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("effectiveDateTime", "effectiveDateTime", fhirdate.FHIRDate, False, "effective", False),
            ("effectivePeriod", "effectivePeriod", period.Period, False, "effective", False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("assessor", "assessor", fhirreference.FHIRReference, False, None, False),
            ("previous", "previous", fhirreference.FHIRReference, False, None, False),
            ("problem", "problem", fhirreference.FHIRReference, True, None, False),
            ("investigation", "investigation", ClinicalImpressionInvestigation, True, None, False),
            ("protocol", "protocol", str, True, None, False),
            ("summary", "summary", str, False, None, False),
            ("finding", "finding", ClinicalImpressionFinding, True, None, False),
            ("prognosisCodeableConcept", "prognosisCodeableConcept", codeableconcept.CodeableConcept, True, None, False),
            ("prognosisReference", "prognosisReference", fhirreference.FHIRReference, True, None, False),
            ("supportingInfo", "supportingInfo", fhirreference.FHIRReference, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


from . import backboneelement

class ClinicalImpressionFinding(backboneelement.BackboneElement):
    """ Possible or likely findings and diagnoses.
    
    Specific findings or diagnoses that were considered likely or relevant to
    ongoing treatment.
    """
    
    resource_type = "ClinicalImpressionFinding"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.itemCodeableConcept = None
        """ What was found.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.itemReference = None
        """ What was found.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.basis = None
        """ Which investigations support finding.
        Type `str`. """
        
        super(ClinicalImpressionFinding, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClinicalImpressionFinding, self).elementProperties()
        js.extend([
            ("itemCodeableConcept", "itemCodeableConcept", codeableconcept.CodeableConcept, False, None, False),
            ("itemReference", "itemReference", fhirreference.FHIRReference, False, None, False),
            ("basis", "basis", str, False, None, False),
        ])
        return js


class ClinicalImpressionInvestigation(backboneelement.BackboneElement):
    """ One or more sets of investigations (signs, symptoms, etc.).
    
    One or more sets of investigations (signs, symptoms, etc.). The actual
    grouping of investigations varies greatly depending on the type and context
    of the assessment. These investigations may include data generated during
    the assessment process, or data previously generated and recorded that is
    pertinent to the outcomes.
    """
    
    resource_type = "ClinicalImpressionInvestigation"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.code = None
        """ A name/code for the set.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.item = None
        """ Record of a specific investigation.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(ClinicalImpressionInvestigation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClinicalImpressionInvestigation, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("item", "item", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import annotation
from . import codeableconcept
from . import fhirdate
from . import fhirreference
from . import identifier
from . import period

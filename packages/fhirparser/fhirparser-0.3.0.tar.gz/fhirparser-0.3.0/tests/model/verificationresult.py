#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/VerificationResult) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class VerificationResult(domainresource.DomainResource):
    """ Describes validation requirements, source(s), status and dates for one or
    more elements.
    """
    
    resource_type = "VerificationResult"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.target = None
        """ A resource that was validated.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.targetLocation = None
        """ The fhirpath location(s) within the resource that was validated.
        List of `str` items. """
        
        self.need = None
        """ none | initial | periodic.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ attested | validated | in-process | req-revalid | val-fail | reval-
        fail.
        Type `str`. """
        
        self.statusDate = None
        """ When the validation status was updated.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.validationType = None
        """ nothing | primary | multiple.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.validationProcess = None
        """ The primary process by which the target is validated (edit check;
        value set; primary source; multiple sources; standalone; in
        context).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.frequency = None
        """ Frequency of revalidation.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.lastPerformed = None
        """ The date/time validation was last completed (including failed
        validations).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.nextScheduled = None
        """ The date when target is next validated, if appropriate.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.failureAction = None
        """ fatal | warn | rec-only | none.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.primarySource = None
        """ Information about the primary source(s) involved in validation.
        List of `VerificationResultPrimarySource` items (represented as `dict` in JSON). """
        
        self.attestation = None
        """ Information about the entity attesting to information.
        Type `VerificationResultAttestation` (represented as `dict` in JSON). """
        
        self.validator = None
        """ Information about the entity validating information.
        List of `VerificationResultValidator` items (represented as `dict` in JSON). """
        
        super(VerificationResult, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VerificationResult, self).elementProperties()
        js.extend([
            ("target", "target", fhirreference.FHIRReference, True, None, False),
            ("targetLocation", "targetLocation", str, True, None, False),
            ("need", "need", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", str, False, None, True),
            ("statusDate", "statusDate", fhirdate.FHIRDate, False, None, False),
            ("validationType", "validationType", codeableconcept.CodeableConcept, False, None, False),
            ("validationProcess", "validationProcess", codeableconcept.CodeableConcept, True, None, False),
            ("frequency", "frequency", timing.Timing, False, None, False),
            ("lastPerformed", "lastPerformed", fhirdate.FHIRDate, False, None, False),
            ("nextScheduled", "nextScheduled", fhirdate.FHIRDate, False, None, False),
            ("failureAction", "failureAction", codeableconcept.CodeableConcept, False, None, False),
            ("primarySource", "primarySource", VerificationResultPrimarySource, True, None, False),
            ("attestation", "attestation", VerificationResultAttestation, False, None, False),
            ("validator", "validator", VerificationResultValidator, True, None, False),
        ])
        return js


from . import backboneelement

class VerificationResultValidator(backboneelement.BackboneElement):
    """ Information about the entity validating information.
    """
    
    resource_type = "VerificationResultValidator"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.organization = None
        """ Reference to the organization validating information.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.identityCertificate = None
        """ A digital identity certificate associated with the validator.
        Type `str`. """
        
        self.attestationSignature = None
        """ Validator signature.
        Type `Signature` (represented as `dict` in JSON). """
        
        super(VerificationResultValidator, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VerificationResultValidator, self).elementProperties()
        js.extend([
            ("organization", "organization", fhirreference.FHIRReference, False, None, True),
            ("identityCertificate", "identityCertificate", str, False, None, False),
            ("attestationSignature", "attestationSignature", signature.Signature, False, None, False),
        ])
        return js


class VerificationResultAttestation(backboneelement.BackboneElement):
    """ Information about the entity attesting to information.
    """
    
    resource_type = "VerificationResultAttestation"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.who = None
        """ The individual or organization attesting to information.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.onBehalfOf = None
        """ When the who is asserting on behalf of another (organization or
        individual).
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.communicationMethod = None
        """ The method by which attested information was submitted/retrieved.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.date = None
        """ The date the information was attested to.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.sourceIdentityCertificate = None
        """ A digital identity certificate associated with the attestation
        source.
        Type `str`. """
        
        self.proxyIdentityCertificate = None
        """ A digital identity certificate associated with the proxy entity
        submitting attested information on behalf of the attestation source.
        Type `str`. """
        
        self.proxySignature = None
        """ Proxy signature.
        Type `Signature` (represented as `dict` in JSON). """
        
        self.sourceSignature = None
        """ Attester signature.
        Type `Signature` (represented as `dict` in JSON). """
        
        super(VerificationResultAttestation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VerificationResultAttestation, self).elementProperties()
        js.extend([
            ("who", "who", fhirreference.FHIRReference, False, None, False),
            ("onBehalfOf", "onBehalfOf", fhirreference.FHIRReference, False, None, False),
            ("communicationMethod", "communicationMethod", codeableconcept.CodeableConcept, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("sourceIdentityCertificate", "sourceIdentityCertificate", str, False, None, False),
            ("proxyIdentityCertificate", "proxyIdentityCertificate", str, False, None, False),
            ("proxySignature", "proxySignature", signature.Signature, False, None, False),
            ("sourceSignature", "sourceSignature", signature.Signature, False, None, False),
        ])
        return js


class VerificationResultPrimarySource(backboneelement.BackboneElement):
    """ Information about the primary source(s) involved in validation.
    """
    
    resource_type = "VerificationResultPrimarySource"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.who = None
        """ Reference to the primary source.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.type = None
        """ Type of primary source (License Board; Primary Education;
        Continuing Education; Postal Service; Relationship owner;
        Registration Authority; legal source; issuing source; authoritative
        source).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.communicationMethod = None
        """ Method for exchanging information with the primary source.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.validationStatus = None
        """ successful | failed | unknown.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.validationDate = None
        """ When the target was validated against the primary source.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.canPushUpdates = None
        """ yes | no | undetermined.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.pushTypeAvailable = None
        """ specific | any | source.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        super(VerificationResultPrimarySource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VerificationResultPrimarySource, self).elementProperties()
        js.extend([
            ("who", "who", fhirreference.FHIRReference, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("communicationMethod", "communicationMethod", codeableconcept.CodeableConcept, True, None, False),
            ("validationStatus", "validationStatus", codeableconcept.CodeableConcept, False, None, False),
            ("validationDate", "validationDate", fhirdate.FHIRDate, False, None, False),
            ("canPushUpdates", "canPushUpdates", codeableconcept.CodeableConcept, False, None, False),
            ("pushTypeAvailable", "pushTypeAvailable", codeableconcept.CodeableConcept, True, None, False),
        ])
        return js


from . import codeableconcept
from . import fhirdate
from . import fhirreference
from . import signature
from . import timing

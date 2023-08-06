#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/PaymentReconciliation) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class PaymentReconciliation(domainresource.DomainResource):
    """ PaymentReconciliation resource.
    
    This resource provides the details including amount of a payment and
    allocates the payment items being paid.
    """
    
    resource_type = "PaymentReconciliation"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.identifier = None
        """ Business Identifier for a payment reconciliation.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ active | cancelled | draft | entered-in-error.
        Type `str`. """
        
        self.period = None
        """ Period covered.
        Type `Period` (represented as `dict` in JSON). """
        
        self.created = None
        """ Creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.paymentIssuer = None
        """ Party generating payment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.request = None
        """ Reference to requesting resource.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.requestor = None
        """ Responsible practitioner.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ queued | complete | error | partial.
        Type `str`. """
        
        self.disposition = None
        """ Disposition message.
        Type `str`. """
        
        self.paymentDate = None
        """ When payment issued.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.paymentAmount = None
        """ Total amount of Payment.
        Type `Money` (represented as `dict` in JSON). """
        
        self.paymentIdentifier = None
        """ Business identifier for the payment.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.detail = None
        """ Settlement particulars.
        List of `PaymentReconciliationDetail` items (represented as `dict` in JSON). """
        
        self.formCode = None
        """ Printed form identifier.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.processNote = None
        """ Note concerning processing.
        List of `PaymentReconciliationProcessNote` items (represented as `dict` in JSON). """
        
        super(PaymentReconciliation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PaymentReconciliation, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("period", "period", period.Period, False, None, False),
            ("created", "created", fhirdate.FHIRDate, False, None, True),
            ("paymentIssuer", "paymentIssuer", fhirreference.FHIRReference, False, None, False),
            ("request", "request", fhirreference.FHIRReference, False, None, False),
            ("requestor", "requestor", fhirreference.FHIRReference, False, None, False),
            ("outcome", "outcome", str, False, None, False),
            ("disposition", "disposition", str, False, None, False),
            ("paymentDate", "paymentDate", fhirdate.FHIRDate, False, None, True),
            ("paymentAmount", "paymentAmount", money.Money, False, None, True),
            ("paymentIdentifier", "paymentIdentifier", identifier.Identifier, False, None, False),
            ("detail", "detail", PaymentReconciliationDetail, True, None, False),
            ("formCode", "formCode", codeableconcept.CodeableConcept, False, None, False),
            ("processNote", "processNote", PaymentReconciliationProcessNote, True, None, False),
        ])
        return js


from . import backboneelement

class PaymentReconciliationProcessNote(backboneelement.BackboneElement):
    """ Note concerning processing.
    
    A note that describes or explains the processing in a human readable form.
    """
    
    resource_type = "PaymentReconciliationProcessNote"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ display | print | printoper.
        Type `str`. """
        
        self.text = None
        """ Note explanatory text.
        Type `str`. """
        
        super(PaymentReconciliationProcessNote, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PaymentReconciliationProcessNote, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, False),
            ("text", "text", str, False, None, False),
        ])
        return js


class PaymentReconciliationDetail(backboneelement.BackboneElement):
    """ Settlement particulars.
    
    Distribution of the payment amount for a previously acknowledged payable.
    """
    
    resource_type = "PaymentReconciliationDetail"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.identifier = None
        """ Business identifier of the payment detail.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.predecessor = None
        """ Business identifier of the prior payment detail.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.type = None
        """ Category of payment.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.request = None
        """ Request giving rise to the payment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.submitter = None
        """ Submitter of the request.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.response = None
        """ Response committing to a payment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ Date of commitment to pay.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.responsible = None
        """ Contact for the response.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.payee = None
        """ Recipient of the payment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Amount allocated to this payable.
        Type `Money` (represented as `dict` in JSON). """
        
        super(PaymentReconciliationDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PaymentReconciliationDetail, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("predecessor", "predecessor", identifier.Identifier, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("request", "request", fhirreference.FHIRReference, False, None, False),
            ("submitter", "submitter", fhirreference.FHIRReference, False, None, False),
            ("response", "response", fhirreference.FHIRReference, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("responsible", "responsible", fhirreference.FHIRReference, False, None, False),
            ("payee", "payee", fhirreference.FHIRReference, False, None, False),
            ("amount", "amount", money.Money, False, None, False),
        ])
        return js


from . import codeableconcept
from . import fhirdate
from . import fhirreference
from . import identifier
from . import money
from . import period

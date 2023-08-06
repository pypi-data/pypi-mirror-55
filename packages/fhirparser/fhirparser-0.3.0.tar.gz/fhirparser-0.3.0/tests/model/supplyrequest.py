#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/SupplyRequest) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class SupplyRequest(domainresource.DomainResource):
    """ Request for a medication, substance or device.
    
    A record of a request for a medication, substance or device used in the
    healthcare setting.
    """
    
    resource_type = "SupplyRequest"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.identifier = None
        """ Business Identifier for SupplyRequest.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ draft | active | suspended +.
        Type `str`. """
        
        self.category = None
        """ The kind of supply (central, non-stock, etc.).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.priority = None
        """ routine | urgent | asap | stat.
        Type `str`. """
        
        self.itemCodeableConcept = None
        """ Medication, Substance, or Device requested to be supplied.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.itemReference = None
        """ Medication, Substance, or Device requested to be supplied.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ The requested amount of the item indicated.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.parameter = None
        """ Ordered item details.
        List of `SupplyRequestParameter` items (represented as `dict` in JSON). """
        
        self.occurrenceDateTime = None
        """ When the request should be fulfilled.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrencePeriod = None
        """ When the request should be fulfilled.
        Type `Period` (represented as `dict` in JSON). """
        
        self.occurrenceTiming = None
        """ When the request should be fulfilled.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.authoredOn = None
        """ When the request was made.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.requester = None
        """ Individual making the request.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.supplier = None
        """ Who is intended to fulfill the request.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ The reason why the supply item was requested.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ The reason why the supply item was requested.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.deliverFrom = None
        """ The origin of the supply.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.deliverTo = None
        """ The destination of the supply.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(SupplyRequest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SupplyRequest, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("priority", "priority", str, False, None, False),
            ("itemCodeableConcept", "itemCodeableConcept", codeableconcept.CodeableConcept, False, "item", True),
            ("itemReference", "itemReference", fhirreference.FHIRReference, False, "item", True),
            ("quantity", "quantity", quantity.Quantity, False, None, True),
            ("parameter", "parameter", SupplyRequestParameter, True, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", False),
            ("occurrencePeriod", "occurrencePeriod", period.Period, False, "occurrence", False),
            ("occurrenceTiming", "occurrenceTiming", timing.Timing, False, "occurrence", False),
            ("authoredOn", "authoredOn", fhirdate.FHIRDate, False, None, False),
            ("requester", "requester", fhirreference.FHIRReference, False, None, False),
            ("supplier", "supplier", fhirreference.FHIRReference, True, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("deliverFrom", "deliverFrom", fhirreference.FHIRReference, False, None, False),
            ("deliverTo", "deliverTo", fhirreference.FHIRReference, False, None, False),
        ])
        return js


from . import backboneelement

class SupplyRequestParameter(backboneelement.BackboneElement):
    """ Ordered item details.
    
    Specific parameters for the ordered item.  For example, the size of the
    indicated item.
    """
    
    resource_type = "SupplyRequestParameter"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.code = None
        """ Item detail.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueCodeableConcept = None
        """ Value of detail.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ Value of detail.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueRange = None
        """ Value of detail.
        Type `Range` (represented as `dict` in JSON). """
        
        self.valueBoolean = None
        """ Value of detail.
        Type `bool`. """
        
        super(SupplyRequestParameter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SupplyRequestParameter, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("valueCodeableConcept", "valueCodeableConcept", codeableconcept.CodeableConcept, False, "value", False),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", False),
            ("valueRange", "valueRange", range.Range, False, "value", False),
            ("valueBoolean", "valueBoolean", bool, False, "value", False),
        ])
        return js


from . import codeableconcept
from . import fhirdate
from . import fhirreference
from . import identifier
from . import period
from . import quantity
from . import range
from . import timing

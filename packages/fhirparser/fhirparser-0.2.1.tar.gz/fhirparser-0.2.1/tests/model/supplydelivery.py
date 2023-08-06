#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/SupplyDelivery) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class SupplyDelivery(domainresource.DomainResource):
    """ Delivery of bulk Supplies.
    
    Record of delivery of what is supplied.
    """
    
    resource_type = "SupplyDelivery"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.identifier = None
        """ External identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.basedOn = None
        """ Fulfills plan, proposal or order.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Part of referenced event.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ in-progress | completed | abandoned | entered-in-error.
        Type `str`. """
        
        self.patient = None
        """ Patient for whom the item is supplied.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.type = None
        """ Category of dispense event.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.suppliedItem = None
        """ The item that is delivered or supplied.
        Type `SupplyDeliverySuppliedItem` (represented as `dict` in JSON). """
        
        self.occurrenceDateTime = None
        """ When event occurred.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrencePeriod = None
        """ When event occurred.
        Type `Period` (represented as `dict` in JSON). """
        
        self.occurrenceTiming = None
        """ When event occurred.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.supplier = None
        """ Dispenser.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.destination = None
        """ Where the Supply was sent.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.receiver = None
        """ Who collected the Supply.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(SupplyDelivery, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SupplyDelivery, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("suppliedItem", "suppliedItem", SupplyDeliverySuppliedItem, False, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", False),
            ("occurrencePeriod", "occurrencePeriod", period.Period, False, "occurrence", False),
            ("occurrenceTiming", "occurrenceTiming", timing.Timing, False, "occurrence", False),
            ("supplier", "supplier", fhirreference.FHIRReference, False, None, False),
            ("destination", "destination", fhirreference.FHIRReference, False, None, False),
            ("receiver", "receiver", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class SupplyDeliverySuppliedItem(backboneelement.BackboneElement):
    """ The item that is delivered or supplied.
    
    The item that is being delivered or has been supplied.
    """
    
    resource_type = "SupplyDeliverySuppliedItem"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.quantity = None
        """ Amount dispensed.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.itemCodeableConcept = None
        """ Medication, Substance, or Device supplied.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.itemReference = None
        """ Medication, Substance, or Device supplied.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(SupplyDeliverySuppliedItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SupplyDeliverySuppliedItem, self).elementProperties()
        js.extend([
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("itemCodeableConcept", "itemCodeableConcept", codeableconcept.CodeableConcept, False, "item", False),
            ("itemReference", "itemReference", fhirreference.FHIRReference, False, "item", False),
        ])
        return js


from . import codeableconcept
from . import fhirdate
from . import fhirreference
from . import identifier
from . import period
from . import quantity
from . import timing

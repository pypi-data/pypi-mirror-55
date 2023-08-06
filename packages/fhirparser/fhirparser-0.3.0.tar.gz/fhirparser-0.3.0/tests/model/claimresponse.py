#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ClaimResponse) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class ClaimResponse(domainresource.DomainResource):
    """ Response to a claim predetermination or preauthorization.
    
    This resource provides the adjudication details from the processing of a
    Claim resource.
    """
    
    resource_type = "ClaimResponse"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.identifier = None
        """ Business Identifier for a claim response.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ active | cancelled | draft | entered-in-error.
        Type `str`. """
        
        self.type = None
        """ More granular claim type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subType = None
        """ More granular claim type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.use = None
        """ claim | preauthorization | predetermination.
        Type `str`. """
        
        self.patient = None
        """ The recipient of the products and services.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.created = None
        """ Response creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.insurer = None
        """ Party responsible for reimbursement.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.requestor = None
        """ Party responsible for the claim.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.request = None
        """ Id of resource triggering adjudication.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ queued | complete | error | partial.
        Type `str`. """
        
        self.disposition = None
        """ Disposition Message.
        Type `str`. """
        
        self.preAuthRef = None
        """ Preauthorization reference.
        Type `str`. """
        
        self.preAuthPeriod = None
        """ Preauthorization reference effective period.
        Type `Period` (represented as `dict` in JSON). """
        
        self.payeeType = None
        """ Party to be paid any benefits payable.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.item = None
        """ Adjudication for claim line items.
        List of `ClaimResponseItem` items (represented as `dict` in JSON). """
        
        self.addItem = None
        """ Insurer added line items.
        List of `ClaimResponseAddItem` items (represented as `dict` in JSON). """
        
        self.adjudication = None
        """ Header-level adjudication.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        self.total = None
        """ Adjudication totals.
        List of `ClaimResponseTotal` items (represented as `dict` in JSON). """
        
        self.payment = None
        """ Payment Details.
        Type `ClaimResponsePayment` (represented as `dict` in JSON). """
        
        self.fundsReserve = None
        """ Funds reserved status.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.formCode = None
        """ Printed form identifier.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.form = None
        """ Printed reference or actual form.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.processNote = None
        """ Note concerning adjudication.
        List of `ClaimResponseProcessNote` items (represented as `dict` in JSON). """
        
        self.communicationRequest = None
        """ Request for additional information.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.insurance = None
        """ Patient insurance information.
        List of `ClaimResponseInsurance` items (represented as `dict` in JSON). """
        
        self.error = None
        """ Processing errors.
        List of `ClaimResponseError` items (represented as `dict` in JSON). """
        
        super(ClaimResponse, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponse, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("subType", "subType", codeableconcept.CodeableConcept, False, None, False),
            ("use", "use", str, False, None, True),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("created", "created", fhirdate.FHIRDate, False, None, True),
            ("insurer", "insurer", fhirreference.FHIRReference, False, None, True),
            ("requestor", "requestor", fhirreference.FHIRReference, False, None, False),
            ("request", "request", fhirreference.FHIRReference, False, None, False),
            ("outcome", "outcome", str, False, None, True),
            ("disposition", "disposition", str, False, None, False),
            ("preAuthRef", "preAuthRef", str, False, None, False),
            ("preAuthPeriod", "preAuthPeriod", period.Period, False, None, False),
            ("payeeType", "payeeType", codeableconcept.CodeableConcept, False, None, False),
            ("item", "item", ClaimResponseItem, True, None, False),
            ("addItem", "addItem", ClaimResponseAddItem, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, False),
            ("total", "total", ClaimResponseTotal, True, None, False),
            ("payment", "payment", ClaimResponsePayment, False, None, False),
            ("fundsReserve", "fundsReserve", codeableconcept.CodeableConcept, False, None, False),
            ("formCode", "formCode", codeableconcept.CodeableConcept, False, None, False),
            ("form", "form", attachment.Attachment, False, None, False),
            ("processNote", "processNote", ClaimResponseProcessNote, True, None, False),
            ("communicationRequest", "communicationRequest", fhirreference.FHIRReference, True, None, False),
            ("insurance", "insurance", ClaimResponseInsurance, True, None, False),
            ("error", "error", ClaimResponseError, True, None, False),
        ])
        return js


from . import backboneelement

class ClaimResponseError(backboneelement.BackboneElement):
    """ Processing errors.
    
    Errors encountered during the processing of the adjudication.
    """
    
    resource_type = "ClaimResponseError"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.itemSequence = None
        """ Item sequence number.
        Type `int`. """
        
        self.detailSequence = None
        """ Detail sequence number.
        Type `int`. """
        
        self.subDetailSequence = None
        """ Subdetail sequence number.
        Type `int`. """
        
        self.code = None
        """ Error code detailing processing issues.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ClaimResponseError, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseError, self).elementProperties()
        js.extend([
            ("itemSequence", "itemSequence", int, False, None, False),
            ("detailSequence", "detailSequence", int, False, None, False),
            ("subDetailSequence", "subDetailSequence", int, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
        ])
        return js


class ClaimResponseInsurance(backboneelement.BackboneElement):
    """ Patient insurance information.
    
    Financial instruments for reimbursement for the health care products and
    services specified on the claim.
    """
    
    resource_type = "ClaimResponseInsurance"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.sequence = None
        """ Insurance instance identifier.
        Type `int`. """
        
        self.focal = None
        """ Coverage to be used for adjudication.
        Type `bool`. """
        
        self.coverage = None
        """ Insurance information.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.businessArrangement = None
        """ Additional provider contract number.
        Type `str`. """
        
        self.claimResponse = None
        """ Adjudication results.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ClaimResponseInsurance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseInsurance, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("focal", "focal", bool, False, None, True),
            ("coverage", "coverage", fhirreference.FHIRReference, False, None, True),
            ("businessArrangement", "businessArrangement", str, False, None, False),
            ("claimResponse", "claimResponse", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class ClaimResponseProcessNote(backboneelement.BackboneElement):
    """ Note concerning adjudication.
    
    A note that describes or explains adjudication results in a human readable
    form.
    """
    
    resource_type = "ClaimResponseProcessNote"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.number = None
        """ Note instance identifier.
        Type `int`. """
        
        self.type = None
        """ display | print | printoper.
        Type `str`. """
        
        self.text = None
        """ Note explanatory text.
        Type `str`. """
        
        self.language = None
        """ Language of the text.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ClaimResponseProcessNote, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseProcessNote, self).elementProperties()
        js.extend([
            ("number", "number", int, False, None, False),
            ("type", "type", str, False, None, False),
            ("text", "text", str, False, None, True),
            ("language", "language", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class ClaimResponsePayment(backboneelement.BackboneElement):
    """ Payment Details.
    
    Payment details for the adjudication of the claim.
    """
    
    resource_type = "ClaimResponsePayment"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ Partial or complete payment.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.adjustment = None
        """ Payment adjustment for non-claim issues.
        Type `Money` (represented as `dict` in JSON). """
        
        self.adjustmentReason = None
        """ Explanation for the adjustment.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.date = None
        """ Expected date of payment.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.amount = None
        """ Payable amount after adjustment.
        Type `Money` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Business identifier for the payment.
        Type `Identifier` (represented as `dict` in JSON). """
        
        super(ClaimResponsePayment, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponsePayment, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("adjustment", "adjustment", money.Money, False, None, False),
            ("adjustmentReason", "adjustmentReason", codeableconcept.CodeableConcept, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("amount", "amount", money.Money, False, None, True),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
        ])
        return js


class ClaimResponseTotal(backboneelement.BackboneElement):
    """ Adjudication totals.
    
    Categorized monetary totals for the adjudication.
    """
    
    resource_type = "ClaimResponseTotal"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.category = None
        """ Type of adjudication information.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Financial total for the category.
        Type `Money` (represented as `dict` in JSON). """
        
        super(ClaimResponseTotal, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseTotal, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, True),
            ("amount", "amount", money.Money, False, None, True),
        ])
        return js


class ClaimResponseAddItem(backboneelement.BackboneElement):
    """ Insurer added line items.
    
    The first-tier service adjudications for payor added product or service
    lines.
    """
    
    resource_type = "ClaimResponseAddItem"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.itemSequence = None
        """ Item sequence number.
        List of `int` items. """
        
        self.detailSequence = None
        """ Detail sequence number.
        List of `int` items. """
        
        self.subdetailSequence = None
        """ Subdetail sequence number.
        List of `int` items. """
        
        self.provider = None
        """ Authorized providers.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.productOrService = None
        """ Billing, service, product, or drug code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.modifier = None
        """ Service/Product billing modifiers.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.programCode = None
        """ Program the product or service is provided under.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.servicedDate = None
        """ Date or dates of service or product delivery.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.servicedPeriod = None
        """ Date or dates of service or product delivery.
        Type `Period` (represented as `dict` in JSON). """
        
        self.locationCodeableConcept = None
        """ Place of service or where product was supplied.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.locationAddress = None
        """ Place of service or where product was supplied.
        Type `Address` (represented as `dict` in JSON). """
        
        self.locationReference = None
        """ Place of service or where product was supplied.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Count of products or services.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.unitPrice = None
        """ Fee, charge or cost per item.
        Type `Money` (represented as `dict` in JSON). """
        
        self.factor = None
        """ Price scaling factor.
        Type `float`. """
        
        self.net = None
        """ Total item cost.
        Type `Money` (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Anatomical location.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subSite = None
        """ Anatomical sub-location.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Added items adjudication.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        self.detail = None
        """ Insurer added line details.
        List of `ClaimResponseAddItemDetail` items (represented as `dict` in JSON). """
        
        super(ClaimResponseAddItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseAddItem, self).elementProperties()
        js.extend([
            ("itemSequence", "itemSequence", int, True, None, False),
            ("detailSequence", "detailSequence", int, True, None, False),
            ("subdetailSequence", "subdetailSequence", int, True, None, False),
            ("provider", "provider", fhirreference.FHIRReference, True, None, False),
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, True),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("programCode", "programCode", codeableconcept.CodeableConcept, True, None, False),
            ("servicedDate", "servicedDate", fhirdate.FHIRDate, False, "serviced", False),
            ("servicedPeriod", "servicedPeriod", period.Period, False, "serviced", False),
            ("locationCodeableConcept", "locationCodeableConcept", codeableconcept.CodeableConcept, False, "location", False),
            ("locationAddress", "locationAddress", address.Address, False, "location", False),
            ("locationReference", "locationReference", fhirreference.FHIRReference, False, "location", False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("bodySite", "bodySite", codeableconcept.CodeableConcept, False, None, False),
            ("subSite", "subSite", codeableconcept.CodeableConcept, True, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, True),
            ("detail", "detail", ClaimResponseAddItemDetail, True, None, False),
        ])
        return js


class ClaimResponseItem(backboneelement.BackboneElement):
    """ Adjudication for claim line items.
    
    A claim line. Either a simple (a product or service) or a 'group' of
    details which can also be a simple items or groups of sub-details.
    """
    
    resource_type = "ClaimResponseItem"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.itemSequence = None
        """ Claim item instance identifier.
        Type `int`. """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Adjudication details.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        self.detail = None
        """ Adjudication for claim details.
        List of `ClaimResponseItemDetail` items (represented as `dict` in JSON). """
        
        super(ClaimResponseItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseItem, self).elementProperties()
        js.extend([
            ("itemSequence", "itemSequence", int, False, None, True),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, True),
            ("detail", "detail", ClaimResponseItemDetail, True, None, False),
        ])
        return js


class ClaimResponseItemDetail(backboneelement.BackboneElement):
    """ Adjudication for claim details.
    
    A claim detail. Either a simple (a product or service) or a 'group' of sub-
    details which are simple items.
    """
    
    resource_type = "ClaimResponseItemDetail"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.detailSequence = None
        """ Claim detail instance identifier.
        Type `int`. """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Detail level adjudication details.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        self.subDetail = None
        """ Adjudication for claim sub-details.
        List of `ClaimResponseItemDetailSubDetail` items (represented as `dict` in JSON). """
        
        super(ClaimResponseItemDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseItemDetail, self).elementProperties()
        js.extend([
            ("detailSequence", "detailSequence", int, False, None, True),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, True),
            ("subDetail", "subDetail", ClaimResponseItemDetailSubDetail, True, None, False),
        ])
        return js


class ClaimResponseItemAdjudication(backboneelement.BackboneElement):
    """ Adjudication details.
    
    If this item is a group then the values here are a summary of the
    adjudication of the detail items. If this item is a simple product or
    service then this is the result of the adjudication of this item.
    """
    
    resource_type = "ClaimResponseItemAdjudication"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.category = None
        """ Type of adjudication information.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reason = None
        """ Explanation of adjudication outcome.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Monetary amount.
        Type `Money` (represented as `dict` in JSON). """
        
        self.value = None
        """ Non-monetary value.
        Type `float`. """
        
        super(ClaimResponseItemAdjudication, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseItemAdjudication, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, True),
            ("reason", "reason", codeableconcept.CodeableConcept, False, None, False),
            ("amount", "amount", money.Money, False, None, False),
            ("value", "value", float, False, None, False),
        ])
        return js


class ClaimResponseItemDetailSubDetail(backboneelement.BackboneElement):
    """ Adjudication for claim sub-details.
    
    A sub-detail adjudication of a simple product or service.
    """
    
    resource_type = "ClaimResponseItemDetailSubDetail"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.subDetailSequence = None
        """ Claim sub-detail instance identifier.
        Type `int`. """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Subdetail level adjudication details.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        super(ClaimResponseItemDetailSubDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseItemDetailSubDetail, self).elementProperties()
        js.extend([
            ("subDetailSequence", "subDetailSequence", int, False, None, True),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, False),
        ])
        return js


class ClaimResponseAddItemDetail(backboneelement.BackboneElement):
    """ Insurer added line details.
    
    The second-tier service adjudications for payor added services.
    """
    
    resource_type = "ClaimResponseAddItemDetail"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.productOrService = None
        """ Billing, service, product, or drug code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.modifier = None
        """ Service/Product billing modifiers.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Count of products or services.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.unitPrice = None
        """ Fee, charge or cost per item.
        Type `Money` (represented as `dict` in JSON). """
        
        self.factor = None
        """ Price scaling factor.
        Type `float`. """
        
        self.net = None
        """ Total item cost.
        Type `Money` (represented as `dict` in JSON). """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Added items detail adjudication.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        self.subDetail = None
        """ Insurer added line items.
        List of `ClaimResponseAddItemDetailSubDetail` items (represented as `dict` in JSON). """
        
        super(ClaimResponseAddItemDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseAddItemDetail, self).elementProperties()
        js.extend([
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, True),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, True),
            ("subDetail", "subDetail", ClaimResponseAddItemDetailSubDetail, True, None, False),
        ])
        return js


class ClaimResponseAddItemDetailSubDetail(backboneelement.BackboneElement):
    """ Insurer added line items.
    
    The third-tier service adjudications for payor added services.
    """
    
    resource_type = "ClaimResponseAddItemDetailSubDetail"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.productOrService = None
        """ Billing, service, product, or drug code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.modifier = None
        """ Service/Product billing modifiers.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Count of products or services.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.unitPrice = None
        """ Fee, charge or cost per item.
        Type `Money` (represented as `dict` in JSON). """
        
        self.factor = None
        """ Price scaling factor.
        Type `float`. """
        
        self.net = None
        """ Total item cost.
        Type `Money` (represented as `dict` in JSON). """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Added items detail adjudication.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        super(ClaimResponseAddItemDetailSubDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseAddItemDetailSubDetail, self).elementProperties()
        js.extend([
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, True),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, True),
        ])
        return js


from . import address
from . import attachment
from . import codeableconcept
from . import fhirdate
from . import fhirreference
from . import identifier
from . import money
from . import period
from . import quantity

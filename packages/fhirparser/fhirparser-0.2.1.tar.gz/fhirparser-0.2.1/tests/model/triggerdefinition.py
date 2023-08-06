#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/TriggerDefinition) on 2019-11-06.
#  2019, SMART Health IT.


from . import element

class TriggerDefinition(element.Element):
    """ Defines an expected trigger for a module.
    
    A description of a triggering event. Triggering events can be named events,
    data events, or periodic, as determined by the type element.
    """
    
    resource_type = "TriggerDefinition"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ named-event | periodic | data-changed | data-added | data-modified
        | data-removed | data-accessed | data-access-ended.
        Type `str`. """
        
        self.name = None
        """ Name or URI that identifies the event.
        Type `str`. """
        
        self.timingTiming = None
        """ Timing of the event.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.timingReference = None
        """ Timing of the event.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.timingDate = None
        """ Timing of the event.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.timingDateTime = None
        """ Timing of the event.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.data = None
        """ Triggering data of the event (multiple = 'and').
        List of `DataRequirement` items (represented as `dict` in JSON). """
        
        self.condition = None
        """ Whether the event triggers (boolean expression).
        Type `Expression` (represented as `dict` in JSON). """
        
        super(TriggerDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(TriggerDefinition, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("name", "name", str, False, None, False),
            ("timingTiming", "timingTiming", timing.Timing, False, "timing", False),
            ("timingReference", "timingReference", fhirreference.FHIRReference, False, "timing", False),
            ("timingDate", "timingDate", fhirdate.FHIRDate, False, "timing", False),
            ("timingDateTime", "timingDateTime", fhirdate.FHIRDate, False, "timing", False),
            ("data", "data", datarequirement.DataRequirement, True, None, False),
            ("condition", "condition", expression.Expression, False, None, False),
        ])
        return js


from . import datarequirement
from . import expression
from . import fhirdate
from . import fhirreference
from . import timing

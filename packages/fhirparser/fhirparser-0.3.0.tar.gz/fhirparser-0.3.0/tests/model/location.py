#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Location) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class Location(domainresource.DomainResource):
    """ Details and position information for a physical place.
    
    Details and position information for a physical place where services are
    provided and resources and participants may be stored, found, contained, or
    accommodated.
    """
    
    resource_type = "Location"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.identifier = None
        """ Unique code or number identifying the location to its users.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ active | suspended | inactive.
        Type `str`. """
        
        self.operationalStatus = None
        """ The operational status of the location (typically only for a
        bed/room).
        Type `Coding` (represented as `dict` in JSON). """
        
        self.name = None
        """ Name of the location as used by humans.
        Type `str`. """
        
        self.alias = None
        """ A list of alternate names that the location is known as, or was
        known as, in the past.
        List of `str` items. """
        
        self.description = None
        """ Additional details about the location that could be displayed as
        further information to identify the location beyond its name.
        Type `str`. """
        
        self.mode = None
        """ instance | kind.
        Type `str`. """
        
        self.type = None
        """ Type of function performed.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.telecom = None
        """ Contact details of the location.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.address = None
        """ Physical location.
        Type `Address` (represented as `dict` in JSON). """
        
        self.physicalType = None
        """ Physical form of the location.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.position = None
        """ The absolute geographic location.
        Type `LocationPosition` (represented as `dict` in JSON). """
        
        self.managingOrganization = None
        """ Organization responsible for provisioning and upkeep.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Another Location this one is physically a part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.hoursOfOperation = None
        """ What days/times during a week is this location usually open.
        List of `LocationHoursOfOperation` items (represented as `dict` in JSON). """
        
        self.availabilityExceptions = None
        """ Description of availability exceptions.
        Type `str`. """
        
        self.endpoint = None
        """ Technical endpoints providing access to services operated for the
        location.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(Location, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Location, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, False),
            ("operationalStatus", "operationalStatus", coding.Coding, False, None, False),
            ("name", "name", str, False, None, False),
            ("alias", "alias", str, True, None, False),
            ("description", "description", str, False, None, False),
            ("mode", "mode", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
            ("address", "address", address.Address, False, None, False),
            ("physicalType", "physicalType", codeableconcept.CodeableConcept, False, None, False),
            ("position", "position", LocationPosition, False, None, False),
            ("managingOrganization", "managingOrganization", fhirreference.FHIRReference, False, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, False, None, False),
            ("hoursOfOperation", "hoursOfOperation", LocationHoursOfOperation, True, None, False),
            ("availabilityExceptions", "availabilityExceptions", str, False, None, False),
            ("endpoint", "endpoint", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class LocationHoursOfOperation(backboneelement.BackboneElement):
    """ What days/times during a week is this location usually open.
    """
    
    resource_type = "LocationHoursOfOperation"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.daysOfWeek = None
        """ mon | tue | wed | thu | fri | sat | sun.
        List of `str` items. """
        
        self.allDay = None
        """ The Location is open all day.
        Type `bool`. """
        
        self.openingTime = None
        """ Time that the Location opens.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.closingTime = None
        """ Time that the Location closes.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(LocationHoursOfOperation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(LocationHoursOfOperation, self).elementProperties()
        js.extend([
            ("daysOfWeek", "daysOfWeek", str, True, None, False),
            ("allDay", "allDay", bool, False, None, False),
            ("openingTime", "openingTime", fhirdate.FHIRDate, False, None, False),
            ("closingTime", "closingTime", fhirdate.FHIRDate, False, None, False),
        ])
        return js


class LocationPosition(backboneelement.BackboneElement):
    """ The absolute geographic location.
    
    The absolute geographic location of the Location, expressed using the WGS84
    datum (This is the same co-ordinate system used in KML).
    """
    
    resource_type = "LocationPosition"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.longitude = None
        """ Longitude with WGS84 datum.
        Type `float`. """
        
        self.latitude = None
        """ Latitude with WGS84 datum.
        Type `float`. """
        
        self.altitude = None
        """ Altitude with WGS84 datum.
        Type `float`. """
        
        super(LocationPosition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(LocationPosition, self).elementProperties()
        js.extend([
            ("longitude", "longitude", float, False, None, True),
            ("latitude", "latitude", float, False, None, True),
            ("altitude", "altitude", float, False, None, False),
        ])
        return js


from . import address
from . import codeableconcept
from . import coding
from . import contactpoint
from . import fhirdate
from . import fhirreference
from . import identifier

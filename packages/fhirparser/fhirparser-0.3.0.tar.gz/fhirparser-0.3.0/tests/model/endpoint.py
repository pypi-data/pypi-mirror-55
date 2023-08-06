#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Endpoint) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class Endpoint(domainresource.DomainResource):
    """ The technical details of an endpoint that can be used for electronic
    services.
    
    The technical details of an endpoint that can be used for electronic
    services, such as for web services providing XDS.b or a REST endpoint for
    another FHIR server. This may include any security context information.
    """
    
    resource_type = "Endpoint"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.identifier = None
        """ Identifies this endpoint across multiple systems.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ active | suspended | error | off | entered-in-error | test.
        Type `str`. """
        
        self.connectionType = None
        """ Protocol/Profile/Standard to be used with this endpoint connection.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.name = None
        """ A name that this endpoint can be identified by.
        Type `str`. """
        
        self.managingOrganization = None
        """ Organization that manages this endpoint (might not be the
        organization that exposes the endpoint).
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.contact = None
        """ Contact details for source (e.g. troubleshooting).
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.period = None
        """ Interval the endpoint is expected to be operational.
        Type `Period` (represented as `dict` in JSON). """
        
        self.payloadType = None
        """ The type of content that may be used at this endpoint (e.g. XDS
        Discharge summaries).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.payloadMimeType = None
        """ Mimetype to send. If not specified, the content could be anything
        (including no payload, if the connectionType defined this).
        List of `str` items. """
        
        self.address = None
        """ The technical base address for connecting to this endpoint.
        Type `str`. """
        
        self.header = None
        """ Usage depends on the channel type.
        List of `str` items. """
        
        super(Endpoint, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Endpoint, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("connectionType", "connectionType", coding.Coding, False, None, True),
            ("name", "name", str, False, None, False),
            ("managingOrganization", "managingOrganization", fhirreference.FHIRReference, False, None, False),
            ("contact", "contact", contactpoint.ContactPoint, True, None, False),
            ("period", "period", period.Period, False, None, False),
            ("payloadType", "payloadType", codeableconcept.CodeableConcept, True, None, True),
            ("payloadMimeType", "payloadMimeType", str, True, None, False),
            ("address", "address", str, False, None, True),
            ("header", "header", str, True, None, False),
        ])
        return js


from . import codeableconcept
from . import coding
from . import contactpoint
from . import fhirreference
from . import identifier
from . import period

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/PlanDefinition) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class PlanDefinition(domainresource.DomainResource):
    """ The definition of a plan for a series of actions, independent of any
    specific patient or context.
    
    This resource allows for the definition of various types of plans as a
    sharable, consumable, and executable artifact. The resource is general
    enough to support the description of a broad range of clinical artifacts
    such as clinical decision support rules, order sets and protocols.
    """
    
    resource_type = "PlanDefinition"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.url = None
        """ Canonical identifier for this plan definition, represented as a URI
        (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the plan definition.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the plan definition.
        Type `str`. """
        
        self.name = None
        """ Name for this plan definition (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this plan definition (human friendly).
        Type `str`. """
        
        self.subtitle = None
        """ Subordinate title of the plan definition.
        Type `str`. """
        
        self.type = None
        """ order-set | clinical-protocol | eca-rule | workflow-definition.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ draft | active | retired | unknown.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
        self.subjectCodeableConcept = None
        """ Type of individual the plan definition is focused on.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subjectReference = None
        """ Type of individual the plan definition is focused on.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ Date last changed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.publisher = None
        """ Name of the publisher (organization or individual).
        Type `str`. """
        
        self.contact = None
        """ Contact details for the publisher.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Natural language description of the plan definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for plan definition (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this plan definition is defined.
        Type `str`. """
        
        self.usage = None
        """ Describes the clinical usage of the plan.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the plan definition was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the plan definition was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the plan definition is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.topic = None
        """ E.g. Education, Treatment, Assessment.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.author = None
        """ Who authored the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.editor = None
        """ Who edited the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.reviewer = None
        """ Who reviewed the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.endorser = None
        """ Who endorsed the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.relatedArtifact = None
        """ Additional documentation, citations.
        List of `RelatedArtifact` items (represented as `dict` in JSON). """
        
        self.library = None
        """ Logic used by the plan definition.
        List of `str` items. """
        
        self.goal = None
        """ What the plan is trying to accomplish.
        List of `PlanDefinitionGoal` items (represented as `dict` in JSON). """
        
        self.action = None
        """ Action defined by the plan.
        List of `PlanDefinitionAction` items (represented as `dict` in JSON). """
        
        super(PlanDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("subtitle", "subtitle", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("subjectCodeableConcept", "subjectCodeableConcept", codeableconcept.CodeableConcept, False, "subject", False),
            ("subjectReference", "subjectReference", fhirreference.FHIRReference, False, "subject", False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("usage", "usage", str, False, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("approvalDate", "approvalDate", fhirdate.FHIRDate, False, None, False),
            ("lastReviewDate", "lastReviewDate", fhirdate.FHIRDate, False, None, False),
            ("effectivePeriod", "effectivePeriod", period.Period, False, None, False),
            ("topic", "topic", codeableconcept.CodeableConcept, True, None, False),
            ("author", "author", contactdetail.ContactDetail, True, None, False),
            ("editor", "editor", contactdetail.ContactDetail, True, None, False),
            ("reviewer", "reviewer", contactdetail.ContactDetail, True, None, False),
            ("endorser", "endorser", contactdetail.ContactDetail, True, None, False),
            ("relatedArtifact", "relatedArtifact", relatedartifact.RelatedArtifact, True, None, False),
            ("library", "library", str, True, None, False),
            ("goal", "goal", PlanDefinitionGoal, True, None, False),
            ("action", "action", PlanDefinitionAction, True, None, False),
        ])
        return js


from . import backboneelement

class PlanDefinitionAction(backboneelement.BackboneElement):
    """ Action defined by the plan.
    
    An action or group of actions to be taken as part of the plan.
    """
    
    resource_type = "PlanDefinitionAction"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.prefix = None
        """ User-visible prefix for the action (e.g. 1. or A.).
        Type `str`. """
        
        self.title = None
        """ User-visible title.
        Type `str`. """
        
        self.description = None
        """ Brief description of the action.
        Type `str`. """
        
        self.textEquivalent = None
        """ Static text equivalent of the action, used if the dynamic aspects
        cannot be interpreted by the receiving system.
        Type `str`. """
        
        self.priority = None
        """ routine | urgent | asap | stat.
        Type `str`. """
        
        self.code = None
        """ Code representing the meaning of the action or sub-actions.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reason = None
        """ Why the action should be performed.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.documentation = None
        """ Supporting documentation for the intended performer of the action.
        List of `RelatedArtifact` items (represented as `dict` in JSON). """
        
        self.goalId = None
        """ What goals this action supports.
        List of `str` items. """
        
        self.subjectCodeableConcept = None
        """ Type of individual the action is focused on.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subjectReference = None
        """ Type of individual the action is focused on.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.trigger = None
        """ When the action should be triggered.
        List of `TriggerDefinition` items (represented as `dict` in JSON). """
        
        self.condition = None
        """ Whether or not the action is applicable.
        List of `PlanDefinitionActionCondition` items (represented as `dict` in JSON). """
        
        self.input = None
        """ Input data requirements.
        List of `DataRequirement` items (represented as `dict` in JSON). """
        
        self.output = None
        """ Output data definition.
        List of `DataRequirement` items (represented as `dict` in JSON). """
        
        self.relatedAction = None
        """ Relationship to another action.
        List of `PlanDefinitionActionRelatedAction` items (represented as `dict` in JSON). """
        
        self.timingDateTime = None
        """ When the action should take place.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.timingAge = None
        """ When the action should take place.
        Type `Age` (represented as `dict` in JSON). """
        
        self.timingPeriod = None
        """ When the action should take place.
        Type `Period` (represented as `dict` in JSON). """
        
        self.timingDuration = None
        """ When the action should take place.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.timingRange = None
        """ When the action should take place.
        Type `Range` (represented as `dict` in JSON). """
        
        self.timingTiming = None
        """ When the action should take place.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.participant = None
        """ Who should participate in the action.
        List of `PlanDefinitionActionParticipant` items (represented as `dict` in JSON). """
        
        self.type = None
        """ create | update | remove | fire-event.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.groupingBehavior = None
        """ visual-group | logical-group | sentence-group.
        Type `str`. """
        
        self.selectionBehavior = None
        """ any | all | all-or-none | exactly-one | at-most-one | one-or-more.
        Type `str`. """
        
        self.requiredBehavior = None
        """ must | could | must-unless-documented.
        Type `str`. """
        
        self.precheckBehavior = None
        """ yes | no.
        Type `str`. """
        
        self.cardinalityBehavior = None
        """ single | multiple.
        Type `str`. """
        
        self.definitionCanonical = None
        """ Description of the activity to be performed.
        Type `str`. """
        
        self.definitionUri = None
        """ Description of the activity to be performed.
        Type `str`. """
        
        self.transform = None
        """ Transform to apply the template.
        Type `str`. """
        
        self.dynamicValue = None
        """ Dynamic aspects of the definition.
        List of `PlanDefinitionActionDynamicValue` items (represented as `dict` in JSON). """
        
        self.action = None
        """ A sub-action.
        List of `PlanDefinitionAction` items (represented as `dict` in JSON). """
        
        super(PlanDefinitionAction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionAction, self).elementProperties()
        js.extend([
            ("prefix", "prefix", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("textEquivalent", "textEquivalent", str, False, None, False),
            ("priority", "priority", str, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, True, None, False),
            ("reason", "reason", codeableconcept.CodeableConcept, True, None, False),
            ("documentation", "documentation", relatedartifact.RelatedArtifact, True, None, False),
            ("goalId", "goalId", str, True, None, False),
            ("subjectCodeableConcept", "subjectCodeableConcept", codeableconcept.CodeableConcept, False, "subject", False),
            ("subjectReference", "subjectReference", fhirreference.FHIRReference, False, "subject", False),
            ("trigger", "trigger", triggerdefinition.TriggerDefinition, True, None, False),
            ("condition", "condition", PlanDefinitionActionCondition, True, None, False),
            ("input", "input", datarequirement.DataRequirement, True, None, False),
            ("output", "output", datarequirement.DataRequirement, True, None, False),
            ("relatedAction", "relatedAction", PlanDefinitionActionRelatedAction, True, None, False),
            ("timingDateTime", "timingDateTime", fhirdate.FHIRDate, False, "timing", False),
            ("timingAge", "timingAge", age.Age, False, "timing", False),
            ("timingPeriod", "timingPeriod", period.Period, False, "timing", False),
            ("timingDuration", "timingDuration", duration.Duration, False, "timing", False),
            ("timingRange", "timingRange", range.Range, False, "timing", False),
            ("timingTiming", "timingTiming", timing.Timing, False, "timing", False),
            ("participant", "participant", PlanDefinitionActionParticipant, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("groupingBehavior", "groupingBehavior", str, False, None, False),
            ("selectionBehavior", "selectionBehavior", str, False, None, False),
            ("requiredBehavior", "requiredBehavior", str, False, None, False),
            ("precheckBehavior", "precheckBehavior", str, False, None, False),
            ("cardinalityBehavior", "cardinalityBehavior", str, False, None, False),
            ("definitionCanonical", "definitionCanonical", str, False, "definition", False),
            ("definitionUri", "definitionUri", str, False, "definition", False),
            ("transform", "transform", str, False, None, False),
            ("dynamicValue", "dynamicValue", PlanDefinitionActionDynamicValue, True, None, False),
            ("action", "action", PlanDefinitionAction, True, None, False),
        ])
        return js


class PlanDefinitionGoal(backboneelement.BackboneElement):
    """ What the plan is trying to accomplish.
    
    Goals that describe what the activities within the plan are intended to
    achieve. For example, weight loss, restoring an activity of daily living,
    obtaining herd immunity via immunization, meeting a process improvement
    objective, etc.
    """
    
    resource_type = "PlanDefinitionGoal"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.category = None
        """ E.g. Treatment, dietary, behavioral.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Code or text describing the goal.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.priority = None
        """ high-priority | medium-priority | low-priority.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.start = None
        """ When goal pursuit begins.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.addresses = None
        """ What does the goal address.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.documentation = None
        """ Supporting documentation for the goal.
        List of `RelatedArtifact` items (represented as `dict` in JSON). """
        
        self.target = None
        """ Target outcome for the goal.
        List of `PlanDefinitionGoalTarget` items (represented as `dict` in JSON). """
        
        super(PlanDefinitionGoal, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionGoal, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", codeableconcept.CodeableConcept, False, None, True),
            ("priority", "priority", codeableconcept.CodeableConcept, False, None, False),
            ("start", "start", codeableconcept.CodeableConcept, False, None, False),
            ("addresses", "addresses", codeableconcept.CodeableConcept, True, None, False),
            ("documentation", "documentation", relatedartifact.RelatedArtifact, True, None, False),
            ("target", "target", PlanDefinitionGoalTarget, True, None, False),
        ])
        return js


class PlanDefinitionGoalTarget(backboneelement.BackboneElement):
    """ Target outcome for the goal.
    
    Indicates what should be done and within what timeframe.
    """
    
    resource_type = "PlanDefinitionGoalTarget"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.measure = None
        """ The parameter whose value is to be tracked.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.detailQuantity = None
        """ The target value to be achieved.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.detailRange = None
        """ The target value to be achieved.
        Type `Range` (represented as `dict` in JSON). """
        
        self.detailCodeableConcept = None
        """ The target value to be achieved.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.due = None
        """ Reach goal within.
        Type `Duration` (represented as `dict` in JSON). """
        
        super(PlanDefinitionGoalTarget, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionGoalTarget, self).elementProperties()
        js.extend([
            ("measure", "measure", codeableconcept.CodeableConcept, False, None, False),
            ("detailQuantity", "detailQuantity", quantity.Quantity, False, "detail", False),
            ("detailRange", "detailRange", range.Range, False, "detail", False),
            ("detailCodeableConcept", "detailCodeableConcept", codeableconcept.CodeableConcept, False, "detail", False),
            ("due", "due", duration.Duration, False, None, False),
        ])
        return js


class PlanDefinitionActionDynamicValue(backboneelement.BackboneElement):
    """ Dynamic aspects of the definition.
    
    Customizations that should be applied to the statically defined resource.
    For example, if the dosage of a medication must be computed based on the
    patient's weight, a customization would be used to specify an expression
    that calculated the weight, and the path on the resource that would contain
    the result.
    """
    
    resource_type = "PlanDefinitionActionDynamicValue"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.path = None
        """ The path to the element to be set dynamically.
        Type `str`. """
        
        self.expression = None
        """ An expression that provides the dynamic value for the customization.
        Type `Expression` (represented as `dict` in JSON). """
        
        super(PlanDefinitionActionDynamicValue, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionActionDynamicValue, self).elementProperties()
        js.extend([
            ("path", "path", str, False, None, False),
            ("expression", "expression", expression.Expression, False, None, False),
        ])
        return js


class PlanDefinitionActionParticipant(backboneelement.BackboneElement):
    """ Who should participate in the action.
    
    Indicates who should participate in performing the action described.
    """
    
    resource_type = "PlanDefinitionActionParticipant"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ patient | practitioner | related-person | device.
        Type `str`. """
        
        self.role = None
        """ E.g. Nurse, Surgeon, Parent.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(PlanDefinitionActionParticipant, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionActionParticipant, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("role", "role", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class PlanDefinitionActionRelatedAction(backboneelement.BackboneElement):
    """ Relationship to another action.
    
    A relationship to another action such as "before" or "30-60 minutes after
    start of".
    """
    
    resource_type = "PlanDefinitionActionRelatedAction"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.actionId = None
        """ What action is this related to.
        Type `str`. """
        
        self.relationship = None
        """ before-start | before | before-end | concurrent-with-start |
        concurrent | concurrent-with-end | after-start | after | after-end.
        Type `str`. """
        
        self.offsetDuration = None
        """ Time offset for the relationship.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.offsetRange = None
        """ Time offset for the relationship.
        Type `Range` (represented as `dict` in JSON). """
        
        super(PlanDefinitionActionRelatedAction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionActionRelatedAction, self).elementProperties()
        js.extend([
            ("actionId", "actionId", str, False, None, True),
            ("relationship", "relationship", str, False, None, True),
            ("offsetDuration", "offsetDuration", duration.Duration, False, "offset", False),
            ("offsetRange", "offsetRange", range.Range, False, "offset", False),
        ])
        return js


class PlanDefinitionActionCondition(backboneelement.BackboneElement):
    """ Whether or not the action is applicable.
    
    An expression that describes applicability criteria or start/stop
    conditions for the action.
    """
    
    resource_type = "PlanDefinitionActionCondition"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.kind = None
        """ applicability | start | stop.
        Type `str`. """
        
        self.expression = None
        """ Boolean-valued expression.
        Type `Expression` (represented as `dict` in JSON). """
        
        super(PlanDefinitionActionCondition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionActionCondition, self).elementProperties()
        js.extend([
            ("kind", "kind", str, False, None, True),
            ("expression", "expression", expression.Expression, False, None, False),
        ])
        return js


from . import age
from . import codeableconcept
from . import contactdetail
from . import datarequirement
from . import duration
from . import expression
from . import fhirdate
from . import fhirreference
from . import identifier
from . import period
from . import quantity
from . import range
from . import relatedartifact
from . import timing
from . import triggerdefinition
from . import usagecontext

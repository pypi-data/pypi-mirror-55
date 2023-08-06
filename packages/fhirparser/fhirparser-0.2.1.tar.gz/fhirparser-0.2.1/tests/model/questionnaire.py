#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Questionnaire) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class Questionnaire(domainresource.DomainResource):
    """ A structured set of questions.
    
    A structured set of questions intended to guide the collection of answers
    from end-users. Questionnaires provide detailed control over order,
    presentation, phraseology and grouping to allow coherent, consistent data
    collection.
    """
    
    resource_type = "Questionnaire"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.url = None
        """ Canonical identifier for this questionnaire, represented as a URI
        (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the questionnaire.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the questionnaire.
        Type `str`. """
        
        self.name = None
        """ Name for this questionnaire (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this questionnaire (human friendly).
        Type `str`. """
        
        self.derivedFrom = None
        """ Instantiates protocol or definition.
        List of `str` items. """
        
        self.status = None
        """ draft | active | retired | unknown.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
        self.subjectType = None
        """ Resource that can be subject of QuestionnaireResponse.
        List of `str` items. """
        
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
        """ Natural language description of the questionnaire.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for questionnaire (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this questionnaire is defined.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the questionnaire was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the questionnaire was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the questionnaire is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.code = None
        """ Concept that represents the overall questionnaire.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.item = None
        """ Questions and sections within the Questionnaire.
        List of `QuestionnaireItem` items (represented as `dict` in JSON). """
        
        super(Questionnaire, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Questionnaire, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("derivedFrom", "derivedFrom", str, True, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("subjectType", "subjectType", str, True, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("approvalDate", "approvalDate", fhirdate.FHIRDate, False, None, False),
            ("lastReviewDate", "lastReviewDate", fhirdate.FHIRDate, False, None, False),
            ("effectivePeriod", "effectivePeriod", period.Period, False, None, False),
            ("code", "code", coding.Coding, True, None, False),
            ("item", "item", QuestionnaireItem, True, None, False),
        ])
        return js


from . import backboneelement

class QuestionnaireItem(backboneelement.BackboneElement):
    """ Questions and sections within the Questionnaire.
    
    A particular question, question grouping or display text that is part of
    the questionnaire.
    """
    
    resource_type = "QuestionnaireItem"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.linkId = None
        """ Unique id for item in questionnaire.
        Type `str`. """
        
        self.definition = None
        """ ElementDefinition - details for the item.
        Type `str`. """
        
        self.code = None
        """ Corresponding concept for this item in a terminology.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.prefix = None
        """ E.g. "1(a)", "2.5.3".
        Type `str`. """
        
        self.text = None
        """ Primary text for the item.
        Type `str`. """
        
        self.type = None
        """ group | display | boolean | decimal | integer | date | dateTime +.
        Type `str`. """
        
        self.enableWhen = None
        """ Only allow data when.
        List of `QuestionnaireItemEnableWhen` items (represented as `dict` in JSON). """
        
        self.enableBehavior = None
        """ all | any.
        Type `str`. """
        
        self.required = None
        """ Whether the item must be included in data results.
        Type `bool`. """
        
        self.repeats = None
        """ Whether the item may repeat.
        Type `bool`. """
        
        self.readOnly = None
        """ Don't allow human editing.
        Type `bool`. """
        
        self.maxLength = None
        """ No more than this many characters.
        Type `int`. """
        
        self.answerValueSet = None
        """ Valueset containing permitted answers.
        Type `str`. """
        
        self.answerOption = None
        """ Permitted answer.
        List of `QuestionnaireItemAnswerOption` items (represented as `dict` in JSON). """
        
        self.initial = None
        """ Initial value(s) when item is first rendered.
        List of `QuestionnaireItemInitial` items (represented as `dict` in JSON). """
        
        self.item = None
        """ Nested questionnaire items.
        List of `QuestionnaireItem` items (represented as `dict` in JSON). """
        
        super(QuestionnaireItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireItem, self).elementProperties()
        js.extend([
            ("linkId", "linkId", str, False, None, True),
            ("definition", "definition", str, False, None, False),
            ("code", "code", coding.Coding, True, None, False),
            ("prefix", "prefix", str, False, None, False),
            ("text", "text", str, False, None, False),
            ("type", "type", str, False, None, True),
            ("enableWhen", "enableWhen", QuestionnaireItemEnableWhen, True, None, False),
            ("enableBehavior", "enableBehavior", str, False, None, False),
            ("required", "required", bool, False, None, False),
            ("repeats", "repeats", bool, False, None, False),
            ("readOnly", "readOnly", bool, False, None, False),
            ("maxLength", "maxLength", int, False, None, False),
            ("answerValueSet", "answerValueSet", str, False, None, False),
            ("answerOption", "answerOption", QuestionnaireItemAnswerOption, True, None, False),
            ("initial", "initial", QuestionnaireItemInitial, True, None, False),
            ("item", "item", QuestionnaireItem, True, None, False),
        ])
        return js


class QuestionnaireItemInitial(backboneelement.BackboneElement):
    """ Initial value(s) when item is first rendered.
    
    One or more values that should be pre-populated in the answer when
    initially rendering the questionnaire for user input.
    """
    
    resource_type = "QuestionnaireItemInitial"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.valueBoolean = None
        """ Actual value for initializing the question.
        Type `bool`. """
        
        self.valueDecimal = None
        """ Actual value for initializing the question.
        Type `float`. """
        
        self.valueInteger = None
        """ Actual value for initializing the question.
        Type `int`. """
        
        self.valueDate = None
        """ Actual value for initializing the question.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueDateTime = None
        """ Actual value for initializing the question.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueTime = None
        """ Actual value for initializing the question.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueString = None
        """ Actual value for initializing the question.
        Type `str`. """
        
        self.valueUri = None
        """ Actual value for initializing the question.
        Type `str`. """
        
        self.valueAttachment = None
        """ Actual value for initializing the question.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.valueCoding = None
        """ Actual value for initializing the question.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ Actual value for initializing the question.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueReference = None
        """ Actual value for initializing the question.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(QuestionnaireItemInitial, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireItemInitial, self).elementProperties()
        js.extend([
            ("valueBoolean", "valueBoolean", bool, False, "value", True),
            ("valueDecimal", "valueDecimal", float, False, "value", True),
            ("valueInteger", "valueInteger", int, False, "value", True),
            ("valueDate", "valueDate", fhirdate.FHIRDate, False, "value", True),
            ("valueDateTime", "valueDateTime", fhirdate.FHIRDate, False, "value", True),
            ("valueTime", "valueTime", fhirdate.FHIRDate, False, "value", True),
            ("valueString", "valueString", str, False, "value", True),
            ("valueUri", "valueUri", str, False, "value", True),
            ("valueAttachment", "valueAttachment", attachment.Attachment, False, "value", True),
            ("valueCoding", "valueCoding", coding.Coding, False, "value", True),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", True),
            ("valueReference", "valueReference", fhirreference.FHIRReference, False, "value", True),
        ])
        return js


class QuestionnaireItemAnswerOption(backboneelement.BackboneElement):
    """ Permitted answer.
    
    One of the permitted answers for a "choice" or "open-choice" question.
    """
    
    resource_type = "QuestionnaireItemAnswerOption"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.valueInteger = None
        """ Answer value.
        Type `int`. """
        
        self.valueDate = None
        """ Answer value.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueTime = None
        """ Answer value.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueString = None
        """ Answer value.
        Type `str`. """
        
        self.valueCoding = None
        """ Answer value.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.valueReference = None
        """ Answer value.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.initialSelected = None
        """ Whether option is selected by default.
        Type `bool`. """
        
        super(QuestionnaireItemAnswerOption, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireItemAnswerOption, self).elementProperties()
        js.extend([
            ("valueInteger", "valueInteger", int, False, "value", True),
            ("valueDate", "valueDate", fhirdate.FHIRDate, False, "value", True),
            ("valueTime", "valueTime", fhirdate.FHIRDate, False, "value", True),
            ("valueString", "valueString", str, False, "value", True),
            ("valueCoding", "valueCoding", coding.Coding, False, "value", True),
            ("valueReference", "valueReference", fhirreference.FHIRReference, False, "value", True),
            ("initialSelected", "initialSelected", bool, False, None, False),
        ])
        return js


class QuestionnaireItemEnableWhen(backboneelement.BackboneElement):
    """ Only allow data when.
    
    A constraint indicating that this item should only be enabled
    (displayed/allow answers to be captured) when the specified condition is
    true.
    """
    
    resource_type = "QuestionnaireItemEnableWhen"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.question = None
        """ Question that determines whether item is enabled.
        Type `str`. """
        
        self.operator = None
        """ exists | = | != | > | < | >= | <=.
        Type `str`. """
        
        self.answerBoolean = None
        """ Value for question comparison based on operator.
        Type `bool`. """
        
        self.answerDecimal = None
        """ Value for question comparison based on operator.
        Type `float`. """
        
        self.answerInteger = None
        """ Value for question comparison based on operator.
        Type `int`. """
        
        self.answerDate = None
        """ Value for question comparison based on operator.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.answerDateTime = None
        """ Value for question comparison based on operator.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.answerTime = None
        """ Value for question comparison based on operator.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.answerString = None
        """ Value for question comparison based on operator.
        Type `str`. """
        
        self.answerCoding = None
        """ Value for question comparison based on operator.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.answerQuantity = None
        """ Value for question comparison based on operator.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.answerReference = None
        """ Value for question comparison based on operator.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(QuestionnaireItemEnableWhen, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireItemEnableWhen, self).elementProperties()
        js.extend([
            ("question", "question", str, False, None, True),
            ("operator", "operator", str, False, None, True),
            ("answerBoolean", "answerBoolean", bool, False, "answer", True),
            ("answerDecimal", "answerDecimal", float, False, "answer", True),
            ("answerInteger", "answerInteger", int, False, "answer", True),
            ("answerDate", "answerDate", fhirdate.FHIRDate, False, "answer", True),
            ("answerDateTime", "answerDateTime", fhirdate.FHIRDate, False, "answer", True),
            ("answerTime", "answerTime", fhirdate.FHIRDate, False, "answer", True),
            ("answerString", "answerString", str, False, "answer", True),
            ("answerCoding", "answerCoding", coding.Coding, False, "answer", True),
            ("answerQuantity", "answerQuantity", quantity.Quantity, False, "answer", True),
            ("answerReference", "answerReference", fhirreference.FHIRReference, False, "answer", True),
        ])
        return js


from . import attachment
from . import codeableconcept
from . import coding
from . import contactdetail
from . import fhirdate
from . import fhirreference
from . import identifier
from . import period
from . import quantity
from . import usagecontext

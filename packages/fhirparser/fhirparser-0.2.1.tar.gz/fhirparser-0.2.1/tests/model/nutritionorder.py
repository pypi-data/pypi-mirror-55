#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/NutritionOrder) on 2019-11-06.
#  2019, SMART Health IT.


from . import domainresource

class NutritionOrder(domainresource.DomainResource):
    """ Diet, formula or nutritional supplement request.
    
    A request to supply a diet, formula feeding (enteral) or oral nutritional
    supplement to a patient/resident.
    """
    
    resource_type = "NutritionOrder"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.identifier = None
        """ Identifiers assigned to this order.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.instantiatesCanonical = None
        """ Instantiates FHIR protocol or definition.
        List of `str` items. """
        
        self.instantiatesUri = None
        """ Instantiates external protocol or definition.
        List of `str` items. """
        
        self.instantiates = None
        """ Instantiates protocol or definition.
        List of `str` items. """
        
        self.status = None
        """ draft | active | on-hold | revoked | completed | entered-in-error |
        unknown.
        Type `str`. """
        
        self.intent = None
        """ proposal | plan | directive | order | original-order | reflex-order
        | filler-order | instance-order | option.
        Type `str`. """
        
        self.patient = None
        """ The person who requires the diet, formula or nutritional supplement.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ The encounter associated with this nutrition order.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.dateTime = None
        """ Date and time the nutrition order was requested.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.orderer = None
        """ Who ordered the diet, formula or nutritional supplement.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.allergyIntolerance = None
        """ List of the patient's food and nutrition-related allergies and
        intolerances.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.foodPreferenceModifier = None
        """ Order-specific modifier about the type of food that should be given.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.excludeFoodModifier = None
        """ Order-specific modifier about the type of food that should not be
        given.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.oralDiet = None
        """ Oral diet components.
        Type `NutritionOrderOralDiet` (represented as `dict` in JSON). """
        
        self.supplement = None
        """ Supplement components.
        List of `NutritionOrderSupplement` items (represented as `dict` in JSON). """
        
        self.enteralFormula = None
        """ Enteral formula components.
        Type `NutritionOrderEnteralFormula` (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(NutritionOrder, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(NutritionOrder, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("instantiatesCanonical", "instantiatesCanonical", str, True, None, False),
            ("instantiatesUri", "instantiatesUri", str, True, None, False),
            ("instantiates", "instantiates", str, True, None, False),
            ("status", "status", str, False, None, True),
            ("intent", "intent", str, False, None, True),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("dateTime", "dateTime", fhirdate.FHIRDate, False, None, True),
            ("orderer", "orderer", fhirreference.FHIRReference, False, None, False),
            ("allergyIntolerance", "allergyIntolerance", fhirreference.FHIRReference, True, None, False),
            ("foodPreferenceModifier", "foodPreferenceModifier", codeableconcept.CodeableConcept, True, None, False),
            ("excludeFoodModifier", "excludeFoodModifier", codeableconcept.CodeableConcept, True, None, False),
            ("oralDiet", "oralDiet", NutritionOrderOralDiet, False, None, False),
            ("supplement", "supplement", NutritionOrderSupplement, True, None, False),
            ("enteralFormula", "enteralFormula", NutritionOrderEnteralFormula, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


from . import backboneelement

class NutritionOrderEnteralFormula(backboneelement.BackboneElement):
    """ Enteral formula components.
    
    Feeding provided through the gastrointestinal tract via a tube, catheter,
    or stoma that delivers nutrition distal to the oral cavity.
    """
    
    resource_type = "NutritionOrderEnteralFormula"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.baseFormulaType = None
        """ Type of enteral or infant formula.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.baseFormulaProductName = None
        """ Product or brand name of the enteral or infant formula.
        Type `str`. """
        
        self.additiveType = None
        """ Type of modular component to add to the feeding.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.additiveProductName = None
        """ Product or brand name of the modular additive.
        Type `str`. """
        
        self.caloricDensity = None
        """ Amount of energy per specified volume that is required.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.routeofAdministration = None
        """ How the formula should enter the patient's gastrointestinal tract.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.administration = None
        """ Formula feeding instruction as structured data.
        List of `NutritionOrderEnteralFormulaAdministration` items (represented as `dict` in JSON). """
        
        self.maxVolumeToDeliver = None
        """ Upper limit on formula volume per unit of time.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.administrationInstruction = None
        """ Formula feeding instructions expressed as text.
        Type `str`. """
        
        super(NutritionOrderEnteralFormula, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(NutritionOrderEnteralFormula, self).elementProperties()
        js.extend([
            ("baseFormulaType", "baseFormulaType", codeableconcept.CodeableConcept, False, None, False),
            ("baseFormulaProductName", "baseFormulaProductName", str, False, None, False),
            ("additiveType", "additiveType", codeableconcept.CodeableConcept, False, None, False),
            ("additiveProductName", "additiveProductName", str, False, None, False),
            ("caloricDensity", "caloricDensity", quantity.Quantity, False, None, False),
            ("routeofAdministration", "routeofAdministration", codeableconcept.CodeableConcept, False, None, False),
            ("administration", "administration", NutritionOrderEnteralFormulaAdministration, True, None, False),
            ("maxVolumeToDeliver", "maxVolumeToDeliver", quantity.Quantity, False, None, False),
            ("administrationInstruction", "administrationInstruction", str, False, None, False),
        ])
        return js


class NutritionOrderSupplement(backboneelement.BackboneElement):
    """ Supplement components.
    
    Oral nutritional products given in order to add further nutritional value
    to the patient's diet.
    """
    
    resource_type = "NutritionOrderSupplement"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ Type of supplement product requested.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.productName = None
        """ Product or brand name of the nutritional supplement.
        Type `str`. """
        
        self.schedule = None
        """ Scheduled frequency of supplement.
        List of `Timing` items (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Amount of the nutritional supplement.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.instruction = None
        """ Instructions or additional information about the oral supplement.
        Type `str`. """
        
        super(NutritionOrderSupplement, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(NutritionOrderSupplement, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("productName", "productName", str, False, None, False),
            ("schedule", "schedule", timing.Timing, True, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("instruction", "instruction", str, False, None, False),
        ])
        return js


class NutritionOrderOralDiet(backboneelement.BackboneElement):
    """ Oral diet components.
    
    Diet given orally in contrast to enteral (tube) feeding.
    """
    
    resource_type = "NutritionOrderOralDiet"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ Type of oral diet or diet restrictions that describe what can be
        consumed orally.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.schedule = None
        """ Scheduled frequency of diet.
        List of `Timing` items (represented as `dict` in JSON). """
        
        self.nutrient = None
        """ Required  nutrient modifications.
        List of `NutritionOrderOralDietNutrient` items (represented as `dict` in JSON). """
        
        self.texture = None
        """ Required  texture modifications.
        List of `NutritionOrderOralDietTexture` items (represented as `dict` in JSON). """
        
        self.fluidConsistencyType = None
        """ The required consistency of fluids and liquids provided to the
        patient.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.instruction = None
        """ Instructions or additional information about the oral diet.
        Type `str`. """
        
        super(NutritionOrderOralDiet, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(NutritionOrderOralDiet, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("schedule", "schedule", timing.Timing, True, None, False),
            ("nutrient", "nutrient", NutritionOrderOralDietNutrient, True, None, False),
            ("texture", "texture", NutritionOrderOralDietTexture, True, None, False),
            ("fluidConsistencyType", "fluidConsistencyType", codeableconcept.CodeableConcept, True, None, False),
            ("instruction", "instruction", str, False, None, False),
        ])
        return js


class NutritionOrderOralDietTexture(backboneelement.BackboneElement):
    """ Required  texture modifications.
    
    Class that describes any texture modifications required for the patient to
    safely consume various types of solid foods.
    """
    
    resource_type = "NutritionOrderOralDietTexture"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.modifier = None
        """ Code to indicate how to alter the texture of the foods, e.g. pureed.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.foodType = None
        """ Concepts that are used to identify an entity that is ingested for
        nutritional purposes.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(NutritionOrderOralDietTexture, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(NutritionOrderOralDietTexture, self).elementProperties()
        js.extend([
            ("modifier", "modifier", codeableconcept.CodeableConcept, False, None, False),
            ("foodType", "foodType", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class NutritionOrderOralDietNutrient(backboneelement.BackboneElement):
    """ Required  nutrient modifications.
    
    Class that defines the quantity and type of nutrient modifications (for
    example carbohydrate, fiber or sodium) required for the oral diet.
    """
    
    resource_type = "NutritionOrderOralDietNutrient"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.modifier = None
        """ Type of nutrient that is being modified.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Quantity of the specified nutrient.
        Type `Quantity` (represented as `dict` in JSON). """
        
        super(NutritionOrderOralDietNutrient, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(NutritionOrderOralDietNutrient, self).elementProperties()
        js.extend([
            ("modifier", "modifier", codeableconcept.CodeableConcept, False, None, False),
            ("amount", "amount", quantity.Quantity, False, None, False),
        ])
        return js


class NutritionOrderEnteralFormulaAdministration(backboneelement.BackboneElement):
    """ Formula feeding instruction as structured data.
    
    Formula administration instructions as structured data.  This repeating
    structure allows for changing the administration rate or volume over time
    for both bolus and continuous feeding.  An example of this would be an
    instruction to increase the rate of continuous feeding every 2 hours.
    """
    
    resource_type = "NutritionOrderEnteralFormulaAdministration"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.schedule = None
        """ Scheduled frequency of enteral feeding.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ The volume of formula to provide.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.rateQuantity = None
        """ Speed with which the formula is provided per period of time.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.rateRatio = None
        """ Speed with which the formula is provided per period of time.
        Type `Ratio` (represented as `dict` in JSON). """
        
        super(NutritionOrderEnteralFormulaAdministration, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(NutritionOrderEnteralFormulaAdministration, self).elementProperties()
        js.extend([
            ("schedule", "schedule", timing.Timing, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("rateQuantity", "rateQuantity", quantity.Quantity, False, "rate", False),
            ("rateRatio", "rateRatio", ratio.Ratio, False, "rate", False),
        ])
        return js


from . import annotation
from . import codeableconcept
from . import fhirdate
from . import fhirreference
from . import identifier
from . import quantity
from . import ratio
from . import timing

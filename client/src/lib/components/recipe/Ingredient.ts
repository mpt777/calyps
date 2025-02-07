import { fractionalize, pluralize } from "$scripts/humanize";
import { precisionRoundMod } from "$utils/math";
import { sys, type Type } from "typescript";

export enum System {
	US = "US",
	Metric = "METRIC",
  Default = "DEFAULT"
}

export const Measurement = {
	Volume: Symbol("volume"),
	Weight: Symbol("weight"),
}

interface Unit {
    title: string;
    abbreviation:string;
    system: System;
    measurement: symbol;
    tags?: symbol[];
    precision: number;

    // constructor(value:number) {
    //     this.value = value;
    // }

}

export const Cup: Unit = {
    title:"cup",
    abbreviation:"cup",
    system:System.US,
    measurement:Measurement.Volume,
    precision:0,
}

export const Teaspoon: Unit = {
    title:"teaspoon",
    abbreviation:"tsp",
    system:System.US,
    measurement:Measurement.Volume,
    precision:0,
}

export const Tablespoon: Unit = {
    title:"tablespoon",
    abbreviation:"tbsp",
    system:System.US,
    measurement:Measurement.Volume,
    precision:0,
}

export const Pint: Unit = {
    title:"pint",
    abbreviation:"pt",
    system:System.US,
    measurement:Measurement.Volume,
    precision:0,
}

export const Quart: Unit = {
    title:"quart",
    abbreviation:"qt",
    system:System.US,
    measurement:Measurement.Volume,
    precision:0,
}

export const Gallon: Unit= {
    title:"gallon",
    abbreviation:"gal",
    system:System.US,
    measurement:Measurement.Volume,
    precision:0,
}

export const Ounce: Unit= {
    title:"ounce",
    abbreviation:"oz",
    system:System.US,
    measurement:Measurement.Weight,
    precision:0,
}

export const FluidOunce: Unit = {
    title:"fluid ounce",
    abbreviation:"fl oz",
    system:System.US,
    measurement:Measurement.Volume,
    precision:0,
}

export const Pound: Unit = {
    title:"pound",
    abbreviation:"lb",
    system:System.US,
    measurement:Measurement.Weight,
    precision:0,
}

//-----------------------------------------

export const Milliliter: Unit = {
    title:"milliliter",
    abbreviation:"ml",
    system:System.Metric,
    measurement:Measurement.Volume,
    precision:0,
}

export const Liter: Unit = {
    title:"liter",
    abbreviation:"l",
    system:System.Metric,
    measurement:Measurement.Volume,
    precision:2,
}

export const Gram: Unit = {
    title:"gram",
    abbreviation:"g",
    system:System.Metric,
    measurement:Measurement.Weight,
    precision:0,
}

export const Kilogram: Unit = {
    title:"kilogram",
    abbreviation:"k",
    system:System.Metric,
    measurement:Measurement.Weight,
    precision:2,
}

//--------------------------------------------------


class Conversion {
    fromUnit!: Unit;
    ratio!: number;
    toUnit!: Unit;

    constructor(fromUnit: Unit, ratio: number, toUnit:Unit) {
        this.fromUnit = fromUnit;
        this.ratio = ratio;
        this.toUnit = toUnit;
    }
}

class Converter {
    private conversions: Conversion[] = [];

    constructor() {
        this.conversions = [
            new Conversion(Cup, 236.588, Milliliter),
            new Conversion(Teaspoon, 4.92892, Milliliter),
            new Conversion(Tablespoon, 14.7868, Milliliter),
            new Conversion(FluidOunce, 29.5735, Milliliter),
            new Conversion(Gallon, 3.78541, Liter),
            new Conversion(Quart, 946.353, Milliliter),
            new Conversion(Pint, 473.176, Milliliter),

            new Conversion(Ounce, 28.3495, Gram),
            new Conversion(Pound, 453.592, Gram),

            new Conversion(Liter, 1000, Milliliter),
        ]
    }

    units(){
        let units = new Set<Unit>();
        this.conversions.forEach(e => units.add(e.fromUnit));
        this.conversions.forEach(e => units.add(e.toUnit));
        return Array.from(units);
    }

    findConversionPath(
        fromUnit: Unit,
        toUnit: Unit,
        visited: Set<Unit> = new Set()
    ): Conversion[] | undefined {
        if (fromUnit === toUnit) {
            return []; // Base case: already in target unit
        }
    
        visited.add(fromUnit);
    
        const possibleConversions = this.conversions.filter(conv =>
            (conv.fromUnit === fromUnit && !visited.has(conv.toUnit)) ||
            (conv.toUnit === fromUnit && !visited.has(conv.fromUnit))
        );

        possibleConversions.sort((a, b) =>
            a.ratio < b.ratio ? -1 : a.ratio > b.ratio ? 1 : 0
        ); 
    
        for (const conv of possibleConversions) {
            const nextUnit = conv.fromUnit === fromUnit ? conv.toUnit : conv.fromUnit;
            const subPath = this.findConversionPath(nextUnit, toUnit, visited);
            if (subPath !== undefined) {
                return [conv, ...subPath];
            }
        }
    
        visited.delete(fromUnit);
        return undefined; // No path foun
    }
    
    convertAmount(
        startingUnit: Unit,
        targetUnit: Unit,
        amount: number
    ): number | undefined {
        if (startingUnit === targetUnit) {
            return amount; // No conversion needed
        }
    
        const conversionPath = this.findConversionPath(startingUnit, targetUnit);
    
        if (!conversionPath) {
            return undefined; // Conversion path not found
        }
    
        let convertedAmount = amount;
    
        for (const conv of conversionPath) {
            if (conv.fromUnit === startingUnit) {
                convertedAmount *= conv.ratio;
            } else {
                convertedAmount *= 1 / conv.ratio;
            }
        }
    
        return precisionRoundMod(convertedAmount, 4);
    }

    // findUnitWithSystem(
    //     fromUnit: Unit,
    //     toSystem: System,
    //     visited: Set<Unit> = new Set()
    // ): Unit | undefined {
    //     if (visited.has(fromUnit)) {
    //         return undefined; // Avoid infinite loops
    //     }
    
    //     visited.add(fromUnit);
    
    //     const matchingConversion = this.conversions.find(conv =>
    //         (conv.fromUnit === fromUnit && conv.toUnit.system === toSystem) ||
    //         (conv.toUnit === fromUnit && conv.fromUnit.system === toSystem)
    //     );
    
    //     if (matchingConversion) {
    //         return matchingConversion.toUnit.system == toSystem ? matchingConversion.toUnit: matchingConversion.fromUnit; // Found a matching unit
    //     }

    //     const possibleConversions = this.conversions.filter(conv =>
    //         (conv.fromUnit === fromUnit && !visited.has(conv.toUnit)) ||
    //         (conv.toUnit === fromUnit && !visited.has(conv.fromUnit))
    //     );
    
    //     for (const conv of possibleConversions) {
    //         const nextUnit = conv.fromUnit === fromUnit ? conv.toUnit : conv.fromUnit;
    //         const unitWithSystem = this.findUnitWithSystem(nextUnit, nextUnit.system, visited);
    //         if (unitWithSystem !== undefined) {
    //             return unitWithSystem; // Found a matching unit in the sub-path
    //         }
    //     }
    
    //     visited.delete(fromUnit);
    //     return undefined; // No matching unit found in the path
    // }

    // convertUnit(fromUnit : Unit, toSystem : System) {
    //     if (fromUnit.system === toSystem){
    //         return fromUnit
    //     }
    //     return this.findUnitWithSystem(fromUnit, toSystem);
    // }
}
export let UnitConverter = new Converter()

export class Ingredient {
    // ingredient : IngrdientInterface;
    unit: Unit;
    amount: number;
    name: string;
    scalar: number;

    constructor(amount : number, unit : Unit, name : string, scalar : number = 1) {
        this.unit = unit;
        this.amount = amount;
        this.name = name;
        this.scalar = scalar;
    }

    getScaledAmount() {
        return this.scalar * this.amount;
    }
    
    fractionalAmount() {
        return fractionalize(this.getScaledAmount())
    }

    getAmount() {
        if (this.unit.system === System.US){
            return this.fractionalAmount()
        }
        return precisionRoundMod(this.getScaledAmount(), this.unit.precision)
    }

    pluralizeUnit() {
        return pluralize(this.unit.title, this.getScaledAmount())
    }

    static asSystem(ingredient : Ingredient, system : System, scalar : number) {
        let unit = getUnitFromString(ingredient.unit_code);
       
        if (unit.system == system || system == System.Default){
            return new Ingredient(ingredient.amount, unit, ingredient.name, scalar)
        }

        let systemAsString = Object.values(System)[Object.keys(System).indexOf(system)];
        let validUnits = UnitConverter.units().filter(e => e.system === systemAsString)

        let ingredients = validUnits.map(function(validUnit) {
            let transformedAmount = UnitConverter.convertAmount(unit, validUnit, ingredient.amount) || 0;
            return new Ingredient(transformedAmount, validUnit, ingredient.name, scalar)
        }).filter(e => e.amount !== 0)

        return ingredients.filter(e => e.getScaledAmount() > 1).reduce((prev, curr) => prev.getScaledAmount() < curr.getScaledAmount() ? prev : curr) ||
                ingredients.reduce((prev, curr) => prev.getScaledAmount() < curr.getScaledAmount() ? prev : curr);
    }
}

let units = [Cup, Teaspoon, Tablespoon, Pint, Quart, Gallon, Ounce, FluidOunce, Pound, Milliliter, Liter, Gram]
export function getUnitFromString(name : string) {
    return units.filter(e => e.abbreviation === name)[0]
}

export function getSystemFromString(name: string){
    return name as System;
}
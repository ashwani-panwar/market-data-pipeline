#!/usr/bin/env python3
"""
Unit Conversion Script - Converts between Metric and Imperial units
Supports: Length, Weight, Temperature, and Volume conversions
"""

import sys
import argparse


class UnitConverter:
    """Handles conversions between metric and imperial units"""
    
    # Length conversion factors (to meters)
    LENGTH_UNITS = {
        'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0,
        'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.34
    }
    
    # Weight conversion factors (to kilograms)
    WEIGHT_UNITS = {
        'g': 0.001, 'kg': 1.0, 't': 1000.0,
        'oz': 0.0283495, 'lb': 0.453592, 'st': 6.35029, 'ton': 907.185
    }
    
    # Volume conversion factors (to liters)
    VOLUME_UNITS = {
        'ml': 0.001, 'l': 1.0, 'kl': 1000.0,
        'fl_oz': 0.0295735, 'cup': 0.236588, 'pt': 0.473176,
        'qt': 0.946353, 'gal': 3.78541
    }
    
    @staticmethod
    def convert_length(value, from_unit, to_unit):
        """Convert length between different units"""
        if from_unit not in UnitConverter.LENGTH_UNITS:
            raise ValueError(f"Unknown length unit: {from_unit}")
        if to_unit not in UnitConverter.LENGTH_UNITS:
            raise ValueError(f"Unknown length unit: {to_unit}")
        
        # Convert to meters first, then to target unit
        meters = value * UnitConverter.LENGTH_UNITS[from_unit]
        result = meters / UnitConverter.LENGTH_UNITS[to_unit]
        return result
    
    @staticmethod
    def convert_weight(value, from_unit, to_unit):
        """Convert weight between different units"""
        if from_unit not in UnitConverter.WEIGHT_UNITS:
            raise ValueError(f"Unknown weight unit: {from_unit}")
        if to_unit not in UnitConverter.WEIGHT_UNITS:
            raise ValueError(f"Unknown weight unit: {to_unit}")
        
        # Convert to kilograms first, then to target unit
        kg = value * UnitConverter.WEIGHT_UNITS[from_unit]
        result = kg / UnitConverter.WEIGHT_UNITS[to_unit]
        return result
    
    @staticmethod
    def convert_volume(value, from_unit, to_unit):
        """Convert volume between different units"""
        if from_unit not in UnitConverter.VOLUME_UNITS:
            raise ValueError(f"Unknown volume unit: {from_unit}")
        if to_unit not in UnitConverter.VOLUME_UNITS:
            raise ValueError(f"Unknown volume unit: {to_unit}")
        
        # Convert to liters first, then to target unit
        liters = value * UnitConverter.VOLUME_UNITS[from_unit]
        result = liters / UnitConverter.VOLUME_UNITS[to_unit]
        return result
    
    @staticmethod
    def convert_temperature(value, from_unit, to_unit):
        """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        # Convert to Celsius first
        if from_unit in ['c', 'celsius']:
            celsius = value
        elif from_unit in ['f', 'fahrenheit']:
            celsius = (value - 32) * 5 / 9
        elif from_unit in ['k', 'kelvin']:
            celsius = value - 273.15
        else:
            raise ValueError(f"Unknown temperature unit: {from_unit}")
        
        # Convert from Celsius to target unit
        if to_unit in ['c', 'celsius']:
            return celsius
        elif to_unit in ['f', 'fahrenheit']:
            return (celsius * 9 / 5) + 32
        elif to_unit in ['k', 'kelvin']:
            return celsius + 273.15
        else:
            raise ValueError(f"Unknown temperature unit: {to_unit}")
    
    @staticmethod
    def get_category(unit):
        """Determine the category of a unit"""
        unit_lower = unit.lower()
        if unit_lower in UnitConverter.LENGTH_UNITS:
            return 'length'
        elif unit_lower in UnitConverter.WEIGHT_UNITS:
            return 'weight'
        elif unit_lower in UnitConverter.VOLUME_UNITS:
            return 'volume'
        elif unit_lower in ['c', 'celsius', 'f', 'fahrenheit', 'k', 'kelvin']:
            return 'temperature'
        else:
            return None


def print_available_units():
    """Print available units for each category"""
    print("\nAvailable Units:")
    print("\nLength:")
    print("  Metric: mm, cm, m, km")
    print("  Imperial: in, ft, yd, mi")
    print("\nWeight:")
    print("  Metric: g, kg, t")
    print("  Imperial: oz, lb, st, ton")
    print("\nVolume:")
    print("  Metric: ml, l, kl")
    print("  Imperial: fl_oz, cup, pt, qt, gal")
    print("\nTemperature:")
    print("  c (Celsius), f (Fahrenheit), k (Kelvin)")


def main():
    parser = argparse.ArgumentParser(
        description='Convert between metric and imperial units',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python convert_units.py 100 km mi          # Convert 100 km to miles
  python convert_units.py 70 kg lb           # Convert 70 kg to pounds
  python convert_units.py 32 f c             # Convert 32°F to Celsius
  python convert_units.py 5 gal l            # Convert 5 gallons to liters
  python convert_units.py --list             # List all available units
        """
    )
    
    parser.add_argument('value', type=float, nargs='?',
                       help='The value to convert')
    parser.add_argument('from_unit', type=str, nargs='?',
                       help='The unit to convert from')
    parser.add_argument('to_unit', type=str, nargs='?',
                       help='The unit to convert to')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all available units')
    
    args = parser.parse_args()
    
    if args.list:
        print_available_units()
        return
    
    if args.value is None or args.from_unit is None or args.to_unit is None:
        parser.print_help()
        return
    
    converter = UnitConverter()
    
    try:
        category = converter.get_category(args.from_unit)
        if category is None:
            print(f"Error: Unknown unit '{args.from_unit}'")
            print_available_units()
            return
        
        if category != converter.get_category(args.to_unit):
            print(f"Error: Units must be of the same category")
            print(f"'{args.from_unit}' is {category}, but '{args.to_unit}' is {converter.get_category(args.to_unit)}")
            return
        
        if category == 'length':
            result = converter.convert_length(args.value, args.from_unit.lower(), args.to_unit.lower())
        elif category == 'weight':
            result = converter.convert_weight(args.value, args.from_unit.lower(), args.to_unit.lower())
        elif category == 'volume':
            result = converter.convert_volume(args.value, args.from_unit.lower(), args.to_unit.lower())
        elif category == 'temperature':
            result = converter.convert_temperature(args.value, args.from_unit, args.to_unit)
        else:
            print(f"Error: Unsupported category: {category}")
            return
        
        print(f"{args.value} {args.from_unit} = {result:.6f} {args.to_unit}")
        
    except ValueError as e:
        print(f"Error: {e}")
        print_available_units()
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()


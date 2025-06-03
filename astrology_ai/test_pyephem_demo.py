#!/usr/bin/env python3
"""
PyEphem Demo - Alternative Astrological Calculations
Demonstrates how to use pyephem for chart calculations in the Astrology AI project
"""

import ephem
from datetime import datetime, timezone
import math

def demo_planetary_positions():
    """Demo: Calculate planetary positions using PyEphem"""
    
    print("🌟 PyEphem Demo - Planetary Position Calculations")
    print("=" * 60)
    
    try:
        # Create an observer for birth location (London, UK)
        observer = ephem.Observer()
        observer.lat = '51:30:0'  # 51°30'N
        observer.long = '0:10:0'  # 0°10'W
        observer.date = '1990/1/1 12:00:00'  # January 1, 1990, 12:00 PM
        
        print(f"📅 Date: {observer.date}")
        print(f"🌍 Location: {observer.lat}, {observer.long}")
        
        print("\n🌌 Planetary Positions:")
        print("-" * 40)
        
        # Define planets
        planets = {
            'Sun': ephem.Sun(),
            'Moon': ephem.Moon(),
            'Mercury': ephem.Mercury(),
            'Venus': ephem.Venus(),
            'Mars': ephem.Mars(),
            'Jupiter': ephem.Jupiter(),
            'Saturn': ephem.Saturn()
        }
        
        positions = {}
        
        for name, planet in planets.items():
            planet.compute(observer)
            
            # Convert to degrees
            ra_deg = math.degrees(planet.ra)
            dec_deg = math.degrees(planet.dec)
            ecliptic_lon = math.degrees(planet.hlon)
            ecliptic_lat = math.degrees(planet.hlat)
            
            positions[name] = {
                'longitude': ecliptic_lon,
                'latitude': ecliptic_lat,
                'sign': get_zodiac_sign(ecliptic_lon),
                'degree_in_sign': ecliptic_lon % 30
            }
            
            print(f"  {name:>8}: {positions[name]['sign']} {positions[name]['degree_in_sign']:.2f}°")
        
        return positions
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_zodiac_sign(longitude):
    """Convert ecliptic longitude to zodiac sign"""
    signs = [
        'Aries', 'Taurus', 'Gemini', 'Cancer',
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    sign_index = int(longitude // 30)
    return signs[sign_index % 12]

def demo_house_calculations():
    """Demo: Basic house calculation concepts"""
    
    print("\n🏠 House System Demo (Placidus)")
    print("=" * 60)
    
    try:
        # Create observer
        observer = ephem.Observer()
        observer.lat = '51:30:0'
        observer.long = '0:10:0' 
        observer.date = '1990/1/1 12:00:00'
        
        # Calculate sidereal time
        sidereal_time = observer.sidereal_time()
        
        print(f"🕐 Local Sidereal Time: {sidereal_time}")
        
        # Basic house cusp calculation (simplified)
        # This is a simplified version - full house systems require more complex calculations
        ascendant_deg = math.degrees(sidereal_time) % 360
        
        print(f"🔼 Ascendant (approx): {get_zodiac_sign(ascendant_deg)} {ascendant_deg % 30:.2f}°")
        
        # Calculate other house cusps (simplified equal house system)
        print("\n🏠 House Cusps (Equal House System):")
        print("-" * 40)
        
        for house in range(1, 13):
            cusp_deg = (ascendant_deg + (house - 1) * 30) % 360
            sign = get_zodiac_sign(cusp_deg)
            degree_in_sign = cusp_deg % 30
            
            print(f"  House {house:>2}: {sign} {degree_in_sign:.2f}°")
        
    except Exception as e:
        print(f"❌ Error calculating houses: {e}")

def demo_aspects():
    """Demo: Calculate aspects between planets"""
    
    print("\n🔗 Planetary Aspects Demo")
    print("=" * 60)
    
    # Use positions from previous calculation
    observer = ephem.Observer()
    observer.lat = '51:30:0'
    observer.long = '0:10:0'
    observer.date = '1990/1/1 12:00:00'
    
    sun = ephem.Sun()
    moon = ephem.Moon()
    sun.compute(observer)
    moon.compute(observer)
    
    sun_lon = math.degrees(sun.hlon)
    moon_lon = math.degrees(moon.hlon)
    
    # Calculate aspect
    aspect_angle = abs(sun_lon - moon_lon)
    if aspect_angle > 180:
        aspect_angle = 360 - aspect_angle
    
    print(f"Sun longitude: {sun_lon:.2f}°")
    print(f"Moon longitude: {moon_lon:.2f}°")
    print(f"Aspect angle: {aspect_angle:.2f}°")
    
    # Determine aspect type
    aspect_type = get_aspect_type(aspect_angle)
    print(f"Aspect type: {aspect_type}")

def get_aspect_type(angle):
    """Determine aspect type from angle"""
    if abs(angle - 0) < 8:
        return "Conjunction"
    elif abs(angle - 60) < 6:
        return "Sextile"
    elif abs(angle - 90) < 6:
        return "Square"
    elif abs(angle - 120) < 6:
        return "Trine"
    elif abs(angle - 180) < 8:
        return "Opposition"
    else:
        return "No major aspect"

def demo_integration_with_rules():
    """Demo: Show how pyephem could integrate with our rule system"""
    
    print("\n🔮 Integration with Astrology AI Rules (401 rules)")
    print("=" * 60)
    
    print("💡 Integration Possibilities:")
    print("  1. Calculate birth chart positions")
    print("  2. Match planetary positions with extracted rules")
    print("  3. Generate interpretations from our 401 rules")
    print("  4. Calculate transits and progressions")
    print("  5. Determine planetary strengths and weaknesses")
    print("  6. Apply classical rules to modern calculations")
    print("")
    
    print("🎯 Example Rule Matching:")
    print("  Rule: 'Mars in the 7th house causes conflicts in marriage'")
    print("  → Calculate Mars position")
    print("  → Determine which house it falls in") 
    print("  → Apply corresponding rule from our database")
    print("  → Generate interpretation")
    print("")
    
    print("📊 Current Capabilities:")
    print(f"  ✅ Planetary calculations: PyEphem")
    print(f"  ✅ Rule database: 401 extracted rules")
    print(f"  ✅ Knowledge export: JSON format")
    print(f"  ✅ Source attribution: Classical texts")

if __name__ == "__main__":
    print("🌟 Astrology AI - Enhanced with Planetary Calculations")
    print("=" * 70)
    
    # Run all demos
    positions = demo_planetary_positions()
    
    if positions:
        demo_house_calculations()
        demo_aspects()
        demo_integration_with_rules()
        
        print("\n🎉 PyEphem Integration Complete!")
        print("✅ Astrological calculations are now available!")
        print("🔗 Ready to integrate with your 401-rule knowledge base!")
    else:
        print("\n❌ Demo failed - please check installation") 
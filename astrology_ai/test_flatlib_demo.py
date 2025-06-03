#!/usr/bin/env python3
"""
Flatlib Demo - Basic Astrological Calculations
Demonstrates how to use flatlib for chart calculations in the Astrology AI project
"""

from datetime import datetime
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

def demo_basic_chart():
    """Demo: Create a basic birth chart using flatlib"""
    
    print("🌟 Flatlib Demo - Basic Birth Chart Calculation")
    print("=" * 60)
    
    try:
        # Create a birth datetime (example: January 1, 1990, 12:00 PM)
        birth_datetime = Datetime('1990/01/01', '12:00', '+00:00')
        print(f"📅 Birth Date/Time: {birth_datetime}")
        
        # Create geographic position (example: London, UK)
        geo_pos = GeoPos('51N30', '0W10')  # London coordinates
        print(f"🌍 Birth Location: {geo_pos}")
        
        # Create the chart
        chart = Chart(birth_datetime, geo_pos)
        print(f"✅ Chart created successfully!")
        
        print("\n🌌 Planetary Positions:")
        print("-" * 40)
        
        # Get planetary positions
        planets = [
            const.SUN, const.MOON, const.MARS, const.MERCURY,
            const.JUPITER, const.VENUS, const.SATURN
        ]
        
        planet_names = {
            const.SUN: "Sun",
            const.MOON: "Moon", 
            const.MARS: "Mars",
            const.MERCURY: "Mercury",
            const.JUPITER: "Jupiter",
            const.VENUS: "Venus",
            const.SATURN: "Saturn"
        }
        
        for planet_id in planets:
            planet = chart.get(planet_id)
            planet_name = planet_names[planet_id]
            sign_name = planet.sign
            degree = planet.signlon
            
            print(f"  {planet_name:>8}: {sign_name} {degree:.2f}°")
        
        print("\n🏠 House Cusps:")
        print("-" * 40)
        
        # Get house cusps
        for house_num in range(1, 13):
            house_id = f"House{house_num}"
            house = chart.get(house_id)
            print(f"  House {house_num:>2}: {house.sign} {house.signlon:.2f}°")
        
        return chart
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def demo_planetary_aspects():
    """Demo: Calculate aspects between planets"""
    
    print("\n🔗 Flatlib Demo - Planetary Aspects")
    print("=" * 60)
    
    try:
        # Create a sample chart
        birth_datetime = Datetime('1990/01/01', '12:00', '+00:00')
        geo_pos = GeoPos('51N30', '0W10')
        chart = Chart(birth_datetime, geo_pos)
        
        # Get two planets
        sun = chart.get(const.SUN)
        moon = chart.get(const.MOON)
        
        # Calculate the aspect between them
        aspect_angle = abs(sun.lon - moon.lon)
        if aspect_angle > 180:
            aspect_angle = 360 - aspect_angle
        
        print(f"Sun position: {sun.sign} {sun.signlon:.2f}°")
        print(f"Moon position: {moon.sign} {moon.signlon:.2f}°")
        print(f"Aspect angle: {aspect_angle:.2f}°")
        
        # Determine aspect type
        if abs(aspect_angle - 0) < 8:
            aspect_type = "Conjunction"
        elif abs(aspect_angle - 60) < 6:
            aspect_type = "Sextile"
        elif abs(aspect_angle - 90) < 6:
            aspect_type = "Square"
        elif abs(aspect_angle - 120) < 6:
            aspect_type = "Trine"
        elif abs(aspect_angle - 180) < 8:
            aspect_type = "Opposition"
        else:
            aspect_type = "No major aspect"
        
        print(f"Aspect type: {aspect_type}")
        
    except Exception as e:
        print(f"❌ Error calculating aspects: {e}")

def demo_integration_potential():
    """Demo: Show how flatlib could integrate with our rule system"""
    
    print("\n🔮 Integration with Astrology AI Rules")
    print("=" * 60)
    
    print("💡 Potential Integration Features:")
    print("  1. Generate birth charts from user input")
    print("  2. Apply extracted rules to chart positions")
    print("  3. Calculate planetary strengths and dignities")
    print("  4. Determine house lords and rulers")
    print("  5. Find active planetary periods (dashas)")
    print("  6. Generate interpretations using our 401 rules")
    print("")
    print("🎯 Next Steps:")
    print("  - Create chart calculation module")
    print("  - Build rule matching engine") 
    print("  - Develop interpretation generator")
    print("  - Add transit calculations")

if __name__ == "__main__":
    # Run the demos
    chart = demo_basic_chart()
    
    if chart:
        demo_planetary_aspects()
        demo_integration_potential()
        
        print("\n🎉 Flatlib installation and demo complete!")
        print("✅ Ready for astrological calculations!")
    else:
        print("\n❌ Demo failed - please check installation") 
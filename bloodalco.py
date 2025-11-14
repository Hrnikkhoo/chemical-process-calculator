import json

def calculate_blood_alcohol(data):
    # Assuming data is a dictionary parsed from JSON
    # It should contain 'w', 'timerAfter', 'speed', 'fill', 'gender'
    # and a list of drinks in 'cartAdded'

    w = data.get('w', 0)
    timerAfter = data.get('timerAfter', 0)
    speed = data.get('speed', 0)
    fill = data.get('fill', 1) # Assuming default fill is 1 (empty stomach)
    gender = data.get('gender', 0.7) # Assuming default gender is 0.7 (male)
    cart_added = data.get('cartAdded', [])

    cs = 0
    for item in cart_added:
        s = item.get('s', 0)
        v = item.get('v', 0)
        cs += s * v / 100

    # Calculate blood alcohol concentration (BAC)
    # The formula seems to be a simplified version of the Widmark formula
    # y = cs * 0.06 * 10 * 1.055 / (w * gender) * fill - (speed + timerAfter) * 0.15
    # Let's break down the JavaScript formula:
    # cs: total grams of pure alcohol consumed (s * v / 100 for each drink)
    # 0.06 * 10 * 1.055: conversion factors (density of alcohol, conversion to grams, etc.)
    # w: body weight
    # gender: gender constant (0.7 for men, 0.6 for women)
    # fill: stomach fullness factor
    # (speed + timerAfter) * 0.15: elimination rate over time

    # Ensure w and gender are not zero to avoid division by zero
    if w == 0 or gender == 0:
        return {"error": "Weight and gender factor cannot be zero."}

    y = (cs * 0.06 * 10 * 1.055) / (w * gender) * fill - (speed + timerAfter) * 0.15

    # BAC cannot be negative
    if y < 0:
        y = 0

    # Calculate alcohol elimination time
    # h = y / 0.13 (assuming 0.13 is the average elimination rate per hour)
    h = y / 0.13 if y > 0 else 0

    # Format elimination time into hours and minutes
    hours = int(h)
    minutes = round((h - hours) * 60)

    result = {
        "maxBloodAlcoPercentage": round(y, 2), # Assuming this is BAC in permille (‰)
        "airAlcoPercentage": round(y * 0.475, 2), # Conversion to mg/L in exhaled air
        "alcoOutTime": {"hours": hours, "minutes": minutes}
    }

    # Determine recommendation based on BAC
    rec = ""
    if y < 0.3:
        rec = "calc.alcoOffImpact"
    elif y < 0.5:
        rec = "calc.alcoMinImpact"
    elif y < 1.5:
        rec = "calc.alcoLightImpact"
    elif y < 2.5:
        rec = "calc.alcoMiddleImpact"
    elif y < 3:
        rec = "calc.alcoStrongImpact"
    else:
        rec = "calc.alcoHardImpact"

    result["recommendation"] = rec

    return result

# Example usage (assuming you receive data as a JSON string or dictionary)
# data = {
#     "w": 70, # weight in kg
#     "timerAfter": 1, # time passed after drinking in hours
#     "speed": 2, # speed of consumption in hours
#     "fill": 0.937, # stomach fullness factor
#     "gender": 0.7, # gender factor
#     "cartAdded": [
#         {"s": 40, "v": 250}, # 250 ml of 40% alcohol
#         {"s": 12, "v": 500}  # 500 ml of 12% alcohol
#     ]
# }
#
# calculation_result = calculate_blood_alcohol(data)
# print(json.dumps(calculation_result, indent=4))

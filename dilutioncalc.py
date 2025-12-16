def calculate_dilution(initial_volume, initial_concentration, final_concentration):
    """
    Calculates the amount of water needed to dilute a solution.

    Args:
        initial_volume (float): The initial volume of the solution.
        initial_concentration (float): The initial concentration of the solution in percent.
        final_concentration (float): The desired final concentration in percent.

    Returns:
        float: The volume of water to add, or an error message string.
    """
    if not all(isinstance(i, (int, float)) for i in [initial_volume, initial_concentration, final_concentration]):
        return "Error: All inputs must be numbers."

    if initial_volume <= 0 or initial_concentration <= 0 or final_concentration <= 0:
        return "Error: All input values must be positive."

    if final_concentration >= initial_concentration:
        return "Error: Final concentration must be less than initial concentration."

    # Formula: C1V1 = C2V2  => V2 = (C1V1)/C2
    final_volume = (initial_volume * initial_concentration) / final_concentration
    water_to_add = final_volume - initial_volume

    return water_to_add

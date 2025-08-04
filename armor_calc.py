
def apply_flat_armor_reduction(base, bonus, flat_red):
    return max(base + bonus - flat_red, 0)

def apply_flat_armor_penetration(armor, flat_pen):
    return max(armor - flat_pen, 0)

def apply_percent_armor_reduction(armor, percent_red):
    return max(armor * (1 - percent_red), 0)

def split_base_and_bonus(total, base, bonus):
    if base + bonus == 0:
        return 0, 0
    ratio = bonus / (base + bonus)
    return total * (1 - ratio), total * ratio

def apply_percent_armor_penetration(bonus_armor, percent_pen):
    return bonus_armor * (1 - percent_pen)

def calculate_effective_armor(base, bonus, flat_red, flat_pen, percent_red, percent_pen):
    step1 = apply_flat_armor_reduction(base, bonus, flat_red)
    step2 = apply_flat_armor_penetration(step1, flat_pen)
    step3 = apply_percent_armor_reduction(step2, percent_red)
    adjusted_base, adjusted_bonus = split_base_and_bonus(step3, base, bonus)
    adjusted_bonus = apply_percent_armor_penetration(adjusted_bonus, percent_pen)
    return round(adjusted_base + adjusted_bonus, 2)
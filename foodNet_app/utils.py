from django.db.models import Sum
from .models import Food

def calculate_total_emissions_saved(user):
    # Sum up the carbon emissions saved for all food items provided by the user
    total_emissions_saved = Food.objects.filter(provider=user).aggregate(total=Sum('carbon_emission'))['total']
    # If there are no food items or carbon emission is None, set total_emissions_saved to 0
    if total_emissions_saved is None:
        total_emissions_saved = 0
    return total_emissions_saved
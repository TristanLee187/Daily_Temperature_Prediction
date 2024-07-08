import matplotlib.pyplot as plt

locs = ['austin', 'chicago', 'miami', 'ny']

# week 2: march 4th to 8th
week_2_dates = ['3/4', '3/5', '3/6', '3/7', '3/8']

week_2_temps = {
    'austin_pred': [75.38, 76.18, 82.08, 80.70, 75.00],
    'austin_gt': [83, 90, 82, 74, 83],
    'chicago_pred': [65.97, 59.11, 49.27, 53.99, 53.66],
    'chicago_gt': [72, 45, 50, 49, 47],
    'miami_pred': [82.08, 82.18, 80.46, 78.40, 84.05],
    'miami_gt': [83, 82, 80, 85, 84],
    'ny_pred': [58.24, 58.36, 51.56, 52.19, 52.97],
    'ny_gt': [59, 48, 53, 54, 56]
}

for loc in locs:
    plt.plot(week_2_dates, week_2_temps[f'{loc}_pred'], label='Predictions')
    plt.plot(week_2_dates, week_2_temps[f'{loc}_gt'], label='Ground Truth')
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Temperature (F)")
    plt.title(f'{loc.capitalize()} Week 2 Predictions')
    plt.savefig(f'{loc}_week_2_plot')
    plt.show()


# week 3: march 18th to 22nd
week_3_dates = ['3/18', '3/19', '3/20', '3/21', '3/22']

week_3_temps = {
    'austin_pred': [72.74748, 69.12, 68.28, 68.20, 64.81737],
    'austin_gt': [65, 66, 67, 64, 79],
    'chicago_pred': [47.736515, 44.19, 52.91, 47.22, 44.2708],
    'chicago_gt': [36, 58, 45, 41, 40],
    'miami_pred': [83.13435, 89.12, 78.39, 81.19, 82.46415],
    'miami_gt': [91, 79, 79, 81, 75],
    'ny_pred': [60.456745, 55.07, 53.90, 56.29, 52.85419],
    'ny_gt': [51, 48, 57, 43, 46]
}

for loc in locs:
    plt.plot(week_3_dates, week_3_temps[f'{loc}_pred'], label='Predictions')
    plt.plot(week_3_dates, week_3_temps[f'{loc}_gt'], label='Ground Truth')
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Temperature (F)")
    plt.title(f'{loc.capitalize()} Week 3 Predictions')
    plt.savefig(f'{loc}_week_3_plot')
    plt.show()

# TWAMP Measurement Data and Weather Simulation Generator

## Link to deepnote project
https://deepnote.com/app/playground-c8b0/TWAMP-correlation-example-8dac6f88-7793-4dc6-903f-465889dd617b?utm_source=share-modal&utm_medium=product-shared-content&utm_campaign=data-app&utm_content=8dac6f88-7793-4dc6-903f-465889dd617b

## Overview

This Python script generates synthetic datasets for Two-Way Active Measurement Protocol (TWAMP) network performance measurements along with correlated weather data focusing on rain impact.

The datasets model 6 months of hourly TWAMP metrics across 100 network nodes distributed over 10 cities. Each node is assigned a geographical location and a link type (underground fiber, underwater fiber, or microwave tower). The weather dataset provides hourly rain intensities per city.

Performance degradation on nodes with microwave tower links is simulated during rain events, with the effect scaling by rain intensity and stochastic variance. Rain events are clustered and spaced such that only 1-3 days of rain occur per week with a minimum 1.5 weeks dry gap.

## Generated Files

- `nodes.csv`: Information about each node, including node ID, city, latitude, longitude, and link type.
- `weather_patterns.csv`: Hourly weather data per city containing rain intensity in millimeters.
- `twamp_measurements_with_rain_updated.csv`: Hourly TWAMP performance data per node, incorporating rain-induced performance drops for microwave links.

## Requirements

- Python 3.8+
- pandas
- numpy

Install dependencies using:

```

pip install pandas numpy

```

## Usage

Run the script to generate the datasets:

```

python generate_twamp_weather.py

```

The script internally:

1. Defines 10 cities with GIS coordinates.
2. Creates 100 nodes distributed randomly among cities with assigned link types.
3. Generates hourly timestamps covering 6 months.
4. Produces rain schedules per city with clustered rain days and dry gaps.
5. Outputs per-hour rain intensities sampled according to rain schedules.
6. Simulates baseline TWAMP RTT and jitter metrics per node, varying by day and hour.
7. Applies rain-induced performance degradation on microwave tower links proportional to rain intensity.
8. Saves all datasets as CSV files.

## Customization

Modify the following parameters within the script before running if needed:

- `cities`: Add or adjust city names and GPS coordinates.
- `link_types`: Change network link types.
- Time period: Adjust `start_date` and `end_date` for dataset duration.
- Rain pattern constraints in the `generate_rain_schedule` function.

## Code Structure

- `generate_rain_schedule(total_days)`: Produces boolean rain day arrays respecting rain clustering and dry gaps.
- `simulate_performance(city, timestamp, link_type)`: Simulates base TWAMP performance metrics with time-of-day/day-of-week variation.
- Main loop: Iterates over each node and timestamp, combining weather impact with base metrics.

## Notes

- The rain performance drop is probabilistic and applies only to microwave tower links.
- Rain amount thresholds and performance drop percentages follow project specs.
- Output CSV files use timestamps in ISO 8601 format.

## License

This script is provided for educational and testing purposes without warranty. Use at your discretion.





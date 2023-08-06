# agent-finder
Find nearby auto insurance agents using the Google Maps Places API, and dump them to a CSV file.

This script was written to help automate part of
my girlfriends job. Maybe someone else will find it useful too.

## Installation

```shell script
pip3 install agent-finder-masterjefferson
```

## Usage

#### Google Maps API
You must have a valid Google Maps API key.

In your shell configuration file (.zshrc, .bash_profile, .bashrc, etc):
```shell script
export GOOGLE_MAPS_API_KEY=<your-api-key>
```

#### Basic search:

```shell script
agent-finder "Los Angeles, CA"
```

You can also customize the CSV filename and the search radius (units = kilometers).
```shell script
agent-finder "Los Angeles, CA" --filename foo.csv --radius 50
```

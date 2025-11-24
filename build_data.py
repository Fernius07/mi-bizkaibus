import csv
import json
import os
import shutil
from datetime import datetime

# Configuration
GTFS_DIR = 'gtfs'
DATA_DIR = 'data'
STOPS_DIR = os.path.join(DATA_DIR, 'stops')

def load_csv(filename):
    """Reads a CSV file from the GTFS directory."""
    filepath = os.path.join(GTFS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filename} not found.")
        return []
    
    with open(filepath, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    print("Starting GTFS processing...")
    
    # 1. Prepare Directories
    if os.path.exists(DATA_DIR):
        # Don't delete everything, just ensure structure
        pass
    ensure_dir(STOPS_DIR)

    # 2. Load GTFS Data
    print("Loading GTFS files...")
    stops = load_csv('stops.txt')
    routes = load_csv('routes.txt')
    trips = load_csv('trips.txt')
    calendar = load_csv('calendar.txt')
    calendar_dates = load_csv('calendar_dates.txt')
    # stop_times is large, we might process it iteratively or load it if memory allows
    # 48MB is fine to load.
    stop_times = load_csv('stop_times.txt')

    print(f"Loaded {len(stops)} stops, {len(routes)} routes, {len(trips)} trips, {len(stop_times)} stop_times.")

    # 3. Process Routes (Map route_id -> route_short_name)
    routes_map = {r['route_id']: r for r in routes}

    # 4. Process Services (Calendar)
    # We need to export this so JS can determine which trips are active today
    services = {}
    
    for cal in calendar:
        services[cal['service_id']] = {
            'start_date': cal['start_date'],
            'end_date': cal['end_date'],
            'days': [
                int(cal['monday']), int(cal['tuesday']), int(cal['wednesday']),
                int(cal['thursday']), int(cal['friday']), int(cal['saturday']), int(cal['sunday'])
            ],
            'added': [],
            'removed': []
        }
    
    for date in calendar_dates:
        sid = date['service_id']
        if sid not in services:
            # Some feeds use calendar_dates ONLY
            services[sid] = {'start_date': '00000000', 'end_date': '99999999', 'days': [0]*7, 'added': [], 'removed': []}
        
        if date['exception_type'] == '1': # Added
            services[sid]['added'].append(date['date'])
        elif date['exception_type'] == '2': # Removed
            services[sid]['removed'].append(date['date'])

    with open(os.path.join(DATA_DIR, 'services.json'), 'w', encoding='utf-8') as f:
        json.dump(services, f)
    print("Generated data/services.json")

    # 5. Process Stops (Master List)
    # We only need basic info for the map
    stops_list = []
    for s in stops:
        stops_list.append({
            'id': s['stop_id'],
            'name': s['stop_name'],
            'lat': float(s['stop_lat']),
            'lon': float(s['stop_lon']),
            'code': s.get('stop_code', '')
        })
    
    with open(os.path.join(DATA_DIR, 'stops.json'), 'w', encoding='utf-8') as f:
        json.dump(stops_list, f)
    print(f"Generated data/stops.json ({len(stops_list)} stops)")

    # 6. Process Stop Times (The heavy part)
    # We want: stops/{stop_id}.json -> [ { time, route, headsign, service_id }, ... ]
    
    # First, map trip_id -> { route_id, service_id, headsign }
    trips_map = {}
    for t in trips:
        trips_map[t['trip_id']] = {
            'route_id': t['route_id'],
            'service_id': t['service_id'],
            'headsign': t.get('trip_headsign', '')
        }

    # Group stop_times by stop_id
    # Using a dictionary of lists
    stops_schedule = {} # stop_id -> list of arrivals

    print("Grouping stop_times by stop...")
    for st in stop_times:
        stop_id = st['stop_id']
        trip_id = st['trip_id']
        arrival_time = st['arrival_time']
        
        if stop_id not in stops_schedule:
            stops_schedule[stop_id] = []
            
        trip_info = trips_map.get(trip_id)
        if not trip_info:
            continue
            
        route_info = routes_map.get(trip_info['route_id'])
        route_name = route_info['route_short_name'] if route_info else "???"
        
        # Handle times > 24:00:00 (GTFS standard)
        # We keep them as strings for sorting, JS can handle the logic or we normalize
        # For simple sorting, HH:MM:SS works if we treat 25:00 as next day
        
        stops_schedule[stop_id].append({
            'time': arrival_time,
            'route': route_name,
            'headsign': trip_info['headsign'],
            'service_id': trip_info['service_id'],
            'trip_id': trip_id
        })

    # 7. Write individual stop files
    print("Writing stop files...")
    count = 0
    for stop_id, arrivals in stops_schedule.items():
        # Sort by time
        arrivals.sort(key=lambda x: x['time'])
        
        # Write to file
        filename = os.path.join(STOPS_DIR, f"{stop_id}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(arrivals, f)
        count += 1
        if count % 1000 == 0:
            print(f"Wrote {count} stop files...")

    print("Done!")

if __name__ == "__main__":
    main()

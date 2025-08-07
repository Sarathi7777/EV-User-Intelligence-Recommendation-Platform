import os
import requests
import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from .snowflake_connector import SnowflakeManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenChargeMapFetcher:
    def __init__(self):
        self.api_key = os.getenv("OCM_API_KEY")
        self.base_url = "https://api.openchargemap.io/v3/poi"
        self.snowflake_manager = SnowflakeManager()
        
        # Tamil Nadu bounding box coordinates (approximate)
        self.tamil_nadu_bounds = {
            "min_lat": 8.0883,  # Southernmost point
            "max_lat": 13.7909,  # Northernmost point
            "min_lon": 76.2276,  # Westernmost point
            "max_lon": 80.2707   # Easternmost point
        }
        
        if not self.api_key:
            raise ValueError("OCM_API_KEY environment variable is required")
    
    def is_within_tamil_nadu_bounds(self, lat: float, lon: float) -> bool:
        """Check if coordinates are within Tamil Nadu bounding box."""
        return (
            self.tamil_nadu_bounds["min_lat"] <= lat <= self.tamil_nadu_bounds["max_lat"] and
            self.tamil_nadu_bounds["min_lon"] <= lon <= self.tamil_nadu_bounds["max_lon"]
        )
    
    def is_tamil_nadu_station(self, station_data: Dict[str, Any]) -> bool:
        """Check if station is in Tamil Nadu using address information."""
        address_info = station_data.get("AddressInfo", {})
        
        # Check state/province
        state = address_info.get("StateOrProvince", "").lower()
        if "tamil nadu" in state or "tamilnadu" in state:
            return True
        
        # Check country
        country = address_info.get("Country", {}).get("Title", "").lower()
        if country != "india":
            return False
        
        # Check coordinates
        lat = address_info.get("Latitude", 0)
        lon = address_info.get("Longitude", 0)
        if lat and lon:
            return self.is_within_tamil_nadu_bounds(float(lat), float(lon))
        
        return False
    
    def fetch_tamil_nadu_stations(self, max_results: int = 2000) -> List[Dict[str, Any]]:
        """Fetch stations specifically from Tamil Nadu using multiple approaches."""
        all_stations = []
        
        # Approach 1: Fetch by bounding box (multiple center points)
        center_points = [
            (11.0168, 76.9558),  # Coimbatore
            (13.0827, 80.2707),  # Chennai
            (9.9252, 78.1198),   # Madurai
            (10.7905, 78.7047),  # Trichy
            (11.2588, 75.7804),  # Calicut (nearby)
            (8.0883, 77.5385),   # Kanyakumari
            (12.9716, 79.1586),  # Vellore
            (10.7905, 78.7047),  # Salem
        ]
        
        logger.info("Fetching Tamil Nadu stations using multiple center points...")
        
        for lat, lon in center_points:
            try:
                stations = self.fetch_stations_by_location(lat, lon, radius_km=100, max_results=500)
                all_stations.extend(stations)
                logger.info(f"Fetched {len(stations)} stations from center point ({lat}, {lon})")
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error fetching from center point ({lat}, {lon}): {e}")
        
        # Approach 2: Fetch by country and filter
        logger.info("Fetching Indian stations and filtering for Tamil Nadu...")
        try:
            indian_stations = self.fetch_stations_by_country("IN", max_results=1000)
            all_stations.extend(indian_stations)
            logger.info(f"Fetched {len(indian_stations)} stations from India")
        except Exception as e:
            logger.error(f"Error fetching Indian stations: {e}")
        
        # Remove duplicates based on OCM ID
        unique_stations = {}
        for station in all_stations:
            station_id = station.get("ID")
            if station_id and station_id not in unique_stations:
                unique_stations[station_id] = station
        
        # Filter for Tamil Nadu stations
        tamil_nadu_stations = []
        for station in unique_stations.values():
            if self.is_tamil_nadu_station(station):
                tamil_nadu_stations.append(station)
        
        logger.info(f"Total unique stations: {len(unique_stations)}")
        logger.info(f"Tamil Nadu stations after filtering: {len(tamil_nadu_stations)}")
        
        return tamil_nadu_stations[:max_results]

    def fetch_stations_by_country(self, country_code: str = "US", max_results: int = 1000) -> List[Dict[str, Any]]:
        """Fetch stations by country code with pagination."""
        all_stations = []
        offset = 0
        limit = 100  # OCM API limit per request
        
        logger.info(f"Starting to fetch stations for country: {country_code}")
        
        while len(all_stations) < max_results:
            try:
                params = {
                    "key": self.api_key,
                    "output": "json",
                    "countrycode": country_code,
                    "maxresults": min(limit, max_results - len(all_stations)),
                    "compact": "true",
                    "verbose": "false",
                    "offset": offset
                }
                
                logger.info(f"Fetching stations with offset {offset}, limit {params['maxresults']}")
                
                response = requests.get(self.base_url, params=params, timeout=30)
                response.raise_for_status()
                
                stations = response.json()
                
                if not stations:
                    logger.info("No more stations to fetch")
                    break
                
                all_stations.extend(stations)
                logger.info(f"Fetched {len(stations)} stations, total: {len(all_stations)}")
                
                offset += len(stations)
                
                # Rate limiting - OCM has rate limits
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching stations: {e}")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                break
        
        logger.info(f"Total stations fetched: {len(all_stations)}")
        return all_stations
    
    def fetch_stations_by_location(self, lat: float, lon: float, radius_km: float = 50, max_results: int = 500) -> List[Dict[str, Any]]:
        """Fetch stations within a radius of a specific location."""
        all_stations = []
        offset = 0
        limit = 100
        
        logger.info(f"Fetching stations near ({lat}, {lon}) within {radius_km}km")
        
        while len(all_stations) < max_results:
            try:
                params = {
                    "key": self.api_key,
                    "output": "json",
                    "latitude": lat,
                    "longitude": lon,
                    "distance": radius_km,
                    "distanceunit": "km",
                    "maxresults": min(limit, max_results - len(all_stations)),
                    "compact": "true",
                    "verbose": "false",
                    "offset": offset
                }
                
                response = requests.get(self.base_url, params=params, timeout=30)
                response.raise_for_status()
                
                stations = response.json()
                
                if not stations:
                    break
                
                all_stations.extend(stations)
                logger.info(f"Fetched {len(stations)} stations, total: {len(all_stations)}")
                
                offset += len(stations)
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching stations: {e}")
                break
        
        return all_stations
    
    def parse_station_data(self, ocm_station: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and clean station data from OCM API response."""
        try:
            address_info = ocm_station.get("AddressInfo", {})
            connections = ocm_station.get("Connections", [])
            
            # Extract energy types from connections
            energy_types = []
            for conn in connections:
                connection_type = conn.get("ConnectionType", {}).get("Title", "")
                if connection_type and connection_type not in energy_types:
                    energy_types.append(connection_type)
            
            # Get station name
            station_name = address_info.get("Title", "")
            if not station_name:
                station_name = f"Station at {address_info.get('AddressLine1', 'Unknown Location')}"
            
            # Parse address components
            address_line1 = address_info.get("AddressLine1", "")
            address_line2 = address_info.get("AddressLine2", "")
            town = address_info.get("Town", "")
            state = address_info.get("StateOrProvince", "")
            country = address_info.get("Country", {}).get("Title", "")
            postcode = address_info.get("Postcode", "")
            
            # Get access comments
            access_comments = address_info.get("AccessComments", "")
            
            # Get coordinates
            latitude = address_info.get("Latitude", 0.0)
            longitude = address_info.get("Longitude", 0.0)
            
            # Validate coordinates
            if not latitude or not longitude:
                logger.warning(f"Invalid coordinates for station {ocm_station.get('ID')}")
                return None
            
            parsed_station = {
                "id": len(energy_types) + 1000,  # Generate unique ID
                "ocm_id": ocm_station.get("ID"),
                "name": station_name,
                "latitude": float(latitude),
                "longitude": float(longitude),
                "energy_type": ", ".join(energy_types) if energy_types else "Unknown",
                "address_line1": address_line1,
                "address_line2": address_line2,
                "town": town,
                "state": state,
                "country": country,
                "postcode": postcode,
                "access_comments": access_comments,
                "available": True,  # OCM doesn't provide real-time availability
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            return parsed_station
            
        except Exception as e:
            logger.error(f"Error parsing station data: {e}")
            return None
    
    def store_stations_in_snowflake(self, stations: List[Dict[str, Any]]) -> int:
        """Store parsed stations in Snowflake database."""
        if not stations:
            logger.warning("No stations to store")
            return 0
        
        try:
            # Create tables if they don't exist
            self.snowflake_manager.create_tables()
            
            # Insert stations in batches
            batch_size = 100
            total_inserted = 0
            
            for i in range(0, len(stations), batch_size):
                batch = stations[i:i + batch_size]
                try:
                    self.snowflake_manager.insert_stations_batch(batch)
                    total_inserted += len(batch)
                    logger.info(f"Inserted batch {i//batch_size + 1}: {len(batch)} stations")
                except Exception as e:
                    logger.error(f"Error inserting batch {i//batch_size + 1}: {e}")
                    # Try inserting one by one for this batch
                    for station in batch:
                        try:
                            self.snowflake_manager.insert_station(station)
                            total_inserted += 1
                        except Exception as single_error:
                            logger.error(f"Error inserting station {station.get('ocm_id')}: {single_error}")
            
            logger.info(f"Successfully stored {total_inserted} stations in Snowflake")
            return total_inserted
            
        except Exception as e:
            logger.error(f"Error storing stations in Snowflake: {e}")
            raise
    
    def get_station_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored stations."""
        try:
            total_stations = self.snowflake_manager.get_station_count()
            
            # Get stations by state (should be mostly Tamil Nadu)
            query = """
                SELECT state, COUNT(*) as count 
                FROM stations 
                GROUP BY state 
                ORDER BY count DESC
            """
            state_stats = self.snowflake_manager.execute_query(query)
            
            # Get stations by energy type
            query = """
                SELECT energy_type, COUNT(*) as count 
                FROM stations 
                GROUP BY energy_type 
                ORDER BY count DESC
            """
            energy_type_stats = self.snowflake_manager.execute_query(query)
            
            # Get stations by city/town
            query = """
                SELECT town, COUNT(*) as count 
                FROM stations 
                WHERE town IS NOT NULL AND town != ''
                GROUP BY town 
                ORDER BY count DESC
                LIMIT 10
            """
            city_stats = self.snowflake_manager.execute_query(query)
            
            return {
                "total_stations": total_stations,
                "by_state": state_stats,
                "by_energy_type": energy_type_stats,
                "by_city": city_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
    
    def run_tamil_nadu_ingestion(self, max_stations: int = 2000) -> Dict[str, Any]:
        """Run data ingestion specifically for Tamil Nadu stations."""
        logger.info("Starting Tamil Nadu station ingestion...")
        
        try:
            # Fetch Tamil Nadu stations
            stations = self.fetch_tamil_nadu_stations(max_stations)
            logger.info(f"Fetched {len(stations)} Tamil Nadu stations")
            
            # Parse station data
            parsed_stations = []
            for station in stations:
                parsed = self.parse_station_data(station)
                if parsed:
                    parsed_stations.append(parsed)
            
            logger.info(f"Parsed {len(parsed_stations)} stations")
            
            # Store in Snowflake
            stored_count = self.store_stations_in_snowflake(parsed_stations)
            
            # Get statistics
            stats = self.get_station_statistics()
            
            results = {
                "summary": {
                    "total_fetched": len(stations),
                    "total_parsed": len(parsed_stations),
                    "total_stored": stored_count,
                    "region": "Tamil Nadu, India"
                },
                "statistics": stats
            }
            
            logger.info(f"Tamil Nadu ingestion complete: {len(stations)} fetched, {len(parsed_stations)} parsed, {stored_count} stored")
            return results
            
        except Exception as e:
            logger.error(f"Error in Tamil Nadu ingestion: {e}")
            raise

    def run_full_ingestion(self, countries: List[str] = None, max_stations_per_country: int = 1000) -> Dict[str, Any]:
        """Run complete data ingestion for multiple countries."""
        if countries is None:
            countries = ["US", "CA", "GB", "DE", "FR", "NL", "AU", "JP"]
        
        total_stations_fetched = 0
        total_stations_stored = 0
        results = {}
        
        logger.info(f"Starting full ingestion for countries: {countries}")
        
        for country in countries:
            try:
                logger.info(f"Processing country: {country}")
                
                # Fetch stations for this country
                stations = self.fetch_stations_by_country(country, max_stations_per_country)
                total_stations_fetched += len(stations)
                
                # Parse station data
                parsed_stations = []
                for station in stations:
                    parsed = self.parse_station_data(station)
                    if parsed:
                        parsed_stations.append(parsed)
                
                # Store in Snowflake
                stored_count = self.store_stations_in_snowflake(parsed_stations)
                total_stations_stored += stored_count
                
                results[country] = {
                    "fetched": len(stations),
                    "parsed": len(parsed_stations),
                    "stored": stored_count
                }
                
                logger.info(f"Country {country}: {len(stations)} fetched, {len(parsed_stations)} parsed, {stored_count} stored")
                
                # Rate limiting between countries
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error processing country {country}: {e}")
                results[country] = {"error": str(e)}
        
        # Get final statistics
        stats = self.get_station_statistics()
        
        final_results = {
            "summary": {
                "total_fetched": total_stations_fetched,
                "total_stored": total_stations_stored,
                "countries_processed": len(countries)
            },
            "by_country": results,
            "statistics": stats
        }
        
        logger.info(f"Ingestion complete: {total_stations_fetched} fetched, {total_stations_stored} stored")
        return final_results

def main():
    """Main function to run the OCM data ingestion."""
    try:
        # Initialize the fetcher
        fetcher = OpenChargeMapFetcher()
        
        # Run Tamil Nadu specific ingestion
        results = fetcher.run_tamil_nadu_ingestion()
        
        # Save results to file
        with open("tamil_nadu_ocm_ingestion_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print("=== Tamil Nadu OCM Data Ingestion Complete ===")
        print(f"Total stations fetched: {results['summary']['total_fetched']}")
        print(f"Total stations parsed: {results['summary']['total_parsed']}")
        print(f"Total stations stored: {results['summary']['total_stored']}")
        print(f"Region: {results['summary']['region']}")
        print("\nResults saved to: tamil_nadu_ocm_ingestion_results.json")
        
        # Print statistics
        if 'statistics' in results:
            stats = results['statistics']
            print(f"\nStatistics:")
            print(f"Total stations in database: {stats.get('total_stations', 0)}")
            
            if 'by_state' in stats:
                print("\nStations by State:")
                for state_stat in stats['by_state'][:5]:
                    print(f"  {state_stat['state']}: {state_stat['count']}")
            
            if 'by_city' in stats:
                print("\nTop Cities:")
                for city_stat in stats['by_city'][:5]:
                    print(f"  {city_stat['town']}: {city_stat['count']}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main()
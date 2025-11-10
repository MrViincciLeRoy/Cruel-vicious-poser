#!/usr/bin/env python3
"""
Wikidata Artist Scraper
Fetches comprehensive artist data from Wikidata and saves to JSON
"""

import requests
import json
import time
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


class WikidataArtistScraper:
    """Scrape artist data from Wikidata SPARQL endpoint"""

    def __init__(self, output_file: str = "config/artist_database.json"):
        """Initialize the scraper"""
        self.output_file = Path(output_file)
        self.sparql_endpoint = "https://query.wikidata.org/sparql"
        self.headers = {
            'User-Agent': 'ArtistDatabaseBuilder/1.0 (Educational Project)',
            'Accept': 'application/json'
        }
        
        # Initialize or load existing database
        self.database = self._load_existing_database()

    def _load_existing_database(self) -> Dict:
        """Load existing database or create new structure"""
        if self.output_file.exists():
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'search_queries': [],
            'movements': [],
            'themes': [],
            'metadata': {
                'last_updated': None,
                'total_artists': 0,
                'total_movements': 0,
                'sources': ['wikidata']
            }
        }

    def save_database(self):
        """Save database to JSON file"""
        # Update metadata
        self.database['metadata']['last_updated'] = datetime.now().isoformat()
        self.database['metadata']['total_artists'] = len(self.database['search_queries'])
        self.database['metadata']['total_movements'] = len(self.database['movements'])
        
        # Create directory if needed
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save with pretty formatting
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.database, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Database saved to {self.output_file}")

    def query_wikidata(self, sparql_query: str, max_retries: int = 3) -> Optional[List[Dict]]:
        """Execute SPARQL query against Wikidata"""
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    self.sparql_endpoint,
                    params={'query': sparql_query, 'format': 'json'},
                    headers=self.headers,
                    timeout=30
                )
                response.raise_for_status()
                
                data = response.json()
                return data['results']['bindings']
                
            except Exception as e:
                print(f"   ⚠️  Query attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"   ❌ Query failed after {max_retries} attempts")
                    return None

    def fetch_painters_by_era(self, era: str, limit: int = 100) -> List[str]:
        """
        Fetch painters from a specific era
        
        Args:
            era: Century or time period (e.g., "15", "16", "17" for centuries)
            limit: Maximum number of results
        """
        print(f"🔍 Fetching {era}th century painters...")
        
        query = f"""
        SELECT DISTINCT ?artist ?artistLabel WHERE {{
          ?artist wdt:P31 wd:Q5;                    # instance of human
                  wdt:P106 wd:Q1028181;              # occupation: painter
                  wdt:P569 ?birthDate.               # has birth date
          
          FILTER(YEAR(?birthDate) >= {era}00 && YEAR(?birthDate) < {int(era)+1}00)
          
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT {limit}
        """
        
        results = self.query_wikidata(query)
        if not results:
            return []
        
        artists = [r['artistLabel']['value'] for r in results if 'artistLabel' in r]
        print(f"   ✅ Found {len(artists)} painters")
        return artists

    def fetch_famous_painters(self, limit: int = 200) -> List[str]:
        """Fetch most notable painters based on Wikipedia article existence"""
        print(f"🔍 Fetching famous painters...")
        
        query = f"""
        SELECT DISTINCT ?artist ?artistLabel WHERE {{
          ?artist wdt:P31 wd:Q5;                    # instance of human
                  wdt:P106 wd:Q1028181;              # occupation: painter
                  wdt:P569 ?birthDate.               # has birth date
          
          ?article schema:about ?artist;            # has Wikipedia article
                   schema:isPartOf <https://en.wikipedia.org/>.
          
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        ORDER BY DESC(?article)
        LIMIT {limit}
        """
        
        results = self.query_wikidata(query)
        if not results:
            return []
        
        artists = [r['artistLabel']['value'] for r in results if 'artistLabel' in r]
        print(f"   ✅ Found {len(artists)} famous painters")
        return artists

    def fetch_painters_by_movement(self, movement_qid: str, movement_name: str, limit: int = 50) -> List[str]:
        """
        Fetch painters associated with an art movement
        
        Args:
            movement_qid: Wikidata QID for the movement (e.g., "Q40415" for Baroque)
            movement_name: Human-readable movement name
            limit: Maximum results
        """
        print(f"🔍 Fetching {movement_name} painters...")
        
        query = f"""
        SELECT DISTINCT ?artist ?artistLabel WHERE {{
          ?artist wdt:P31 wd:Q5;                    # instance of human
                  wdt:P106 wd:Q1028181;              # occupation: painter
                  wdt:P135 wd:{movement_qid}.        # movement
          
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT {limit}
        """
        
        results = self.query_wikidata(query)
        if not results:
            return []
        
        artists = [r['artistLabel']['value'] for r in results if 'artistLabel' in r]
        print(f"   ✅ Found {len(artists)} {movement_name} painters")
        return artists

    def fetch_art_movements(self, limit: int = 100) -> List[str]:
        """Fetch major art movements from Wikidata"""
        print(f"🔍 Fetching art movements...")
        
        query = f"""
        SELECT DISTINCT ?movement ?movementLabel WHERE {{
          ?movement wdt:P31/wdt:P279* wd:Q968159.   # instance of/subclass of art movement
          
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT {limit}
        """
        
        results = self.query_wikidata(query)
        if not results:
            return []
        
        movements = [r['movementLabel']['value'] for r in results if 'movementLabel' in r]
        # Add "painting" suffix for better search results
        movements_with_suffix = [f"{m} painting" if 'painting' not in m.lower() else m for m in movements]
        
        print(f"   ✅ Found {len(movements)} art movements")
        return movements_with_suffix

    def fetch_painting_genres(self, limit: int = 50) -> List[str]:
        """Fetch painting genres/themes"""
        print(f"🔍 Fetching painting genres...")
        
        query = f"""
        SELECT DISTINCT ?genre ?genreLabel WHERE {{
          ?genre wdt:P31/wdt:P279* wd:Q1047337.     # instance of/subclass of genre
          
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT {limit}
        """
        
        results = self.query_wikidata(query)
        if not results:
            return []
        
        genres = [r['genreLabel']['value'] for r in results if 'genreLabel' in r]
        # Add "painting" suffix
        genres_with_suffix = [f"{g} painting" if 'painting' not in g.lower() else g for g in genres]
        
        print(f"   ✅ Found {len(genres)} genres")
        return genres_with_suffix

    def scrape_renaissance_masters(self):
        """Scrape Renaissance period artists"""
        print("\n" + "="*70)
        print("SCRAPING RENAISSANCE MASTERS (15th-16th Century)")
        print("="*70)
        
        artists = []
        artists.extend(self.fetch_painters_by_era("14", limit=30))  # Early Renaissance
        time.sleep(2)
        artists.extend(self.fetch_painters_by_era("15", limit=50))  # High Renaissance
        time.sleep(2)
        artists.extend(self.fetch_painters_by_era("16", limit=50))  # Late Renaissance
        
        self._add_to_queries(artists)
        return artists

    def scrape_baroque_masters(self):
        """Scrape Baroque period artists"""
        print("\n" + "="*70)
        print("SCRAPING BAROQUE MASTERS (17th Century)")
        print("="*70)
        
        artists = self.fetch_painters_by_era("16", limit=50)
        time.sleep(2)
        artists.extend(self.fetch_painters_by_era("17", limit=50))
        
        # Also fetch by movement
        time.sleep(2)
        baroque_artists = self.fetch_painters_by_movement("Q40415", "Baroque", limit=50)
        artists.extend(baroque_artists)
        
        self._add_to_queries(artists)
        return artists

    def scrape_18th_century_artists(self):
        """Scrape 18th century artists"""
        print("\n" + "="*70)
        print("SCRAPING 18TH CENTURY ARTISTS")
        print("="*70)
        
        artists = self.fetch_painters_by_era("17", limit=50)
        time.sleep(2)
        artists.extend(self.fetch_painters_by_era("18", limit=50))
        
        self._add_to_queries(artists)
        return artists

    def scrape_19th_century_artists(self):
        """Scrape 19th century artists"""
        print("\n" + "="*70)
        print("SCRAPING 19TH CENTURY ARTISTS")
        print("="*70)
        
        artists = self.fetch_painters_by_era("18", limit=50)
        time.sleep(2)
        artists.extend(self.fetch_painters_by_era("19", limit=100))
        
        # Impressionism
        time.sleep(2)
        artists.extend(self.fetch_painters_by_movement("Q40415", "Impressionism", limit=50))
        
        self._add_to_queries(artists)
        return artists

    def scrape_20th_century_artists(self):
        """Scrape 20th century artists"""
        print("\n" + "="*70)
        print("SCRAPING 20TH CENTURY ARTISTS")
        print("="*70)
        
        artists = self.fetch_painters_by_era("19", limit=100)
        time.sleep(2)
        artists.extend(self.fetch_painters_by_era("20", limit=100))
        
        self._add_to_queries(artists)
        return artists

    def scrape_famous_painters(self):
        """Scrape most famous painters"""
        print("\n" + "="*70)
        print("SCRAPING FAMOUS PAINTERS")
        print("="*70)
        
        artists = self.fetch_famous_painters(limit=200)
        self._add_to_queries(artists)
        return artists

    def scrape_art_movements(self):
        """Scrape art movements"""
        print("\n" + "="*70)
        print("SCRAPING ART MOVEMENTS")
        print("="*70)
        
        movements = self.fetch_art_movements(limit=100)
        self._add_to_movements(movements)
        return movements

    def scrape_painting_genres(self):
        """Scrape painting genres and themes"""
        print("\n" + "="*70)
        print("SCRAPING PAINTING GENRES")
        print("="*70)
        
        genres = self.fetch_painting_genres(limit=50)
        self._add_to_themes(genres)
        return genres

    def scrape_all(self):
        """Scrape everything - comprehensive database build"""
        print("\n" + "🎨"*35)
        print("   COMPREHENSIVE ARTIST DATABASE BUILDER")
        print("   Powered by Wikidata")
        print("🎨"*35 + "\n")
        
        try:
            # Scrape famous painters first (most important)
            self.scrape_famous_painters()
            time.sleep(3)
            
            # Scrape by century
            self.scrape_renaissance_masters()
            time.sleep(3)
            
            self.scrape_baroque_masters()
            time.sleep(3)
            
            self.scrape_18th_century_artists()
            time.sleep(3)
            
            self.scrape_19th_century_artists()
            time.sleep(3)
            
            self.scrape_20th_century_artists()
            time.sleep(3)
            
            # Scrape movements and genres
            self.scrape_art_movements()
            time.sleep(3)
            
            self.scrape_painting_genres()
            
            # Save everything
            self.save_database()
            
            # Show statistics
            self.show_statistics()
            
            print("\n" + "✨"*35)
            print("🎉 SCRAPING COMPLETE!")
            print("✨"*35 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Scraping interrupted by user")
            print("💾 Saving partial data...")
            self.save_database()
            self.show_statistics()
        
        except Exception as e:
            print(f"\n❌ Error during scraping: {e}")
            print("💾 Saving partial data...")
            self.save_database()
            import traceback
            traceback.print_exc()

    def _add_to_queries(self, items: List[str]):
        """Add items to search queries, avoiding duplicates"""
        current = set(self.database['search_queries'])
        new_items = [item for item in items if item and item not in current]
        self.database['search_queries'].extend(new_items)
        print(f"   📝 Added {len(new_items)} new artists")

    def _add_to_movements(self, items: List[str]):
        """Add items to movements, avoiding duplicates"""
        current = set(self.database['movements'])
        new_items = [item for item in items if item and item not in current]
        self.database['movements'].extend(new_items)
        print(f"   📝 Added {len(new_items)} new movements")

    def _add_to_themes(self, items: List[str]):
        """Add items to themes, avoiding duplicates"""
        current = set(self.database['themes'])
        new_items = [item for item in items if item and item not in current]
        self.database['themes'].extend(new_items)
        print(f"   📝 Added {len(new_items)} new themes")

    def show_statistics(self):
        """Display database statistics"""
        print("\n" + "="*70)
        print("DATABASE STATISTICS")
        print("="*70)
        print(f"Total Artists: {len(self.database['search_queries'])}")
        print(f"Art Movements: {len(self.database['movements'])}")
        print(f"Themes/Genres: {len(self.database['themes'])}")
        print(f"Total Search Terms: {len(self.database['search_queries']) + len(self.database['movements']) + len(self.database['themes'])}")
        print("="*70)
        
        # Show sample data
        if self.database['search_queries']:
            print("\nSample Artists:")
            for artist in self.database['search_queries'][:10]:
                print(f"  • {artist}")
        
        if self.database['movements']:
            print("\nSample Movements:")
            for movement in self.database['movements'][:5]:
                print(f"  • {movement}")

    def add_manual_artists(self, artists: List[str]):
        """Manually add specific artists"""
        self._add_to_queries(artists)
        print(f"✅ Manually added {len(artists)} artists")

    def add_manual_movements(self, movements: List[str]):
        """Manually add specific movements"""
        self._add_to_movements(movements)
        print(f"✅ Manually added {len(movements)} movements")

    def add_manual_themes(self, themes: List[str]):
        """Manually add specific themes"""
        self._add_to_themes(themes)
        print(f"✅ Manually added {len(themes)} themes")


def interactive_menu():
    """Interactive menu for scraping"""
    scraper = WikidataArtistScraper()
    
    print("\n" + "🎨"*35)
    print("   WIKIDATA ARTIST SCRAPER")
    print("   Build Your Artist Database from Wikidata")
    print("🎨"*35 + "\n")

    while True:
        print("\n" + "="*70)
        print("OPTIONS:")
        print("="*70)
        print("1. Scrape ALL data (comprehensive) - RECOMMENDED")
        print("2. Scrape famous painters only")
        print("3. Scrape Renaissance masters")
        print("4. Scrape Baroque masters")
        print("5. Scrape 18th century artists")
        print("6. Scrape 19th century artists")
        print("7. Scrape 20th century artists")
        print("8. Scrape art movements")
        print("9. Scrape painting genres/themes")
        print("10. Show statistics")
        print("11. Save and exit")
        print("="*70)

        choice = input("\n👉 Your choice (or 'quit'): ").strip()

        if choice == 'quit' or choice == '11':
            scraper.save_database()
            scraper.show_statistics()
            print("\n👋 Database saved! Ready for use.\n")
            break

        elif choice == '1':
            scraper.scrape_all()

        elif choice == '2':
            scraper.scrape_famous_painters()
            time.sleep(2)

        elif choice == '3':
            scraper.scrape_renaissance_masters()
            time.sleep(2)

        elif choice == '4':
            scraper.scrape_baroque_masters()
            time.sleep(2)

        elif choice == '5':
            scraper.scrape_18th_century_artists()
            time.sleep(2)

        elif choice == '6':
            scraper.scrape_19th_century_artists()
            time.sleep(2)

        elif choice == '7':
            scraper.scrape_20th_century_artists()
            time.sleep(2)

        elif choice == '8':
            scraper.scrape_art_movements()
            time.sleep(2)

        elif choice == '9':
            scraper.scrape_painting_genres()
            time.sleep(2)

        elif choice == '10':
            scraper.show_statistics()

        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    # Option 1: Interactive menu
    #interactive_menu()
    
    # Option 2: Direct scraping (uncomment to use)
    scraper = WikidataArtistScraper()
    scraper.scrape_all()

#!/usr/bin/env python3
"""
Expand artist database by adding more artists, movements, and themes
This script helps you build a comprehensive database for variety
"""

import json
from pathlib import Path
from typing import Dict, List

class ArtistDatabaseExpander:
    """Expand and manage artist database"""

    def __init__(self):
        self.config_path = Path("config/artists_database.json")
        self.database = self._load_database()

    def _load_database(self) -> Dict:
        """Load existing database or create new one"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            return {
                'search_queries': [],
                'movements': [],
                'themes': []
            }

    def save_database(self):
        """Save database to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.database, f, indent=2)
        print(f"✅ Database saved to {self.config_path}")

    def add_artists_18th_century(self):
        """Add major 18th century artists"""
        artists = [
            "Jean-Honoré Fragonard",
            "François Boucher",
            "Antoine Watteau",
            "Jean-Baptiste-Siméon Chardin",
            "Thomas Gainsborough",
            "Joshua Reynolds",
            "George Romney",
            "Jean-Antoine Houdon",
            "Jacques-Louis David",
            "Elisabeth Vigée Le Brun",
            "Angelica Kauffman",
            "Giovanni Battista Tiepolo",
            "Canaletto",
            "Francesco Guardi",
            "William Hogarth",
            "Henry Fuseli",
            "Francisco Goya",
            "Gilbert Stuart"
        ]
        self._add_to_queries(artists)
        print(f"✅ Added {len(artists)} 18th century artists")

    def add_artists_19th_century(self):
        """Add major 19th century artists"""
        artists = [
            "J.M.W. Turner",
            "John Constable",
            "Caspar David Friedrich",
            "Eugène Delacroix",
            "Jean-Auguste-Dominique Ingres",
            "Gustave Courbet",
            "Jean-François Millet",
            "Honoré Daumier",
            "Édouard Manet",
            "Claude Monet",
            "Pierre-Auguste Renoir",
            "Edgar Degas",
            "Camille Pissarro",
            "Alfred Sisley",
            "Berthe Morisot",
            "Mary Cassatt",
            "Paul Cézanne",
            "Vincent van Gogh",
            "Paul Gauguin",
            "Georges Seurat",
            "Henri de Toulouse-Lautrec",
            "Odilon Redon",
            "James McNeill Whistler",
            "John Singer Sargent",
            "Winslow Homer",
            "Thomas Eakins",
            "Frederic Edwin Church",
            "Albert Bierstadt",
            "Dante Gabriel Rossetti",
            "Edward Burne-Jones",
            "William Morris",
            "Gustav Klimt",
            "Edvard Munch"
        ]
        self._add_to_queries(artists)
        print(f"✅ Added {len(artists)} 19th century artists")

    def add_artists_20th_century(self):
        """Add major 20th century artists"""
        artists = [
            "Pablo Picasso",
            "Henri Matisse",
            "Wassily Kandinsky",
            "Piet Mondrian",
            "Paul Klee",
            "Joan Miró",
            "Marc Chagall",
            "Georges Braque",
            "Fernand Léger",
            "Robert Delaunay",
            "Kazimir Malevich",
            "El Lissitzky",
            "Amedeo Modigliani",
            "Chaim Soutine",
            "Max Ernst",
            "Salvador Dalí",
            "René Magritte",
            "Giorgio de Chirico",
            "Frida Kahlo",
            "Diego Rivera",
            "José Clemente Orozco",
            "David Alfaro Siqueiros",
            "Edward Hopper",
            "Georgia O'Keeffe",
            "Grant Wood",
            "Jackson Pollock",
            "Willem de Kooning",
            "Mark Rothko",
            "Franz Kline",
            "Barnett Newman",
            "Clyfford Still",
            "Robert Motherwell",
            "Francis Bacon",
            "Lucian Freud",
            "David Hockney",
            "Gerhard Richter",
            "Anselm Kiefer",
            "Andy Warhol",
            "Roy Lichtenstein",
            "Jean-Michel Basquiat",
            "Keith Haring"
        ]
        self._add_to_queries(artists)
        print(f"✅ Added {len(artists)} 20th century artists")

    def add_artists_21st_century(self):
        """Add notable 21st century artists"""
        artists = [
            "Kehinde Wiley",
            "Jenny Saville",
            "Cecily Brown",
            "Julie Mehretu",
            "Kara Walker",
            "Wangechi Mutu",
            "Glenn Ligon",
            "Mark Bradford",
            "Oscar Murillo",
            "Adrian Ghenie",
            "Neo Rauch",
            "Marlene Dumas",
            "Luc Tuymans",
            "Peter Doig",
            "Chris Ofili"
        ]
        self._add_to_queries(artists)
        print(f"✅ Added {len(artists)} 21st century artists")

    def add_renaissance_masters(self):
        """Add Renaissance masters"""
        artists = [
            "Leonardo da Vinci",
            "Michelangelo",
            "Raphael",
            "Sandro Botticelli",
            "Donatello",
            "Masaccio",
            "Fra Angelico",
            "Piero della Francesca",
            "Paolo Uccello",
            "Andrea Mantegna",
            "Filippo Lippi",
            "Benozzo Gozzoli",
            "Domenico Ghirlandaio",
            "Pietro Perugino",
            "Giorgione",
            "Titian",
            "Tintoretto",
            "Paolo Veronese",
            "Correggio",
            "Andrea del Sarto"
        ]
        self._add_to_queries(artists)
        print(f"✅ Added {len(artists)} Renaissance masters")

    def add_baroque_masters(self):
        """Add Baroque period masters"""
        artists = [
            "Caravaggio",
            "Peter Paul Rubens",
            "Rembrandt",
            "Johannes Vermeer",
            "Diego Velázquez",
            "Anthony van Dyck",
            "Frans Hals",
            "Georges de La Tour",
            "Nicolas Poussin",
            "Claude Lorrain",
            "Artemisia Gentileschi",
            "Guido Reni",
            "Gian Lorenzo Bernini",
            "Jusepe de Ribera",
            "Francisco de Zurbarán",
            "Bartolomé Esteban Murillo"
        ]
        self._add_to_queries(artists)
        print(f"✅ Added {len(artists)} Baroque masters")

    def add_dutch_golden_age(self):
        """Add Dutch Golden Age artists"""
        artists = [
            "Rembrandt",
            "Johannes Vermeer",
            "Frans Hals",
            "Jan Steen",
            "Pieter de Hooch",
            "Gerard ter Borch",
            "Jacob van Ruisdael",
            "Rachel Ruysch",
            "Jan van Goyen",
            "Aelbert Cuyp",
            "Willem Kalf",
            "Jan Davidsz de Heem",
            "Judith Leyster",
            "Hendrick Avercamp"
        ]
        self._add_to_queries(artists)
        print(f"✅ Added {len(artists)} Dutch Golden Age artists")

    def add_northern_renaissance(self):
        """Add Northern Renaissance artists"""
        artists = [
            "Jan van Eyck",
            "Hieronymus Bosch",
            "Pieter Bruegel the Elder",
            "Albrecht Dürer",
            "Hans Holbein the Younger",
            "Lucas Cranach the Elder",
            "Matthias Grünewald",
            "Rogier van der Weyden",
            "Hugo van der Goes",
            "Hans Memling",
            "Quentin Matsys",
            "Joachim Patinir"
        ]
        self._add_to_queries(artists)
        print(f"✅ Added {len(artists)} Northern Renaissance artists")

    def add_movements(self):
        """Add comprehensive art movements"""
        movements = [
            "Early Renaissance",
            "High Renaissance",
            "Mannerism",
            "Baroque painting",
            "Rococo art",
            "Neoclassicism",
            "Romanticism painting",
            "Realism painting",
            "Pre-Raphaelite",
            "Impressionism painting",
            "Post-Impressionism",
            "Pointillism",
            "Symbolism art",
            "Art Nouveau",
            "Fauvism",
            "Expressionism painting",
            "Cubism",
            "Futurism art",
            "Constructivism",
            "Suprematism",
            "De Stijl",
            "Dada art",
            "Surrealism painting",
            "Abstract Expressionism",
            "Color Field painting",
            "Pop Art",
            "Minimalism art",
            "Conceptual art",
            "Photorealism",
            "Neo-Expressionism",
            "Hudson River School",
            "Ashcan School",
            "American Regionalism",
            "Mexican Muralism",
            "Social Realism",
            "Magic Realism"
        ]
        self.database['movements'] = list(set(self.database['movements'] + movements))
        print(f"✅ Added {len(movements)} art movements")

    def add_themes(self):
        """Add comprehensive themes"""
        themes = [
            "portrait painting",
            "self-portrait",
            "landscape painting",
            "seascape painting",
            "cityscape painting",
            "still life painting",
            "flower painting",
            "religious painting",
            "mythology painting",
            "biblical scene",
            "genre painting",
            "history painting",
            "battle scene",
            "interior scene",
            "nude painting",
            "animal painting",
            "horse painting",
            "mother and child",
            "peasant life",
            "aristocratic portrait",
            "group portrait",
            "nocturne painting",
            "winter landscape",
            "harvest scene",
            "market scene",
            "tavern scene",
            "garden painting",
            "architectural painting"
        ]
        self.database['themes'] = list(set(self.database['themes'] + themes))
        print(f"✅ Added {len(themes)} themes")

    def _add_to_queries(self, items: List[str]):
        """Add items to search queries, avoiding duplicates"""
        current = set(self.database['search_queries'])
        new_items = [item for item in items if item not in current]
        self.database['search_queries'].extend(new_items)

    def show_statistics(self):
        """Display database statistics"""
        print("\n" + "=" * 70)
        print("DATABASE STATISTICS")
        print("=" * 70)
        print(f"Total Artists: {len(self.database['search_queries'])}")
        print(f"Art Movements: {len(self.database['movements'])}")
        print(f"Themes: {len(self.database['themes'])}")
        print(f"Total Search Terms: {len(self.database['search_queries']) + len(self.database['movements']) + len(self.database['themes'])}")
        print("=" * 70)

    def add_custom_artists(self, artists: List[str]):
        """Add custom list of artists"""
        self._add_to_queries(artists)
        print(f"✅ Added {len(artists)} custom artists")

    def add_custom_movements(self, movements: List[str]):
        """Add custom movements"""
        self.database['movements'] = list(set(self.database['movements'] + movements))
        print(f"✅ Added {len(movements)} custom movements")

    def add_custom_themes(self, themes: List[str]):
        """Add custom themes"""
        self.database['themes'] = list(set(self.database['themes'] + themes))
        print(f"✅ Added {len(themes)} custom themes")


def interactive_menu():
    """Interactive menu for database expansion"""
    expander = ArtistDatabaseExpander()
    
    print("\n" + "🎨" * 35)
    print("   ARTIST DATABASE EXPANDER")
    print("   Build Your Comprehensive Art Database")
    print("🎨" * 35 + "\n")

    while True:
        print("\n" + "=" * 70)
        print("OPTIONS:")
        print("=" * 70)
        print("1. Add all artists (18th-21st century) - RECOMMENDED")
        print("2. Add 18th century artists")
        print("3. Add 19th century artists")
        print("4. Add 20th century artists")
        print("5. Add 21st century artists")
        print("6. Add Renaissance masters")
        print("7. Add Baroque masters")
        print("8. Add Dutch Golden Age artists")
        print("9. Add Northern Renaissance artists")
        print("10. Add all art movements")
        print("11. Add all themes")
        print("12. Add everything (FULL DATABASE)")
        print("13. Show statistics")
        print("14. Save and exit")
        print("=" * 70)

        choice = input("\n👉 Your choice (or 'quit'): ").strip()

        if choice == 'quit' or choice == '14':
            expander.save_database()
            expander.show_statistics()
            print("\n👋 Database saved! Ready for posting.\n")
            break

        elif choice == '1':
            expander.add_artists_18th_century()
            expander.add_artists_19th_century()
            expander.add_artists_20th_century()
            expander.add_artists_21st_century()

        elif choice == '2':
            expander.add_artists_18th_century()

        elif choice == '3':
            expander.add_artists_19th_century()

        elif choice == '4':
            expander.add_artists_20th_century()

        elif choice == '5':
            expander.add_artists_21st_century()

        elif choice == '6':
            expander.add_renaissance_masters()

        elif choice == '7':
            expander.add_baroque_masters()

        elif choice == '8':
            expander.add_dutch_golden_age()

        elif choice == '9':
            expander.add_northern_renaissance()

        elif choice == '10':
            expander.add_movements()

        elif choice == '11':
            expander.add_themes()

        elif choice == '12':
            print("\n🚀 Adding FULL database...")
            expander.add_renaissance_masters()
            expander.add_northern_renaissance()
            expander.add_baroque_masters()
            expander.add_dutch_golden_age()
            expander.add_artists_18th_century()
            expander.add_artists_19th_century()
            expander.add_artists_20th_century()
            expander.add_artists_21st_century()
            expander.add_movements()
            expander.add_themes()
            print("\n✅ Full database added!")

        elif choice == '13':
            expander.show_statistics()

        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    interactive_menu()

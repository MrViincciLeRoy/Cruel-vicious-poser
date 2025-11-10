#!/usr/bin/env python3
"""
Automated daily art post generator and poster
Generates one post per day and posts it to Facebook
"""

import requests
import json
import os
import sys
import time
import random
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MetMuseumAPI:
    """Interact with The Metropolitan Museum of Art API"""

    def __init__(self):
        self.base_url = "https://collectionapi.metmuseum.org/public/collection/v1"
        # FIX: Look for both possible filenames
        self.config_path = None
        for filename in ["config/artists_database.json", "config/artist_database.json"]:
            if Path(filename).exists():
                self.config_path = Path(filename)
                break
        
        self.search_queries = self._load_search_database()

    def _load_search_database(self) -> List[str]:
        """Load artist and movement database"""
        try:
            if self.config_path and self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    queries = []
                    queries.extend(data.get('search_queries', []))
                    queries.extend(data.get('movements', []))
                    queries.extend(data.get('themes', []))
                    print(f"✅ Loaded {len(queries)} search terms from {self.config_path}")
                    return queries
            else:
                print(f"⚠️ Config file not found, using defaults")
                return self._get_default_queries()
        except Exception as e:
            print(f"⚠️ Error loading config: {e}")
            return self._get_default_queries()

    def _get_default_queries(self) -> List[str]:
        """Fallback search queries"""
        return [
            "Rembrandt", "Leonardo da Vinci", "Michelangelo", "Picasso",
            "Van Gogh", "Monet", "Vermeer", "Caravaggio", "Titian",
            "Renaissance painting", "Impressionism painting", "Baroque painting"
        ]

    def search_artworks(self, query: str, limit: int = 20) -> List[int]:
        """Search for artworks"""
        try:
            url = f"{self.base_url}/search"
            params = {
                'q': query,
                'hasImages': 'true',
                'departmentId': 11  # European Paintings
            }

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            object_ids = data.get('objectIDs', [])
            return object_ids[:limit] if object_ids else []

        except Exception as e:
            print(f"❌ Search error: {e}")
            return []

    def get_artwork_details(self, object_id: int) -> Optional[Dict]:
        """Get detailed artwork information"""
        try:
            url = f"{self.base_url}/objects/{object_id}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()

            if not data.get('primaryImage'):
                return None

            return {
                'object_id': object_id,
                'title': data.get('title', 'Untitled'),
                'artist': data.get('artistDisplayName', 'Unknown Artist'),
                'date': data.get('objectDate', 'Date unknown'),
                'medium': data.get('medium', 'Medium unknown'),
                'culture': data.get('culture', ''),
                'period': data.get('period', ''),
                'image_url': data.get('primaryImage', ''),
                'museum_url': data.get('objectURL', ''),
                'department': data.get('department', ''),
                'dimensions': data.get('dimensions', ''),
                'classification': data.get('classification', '')
            }

        except Exception as e:
            print(f"❌ Error fetching artwork {object_id}: {e}")
            return None


class PostTracker:
    """Track used artworks and posting history"""

    def __init__(self):
        self.used_file = Path("used_artworks.json")
        self.log_file = Path("posted_log.json")
        self.queue_file = Path("generated_posts.json")
        
        self.used_artworks = self._load_used()
        self.posting_log = self._load_log()

    def _load_used(self) -> set:
        """Load used artwork IDs"""
        if self.used_file.exists():
            try:
                with open(self.used_file, 'r') as f:
                    return set(json.load(f))
            except:
                return set()
        return set()

    def _load_log(self) -> List[Dict]:
        """Load posting log"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def is_used(self, object_id: int) -> bool:
        """Check if artwork was already used"""
        return str(object_id) in self.used_artworks

    def mark_used(self, object_id: int):
        """Mark artwork as used"""
        self.used_artworks.add(str(object_id))
        self._save_used()

    def _save_used(self):
        """Save used artworks"""
        with open(self.used_file, 'w') as f:
            json.dump(list(self.used_artworks), f, indent=2)

    def log_post(self, post_data: Dict):
        """Log successful post"""
        self.posting_log.append({
            'timestamp': datetime.now().isoformat(),
            'post_id': post_data.get('id', 'unknown'),
            'object_id': post_data.get('object_id'),
            'title': post_data.get('title', 'Unknown'),
            'artist': post_data.get('artist', 'Unknown')
        })
        self._save_log()

    def _save_log(self):
        """Save posting log"""
        with open(self.log_file, 'w') as f:
            json.dump(self.posting_log, f, indent=2)

    def get_post_queue(self) -> List[Dict]:
        """Get posts from queue"""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_post_queue(self, posts: List[Dict]):
        """Save posts to queue"""
        with open(self.queue_file, 'w') as f:
            json.dump(posts, f, indent=2)


class SimplePostGenerator:
    """Generate simple engaging posts without LLM"""

    def __init__(self):
        self.post_templates = [
            'daily_artwork',
            'artist_spotlight',
            'technique_focus',
            'period_context'
        ]

    def generate_post(self, artwork: Dict, post_type: str = None) -> Dict:
        """Generate a post for the artwork"""
        if post_type is None:
            post_type = random.choice(self.post_templates)

        if post_type == 'artist_spotlight':
            return self._artist_spotlight(artwork)
        elif post_type == 'technique_focus':
            return self._technique_focus(artwork)
        elif post_type == 'period_context':
            return self._period_context(artwork)
        else:
            return self._daily_artwork(artwork)

    def _daily_artwork(self, artwork: Dict) -> Dict:
        """Create daily artwork post"""
        post = f"🎨 𝗔𝗿𝘁𝘄𝗼𝗿𝗸 𝗼𝗳 𝘁𝗵𝗲 𝗗𝗮𝘆\n\n"
        post += f'"{artwork["title"]}"\n'
        post += f"by {artwork['artist']}\n"
        post += f"({artwork['date']})\n\n"
        
        post += f"✨ {self._get_appreciation_line(artwork)}\n\n"
        post += f"🏛️ The Metropolitan Museum of Art\n\n"
        
        post += f"{self._get_engagement_question(artwork)}\n\n"
        
        post += "#ArtHistory #Painting #FineArt #ClassicalArt #Museum "
        post += "#ArtLovers #ArtAppreciation #DailyArt #MetMuseum"

        return {
            'post_text': post,
            'image_url': artwork['image_url'],
            'link_url': artwork['museum_url'],
            'type': 'daily_artwork',
            'artwork_details': artwork
        }

    def _artist_spotlight(self, artwork: Dict) -> Dict:
        """Create artist spotlight post"""
        post = f"👨‍🎨 𝗔𝗿𝘁𝗶𝘀𝘁 𝗦𝗽𝗼𝘁𝗹𝗶𝗴𝗵𝘁: {artwork['artist']}\n\n"
        
        post += f"A master of {artwork.get('period', 'their era')}, "
        post += f"{artwork['artist']} created works that continue to captivate audiences centuries later.\n\n"
        
        post += f'Featured work: "{artwork["title"]}" ({artwork["date"]})\n\n'
        post += f"🏛️ Collection: The Metropolitan Museum of Art\n\n"
        post += f"What draws you to this artist's work? Share your thoughts! 💭\n\n"
        
        artist_tag = artwork['artist'].replace(' ', '').replace('.', '')
        post += f"#ArtHistory #{artist_tag} #ArtistSpotlight #FineArt #Painting"

        return {
            'post_text': post,
            'image_url': artwork['image_url'],
            'link_url': artwork['museum_url'],
            'type': 'artist_spotlight',
            'artwork_details': artwork
        }

    def _technique_focus(self, artwork: Dict) -> Dict:
        """Focus on artistic technique"""
        post = f"🖌️ 𝗧𝗲𝗰𝗵𝗻𝗶𝗾𝘂𝗲 𝗦𝗽𝗼𝘁𝗹𝗶𝗴𝗵𝘁\n\n"
        post += f'"{artwork["title"]}"\n'
        post += f"by {artwork['artist']} ({artwork['date']})\n\n"
        
        post += f"Medium: {artwork['medium']}\n\n"
        post += f"Notice the mastery in technique and composition. "
        post += f"Each brushstroke contributes to the overall impact of the piece.\n\n"
        
        post += f"🏛️ The Metropolitan Museum of Art\n\n"
        post += "What technical aspects catch your eye? 🔍\n\n"
        
        post += "#ArtTechnique #Painting #FineArt #ArtHistory #Museum"

        return {
            'post_text': post,
            'image_url': artwork['image_url'],
            'link_url': artwork['museum_url'],
            'type': 'technique_focus',
            'artwork_details': artwork
        }

    def _period_context(self, artwork: Dict) -> Dict:
        """Provide historical context"""
        period = artwork.get('period', artwork.get('culture', 'this period'))
        
        post = f"📖 𝗔𝗿𝘁 𝗛𝗶𝘀𝘁𝗼𝗿𝘆 𝗖𝗼𝗻𝘁𝗲𝘅𝘁\n\n"
        if period:
            post += f"Focus: {period}\n\n"
        
        post += f'"{artwork["title"]}"\n'
        post += f"by {artwork['artist']} ({artwork['date']})\n\n"
        
        post += f"This work exemplifies the artistic ideals and techniques of its time. "
        post += f"Understanding the historical context enriches our appreciation of the artwork.\n\n"
        
        post += f"🏛️ The Metropolitan Museum of Art\n\n"
        post += "What elements of the period do you notice? 🎨\n\n"
        
        period_tag = period.replace(' ', '') if period else 'ArtMovement'
        post += f"#ArtHistory #{period_tag} #FineArt #Museum #Painting"

        return {
            'post_text': post,
            'image_url': artwork['image_url'],
            'link_url': artwork['museum_url'],
            'type': 'period_context',
            'artwork_details': artwork
        }

    def _get_appreciation_line(self, artwork: Dict) -> str:
        """Generate an appreciation line"""
        lines = [
            "A masterpiece that continues to inspire art lovers worldwide.",
            "The skillful composition and technique make this a timeless work.",
            "Notice the masterful use of light, color, and form in this piece.",
            "A stunning example of artistic excellence from this period.",
            "The attention to detail and artistic vision are truly remarkable."
        ]
        return random.choice(lines)

    def _get_engagement_question(self, artwork: Dict) -> str:
        """Generate an engagement question"""
        questions = [
            "What emotions does this artwork evoke for you?",
            "What details do you notice first in this painting?",
            "How would you describe this work to someone who can't see it?",
            "What story do you think this painting tells?",
            "Which element of this artwork speaks to you most?"
        ]
        return random.choice(questions)


class FacebookPoster:
    """Post content to Facebook Page"""

    def __init__(self):
        # FIX: Use only FB_PAGE_ACCESS_TOKEN - simpler approach
        self.access_token = os.getenv('FB_PAGE_ACCESS_TOKEN')
        self.page_id = os.getenv('FB_PAGE_ID')
        self.graph_api_url = "https://graph.facebook.com/v21.0"

        if not self.access_token:
            raise ValueError("❌ Missing FB_PAGE_ACCESS_TOKEN environment variable!")
        
        if not self.page_id:
            raise ValueError("❌ Missing FB_PAGE_ID environment variable!")
        
        print(f"✅ Facebook credentials loaded")
        print(f"   Page ID: {self.page_id}")
        print(f"   Token: {self.access_token[:20]}...")

    def post_photo(self, image_url: str, caption: str) -> Dict:
        """Post photo to Facebook"""
        endpoint = f"{self.graph_api_url}/{self.page_id}/photos"
        
        payload = {
            'url': image_url,
            'message': caption,
            'published': True,
            'access_token': self.access_token
        }

        try:
            print(f"📤 Posting to: {endpoint}")
            response = requests.post(endpoint, data=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error posting: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise


def main():
    """Main execution"""
    print("\n" + "🤖" * 35)
    print(f"   AUTOMATED DAILY ART POST")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🤖" * 35 + "\n")

    try:
        # Initialize components
        tracker = PostTracker()
        met = MetMuseumAPI()
        generator = SimplePostGenerator()
        poster = FacebookPoster()

        # Check if we have queued posts
        queue = tracker.get_post_queue()
        
        # Filter out already used posts
        queue = [p for p in queue if not tracker.is_used(p['artwork_details']['object_id'])]
        
        # If queue is low, generate more posts
        if len(queue) < 7:
            print("📝 Queue is low, generating more posts...\n")
            
            new_posts = []
            attempts = 0
            max_attempts = 50
            
            while len(new_posts) < 14 and attempts < max_attempts:
                query = random.choice(met.search_queries)
                print(f"🔍 Searching: {query}")
                
                object_ids = met.search_artworks(query, limit=20)
                
                for obj_id in object_ids:
                    if tracker.is_used(obj_id):
                        continue
                    
                    artwork = met.get_artwork_details(obj_id)
                    
                    if not artwork or artwork['artist'] == 'Unknown Artist':
                        continue
                    
                    post = generator.generate_post(artwork)
                    new_posts.append(post)
                    print(f"✅ Generated post for: {artwork['title'][:50]}")
                    
                    if len(new_posts) >= 14:
                        break
                    
                    time.sleep(1)
                
                attempts += 1
            
            queue.extend(new_posts)
            tracker.save_post_queue(queue)
            print(f"\n✅ Queue now has {len(queue)} posts\n")

        # Post today's artwork
        if not queue:
            print("❌ No posts available in queue!")
            sys.exit(1)

        today_post = queue[0]
        artwork = today_post['artwork_details']

        print("=" * 70)
        print(f"📤 POSTING TODAY'S ARTWORK")
        print("=" * 70)
        print(f"Title: {artwork['title']}")
        print(f"Artist: {artwork['artist']}")
        print(f"Date: {artwork['date']}")
        print()

        # Post to Facebook
        print("⏳ Posting to Facebook...")
        response = poster.post_photo(
            image_url=today_post['image_url'],
            caption=today_post['post_text']
        )

        post_id = response.get('id', 'unknown')
        print(f"✅ Successfully posted!")
        print(f"📍 Post ID: {post_id}")
        print(f"🔗 URL: https://facebook.com/{post_id}")

        # Update tracking
        tracker.mark_used(artwork['object_id'])
        tracker.log_post({
            'id': post_id,
            'object_id': artwork['object_id'],
            'title': artwork['title'],
            'artist': artwork['artist']
        })

        # Remove posted item from queue
        queue.pop(0)
        tracker.save_post_queue(queue)

        print(f"\n📊 Queue remaining: {len(queue)} posts")
        print("\n" + "✨" * 35)
        print("🎉 DAILY POST COMPLETE!")
        print("✨" * 35 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
NUMERIC_WEIGHTS = {"energy": 2.0, "valence": 1.5, "acousticness": 0.5}
MAX_SCORE = GENRE_WEIGHT + MOOD_WEIGHT + sum(NUMERIC_WEIGHTS.values())

# Diversity penalty: subtracted once for each earlier pick by the same artist or in the same genre
ARTIST_PENALTY = 1.0
GENRE_PENALTY = 0.5

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None
    target_acousticness: Optional[float] = None

    def to_prefs(self) -> Dict:
        """Convert the profile to the preference dict that score_song expects."""
        acousticness = self.target_acousticness
        if acousticness is None:
            acousticness = 0.8 if self.likes_acoustic else 0.2
        prefs = {
            "genre": self.favorite_genre,
            "mood": self.favorite_mood,
            "energy": self.target_energy,
            "acousticness": acousticness,
        }
        if self.target_valence is not None:
            prefs["valence"] = self.target_valence
        return prefs

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the k best-matching Song objects for a user, best first."""
        results = recommend_songs(user.to_prefs(), [asdict(song) for song in self.songs], k)
        by_id = {song.id: song for song in self.songs}
        return [by_id[song["id"]] for song, _, _ in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain a song's score for a user as a short sentence of reasons."""
        score, reasons = score_song(user.to_prefs(), asdict(song))
        return f"{song.title} scored {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file into dicts, converting id to int and numeric features to float."""
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against a taste profile, returning (score, list of reasons)."""
    score = 0.0
    reasons: List[str] = []

    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT:.1f})")

    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT:.1f})")

    for feature, weight in NUMERIC_WEIGHTS.items():
        if feature not in user_prefs:
            continue
        closeness = 1 - abs(song[feature] - user_prefs[feature])
        points = weight * closeness
        score += points
        reasons.append(
            f"{feature} {song[feature]:.2f} vs target {user_prefs[feature]:.2f} (+{points:.2f})"
        )

    return score, reasons

def validate_prefs(user_prefs: Dict) -> None:
    """Raise ValueError if any numeric target is outside the 0 to 1 scale."""
    for feature in NUMERIC_WEIGHTS:
        if feature in user_prefs and not 0.0 <= user_prefs[feature] <= 1.0:
            raise ValueError(f"{feature} target must be between 0 and 1, got {user_prefs[feature]}")

def diversity_penalty(song: Dict, chosen: List[Dict]) -> Tuple[float, List[str]]:
    """Return the points to subtract from a song that repeats an artist or genre already chosen."""
    penalty = 0.0
    reasons: List[str] = []

    same_artist = sum(1 for picked in chosen if picked["artist"] == song["artist"])
    if same_artist:
        points = ARTIST_PENALTY * same_artist
        penalty += points
        reasons.append(f"artist already picked {same_artist}x (-{points:.1f})")

    same_genre = sum(1 for picked in chosen if picked["genre"] == song["genre"])
    if same_genre:
        points = GENRE_PENALTY * same_genre
        penalty += points
        reasons.append(f"genre already picked {same_genre}x (-{points:.1f})")

    return penalty, reasons

def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5, diversity: bool = True
) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs as (song, score, explanation), best first, penalizing repeat artists and genres."""
    validate_prefs(user_prefs)

    candidates = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        candidates.append((song, score, reasons))

    if not diversity:
        ranked = sorted(candidates, key=lambda item: item[1], reverse=True)
        return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]

    # Greedy re-ranking: pick the best remaining song one at a time, charging each
    # candidate for artists and genres that are already in the list.
    chosen: List[Tuple[Dict, float, str]] = []
    remaining = candidates
    while remaining and len(chosen) < k:
        picked_songs = [item[0] for item in chosen]
        best = None
        for song, score, reasons in remaining:
            penalty, penalty_reasons = diversity_penalty(song, picked_songs)
            adjusted = score - penalty
            if best is None or adjusted > best[1]:
                best = (song, adjusted, reasons + penalty_reasons)
        chosen.append((best[0], best[1], "; ".join(best[2])))
        remaining = [item for item in remaining if item[0] is not best[0]]
    return chosen

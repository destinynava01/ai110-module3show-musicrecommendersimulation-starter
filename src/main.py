"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

PROFILES = {
    "Pop / Happy (default)": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "valence": 0.80,
        "acousticness": 0.20,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.40,
        "valence": 0.58,
        "acousticness": 0.75,
    },
    "Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "valence": 0.48,
        "acousticness": 0.10,
    },
}

WIDTH = 64


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    print("=" * WIDTH)
    print(f"User profile: {name}")
    print("  " + ", ".join(f"{key}={value}" for key, value in user_prefs.items()))
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / 7.00   [{song['genre']}, {song['mood']}]")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


if __name__ == "__main__":
    main()

import pytest

from src.recommender import Song, UserProfile, Recommender, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def make_song_dicts() -> list:
    def song(title, artist, genre, energy):
        return {
            "title": title, "artist": artist, "genre": genre, "mood": "chill",
            "energy": energy, "valence": 0.5, "acousticness": 0.5,
        }

    return [
        song("A1", "Same Artist", "lofi", 0.40),
        song("A2", "Same Artist", "lofi", 0.41),
        song("B1", "Other Artist", "lofi", 0.45),
    ]


def test_diversity_penalty_pushes_repeat_artist_down():
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.4, "valence": 0.5, "acousticness": 0.5}
    songs = make_song_dicts()

    plain = recommend_songs(prefs, songs, k=3, diversity=False)
    diverse = recommend_songs(prefs, songs, k=3)

    assert [s["title"] for s, _, _ in plain] == ["A1", "A2", "B1"]
    assert [s["title"] for s, _, _ in diverse] == ["A1", "B1", "A2"]
    assert "artist already picked" in diverse[2][2]


def test_diversity_penalty_leaves_first_pick_unchanged():
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.4, "valence": 0.5, "acousticness": 0.5}
    songs = make_song_dicts()

    plain = recommend_songs(prefs, songs, k=1, diversity=False)
    diverse = recommend_songs(prefs, songs, k=1)

    assert plain[0][0] is diverse[0][0]
    assert plain[0][1] == diverse[0][1]


def test_out_of_range_target_is_rejected():
    prefs = {"genre": "lofi", "mood": "chill", "energy": 3.0}
    with pytest.raises(ValueError):
        recommend_songs(prefs, make_song_dicts(), k=3)


def test_recommender_class_uses_scoring_and_returns_songs():
    rec = make_small_recommender()
    user = UserProfile("lofi", "chill", 0.4, likes_acoustic=True)

    results = rec.recommend(user, k=2)

    assert [song.title for song in results] == ["Chill Lofi Loop", "Test Pop Track"]
    assert "genre match" in rec.explain_recommendation(user, results[0])


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""

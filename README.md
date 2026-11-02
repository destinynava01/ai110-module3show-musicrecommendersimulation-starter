# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders such as Spotify or YouTube combine two kinds of signals. Collaborative filtering learns from what millions of other listeners play, skip, and save, while content-based filtering compares the attributes of the songs themselves to what a listener already likes. My version is a small content-based recommender: it has no listening history or other users, so it can only compare a song's attributes to a stated taste profile. It prioritizes the "vibe" of a song over its label. Energy and valence (how positive a song sounds) carry the most weight, followed by an exact mood match. Genre is only a small bonus, because a listener's mood usually says more about what they want right now than a genre tag does.

### Song features

Each `Song` has these attributes from `data/songs.csv`:

- `genre` and `mood` (categorical, scored as a match or no match)
- `energy`, `valence`, and `acousticness` (0-1, scored by closeness to the user's target)
- `tempo_bpm` and `danceability` (stored, but not used in scoring at first, since they largely overlap with energy)
- `id`, `title`, and `artist` (identification only)

### UserProfile features

Each `UserProfile` stores the user's taste targets:

- `favorite_genre` (string)
- `favorite_mood` (string)
- `target_energy` (0-1)
- `target_valence` (0-1)
- `target_acousticness` (0-1), which replaces the starter's `likes_acoustic` boolean so acoustic taste can be compared on the same scale as the song data

### Algorithm Recipe

#### Scoring rule (one song)

Numeric features score `1 - |song_value - target|`, so a song closer to the target scores higher and being "higher" or "lower" doesn't matter. Categorical features score 1 for an exact match and 0 otherwise. The final score is a weighted sum:

| Feature | Rule | Weight |
|---|---|---|
| genre | exact match | 2.0 |
| mood | exact match | 1.0 |
| energy | closeness | 2.0 |
| valence | closeness | 1.5 |
| acousticness | closeness | 0.5 |

The maximum score is 7.0. I tested genre 2.0 / mood 1.0 against the reverse (mood 2.0 / genre 1.0) on a "chill lofi" and an "intense rock" profile. Genre-heavy weights ranked Focus Flow (lofi) above Spacewalk Thoughts (ambient) for the lofi listener and pushed Gym Hero (pop) further down for the rock listener, which both matched my sense of the vibe better. Mood is the more fragile signal because labels like "intense" and "angry" are near-synonyms that an exact match treats as unrelated.

#### Ranking rule (the whole catalog)

The `Recommender` applies the scoring rule to every song, sorts the songs by score from highest to lowest, and returns the top `k`.

### Expected biases

- **Genre may be over-prioritized.** A genre match is worth 2.0 points, the most of any single feature besides energy. A song in the "wrong" genre that matches the user's mood and energy exactly can still lose to a same-genre song that is a worse fit. For example, Iron Tide (metal, angry, energy 0.97) ranks only fifth for an intense rock listener, behind a pop song, because "metal" does not equal "rock".
- **Exact-match labels are brittle.** Mood and genre score 1 or 0, so near-synonyms (intense/angry, chill/relaxed/focused) get no partial credit.
- **The catalog skews toward lofi.** Lofi has three of the 18 songs and most other genres have one, so lofi listeners get more good matches than anyone else.
- **One profile means one taste.** A listener who likes both gym rock and study lofi can only be represented by a single set of targets, and averaging them would favor mid-energy songs that neither mood wants.
- **The features reflect my assumptions about "vibe".** I chose energy and valence as the core features, and I left out lyrics, language, artist familiarity, and listening context. Listeners whose taste depends on those will be served worse.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` on the 18-song catalog, for three profiles:

```
Loaded songs: 18

================================================================
User profile: Pop / Happy (default)
  genre=pop, mood=happy, energy=0.8, valence=0.8, acousticness=0.2
================================================================

1. Sunrise City by Neon Echo
   Score: 6.89 / 7.00   [pop, happy]
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.82 vs target 0.80 (+1.96)
     - valence 0.84 vs target 0.80 (+1.44)
     - acousticness 0.18 vs target 0.20 (+0.49)

2. Gym Hero by Max Pulse
   Score: 5.62 / 7.00   [pop, intense]
     - genre match (+2.0)
     - energy 0.93 vs target 0.80 (+1.74)
     - valence 0.77 vs target 0.80 (+1.46)
     - acousticness 0.05 vs target 0.20 (+0.42)

3. Rooftop Lights by Indigo Parade
   Score: 4.83 / 7.00   [indie pop, happy]
     - mood match (+1.0)
     - energy 0.76 vs target 0.80 (+1.92)
     - valence 0.81 vs target 0.80 (+1.48)
     - acousticness 0.35 vs target 0.20 (+0.43)

4. Concrete Crown by Verse Mason
   Score: 3.65 / 7.00   [hip hop, confident]
     - energy 0.78 vs target 0.80 (+1.96)
     - valence 0.62 vs target 0.80 (+1.23)
     - acousticness 0.12 vs target 0.20 (+0.46)

5. Laser Garden by Pixel Bloom
   Score: 3.50 / 7.00   [edm, euphoric]
     - energy 0.95 vs target 0.80 (+1.70)
     - valence 0.88 vs target 0.80 (+1.38)
     - acousticness 0.03 vs target 0.20 (+0.41)

================================================================
User profile: Chill Lofi
  genre=lofi, mood=chill, energy=0.4, valence=0.58, acousticness=0.75
================================================================

1. Midnight Coding by LoRoom
   Score: 6.91 / 7.00   [lofi, chill]
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.42 vs target 0.40 (+1.96)
     - valence 0.56 vs target 0.58 (+1.47)
     - acousticness 0.71 vs target 0.75 (+0.48)

2. Library Rain by Paper Lanterns
   Score: 6.82 / 7.00   [lofi, chill]
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.35 vs target 0.40 (+1.90)
     - valence 0.60 vs target 0.58 (+1.47)
     - acousticness 0.86 vs target 0.75 (+0.45)

3. Focus Flow by LoRoom
   Score: 5.97 / 7.00   [lofi, focused]
     - genre match (+2.0)
     - energy 0.40 vs target 0.40 (+2.00)
     - valence 0.59 vs target 0.58 (+1.48)
     - acousticness 0.78 vs target 0.75 (+0.48)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 4.57 / 7.00   [ambient, chill]
     - mood match (+1.0)
     - energy 0.28 vs target 0.40 (+1.76)
     - valence 0.65 vs target 0.58 (+1.40)
     - acousticness 0.92 vs target 0.75 (+0.41)

5. Coffee Shop Stories by Slow Stereo
   Score: 3.68 / 7.00   [jazz, relaxed]
     - energy 0.37 vs target 0.40 (+1.94)
     - valence 0.71 vs target 0.58 (+1.30)
     - acousticness 0.89 vs target 0.75 (+0.43)

================================================================
User profile: Intense Rock
  genre=rock, mood=intense, energy=0.92, valence=0.48, acousticness=0.1
================================================================

1. Storm Runner by Voltline
   Score: 6.98 / 7.00   [rock, intense]
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.91 vs target 0.92 (+1.98)
     - valence 0.48 vs target 0.48 (+1.50)
     - acousticness 0.10 vs target 0.10 (+0.50)

2. Gym Hero by Max Pulse
   Score: 4.52 / 7.00   [pop, intense]
     - mood match (+1.0)
     - energy 0.93 vs target 0.92 (+1.98)
     - valence 0.77 vs target 0.48 (+1.06)
     - acousticness 0.05 vs target 0.10 (+0.47)

3. Night Drive Loop by Neon Echo
   Score: 3.58 / 7.00   [synthwave, moody]
     - energy 0.75 vs target 0.92 (+1.66)
     - valence 0.49 vs target 0.48 (+1.48)
     - acousticness 0.22 vs target 0.10 (+0.44)

4. Concrete Crown by Verse Mason
   Score: 3.50 / 7.00   [hip hop, confident]
     - energy 0.78 vs target 0.92 (+1.72)
     - valence 0.62 vs target 0.48 (+1.29)
     - acousticness 0.12 vs target 0.10 (+0.49)

5. Iron Tide by Black Anvil
   Score: 3.48 / 7.00   [metal, angry]
     - energy 0.97 vs target 0.92 (+1.90)
     - valence 0.22 vs target 0.48 (+1.11)
     - acousticness 0.04 vs target 0.10 (+0.47)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this




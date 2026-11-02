# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version, VibeMatch 1.0, is a small content-based music recommender that runs in the terminal. It loads an 18-song catalog from `data/songs.csv` and compares each song to a listener's taste profile: a favorite genre, a favorite mood, and target levels for energy, valence, and acousticness. Each song gets a score out of 7, with a written reason for every point. The five highest-scoring songs are printed in order. I tested it on seven profiles, including four adversarial ones, ran one weight experiment, and documented the results and biases in the model card.

---

## How The System Works

Real-world recommenders such as Spotify or YouTube combine two kinds of signals. Collaborative filtering learns from what millions of other listeners play, skip, and save, while content-based filtering compares the attributes of the songs themselves to what a listener already likes. My version is a small content-based recommender: it has no listening history or other users, so it can only compare a song's attributes to a stated taste profile. It tries to capture the "vibe" of a song with numbers. Energy and genre carry the most weight (2.0 points each), followed by valence (how positive a song sounds, up to 1.5 points), an exact mood match (1.0), and acoustic feel (up to 0.5). I first weighted mood above genre, but testing on a lofi and a rock listener gave better lists with genre weighted higher, so I switched.

### Song features

Each `Song` has these attributes from `data/songs.csv`:

- `genre` and `mood` (categorical, scored as a match or no match)
- `energy`, `valence`, and `acousticness` (0-1, scored by closeness to the user's target)
- `tempo_bpm` and `danceability` (stored, but not used in scoring at first, since they largely overlap with energy)
- `id`, `title`, and `artist` (identification only)

### UserProfile features

A listener's taste profile is a dictionary (see `PROFILES` in `src/main.py`) with these keys:

- `genre` (string)
- `mood` (string)
- `energy` (0-1 target)
- `valence` (0-1 target)
- `acousticness` (0-1 target), a number instead of the starter's `likes_acoustic` yes/no, so acoustic taste can be compared on the same scale as the song data

The starter's `UserProfile` dataclass in `src/recommender.py` is left as it was, because the starter tests use it. The simulation itself runs on the dictionaries above.

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

`recommend_songs` applies the scoring rule to every song, sorts the songs by score from highest to lowest, and returns the top `k`.

### Expected biases

- **Genre may be over-prioritized.** A genre match is worth 2.0 points, tied with energy for the largest weight. A song in the "wrong" genre that matches the user's mood and energy closely can still lose to a same-genre song that is a worse fit. For example, Iron Tide (metal, angry, energy 0.97) ranks only fifth for an intense rock listener, because "metal" does not equal "rock".
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
   ```

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

### Weight shift: double energy, halve genre

I changed `GENRE_WEIGHT` from 2.0 to 1.0 and the energy weight from 2.0 to 4.0, then compared the top 5 for each profile against the baseline. The maximum score rose from 7.0 to 8.0, and `MAX_SCORE` is now computed from the weights so the printed "/ max" stays correct. Every song's score is still a sum of non-negative terms, so the math stays valid for inputs inside the 0 to 1 range. I reverted to the baseline weights afterwards.

| Profile | Baseline top 3 | Energy x2, genre /2 top 3 |
|---|---|---|
| Pop / Happy | Sunrise City, Gym Hero, Rooftop Lights | Sunrise City, Rooftop Lights, Gym Hero |
| Chill Lofi | Midnight Coding, Library Rain, Focus Flow | unchanged |
| Intense Rock | Storm Runner, Gym Hero, Night Drive Loop | Storm Runner, Gym Hero, Iron Tide |
| Sad but Energetic | Cold Harbor Blues, Iron Tide, Storm Runner | Iron Tide, Storm Runner, Cold Harbor Blues |
| Split Taste | Storm Runner, Midnight Coding, Library Rain | Midnight Coding, Storm Runner, Library Rain |

**More accurate or just different?** Mostly more accurate, with a cost.

- **Better:** the happy listener now gets Rooftop Lights (happy) before Gym Hero (intense). The rock listener's Iron Tide jumps from fifth to third. For the sad-but-energetic listener, Iron Tide (loud and dark) now beats Cold Harbor Blues (quiet), because a genre match no longer outweighs a big energy gap.
- **Worse or just different:** with energy dominating, songs that are merely close on energy start to crowd in regardless of label. Night Drive Loop (synthwave, moody) enters the Pop / Happy top 5. In the Split Taste case the swap between Midnight Coding and Storm Runner is close to a coin flip, since both are about 0.25 away from the energy target.
- **Fragile:** in Sad but Energetic the top three scores are 5.66, 5.54 and 5.51. A tiny weight change can reorder them.
- **Lofi unchanged:** the lofi listener's list didn't move, because those songs already match on every feature.

### Diversity penalty (Challenge 3)

`recommend_songs` now re-ranks greedily. It picks the best song, then charges every remaining song **1.0 point for each earlier pick by the same artist** and **0.5 points for each earlier pick in the same genre** before choosing the next one. The penalty shows up as a reason line (for example `artist already picked 1x (-1.0)`). Pass `diversity=False` to get the plain ranking. I chose 1.0 and 0.5 after trying 1.0 and 1.0 as well. The stronger genre penalty pushed Focus Flow out of the lofi listener's top five completely, which is too much for a listener who really does want lofi.

| Profile | Plain top 5 | With diversity penalty |
|---|---|---|
| Chill Lofi | Midnight Coding, Library Rain, Focus Flow, Spacewalk Thoughts, Coffee Shop Stories | Midnight Coding, Library Rain, **Spacewalk Thoughts, Focus Flow**, Coffee Shop Stories |
| Split Taste | Storm Runner, Midnight Coding, Library Rain, Spacewalk Thoughts, Velvet Hours | Storm Runner, Midnight Coding, **Spacewalk Thoughts, Velvet Hours, Library Rain** |
| Genre Not In Catalog | Laser Garden, Sunrise City, Gym Hero, Rooftop Lights, Concrete Crown | Laser Garden, Sunrise City, **Rooftop Lights, Concrete Crown, Storm Runner** |
| Pop / Happy, Intense Rock, Sad but Energetic | | same songs in the same order (Gym Hero's score drops from 5.62 to 5.12 for Pop / Happy) |

**What it fixed and what it didn't.** It breaks up the lofi listener's block of three lofi songs, so an ambient song now comes third, and it stops LoRoom's two songs from sitting side by side. It does not fix the one-song-genre problem, because a single song can't repeat. It also costs a little accuracy: Library Rain drops from third to fifth for the Split Taste listener only because of its genre. The diversity penalty only works inside one list, so the same middle-of-the-road songs (like Concrete Crown) still show up for many different listeners.

The sample outputs below and in the model card were captured **before** this penalty was added, so they match `diversity=False`. Running `python -m src.main` now gives the diversity-adjusted lists above.

Other experiments still to try: removing the mood check, adding tempo or danceability to the score, and partial credit for similar moods and genres. (Rejecting out-of-range targets was added afterwards. See the model card.)

---

## Limitations and Risks

- **Tiny catalog.** There are only 18 songs, and 12 of the 15 genres have a single song. A listener of one of those genres almost automatically gets that song first, and the same middle-of-the-road songs fill the lower spots for everyone.
- **Exact-match labels.** Genre and mood score 1 or 0, so "angry" and "intense" or "rock" and "metal" count as unrelated. Iron Tide, a loud metal song, only ranks fifth for an intense rock listener.
- **Labels can beat the sound.** Genre is worth 2.0 points, so a quiet blues song beat loud, dark songs for a listener who asked for high energy and low positivity.
- **One taste per profile.** A listener who likes both gym rock and study lofi can only be described by a single set of targets.
- **Input checks are minimal.** Numeric targets outside 0 to 1 are now rejected with an error (they used to give negative scores). Other bad input, like a misspelled genre, is still accepted and just earns no genre points.
- **Limited features.** It does not understand lyrics, language, artist, or listening context, and the song numbers are made up, not measured.

The full discussion is in [`model_card.md`](model_card.md).

---

## Reflection

The full model card is here: [**Model Card**](model_card.md)

**How recommenders turn data into predictions.** A recommender like this one turns taste into numbers, then ranks songs by how close they are to those numbers. A few weighted rules and a sort were enough to give lists that felt like real recommendations, and the "because" lines made them feel even smarter than they are. The system never understands the music. It only adds up points. Small weight changes also moved real songs up and down, so the weights are really design choices.

**Where bias or unfairness could show up.** Bias came from the choices I made, not from any bad intent. Giving genre a big weight, using exact-match labels, and keeping a tiny catalog meant some listeners got better results than others. Listeners of rare genres were locked to one song, and listeners with mixed tastes could not be described at all. In a real app the same kind of bias would grow, because popular songs and common tastes would keep winning and everyone else would see less variety.




# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

A small, explainable music recommender that runs in the terminal.

---

## 2. Intended Use  

**Goal:** VibeMatch suggests songs that fit one listener's taste. It gives a top five list. Each song comes with the reasons for its score.

**Intended use:**

- Classroom learning about how recommenders work.
- Trying out scoring rules and seeing how the results change.
- Explaining why a song was recommended.

**Assumptions about the user:**

- They can describe their taste with one genre, one mood, and three target levels.
- The levels are energy, positivity (valence), and acoustic feel.
- Their taste stays the same from one moment to the next.

**Not intended for:**

- Real music apps or real listeners.
- Judging artists or deciding what gets played.
- Anyone with mixed tastes, because a profile only holds one set of targets.
- Large catalogs. The scoring was only checked on 18 songs.

---

## 3. How the Model Works  

Think of the recommender as a judge who gives every song in the catalog a score out of 7 for how well it fits one listener, then hands back the five highest.

The listener is described by a short taste profile: a favorite genre, a favorite mood, and three target "feel" levels from 0 to 1. Those are how energetic the music is, how positive or upbeat it sounds (valence), and how acoustic versus electronic it is.

For each song, the judge awards points in two ways:

- **Matching labels.** A song earns 2 points if its genre is the listener's favorite and 1 point if its mood is. It is all or nothing, so "close" does not count, and a "metal" song gets no genre credit for a "rock" listener.
- **Closeness on the feel levels.** For energy, valence, and acousticness, the judge looks at how far the song is from the listener's target, not whether the number is high or low. A song that lands exactly on the target earns full points, and the points shrink the further away it is. Energy is worth up to 2 points, valence up to 1.5, and acousticness up to 0.5.

The points add up to the song's score. The judge also writes down each reason as it goes (for example "genre match (+2.0)"), so every recommendation comes with an explanation. Finally, all songs are sorted from highest score to lowest and the top five are shown.

Compared to the starter, which had no working logic, I added the valence and acousticness targets, weighted genre above mood after testing both orders on a lofi listener and a rock listener, and added the written reasons.

---

## 4. Data  

- The catalog is `data/songs.csv`. It has 18 songs.
- The starter file had 10 songs. I added 8 more with new genres and moods.
- Each song has a title, artist, genre, mood, and five numbers. The numbers are energy, tempo, valence, danceability, and acousticness.
- There are 15 genres. Lofi has 3 songs and pop has 2. The other 13 genres have 1 song each.
- There are 14 moods. Chill has 3 songs, happy and intense have 2 each, and the rest have 1 each.
- The numbers are made up. I picked them to feel right for each genre. They are not measured from real songs.
- Tempo and danceability are in the file but not used in the score.
- Missing: lyrics, language, artist fame, and how a listener feels at a given moment.

---

## 5. Strengths  

- It works well for clear tastes. Chill Lofi and Intense Rock got lists that matched my gut.
- Calm and intense listeners get completely different lists. They share no songs.
- Every result comes with its reasons, so it is easy to see why a song ranked where it did.
- It handles a missing genre without crashing. It falls back on mood and sound.

---

## 6. Limitations and Bias 

**Weakness found in experiments: exact genre matching creates a filter bubble in a tiny catalog.** Genre is worth 2.0 points and only an exact string match earns them, but 12 of the 15 genres in the 18-song catalog have just one song. A listener whose genre has a single song gets that song at number one almost automatically, and a listener of the three-song lofi group gets their whole top three filled by lofi before any other genre appears (Focus Flow scores 5.97, while the next best non-lofi song scores 4.57). The "Sad but Energetic" test shows the cost: the quiet blues song (energy 0.39) beat the loud, dark songs that sound like the request, because its genre and mood labels were worth 3.0 points. The energy gap also treats users unevenly. Only one song sits within 0.15 of an energy target of 0.1, against six or seven songs near targets of 0.3 to 0.7, so listeners with very quiet or very loud tastes see fewer good options.

---

## 7. Evaluation  

I checked the recommender by running different listener profiles, comparing their lists, and trying one weight experiment (written up in the README).

### Profiles tested

I ran seven listener profiles through the recommender and looked at the top five songs for each:

- **Three everyday listeners:** Pop / Happy, Chill Lofi, and Intense Rock.
- **Four trick profiles**, built to try to confuse the system: Sad but Energetic, Split Taste (gym and study), Genre Not In Catalog (k-pop), and Out-of-Range Energy (an energy target of 3.0, which is off the 0 to 1 scale).

What I looked for was simple: does each listener get songs that sound like what they asked for, and do two different listeners get different lists?

### What surprised me

- **The same few songs kept turning up.** Gym Hero, Storm Runner, and Concrete Crown (a middle-of-the-road hip hop song) each appeared in the top five for four of the seven profiles. Concrete Crown did so without ever matching anyone's genre or mood. With only 18 songs, the "average" ones fill the lower spots for everybody.
- **A label could beat the actual sound.** The sad-but-energetic listener asked for loud music, but a quiet blues song won, because matching its genre and mood earned more points than being close in energy.
- **Pop / Happy ranked an intense workout song above a happy one.** More on that below.
- **A bad input was accepted without any warning.** The out-of-range energy profile simply produced negative scores. I fixed this afterwards: the recommender now rejects targets outside 0 to 1 with a clear error.

### Why does "Gym Hero" keep showing up for people who just want Happy Pop?

Think of the system as a judge handing out points. A listener who says "pop, happy, fairly energetic and upbeat" gets 2 points for a song being pop, 1 point for it being happy, and then more points for how closely the energy, positivity, and acoustic feel line up. Gym Hero is a pop song, and it is loud and upbeat, so it scores almost as high as the happy pop song, Sunrise City. It only misses the 1 point for the "happy" label, because the song is tagged "intense". The happy indie song, Rooftop Lights, gets that 1 point, but it is tagged "indie pop", not "pop", so it misses the 2 points for genre. Two points for "pop" beat one point for "happy", and Gym Hero ends up second (5.62 points against 4.83). Gym Hero does not really feel happy, so this is a case where a label wins over the vibe. It also shows up for Intense Rock listeners, because it is the only other "intense" song and it is just as loud.

### Comparing pairs of profiles

- **Pop / Happy vs. Chill Lofi.** No song appears in both lists. Pop / Happy gets bright, fast songs (energy around 0.8) and Chill Lofi gets slow, quiet, acoustic ones (energy around 0.4, acousticness above 0.7). That makes sense, because these two listeners are asking for opposite ends of every scale, and the scoring rewards being close to whatever the listener asked for.
- **Pop / Happy vs. Intense Rock.** Both want loud music, so they share Gym Hero and Concrete Crown. The difference is the feel: the happy listener gets cheerful songs (Sunrise City, Rooftop Lights) and the rock listener gets darker ones (Storm Runner, Night Drive Loop, Iron Tide), because the two profiles ask for different positivity levels (0.80 against 0.48). That is a sensible split, and it shows the "valence" setting is doing real work.
- **Chill Lofi vs. Intense Rock.** These are the cleanest opposites: again no song in common. Lofi gets quiet, acoustic songs and rock gets loud, electric ones. This is the pair that shows the system can tell a calm listener from an intense one.
- **Intense Rock vs. Sad but Energetic.** Four of the five songs are the same (Storm Runner, Iron Tide, Night Drive Loop, Concrete Crown), because both listeners want loud and not-so-cheerful music. The differences are that Cold Harbor Blues (a quiet blues song) jumps to number one for the sad listener because its genre and mood labels match, and Gym Hero drops out, because it is too cheerful for someone who wants positivity near 0.2. This is partly right (the cheerful song should go) and partly wrong (a quiet song should not win a request for loud music).
- **Chill Lofi vs. Split Taste.** Three songs overlap (Midnight Coding, Library Rain, Spacewalk Thoughts), because the split listener asked for "chill" and those songs match that mood. The split listener also gets Storm Runner at number one and Velvet Hours, a medium-energy r&b song, because their energy target of 0.65 sits between calm and loud. The list is a blend of the two tastes, which makes sense, although it comes from the labels more than from the middle-range numbers.
- **Pop / Happy vs. Genre Not In Catalog.** The same five songs appear in both lists, but in a different order. The k-pop listener has no genre to match, so nobody gets the 2 genre points, and Laser Garden (euphoric, very upbeat) wins over Sunrise City. That is valid: with no genre to match, the system falls back on mood and sound and returns the closest-sounding songs, which are the same bright pop-like songs. It never tells the listener that no k-pop exists.
- **Pop / Happy vs. Out-of-Range Energy.** The top three songs are in the same order (Sunrise City, Gym Hero, Rooftop Lights), because the ranking only depends on which songs are closest to the target, and the same songs are still closest. Only the scores change: the loudest songs end up with negative totals. This shows the order can still be sensible even when the numbers are not, but it also showed the system should reject impossible inputs, which it now does.

Overall, the profiles test what I meant them to test: calm vs. intense (energy, acousticness), cheerful vs. dark (valence), and label matching vs. actual sound (the genre and mood bonuses). The system separates the clear cases well. It is weakest when a label and the sound disagree, and the results there are more a product of how I chose the weights than of what a listener would call a good match.

### Adversarial and edge-case profiles

The three normal profiles (Pop / Happy, Chill Lofi, Intense Rock) are shown in the README. I added four adversarial profiles in `src/main.py` to try to trick the scoring logic. Output of `python -m src.main`, top 5 for each:

#### Sad but Energetic

```
================================================================
User profile: Adversarial: Sad but Energetic
  genre=blues, mood=melancholic, energy=0.9, valence=0.2, acousticness=0.1
================================================================

1. Cold Harbor Blues by Delta Marlow
   Score: 5.53 / 7.00   [blues, melancholic]
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.39 vs target 0.90 (+0.98)
     - valence 0.28 vs target 0.20 (+1.38)
     - acousticness 0.76 vs target 0.10 (+0.17)

2. Iron Tide by Black Anvil
   Score: 3.80 / 7.00   [metal, angry]
     - energy 0.97 vs target 0.90 (+1.86)
     - valence 0.22 vs target 0.20 (+1.47)
     - acousticness 0.04 vs target 0.10 (+0.47)

3. Storm Runner by Voltline
   Score: 3.56 / 7.00   [rock, intense]
     - energy 0.91 vs target 0.90 (+1.98)
     - valence 0.48 vs target 0.20 (+1.08)
     - acousticness 0.10 vs target 0.10 (+0.50)

4. Night Drive Loop by Neon Echo
   Score: 3.20 / 7.00   [synthwave, moody]
     - energy 0.75 vs target 0.90 (+1.70)
     - valence 0.49 vs target 0.20 (+1.06)
     - acousticness 0.22 vs target 0.10 (+0.44)

5. Concrete Crown by Verse Mason
   Score: 3.12 / 7.00   [hip hop, confident]
     - energy 0.78 vs target 0.90 (+1.76)
     - valence 0.62 vs target 0.20 (+0.87)
     - acousticness 0.12 vs target 0.10 (+0.49)
```

**What happened:** Cold Harbor Blues (energy 0.39) wins even though the listener asked for energy 0.90. Its genre and mood matches are worth 3.0 points, which outweighs losing about 1.0 point on energy. Iron Tide, the song that actually sounds like the request (loud and dark), is second. Exact-match labels can override the numeric feel of a song.

#### Split Taste (gym + study)

```
================================================================
User profile: Adversarial: Split Taste (gym + study)
  genre=rock, mood=chill, energy=0.65, valence=0.55, acousticness=0.45
================================================================

1. Storm Runner by Voltline
   Score: 5.20 / 7.00   [rock, intense]
     - genre match (+2.0)
     - energy 0.91 vs target 0.65 (+1.48)
     - valence 0.48 vs target 0.55 (+1.40)
     - acousticness 0.10 vs target 0.45 (+0.33)

2. Midnight Coding by LoRoom
   Score: 4.40 / 7.00   [lofi, chill]
     - mood match (+1.0)
     - energy 0.42 vs target 0.65 (+1.54)
     - valence 0.56 vs target 0.55 (+1.48)
     - acousticness 0.71 vs target 0.45 (+0.37)

3. Library Rain by Paper Lanterns
   Score: 4.12 / 7.00   [lofi, chill]
     - mood match (+1.0)
     - energy 0.35 vs target 0.65 (+1.40)
     - valence 0.60 vs target 0.55 (+1.43)
     - acousticness 0.86 vs target 0.45 (+0.30)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 3.88 / 7.00   [ambient, chill]
     - mood match (+1.0)
     - energy 0.28 vs target 0.65 (+1.26)
     - valence 0.65 vs target 0.55 (+1.35)
     - acousticness 0.92 vs target 0.45 (+0.27)

5. Velvet Hours by Amara Skye
   Score: 3.63 / 7.00   [r&b, romantic]
     - energy 0.55 vs target 0.65 (+1.80)
     - valence 0.64 vs target 0.55 (+1.36)
     - acousticness 0.38 vs target 0.45 (+0.46)
```

**What happened:** the energy target of 0.65 sits between the two tastes, but no mid-energy song wins. Storm Runner takes first on the rock genre match (+2.0), then the chill lofi songs follow, so the list ends up a mix of both tastes. That is a reasonable outcome, but it comes from the label matches, not from the numbers.

#### Genre Not In Catalog

```
================================================================
User profile: Adversarial: Genre Not In Catalog
  genre=k-pop, mood=euphoric, energy=0.85, valence=0.9, acousticness=0.1
================================================================

1. Laser Garden by Pixel Bloom
   Score: 4.73 / 7.00   [edm, euphoric]
     - mood match (+1.0)
     - energy 0.95 vs target 0.85 (+1.80)
     - valence 0.88 vs target 0.90 (+1.47)
     - acousticness 0.03 vs target 0.10 (+0.46)

2. Sunrise City by Neon Echo
   Score: 3.81 / 7.00   [pop, happy]
     - energy 0.82 vs target 0.85 (+1.94)
     - valence 0.84 vs target 0.90 (+1.41)
     - acousticness 0.18 vs target 0.10 (+0.46)

3. Gym Hero by Max Pulse
   Score: 3.62 / 7.00   [pop, intense]
     - energy 0.93 vs target 0.85 (+1.84)
     - valence 0.77 vs target 0.90 (+1.30)
     - acousticness 0.05 vs target 0.10 (+0.47)

4. Rooftop Lights by Indigo Parade
   Score: 3.56 / 7.00   [indie pop, happy]
     - energy 0.76 vs target 0.85 (+1.82)
     - valence 0.81 vs target 0.90 (+1.36)
     - acousticness 0.35 vs target 0.10 (+0.38)

5. Concrete Crown by Verse Mason
   Score: 3.43 / 7.00   [hip hop, confident]
     - energy 0.78 vs target 0.85 (+1.86)
     - valence 0.62 vs target 0.90 (+1.08)
     - acousticness 0.12 vs target 0.10 (+0.49)
```

**What happened:** with no k-pop songs, nobody can earn the +2.0 genre bonus, so the best possible score is 5.0 out of 7.0. The system degrades gracefully: the euphoric edm song wins on mood and feel, and the next results are the upbeat pop songs. It never says that the genre was unavailable.

#### Out-of-Range Energy

```
================================================================
User profile: Adversarial: Out-of-Range Energy
  genre=pop, mood=happy, energy=3.0, valence=0.8, acousticness=0.2
================================================================

1. Sunrise City by Neon Echo
   Score: 2.57 / 7.00   [pop, happy]
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.82 vs target 3.00 (+-2.36)
     - valence 0.84 vs target 0.80 (+1.44)
     - acousticness 0.18 vs target 0.20 (+0.49)

2. Gym Hero by Max Pulse
   Score: 1.74 / 7.00   [pop, intense]
     - genre match (+2.0)
     - energy 0.93 vs target 3.00 (+-2.14)
     - valence 0.77 vs target 0.80 (+1.46)
     - acousticness 0.05 vs target 0.20 (+0.42)

3. Rooftop Lights by Indigo Parade
   Score: 0.43 / 7.00   [indie pop, happy]
     - mood match (+1.0)
     - energy 0.76 vs target 3.00 (+-2.48)
     - valence 0.81 vs target 0.80 (+1.48)
     - acousticness 0.35 vs target 0.20 (+0.43)

4. Laser Garden by Pixel Bloom
   Score: -0.30 / 7.00   [edm, euphoric]
     - energy 0.95 vs target 3.00 (+-2.10)
     - valence 0.88 vs target 0.80 (+1.38)
     - acousticness 0.03 vs target 0.20 (+0.41)

5. Storm Runner by Voltline
   Score: -0.71 / 7.00   [rock, intense]
     - energy 0.91 vs target 3.00 (+-2.18)
     - valence 0.48 vs target 0.80 (+1.02)
     - acousticness 0.10 vs target 0.20 (+0.45)
```

**What happened:** a target energy of 3.0 is outside the 0 to 1 scale, and the closeness formula `1 - |song - target|` goes negative, so songs get negative scores (-0.30 and -0.71 in the top five). The order is still sensible, but the scores are meaningless. The input was never validated. **Fixed afterwards:** `recommend_songs` now raises an error for targets outside 0 to 1, and `main.py` prints "Profile rejected: energy target must be between 0 and 1, got 3.0" for this profile. The output above is from before the fix.


---

## 8. Future Work  

1. **Give partial credit for similar labels.** Right now "angry" and "intense" count as unrelated, and so do "rock" and "metal". A small table of related moods and genres would fix cases like Iron Tide ranking fifth for a rock fan.
2. **Check more of the input.** Targets outside 0 to 1 are now rejected. A next step is to warn when a genre or mood is not in the catalog, instead of silently giving no points.
3. **Add more songs and more variety.** A bigger catalog would end the one-song-per-genre problem. A rule that limits repeats of one artist or genre would add variety.
4. **Support more than one taste.** Let a listener save a few profiles, like "gym" and "study".

---

## 9. Personal Reflection  

**Biggest learning moment.** Weights are choices, and the choices change who wins. I first guessed that mood should count more than genre. Then I ran both versions on a lofi listener and a rock listener. Genre-heavy gave better lists, so I switched. Later I doubled energy and halved genre, and the happy listener finally got a happy song ahead of Gym Hero. A small number change moved real songs up and down. That showed me a recommender is a set of opinions written as math.

**How AI helped, and when I double-checked it.** AI helped me move fast. It suggested the closeness formula, wrote the CSV loader and the scoring function, and drafted the profiles and the write-ups. But I checked it in a few places:

- I ran the code instead of trusting it. `python -m src.main`, the command the README gives, failed with an import error until I fixed the import in `main.py`. The tests also could not run until `pytest` was installed.
- I checked its advice against data. The first weight suggestion looked fine on paper, and the test showed a better option.
- The 8 songs it generated have made-up numbers. They are plausible, but they are not real measurements.
- The out-of-range energy profile showed that the code never validated input. It happily gave negative scores. I added a check that rejects those targets.

**What surprised me.** A few additions and a sort felt like a real recommender. The top song for a chill lofi listener was exactly what I would have picked. The "because" lines made it feel even smarter than it is. It was also odd to see how a wrong label can fool it. Gym Hero keeps appearing for happy pop fans, because "pop" earns more points than "happy". The system is not thinking about the music at all. It only adds up points.

**What I would try next.** First, partial credit for similar moods and genres, so "angry" and "intense" count as close. Second, input checks. Third, a bigger catalog so one-song genres stop locking the top spot. Fourth, profiles that can hold two tastes, like gym and study. I would also try adding tempo and danceability to the score and see if the lists feel better or just different.

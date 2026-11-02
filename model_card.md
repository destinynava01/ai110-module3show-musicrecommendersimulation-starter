# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

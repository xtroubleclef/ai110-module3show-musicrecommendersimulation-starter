# Model Card: VibeFinder 1.0

## 1. Model Name
VibeFinder 1.0

## 2. Goal / Task
This recommender suggests songs from a small music catalog by matching a user's *vibe* using genre, mood, energy, tempo, and acousticness.
The output is a ranked, top-5 list with short reasons.

## 3. Data Used
The dataset has 18 songs.
Each song has: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness.
The user profile includes favorite_genre, favorite_mood, target_energy, target_tempo_bpm, likes_acoustic, and target_acousticness.
Limits: small catalog, no listening history, no lyric features.

## 4. Algorithm Summary
Each song gets points for matching genre and mood.
Each song gets "similarity points" for energy and tempo closeness.
It gets an acoustic-preference score based on if the user likes acoustic songs.
All points are then added.
Songs sorted from highest to lowest score.
The system returns the top 5 songs and describes how each one scored well.

## 5. Observed Behavior / Biases
The system can create a "filter bubble" around energy.
When energy "weight" is high, songs with similar intensity reappear, even with different genres.
The small catalog causes repeated artists and repeated "safe" recommendations.
Some moods and genres have fewer options, so those users get less variety.

## 6. Evaluation Process
I tested three profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock.
I checked whether each profile produced a different top song and different top-5 list.
I also experimented with parameters for checking recommendation results by halving genre weight and doubling energy weight.
This made recommendations more intensity-driven and less strict about genre.
I compared outputs across profiles and wrote notes in reflection.md.

## 7. Intended Use and Non-Intended Use
Intended use: Learn basic recommender logic.
Understanding scoring, ranking, and explainability.
Non-intended use: real music product decisions or personalized production recommendations.
It should not be used for high-stakes decisions about users.

## 8. Ideas for Improvement
1. Add more songs to improve coverage and reduce repetition.
2. Add diversity rules so top-5 results are not too similar.
3. Add more user signals, like skips, repeats, and playlist behavior.

## 9. Personal Reflection
My biggest learning moment was seeing how small "weight" changes can reshape the whole ranking.
AI tools helped me move faster when writing boilerplate and checking prompt design.
I still had to manually double-check outputs, especially when commands were typed incorrectly or when long terminal lines wrapped.
I was surprised that a simple weighted score can still feel like a real recommendation engine.
If I continue this project, I'd add user behavior data and a diversity-aware "reranking" step.

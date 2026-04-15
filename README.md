# 🎵 Music Recommender Simulation

## Project Summary

This project builds a small CLI-first music recommender that ranks songs from a CSV catalog.
It uses user taste preferences like genre, mood, energy, tempo, and acousticness to score songs.
The output is a ranked top-5 list with short reasons for each recommendation.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Turn that data into recommendations—design a scoring rule to do so
- Evaluate what your system gets right and wrong
- Reflect: How does this mirror real-world AI recommenders?

My version focuses on transparent vibe matching instead of hidden machine learning.
It also supports multiple scoring modes and a diversity penalty so the top results do not feel too repetitive.

---

## How The System Works

Real world recommender systems combine huge amounts of user behavior (plays, skips, likes, playlist adds, and session context) with song attributes, then rank millions of candidate tracks using learned models. At scale, platforms usually run this in stages: candidate generation, scoring, and final ranking with diversity and freshness rules. In this classroom simulation, I prioritize transparent, explainable matching over complexity: songs score higher when they are closer to the user's preferred vibe, and top recommendations are the highest scoring songs.

### Song Features Used in This Simulation

- `id`
- `title`
- `artist`
- `genre`
- `mood`
- `energy`
- `tempo_bpm`
- `valence`
- `danceability`
- `acousticness`

### UserProfile Features Used in This Simulation

- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `target_tempo_bpm`
- `target_valence`
- `target_danceability`
- `likes_acoustic`
- `target_acousticness`

### Scoring and Ranking Overview

- Score each song by how well its genre and mood match the user, and how close its numeric vibe features are to user preference.
- Attach short reasons to each score so recommendations are interpretable.
- Rank songs by score from highest to lowest and return the top `k` items.

### Finalized Algorithm Recipe

- `+1.5` points for a genre match.
- `+2.0` points for a mood match.
- Up to `+2.5` points for energy closeness: `2.5 * (1 - abs(song_energy - target_energy))`.
- Up to `+1.5` points for tempo closeness (normalized): `1.5 * (1 - min(1, abs(song_tempo_bpm - target_tempo_bpm) / 120))`.
- Up to `+1.0` point for acoustic preference alignment.
- Final score is the sum; recommendations are the highest scoring songs.

### Data and Profile Plan (Checkpoint)

- Dataset was expanded from 10 songs to 18 songs to improve genre and mood diversity.
- Initial user profile is tuned for a chill/focused vibe (lofi, focused mood, lower target energy, slower target tempo, higher acoustic preference).

### Expected Biases

- This system may over-prioritize mood and energy, which can hide songs that are stylistically different but still enjoyable.
- Genre matching can still narrow discovery if weighted too strongly.
- A small catalog can make recommendations look repetitive even when the scoring rule is reasonable.

## System Evaluation

I tested the recommender with three different user profiles to see whether the top results changed in a sensible way:

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock

### Screenshot Placeholders

Run python -m src.main and add screenshots in the two groups below.

#### Phase 3 Step 4: CLI Verification Screenshot (Default pop/happy style output)

- CLI verification screenshot: [insert image here]

This screenshot should show Loaded songs, Top recommendations, and the recommendation rows with title, score, and reasons.

#### Phase 4 Step 1: Stress Test Screenshots (Diverse Profiles)

- High-Energy Pop screenshot: [insert image here]
- Chill Lofi screenshot: [insert image here]
- Deep Intense Rock screenshot: [insert image here]
- No-Diversity Baseline screenshot (optional comparison): [insert image here]

### Copilot Prompt for Edge Cases

Use this in a new chat session with `#codebase` context:

> Suggest 5 adversarial or edge-case user profiles for my music recommender. I want profiles that could expose weaknesses in my scoring logic, such as conflicting preferences (for example, very high energy with a sad mood), extreme genre loyalty, or preference combinations that might cause repetitive recommendations. For each profile, explain what failure mode it is trying to test.

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

## Experiments You Tried

I tried a weight-shift experiment where energy mattered more and genre mattered less.
That made the recommender favor songs with the right intensity even when the genre was not a perfect match.
I also tested several user profiles, like High-Energy Pop, Chill Lofi, and Deep Intense Rock, to see whether the results changed in a sensible way.
After that, I added a no-diversity baseline to compare how much the diversity penalty changes the top results.

---

## Limitations and Risks

The recommender can only work with a small catalog, so the results quickly repeat.
It doesn't have any real understanding of lyrics, artist context, or real listening history.
It also over-favor songs with a similar energy if its "weight" for it is too strong.
Some genres and moods have fewer examples, so those users may see less variety.
*These limits are discussed further in the model card.*

---

## Reflection

(Fuller version of my model card in `model_card.md`)

[**Model Card**](model_card.md)

I learned that simple scoring rules can still produce very believable recommendations.
Small changes in "weights" can shift the whole ranking, which made me consider more for fairness and bias.
AI tools assisted with moving faster for drafting code and prompts, but manual logic and output checks are still necessary.
What was most surprising to me was that the system felt smart even though it was only using a few hand-written rules.
If I built the recommender further, I'd add more user behavior data, songs, and a "reranking" step for song diversity.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3-5 songs from a small catalog based on a user's preferred genre, mood, and energy level 
*(just for learning purposes only, not real users)*

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"


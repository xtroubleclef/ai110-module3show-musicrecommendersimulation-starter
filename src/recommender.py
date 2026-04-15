from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv

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

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k songs ranked by profile match score."""
        scored: List[Tuple[Song, float]] = []
        for song in self.songs:
            score, _ = score_song(
                {
                    "favorite_genre": user.favorite_genre,
                    "favorite_mood": user.favorite_mood,
                    "target_energy": user.target_energy,
                    "likes_acoustic": user.likes_acoustic,
                },
                {
                    "id": song.id,
                    "title": song.title,
                    "artist": song.artist,
                    "genre": song.genre,
                    "mood": song.mood,
                    "energy": song.energy,
                    "tempo_bpm": song.tempo_bpm,
                    "valence": song.valence,
                    "danceability": song.danceability,
                    "acousticness": song.acousticness,
                },
            )
            scored.append((song, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song matched."""
        _, reasons = score_song(
            {
                "favorite_genre": user.favorite_genre,
                "favorite_mood": user.favorite_mood,
                "target_energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "tempo_bpm": song.tempo_bpm,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            },
        )
        return ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    print(f"Loaded songs: {len(songs)}")
    return songs


def _mode_weights(mode: str) -> Dict[str, float]:
    """Return per-feature weights for the selected scoring mode."""
    weights_by_mode = {
        "balanced": {
            "genre": 1.5,
            "mood": 2.0,
            "energy": 2.5,
            "tempo": 1.5,
            "acoustic": 1.0,
        },
        "genre-first": {
            "genre": 2.8,
            "mood": 1.4,
            "energy": 2.0,
            "tempo": 1.1,
            "acoustic": 0.7,
        },
        "mood-first": {
            "genre": 1.0,
            "mood": 3.0,
            "energy": 2.2,
            "tempo": 1.2,
            "acoustic": 0.8,
        },
        "energy-focused": {
            "genre": 0.75,
            "mood": 2.0,
            "energy": 5.0,
            "tempo": 1.5,
            "acoustic": 1.0,
        },
    }
    return weights_by_mode.get(mode, weights_by_mode["balanced"])

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute one song's weighted score and explain the contributing reasons."""
    score = 0.0
    reasons: List[str] = []

    scoring_mode = str(user_prefs.get("scoring_mode", "balanced")).strip().lower()
    weights = _mode_weights(scoring_mode)

    preferred_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    preferred_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = float(user_prefs.get("target_energy", user_prefs.get("energy", 0.5)))
    target_tempo = float(user_prefs.get("target_tempo_bpm", 100.0))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))
    target_acousticness = float(user_prefs.get("target_acousticness", 0.7 if likes_acoustic else 0.3))

    if preferred_genre and song.get("genre") == preferred_genre:
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.2f})")

    if preferred_mood and song.get("mood") == preferred_mood:
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.2f})")

    energy_diff = abs(float(song.get("energy", 0.0)) - target_energy)
    energy_points = weights["energy"] * max(0.0, 1.0 - min(1.0, energy_diff))
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    tempo_diff_normalized = min(1.0, abs(float(song.get("tempo_bpm", 0.0)) - target_tempo) / 120.0)
    tempo_points = weights["tempo"] * (1.0 - tempo_diff_normalized)
    score += tempo_points
    reasons.append(f"tempo closeness (+{tempo_points:.2f})")

    acousticness = float(song.get("acousticness", 0.0))
    if likes_acoustic:
        acoustic_alignment = 1.0 - min(1.0, abs(acousticness - target_acousticness))
    else:
        acoustic_alignment = 1.0 - acousticness
    acoustic_points = weights["acoustic"] * max(0.0, acoustic_alignment)
    score += acoustic_points
    reasons.append(f"acoustic preference (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top-k songs sorted by descending score with explanations."""
    scored_recs: List[Tuple[Dict, float, List[str]]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_recs.append((song, score, reasons))

    apply_diversity = bool(user_prefs.get("apply_diversity_penalty", True))
    artist_penalty_weight = float(user_prefs.get("artist_repeat_penalty", 0.8))
    genre_penalty_weight = float(user_prefs.get("genre_repeat_penalty", 0.35))

    if not apply_diversity:
        scored_recs.sort(key=lambda rec: (-rec[1], rec[0].get("title", "")))
        return [(song, score, "; ".join(reasons)) for song, score, reasons in scored_recs[:k]]

    ranked: List[Tuple[Dict, float, str]] = []
    selected_artist_counts: Dict[str, int] = {}
    selected_genre_counts: Dict[str, int] = {}
    candidates = list(scored_recs)

    while candidates and len(ranked) < k:
        best_index = 0
        best_adjusted_score = float("-inf")
        best_tie_title = ""

        for index, (song, base_score, _) in enumerate(candidates):
            artist = str(song.get("artist", ""))
            genre = str(song.get("genre", ""))
            artist_penalty = artist_penalty_weight * selected_artist_counts.get(artist, 0)
            genre_penalty = genre_penalty_weight * selected_genre_counts.get(genre, 0)
            adjusted_score = base_score - artist_penalty - genre_penalty
            title = str(song.get("title", ""))

            if adjusted_score > best_adjusted_score or (
                adjusted_score == best_adjusted_score and title < best_tie_title
            ):
                best_index = index
                best_adjusted_score = adjusted_score
                best_tie_title = title

        song, base_score, reasons = candidates.pop(best_index)
        artist = str(song.get("artist", ""))
        genre = str(song.get("genre", ""))
        artist_penalty = artist_penalty_weight * selected_artist_counts.get(artist, 0)
        genre_penalty = genre_penalty_weight * selected_genre_counts.get(genre, 0)

        final_reasons = list(reasons)
        if artist_penalty > 0:
            final_reasons.append(f"artist diversity penalty (-{artist_penalty:.2f})")
        if genre_penalty > 0:
            final_reasons.append(f"genre diversity penalty (-{genre_penalty:.2f})")

        final_score = base_score - artist_penalty - genre_penalty
        ranked.append((song, final_score, "; ".join(final_reasons)))
        selected_artist_counts[artist] = selected_artist_counts.get(artist, 0) + 1
        selected_genre_counts[genre] = selected_genre_counts.get(genre, 0) + 1

    return ranked

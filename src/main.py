"""Command-line runner for the Music Recommender Simulation."""

from typing import List, Tuple, Dict

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def _truncate(text: str, max_len: int) -> str:
    """Trim long text for fixed-width terminal tables."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _print_recommendation_table(recommendations: List[Tuple[Dict, float, str]]) -> None:
    """Print recommendations in a readable ASCII table with reasons."""
    headers = ["#", "Title", "Artist", "Score", "Reasons"]
    def summarize_reasons(explanation: str) -> str:
        labels = []
        for chunk in explanation.split(";"):
            part = chunk.strip()
            if not part:
                continue
            labels.append(part.split("(")[0].strip())
        return ", ".join(labels)

    rows: List[List[str]] = []
    for idx, (song, score, explanation) in enumerate(recommendations, start=1):
        reason_summary = summarize_reasons(explanation)
        rows.append(
            [
                str(idx),
                _truncate(str(song.get("title", "")), 16),
                _truncate(str(song.get("artist", "")), 12),
                f"{score:.2f}",
                _truncate(reason_summary, 34),
            ]
        )

    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, value in enumerate(row):
            col_widths[i] = max(col_widths[i], len(value))

    def format_row(values: List[str]) -> str:
        return "| " + " | ".join(value.ljust(col_widths[i]) for i, value in enumerate(values)) + " |"

    divider = "+-" + "-+-".join("-" * width for width in col_widths) + "-+"
    print(divider)
    print(format_row(headers))
    print(divider)
    for row in rows:
        print(format_row(row))
    print(divider)


def main() -> None:
    songs = load_songs("data/songs.csv") 

    profiles = [
        {
            "name": "High-Energy Pop",
            "prefs": {
                "scoring_mode": "genre-first",
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.90,
                "target_tempo_bpm": 128,
                "likes_acoustic": False,
                "target_acousticness": 0.15,
                "apply_diversity_penalty": True,
                "artist_repeat_penalty": 0.8,
                "genre_repeat_penalty": 0.35,
                "genre": "pop",
                "mood": "happy",
                "energy": 0.90,
            },
        },
        {
            "name": "Chill Lofi",
            "prefs": {
                "scoring_mode": "mood-first",
                "favorite_genre": "lofi",
                "favorite_mood": "focused",
                "target_energy": 0.40,
                "target_tempo_bpm": 80,
                "likes_acoustic": True,
                "target_acousticness": 0.78,
                "apply_diversity_penalty": True,
                "artist_repeat_penalty": 0.8,
                "genre_repeat_penalty": 0.35,
                "genre": "lofi",
                "mood": "focused",
                "energy": 0.40,
            },
        },
        {
            "name": "Deep Intense Rock",
            "prefs": {
                "scoring_mode": "energy-focused",
                "favorite_genre": "rock",
                "favorite_mood": "intense",
                "target_energy": 0.92,
                "target_tempo_bpm": 150,
                "likes_acoustic": False,
                "target_acousticness": 0.10,
                "apply_diversity_penalty": True,
                "artist_repeat_penalty": 0.8,
                "genre_repeat_penalty": 0.35,
                "genre": "rock",
                "mood": "intense",
                "energy": 0.92,
            },
        },
        {
            "name": "No-Diversity Baseline (High-Energy Pop)",
            "prefs": {
                "scoring_mode": "genre-first",
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.90,
                "target_tempo_bpm": 128,
                "likes_acoustic": False,
                "target_acousticness": 0.15,
                "apply_diversity_penalty": False,
                "genre": "pop",
                "mood": "happy",
                "energy": 0.90,
            },
        },
    ]

    for profile in profiles:
        recommendations = recommend_songs(profile["prefs"], songs, k=5)

        print(f"\n=== {profile['name']} ===")
        print(f"Scoring mode: {profile['prefs'].get('scoring_mode', 'balanced')}")
        print("Top recommendations:\n")
        _print_recommendation_table(recommendations)


if __name__ == "__main__":
    main()

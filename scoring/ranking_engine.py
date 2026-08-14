"""
Candidate Ranking and Shortlisting Engine

Ranks candidates based on ATS score and classifies them
into shortlist, review, and auto-reject zones.
"""


class RankingEngine:
    """
    Automatically ranks and classifies candidates
    based on their overall ATS score.
    """

    SHORTLIST_THRESHOLD = 80
    REVIEW_THRESHOLD = 60

    def rank_candidates(self, candidates):
        """
        Sort candidates by overall ATS score in descending order
        and assign ranking positions.
        """

        ranked_candidates = sorted(
            candidates,
            key=lambda candidate: candidate.get("overall_score", 0),
            reverse=True
        )

        for rank, candidate in enumerate(ranked_candidates, start=1):
            candidate["rank"] = rank
            candidate["status"] = self.classify_candidate(
                candidate.get("overall_score", 0)
            )

        return ranked_candidates

    def classify_candidate(self, score):
        """
        Classify a candidate based on ATS score.

        80-100   -> Shortlisted
        60-79.99 -> Review
        0-59.99  -> Auto-Rejected
        """

        if score >= self.SHORTLIST_THRESHOLD:
            return "Shortlisted"

        if score >= self.REVIEW_THRESHOLD:
            return "Review"

        return "Auto-Rejected"

    def get_top_candidates(self, candidates, top_n=5):
        """
        Return the top N candidates based on ATS score.
        """

        ranked_candidates = self.rank_candidates(candidates)

        return ranked_candidates[:top_n]
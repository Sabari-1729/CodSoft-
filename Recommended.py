import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class RecommendationSystem:
    def __init__(self, data, user_col, item_col, rating_col=None, description_col=None):
        """
        Initializes the recommendation system.

        Args:
            data (pd.DataFrame): DataFrame containing user-item interactions or item descriptions.
            user_col (str): Name of the user column.
            item_col (str): Name of the item column.
            rating_col (str, optional): Name of the rating column (for collaborative filtering). Defaults to None.
            description_col (str, optional): Name of the description column (for content-based filtering). Defaults to None.
        """
        self.data = data
        self.user_col = user_col
        self.item_col = item_col
        self.rating_col = rating_col
        self.description_col = description_col
        self.user_item_matrix = None
        self.item_similarity = None
        self.tfidf_matrix = None

        if rating_col:
            self.user_item_matrix = self._create_user_item_matrix()
            self.item_similarity = self._calculate_item_similarity()
        elif description_col:
            self.tfidf_matrix = self._create_tfidf_matrix()
            self.item_similarity = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def _create_user_item_matrix(self):
        """Creates a user-item matrix from the data."""
        return self.data.pivot_table(index=self.user_col, columns=self.item_col, values=self.rating_col, fill_value=0)

    def _calculate_item_similarity(self):
        """Calculates the cosine similarity between items."""
        return cosine_similarity(self.user_item_matrix.T)

    def _create_tfidf_matrix(self):
        """Creates TF-IDF matrix from item descriptions."""
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        return tfidf_vectorizer.fit_transform(self.data[self.description_col])

    def recommend_items(self, user_id=None, item_title=None, num_recommendations=5):
        """
        Recommends items for a given user (collaborative filtering) or item (content-based filtering).

        Args:
            user_id (int or str, optional): ID of the user (for collaborative filtering). Defaults to None.
            item_title(str, optional): Title of the item (for content-based filtering). Defaults to None.
            num_recommendations (int): Number of items to recommend.

        Returns:
            list: List of recommended item IDs.
        """
        if user_id and self.rating_col:  # Collaborative filtering
            if user_id not in self.user_item_matrix.index:
                print(f"User {user_id} not found.")
                return None

            user_ratings = self.user_item_matrix.loc[user_id]
            rated_items = user_ratings[user_ratings > 0].index
            unrated_items = user_ratings[user_ratings == 0].index

            if len(rated_items) == 0:
                print(f"User {user_id} has not rated any items")
                return None

            predicted_ratings = {}
            for unrated_item in unrated_items:
                predicted_rating = 0
                total_similarity = 0
                for rated_item in rated_items:
                    similarity = self.item_similarity[self.user_item_matrix.columns.get_loc(rated_item), self.user_item_matrix.columns.get_loc(unrated_item)]
                    predicted_rating += user_ratings[rated_item] * similarity
                    total_similarity += similarity

                if total_similarity > 0:
                    predicted_ratings[unrated_item] = predicted_rating / total_similarity
                else:
                    predicted_ratings[unrated_item] = 0

            recommended_items = sorted(predicted_ratings, key=predicted_ratings.get, reverse=True)[:num_recommendations]
            return recommended_items

        elif item_title and self.description_col: #content based filtering
            if item_title not in self.data[self.item_col].values:
                print(f"item {item_title} not found.")
                return None

            idx = self.data.index[self.data[self.item_col] == item_title].tolist()[0]
            sim_scores = list(enumerate(self.item_similarity[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]
            item_indices = [i[0] for i in sim_scores]
            return self.data[self.item_col].iloc[item_indices].tolist()

        else:
            print("Please provide either user_id for collaborative filtering or item_title for content-based filtering.")
            return None

# Example usage (Collaborative Filtering)
data_ratings = pd.DataFrame({
    'user_id': [1, 1, 2, 2, 3, 3, 4, 4, 1, 2, 3, 4],
    'movie_id': ['A', 'B', 'A', 'C', 'B', 'C', 'A', 'D', 'C', 'D', 'A', 'B'],
    'rating': [5, 4, 3, 5, 2, 4, 1, 5, 2, 1, 5, 3]
})
rec_system_cf = RecommendationSystem(data_ratings, 'user_id', 'movie_id', rating_col='rating')
print(f"Recommendations for user 1 (CF): {rec_system_cf.recommend_items(user_id=1)}")

# Example usage (Content-Based Filtering)
data_content = pd.DataFrame({
    'movie_id': ["Inception", "Interstellar", "The Matrix", "The Dark Knight"],
    'description': [
        "A thief who enters the dreams of others to steal secrets.",
        "A team of explorers travels through a wormhole in space.",
        "A hacker discovers the reality he lives in is a simulation.",
        "Batman battles the Joker to save Gotham City."
    ]
})
rec_system_cb = RecommendationSystem(data_content, 'movie_id', 'movie_id', description_col='description')
print(f"Recommendations for Inception (CB): {rec_system_cb.recommend_items(item_title='Inception')}")

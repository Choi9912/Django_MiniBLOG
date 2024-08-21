from konlpy.tag import Okt
from collections import Counter


class AutoTaggerCategorizer:
    def __init__(self):
        self.okt = Okt()
        self.predefined_categories = {
            "기술": ["컴퓨터", "소프트웨어", "하드웨어", "프로그래밍", "인공지능"],
            "여행": ["휴가", "여행", "관광", "목적지", "관광지"],
            "음식": ["레시피", "요리", "맛집", "음식", "식당"],
            # 필요에 따라 더 많은 카테고리를 추가하세요
        }

    def preprocess_text(self, text):
        return self.okt.nouns(text)

    def extract_keywords(self, text, num_keywords=5):
        words = self.preprocess_text(text)
        word_freq = Counter(words)
        return [word for word, _ in word_freq.most_common(num_keywords)]

    def suggest_category(self, keywords):
        category_scores = {category: 0 for category in self.predefined_categories}
        for keyword in keywords:
            for category, category_keywords in self.predefined_categories.items():
                if keyword in category_keywords:
                    category_scores[category] += 1
        return max(category_scores, key=category_scores.get)

    def process_post(self, title, content):
        full_text = f"{title} {content}"
        keywords = self.extract_keywords(full_text)
        category = self.suggest_category(keywords)
        return {"suggested_tags": keywords, "suggested_category": category}

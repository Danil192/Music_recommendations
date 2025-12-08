"""
Экспертная система Музыкальные рекомендации
Реализация на основе библиотеки experta
"""

# Исправление для совместимости с Python 3.13+
import collections.abc
import collections

# Патч для совместимости с experta
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, 'Iterable'):
    collections.Iterable = collections.abc.Iterable
if not hasattr(collections, 'MutableSet'):
    collections.MutableSet = collections.abc.MutableSet
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

from experta import *


# ============================================================================
# Определение фактов (Fact classes)
# ============================================================================

class UserActivity(Fact):
    """Факт о занятии пользователя"""
    value = Field(str, mandatory=True)


class UserPopularity(Fact):
    """Факт о предпочтении популярности"""
    value = Field(str, mandatory=True)


class UserMood(Fact):
    """Факт о настроении пользователя"""
    value = Field(str, mandatory=True)


class UserLanguage(Fact):
    """Факт о языке музыки"""
    value = Field(str, mandatory=True)


class Track(Fact):
    """Факт о музыкальном треке"""
    name = Field(str, mandatory=True)
    artist = Field(str, mandatory=True)
    activities = Field(list, mandatory=True)  # список занятий
    popularity = Field(str, mandatory=True)
    mood = Field(str, mandatory=True)
    language = Field(str, mandatory=True)


class Recommendation(Fact):
    """Факт о рекомендации"""
    track = Field(str, mandatory=True)
    artist = Field(str, mandatory=True)
    reason = Field(str, mandatory=True)
    match_percent = Field(float, mandatory=True)


class Comment(Fact):
    """Комментарий системы"""
    text = Field(str, mandatory=True)


class Log(Fact):
    """Лог выполнения правил"""
    rule = Field(str, mandatory=True)
    text = Field(str, mandatory=True)


# ============================================================================
# Онтологическая модель музыкальных треков
# ============================================================================

MUSIC_TRACKS = [
    # Цунами NYSHA
    Track(
        name="Цунами",
        artist="NY SHA",
        activities=["train"],
        popularity="popular",
        mood="energetic",
        language="russian"
    ),
    # Сказка Mav-d
    Track(
        name="Сказка",
        artist="Mav-d",
        activities=["work", "sleep"],
        popularity="unpopular",
        mood="calm",
        language="russian"
    ),
    # Sorry Madonna
    Track(
        name="Sorry",
        artist="Madonna",
        activities=["work", "train"],
        popularity="popular",
        mood="energetic",
        language="foreign"
    ),
    # Долины Mnogoznaal
    Track(
        name="Долины",
        artist="Mnogoznaal",
        activities=["work", "train"],
        popularity="unpopular",
        mood="calm",
        language="russian"
    ),
    # Счастье CREAM SODA
    Track(
        name="Счастье",
        artist="CREAM SODA",
        activities=["work", "train"],
        popularity="unpopular",
        mood="energetic",
        language="russian"
    ),
    # Прощай MAYOT
    Track(
        name="Прощай",
        artist="MAYOT",
        activities=["sleep"],
        popularity="unpopular",
        mood="calm",
        language="russian"
    ),
    # Just Dance Lady Gaga
    Track(
        name="Just Dance",
        artist="Lady Gaga",
        activities=["train"],
        popularity="popular",
        mood="energetic",
        language="foreign"
    ),
    # Восход Miyagi
    Track(
        name="Восход",
        artist="Miyagi",
        activities=["work"],
        popularity="unpopular",
        mood="calm",
        language="russian"
    ),
    # Roar Katy Perry
    Track(
        name="Roar",
        artist="Katy Perry",
        activities=["train"],
        popularity="popular",
        mood="energetic",
        language="foreign"
    ),
    # Ночь Каспийский груз
    Track(
        name="Ночь",
        artist="Каспийский груз",
        activities=["work", "sleep"],
        popularity="popular",
        mood="calm",
        language="russian"
    ),
    # Реальная жизнь Вера Брежнева
    Track(
        name="Реальная жизнь",
        artist="Вера Брежнева",
        activities=["train"],
        popularity="popular",
        mood="energetic",
        language="russian"
    ),
    # 101 Portico
    Track(
        name="101",
        artist="Portico",
        activities=["work", "sleep"],
        popularity="unpopular",
        mood="calm",
        language="foreign"
    ),
    # Uppercuts Terror Reid
    Track(
        name="Uppercuts",
        artist="Terror Reid",
        activities=["train"],
        popularity="unpopular",
        mood="energetic",
        language="foreign"
    ),
    # Settle Down North Downs
    Track(
        name="Settle Down",
        artist="North Downs",
        activities=["sleep"],
        popularity="unpopular",
        mood="calm",
        language="foreign"
    ),
    # Странно T-Fest
    Track(
        name="Странно",
        artist="T-Fest",
        activities=["work", "train"],
        popularity="unpopular",
        mood="energetic",
        language="russian"
    ),
]


# ============================================================================
# Экспертная система рекомендаций
# ============================================================================

class MusicRecommendationEngine(KnowledgeEngine):
    """Экспертная система для рекомендации музыки"""
    
    def __init__(self):
        super().__init__()
    
    @DefFacts()
    def initial_facts(self):
        """Инициализация фактов о треках"""
        for track in MUSIC_TRACKS:
            yield track
    
    # ========================================================================
    # Правила создания профилей
    # ========================================================================
    
    @Rule(UserActivity(value="work"))
    def make_activity_profile_work(self):
        """Создание профиля для работы"""
        self.declare(Comment(text="Подбор треков для работы"))
        self.declare(Log(rule="make_activity_profile_work", text="Режим работа"))
    
    @Rule(UserActivity(value="train"))
    def make_activity_profile_train(self):
        """Создание профиля для тренировки"""
        self.declare(Comment(text="Подбор треков для тренировки"))
        self.declare(Log(rule="make_activity_profile_train", text="Режим тренировка"))
    
    @Rule(UserActivity(value="sleep"))
    def make_activity_profile_sleep(self):
        """Создание профиля для засыпания"""
        self.declare(Comment(text="Подбор треков для засыпания"))
        self.declare(Log(rule="make_activity_profile_sleep", text="Режим сон"))
    
    @Rule(UserPopularity(value="popular"))
    def comment_popular(self):
        """Комментарий о популярных треках"""
        self.declare(Comment(text="Популярные треки"))
        self.declare(Log(rule="comment_popular", text="Популярные треки"))
    
    @Rule(UserPopularity(value="unpopular"))
    def comment_unpopular(self):
        """Комментарий о непопулярных треках"""
        self.declare(Comment(text="Менее распространенные треки"))
        self.declare(Log(rule="comment_unpopular", text="Менее распространенные треки"))
    
    # ========================================================================
    # Правила для логирования процесса подбора
    # ========================================================================
    
    @Rule(AS.track << Track())
    def log_track_analysis(self, track):
        """Логирование анализа трека"""
        self.declare(Log(
            rule="track_analysis",
            text=f"Анализ трека: {track['name']} - {track['artist']}"
        ))
    
    # ========================================================================
    # Метод для вычисления процента совпадения
    # ========================================================================
    
    def calculate_match_percent(self, track, user_activity, user_popularity, user_mood, user_language):
        """
        Вычислить процент совпадения трека с предпочтениями пользователя
        
        Args:
            track: объект Track
            user_activity: занятие пользователя
            user_popularity: популярность
            user_mood: настроение
            user_language: язык
        
        Returns:
            float: процент совпадения (0-100)
        """
        match_score = 0.0
        total_criteria = 4.0  # Всего 4 критерия
        
        # 1. Занятие (25%)
        if user_activity in track["activities"]:
            match_score += 25.0
        
        # 2. Популярность (25%)
        if track["popularity"] == user_popularity:
            match_score += 25.0
        
        # 3. Настроение (25%)
        if track["mood"] == user_mood:
            match_score += 25.0
        
        # 4. Язык (25%)
        if track["language"] == user_language:
            match_score += 25.0
        
        return match_score
    
    # ========================================================================
    # Метод для получения результатов
    # ========================================================================
    
    def get_results(self):
        """Получить результаты работы системы"""
        recommendations = []
        comments = []
        logs = []
        
        # Получаем предпочтения пользователя
        user_activity = None
        user_popularity = None
        user_mood = None
        user_language = None
        
        for fact_id, fact in self.facts.items():
            if isinstance(fact, UserActivity):
                user_activity = fact["value"]
            elif isinstance(fact, UserPopularity):
                user_popularity = fact["value"]
            elif isinstance(fact, UserMood):
                user_mood = fact["value"]
            elif isinstance(fact, UserLanguage):
                user_language = fact["value"]
            elif isinstance(fact, Log):
                logs.append({
                    "rule": fact["rule"],
                    "text": fact["text"]
                })
            elif isinstance(fact, Comment):
                comments.append(fact["text"])
        
        # Вычисляем процент совпадения для всех треков
        track_scores = []
        for fact_id, fact in self.facts.items():
            if isinstance(fact, Track):
                # Получаем значения из факта
                track_name = fact.get("name", "")
                track_artist = fact.get("artist", "")
                track_activities = fact.get("activities", [])
                track_popularity = fact.get("popularity", "")
                track_mood = fact.get("mood", "")
                track_language = fact.get("language", "")
                
                match_percent = self.calculate_match_percent(
                    fact, user_activity, user_popularity, user_mood, user_language
                )
                track_scores.append({
                    "track": track_name,
                    "artist": track_artist,
                    "match_percent": match_percent,
                    "activity_match": user_activity in track_activities if user_activity else False,
                    "popularity_match": track_popularity == user_popularity,
                    "mood_match": track_mood == user_mood,
                    "language_match": track_language == user_language
                })
        
        # Сортируем по проценту совпадения (от большего к меньшему)
        track_scores.sort(key=lambda x: x["match_percent"], reverse=True)
        
        # Берем топ-5
        top_tracks = track_scores[:5]
        
        # Формируем рекомендации с описанием
        for track_info in top_tracks:
            reasons = []
            if track_info["activity_match"]:
                reasons.append("подходит по занятию")
            if track_info["popularity_match"]:
                reasons.append("подходит по популярности")
            if track_info["mood_match"]:
                reasons.append("подходит по настроению")
            if track_info["language_match"]:
                reasons.append("подходит по языку")
            
            if reasons:
                reason_text = ", ".join(reasons)
            else:
                reason_text = "частичное совпадение"
            
            recommendations.append({
                "track": track_info["track"],
                "artist": track_info["artist"],
                "match_percent": track_info["match_percent"],
                "reason": reason_text
            })
        
        return {
            "recommendations": recommendations,
            "comments": comments,
            "logs": logs
        }
    
    def format_output(self):
        """Форматированный вывод результатов"""
        results = self.get_results()
        output = []
        
        output.append("Музыкальные рекомендации")
        output.append("")
        
        if results["recommendations"]:
            for i, rec in enumerate(results["recommendations"], 1):
                percent = rec['match_percent']
                output.append(f"{i}. {rec['track']} - {rec['artist']} ({percent:.0f}% совпадение)")
                output.append(f"   Причина: {rec['reason']}")
        else:
            output.append("Рекомендации не найдены")
        
        output.append("")
        output.append("Комментарии")
        for comment in results["comments"]:
            output.append(f"* {comment}")
        
        output.append("")
        output.append("Цепочка правил")
        for log in results["logs"]:
            output.append(f"* {log['rule']} : {log['text']}")
        
        return "\n".join(output)


# ============================================================================
# Функция для запуска системы
# ============================================================================

def get_recommendations(activity, popularity, mood, language):
    """
    Получить рекомендации на основе предпочтений пользователя
    
    Args:
        activity: занятие (work, train, sleep)
        popularity: популярность (popular, unpopular)
        mood: настроение (energetic, calm)
        language: язык (russian, foreign)
    
    Returns:
        dict: результаты работы системы
    """
    engine = MusicRecommendationEngine()
    engine.reset()
    
    # Добавляем факты о предпочтениях пользователя
    engine.declare(UserActivity(value=activity))
    engine.declare(UserPopularity(value=popularity))
    engine.declare(UserMood(value=mood))
    engine.declare(UserLanguage(value=language))
    
    # Запускаем систему
    engine.run()
    
    # Возвращаем результаты
    return engine.get_results()


def get_formatted_output(activity, popularity, mood, language):
    """
    Получить форматированный вывод рекомендаций
    
    Args:
        activity: занятие (work, train, sleep)
        popularity: популярность (popular, unpopular)
        mood: настроение (energetic, calm)
        language: язык (russian, foreign)
    
    Returns:
        str: форматированный текст результатов
    """
    engine = MusicRecommendationEngine()
    engine.reset()
    
    # Логируем начало работы системы
    engine.declare(Log(rule="system_start", text="Запуск системы рекомендаций"))
    
    # Добавляем факты о предпочтениях пользователя
    engine.declare(UserActivity(value=activity))
    engine.declare(Log(rule="user_input", text=f"Пользователь выбрал занятие: {activity}"))
    
    engine.declare(UserPopularity(value=popularity))
    engine.declare(Log(rule="user_input", text=f"Пользователь выбрал популярность: {popularity}"))
    
    engine.declare(UserMood(value=mood))
    engine.declare(Log(rule="user_input", text=f"Пользователь выбрал настроение: {mood}"))
    
    engine.declare(UserLanguage(value=language))
    engine.declare(Log(rule="user_input", text=f"Пользователь выбрал язык: {language}"))
    
    # Запускаем систему
    engine.run()
    
    # Логируем завершение работы
    engine.declare(Log(rule="system_end", text="Завершение работы системы"))
    
    # Возвращаем форматированный вывод
    return engine.format_output()


if __name__ == "__main__":
    # Пример использования
    print("Тест системы рекомендаций")
    print("=" * 50)
    
    result = get_formatted_output("work", "popular", "energetic", "russian")
    print(result)


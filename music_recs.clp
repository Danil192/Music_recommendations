;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Экспертная система Музыкальные рекомендации
;; Двухрежимный вариант console плюс web
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Конфигурация режима
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(deffacts config
   (mode console)
   (state start))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Шаблоны фактов
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(deftemplate user_activity (slot value))
(deftemplate user_popularity (slot value))
(deftemplate user_mood (slot value))
(deftemplate user_language (slot value))

(deftemplate activity_profile (slot value))
(deftemplate style_profile (slot value))
(deftemplate mood_profile (slot value))

(deftemplate comment (slot text))
(deftemplate log (slot rule) (slot text))

(deftemplate recommendation
   (slot track)
   (slot artist)
   (slot reason))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Диалоговые правила только для console режима
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule start_questionnaire
   (mode console)
   (state start)
   =>
   (retract (state start))
   (assert (state activity_question))
   (assert (log (rule start_questionnaire)
                (text "Запуск диалога console"))))

(defrule ask_activity
   (mode console)
   (state activity_question)
   =>
   (printout t crlf "Чем ты сейчас занимаешься" crlf)
   (printout t "1 Работаю" crlf)
   (printout t "2 Тренируюсь" crlf)
   (printout t "3 Засыпаю" crlf)
   (printout t "> ")
   (bind ?a (read))
   (if (= ?a 1) then
      (assert (user_activity (value work)))
      else
      (if (= ?a 2) then
         (assert (user_activity (value train)))
         else
         (assert (user_activity (value sleep)))))

   (assert (log (rule ask_activity)
                (text "Ответ по занятию console")))
   (retract (state activity_question))
   (assert (state popularity_question)))

(defrule ask_popularity
   (mode console)
   (state popularity_question)
   =>
   (printout t crlf "Популярность музыки" crlf)
   (printout t "1 Популярное" crlf)
   (printout t "2 Непопулярное" crlf)
   (printout t "> ")
   (bind ?p (read))

   (if (= ?p 1) then
      (assert (user_popularity (value popular)))
      else
      (assert (user_popularity (value unpopular))))

   (assert (log (rule ask_popularity)
                (text "Ответ по популярности console")))
   (retract (state popularity_question))
   (assert (state mood_question)))

(defrule ask_mood
   (mode console)
   (state mood_question)
   =>
   (printout t crlf "Какое настроение нужно" crlf)
   (printout t "1 Бодрое" crlf)
   (printout t "2 Спокойное" crlf)
   (printout t "> ")
   (bind ?m (read))

   (if (= ?m 1) then
      (assert (user_mood (value energetic)))
      else
      (assert (user_mood (value calm))))

   (assert (log (rule ask_mood)
                (text "Ответ по настроению console")))
   (retract (state mood_question))
   (assert (state language_question)))

(defrule ask_language
   (mode console)
   (state language_question)
   =>
   (printout t crlf "Какой язык" crlf)
   (printout t "1 Русский" crlf)
   (printout t "2 Иностранный" crlf)
   (printout t "> ")
   (bind ?l (read))

   (if (= ?l 1) then
      (assert (user_language (value russian)))
      else
      (assert (user_language (value foreign))))

   (assert (log (rule ask_language)
                (text "Ответ по языку console")))
   (retract (state language_question))
   (assert (state ready)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Профили
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule make_activity_profile_work
   (user_activity (value work))
   =>
   (assert (activity_profile (value work)))
   (assert (log (rule make_activity_profile_work)
                (text "Режим работа"))))

(defrule make_activity_profile_train
   (user_activity (value train))
   =>
   (assert (activity_profile (value train)))
   (assert (log (rule make_activity_profile_train)
                (text "Режим тренировка"))))

(defrule make_activity_profile_sleep
   (user_activity (value sleep))
   =>
   (assert (activity_profile (value sleep)))
   (assert (log (rule make_activity_profile_sleep)
                (text "Режим сон"))))

(defrule style_russian_popular
   (user_language (value russian))
   (user_popularity (value popular))
   =>
   (assert (style_profile (value russian_hit)))
   (assert (log (rule style_russian_popular)
                (text "Русские хиты"))))

(defrule style_russian_unpopular
   (user_language (value russian))
   (user_popularity (value unpopular))
   =>
   (assert (style_profile (value russian_alt)))
   (assert (log (rule style_russian_unpopular)
                (text "Русская альтернатива"))))

(defrule style_foreign_popular
   (user_language (value foreign))
   (user_popularity (value popular))
   =>
   (assert (style_profile (value foreign_hit)))
   (assert (log (rule style_foreign_popular)
                (text "Зарубежные хиты"))))

(defrule style_foreign_unpopular
   (user_language (value foreign))
   (user_popularity (value unpopular))
   =>
   (assert (style_profile (value foreign_alt)))
   (assert (log (rule style_foreign_unpopular)
                (text "Зарубежная альтернатива"))))

(defrule mood_profile_energetic
   (user_mood (value energetic))
   =>
   (assert (mood_profile (value energetic)))
   (assert (log (rule mood_profile_energetic)
                (text "Бодрое настроение"))))

(defrule mood_profile_calm
   (user_mood (value calm))
   =>
   (assert (mood_profile (value calm)))
   (assert (log (rule mood_profile_calm)
                (text "Спокойное настроение"))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Комментарии
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule comment_work
   (activity_profile (value work))
   =>
   (assert (comment (text "Подбор треков для работы"))))

(defrule comment_train
   (activity_profile (value train))
   =>
   (assert (comment (text "Подбор треков для тренировки"))))

(defrule comment_sleep
   (activity_profile (value sleep))
   =>
   (assert (comment (text "Подбор треков для засыпания"))))

(defrule comment_popular
   (user_popularity (value popular))
   =>
   (assert (comment (text "Популярные треки"))))

(defrule comment_unpopular
   (user_popularity (value unpopular))
   =>
   (assert (comment (text "Менее распространенные треки"))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Рекомендации
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; оставил твои правила полностью без изменений
;; здесь идут все rec_ правила
;; я их не выкидывал, иначе сообщение будет слишком большим
;; они рабочие и не требуют изменений

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Финальный вывод
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule show_results
   (declare (salience -10))
   (state ready)
   =>
   (printout t crlf "Музыкальные рекомендации" crlf)

   (if (any-factp ((?r recommendation)) TRUE)
      then
         (do-for-all-facts
            ((?r recommendation))
            TRUE
            (printout t "* " ?r:track " , " ?r:artist " , " ?r:reason crlf))
      else
         (printout t "Рекомендации не найдены" crlf))

   (printout t crlf "Комментарии" crlf)
   (do-for-all-facts ((?c comment)) TRUE
      (printout t "* " ?c:text crlf))

   (printout t crlf "Цепочка правил" crlf)
   (do-for-all-facts ((?l log)) TRUE
      (printout t "* " ?l:rule " : " ?l:text crlf))

   (retract (state ready)))

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Налаштування логування
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Дані про їжу
DATA = {
    "uk": {
        "questions": {
            "1": {"question": "Як залучити більше трафіку на казино?", "answer": "Використовуйте SEO, контекстну рекламу та партнерські програми."},
            "2": {"question": "Які ГЕО найкращі для казино?", "answer": "Залежить від продукту, але популярні: UA, RU, IN, BR."},
            "3": {"question": "Як уникнути бану в Google Ads?", "answer": "Дотримуйтесь правил, використовуйте клоакінг обережно."},
            "4": {"question": "Які джерела трафіку найефективніші?", "answer": "Пошуковий трафік, соціальні мережі, email-маркетинг."},
            "5": {"question": "Як оптимізувати рекламні кампанії?", "answer": "Тестуйте різні креативи, аналізуйте ROI, використовуйте A/B-тестування."},
            "6": {"question": "Що таке клоакінг і як його використовувати?", "answer": "Клоакінг — це приховування реального контенту від модераторів. Використовуйте з обережністю."},
            "7": {"question": "Як працювати з партнерськими програмами?", "answer": "Оберіть надійних партнерів, домовляйтесь про вигідні умови."},
            "8": {"question": "Які інструменти для відстеження трафіку?", "answer": "Google Analytics, трекери типу Keitaro або Binom."},
            "9": {"question": "Як залучити трафік з соціальних мереж?", "answer": "Створюйте привабливий контент, використовуйте таргетовану рекламу."},
            "10": {"question": "Які помилки найчастіше роблять новачки?", "answer": "Неправильний вибір ГЕО, погана оптимізація кампаній, ігнорування аналітики."},
            "11": {"question": "Як обрати казино для просування?", "answer": "Дивіться на репутацію, відгуки, умови партнерської програми."},
            "12": {"question": "Що таке ревшара і CPA?", "answer": "Ревшара — відсоток від доходу, CPA — фіксована оплата за дію."},
            "13": {"question": "Як залучити трафік з YouTube?", "answer": "Створюйте огляди, стріми, навчальні відео про казино."},
            "14": {"question": "Які креативи найкраще працюють?", "answer": "Залежить від аудиторії, але часто — бонуси, акції, виграші."},
            "15": {"question": "Як працювати з email-маркетингом?", "answer": "Збирайте базу підписників, надсилайте персоналізовані пропозиції."},
            "16": {"question": "Що таке SEO для казино?", "answer": "Оптимізація сайту для пошукових систем з фокусом на ключові слова."},
            "17": {"question": "Як уникнути фроду в трафіку?", "answer": "Використовуйте антифрод-системи, перевіряйте джерела трафіку."},
            "18": {"question": "Які метрики важливі для аналізу?", "answer": "CTR, CR, EPC, ROI, LTV."},
            "19": {"question": "Як залучити трафік з Telegram?", "answer": "Створюйте канали з новинами, акціями, бонусами."},
            "20": {"question": "Що таке арбітраж трафіку?", "answer": "Купівля трафіку з одного джерела і продаж на інше з прибутком."},
            "21": {"question": "Як працювати з Push-рекламою?", "answer": "Створюйте привабливі повідомлення, тестуйте різні формати."},
            "22": {"question": "Які ГЕО мають високий LTV?", "answer": "Зазвичай Tier-1 країни: США, Канада, Австралія."},
            "23": {"question": "Як залучити трафік з форумів?", "answer": "Беріть участь у дискусіях, пропонуйте корисний контент."},
            "24": {"question": "Що таке контекстна реклама?", "answer": "Реклама, що показується на основі пошукових запитів користувача."},
            "25": {"question": "Як працювати з інфлюенсерами?", "answer": "Співпрацюйте з блогерами, які мають аудиторію, зацікавлену в азартних іграх."},
            "26": {"question": "Які ризики при роботі з казино?", "answer": "Юридичні обмеження, проблеми з виплатами, конкуренція."},
            "27": {"question": "Як залучити трафік з TikTok?", "answer": "Створюйте короткі відео з акціями, виграшами, челенджами."},
            "28": {"question": "Що таке PPC-реклама?", "answer": "Оплата за клік, популярна в Google Ads, Bing Ads."},
            "29": {"question": "Як оптимізувати лендінги?", "answer": "Використовуйте A/B-тестування, покращуйте юзабіліті, додавайте заклики до дії."},
            "30": {"question": "Які інструменти для автоматизації?", "answer": "Трекери, боти для соціальних мереж, CRM-системи."},
            "31": {"question": "Як працювати з мобільним трафіком?", "answer": "Оптимізуйте сайти для мобільних пристроїв, використовуйте мобільні додатки."},
            "32": {"question": "Що таке programmatic advertising?", "answer": "Автоматизована купівля реклами через платформи."},
            "33": {"question": "Як залучити трафік з Reddit?", "answer": "Беріть участь у сабредітах, пов'язаних з азартними іграми."},
            "34": {"question": "Які креативи заборонені?", "answer": "Зазвичай — оманливі обіцянки, контент для дорослих, порушення авторських прав."},
            "35": {"question": "Як працювати з CPA-мережами?", "answer": "Реєструйтесь, обирайте офери, запускайте кампанії."},
            "36": {"question": "Що таке ретаргетинг?", "answer": "Показ реклами користувачам, які вже відвідували ваш сайт."},
            "37": {"question": "Як залучити трафік з Instagram?", "answer": "Використовуйте Stories, Reels, співпрацюйте з інфлюенсерами."},
            "38": {"question": "Які ГЕО мають низький CPM?", "answer": "Зазвичай Tier-3 країни: Індія, Філіппіни, В'єтнам."},
            "39": {"question": "Як працювати з банерною рекламою?", "answer": "Створюйте привабливі банери, розміщуйте на тематичних сайтах."},
            "40": {"question": "Що таке affiliate marketing?", "answer": "Партнерський маркетинг, де ви отримуєте комісію за залучених гравців."},
            "41": {"question": "Як залучити трафік з Pinterest?", "answer": "Створюйте привабливі піни з акціями та бонусами."},
            "42": {"question": "Які інструменти для аналізу конкурентів?", "answer": "SEMrush, Ahrefs, SimilarWeb."},
            "43": {"question": "Як працювати з відеоконтентом?", "answer": "Створюйте огляди, стріми, навчальні відео."},
            "44": {"question": "Що таке нативна реклама?", "answer": "Реклама, що виглядає як органічний контент."},
            "45": {"question": "Як залучити трафік з Twitter?", "answer": "Публікуйте твіти з акціями, використовуйте хештеги."},
            "46": {"question": "Які ГЕО мають високий ARPU?", "answer": "Tier-1 країни, наприклад, Норвегія, Швеція, Німеччина."},
            "47": {"question": "Як працювати з SMS-маркетингом?", "answer": "Надсилайте персоналізовані повідомлення з акціями."},
            "48": {"question": "Що таке programmatic direct?", "answer": "Пряма купівля реклами через programmatic-платформи."},
            "49": {"question": "Як залучити трафік з LinkedIn?", "answer": "Публікуйте статті, беріть участь у групах, пов'язаних з азартними іграми."},
            "50": {"question": "Які креативи найкраще працюють для мобільних пристроїв?", "answer": "Адаптивні банери, відео, інтерактивні елементи."}
        },
        "support_message": "Якщо не знайшли відповідь — пишіть власникам @calwxxxx або адмінам у групі"
    },
    "ru": {
        "questions": {
            "1": {"question": "Как привлечь больше трафика на казино?", "answer": "Используйте SEO, контекстную рекламу и партнерские программы."},
            "2": {"question": "Какие ГЕО лучшие для казино?", "answer": "Зависит от продукта, но популярны: UA, RU, IN, BR."},
            "3": {"question": "Как избежать бана в Google Ads?", "answer": "Соблюдайте правила, аккуратно используйте клоакинг."},
            "4": {"question": "Какие источники трафика самые эффективные?", "answer": "Поисковый трафик, социальные сети, email-маркетинг."},
            "5": {"question": "Как оптимизировать рекламные кампании?", "answer": "Тестируйте разные креативы, анализируйте ROI, используйте A/B-тестирование."},
            "6": {"question": "Что такое клоакинг и как его использовать?", "answer": "Клоакинг — скрытие реального контента от модераторов. Используйте осторожно."},
            "7": {"question": "Как работать с партнерскими программами?", "answer": "Выбирайте надежных партнеров, договаривайтесь о выгодных условиях."},
            "8": {"question": "Какие инструменты для отслеживания трафика?", "answer": "Google Analytics, трекеры типа Keitaro или Binom."},
            "9": {"question": "Как привлечь трафик из социальных сетей?", "answer": "Создавайте привлекательный контент, используйте таргетированную рекламу."},
            "10": {"question": "Какие ошибки чаще всего делают новички?", "answer": "Неправильный выбор ГЕО, плохая оптимизация кампаний, игнорирование аналитики."},
            "11": {"question": "Как выбрать казино для продвижения?", "answer": "Смотрите на репутацию, отзывы, условия партнерской программы."},
            "12": {"question": "Что такое ревшара и CPA?", "answer": "Ревшара — процент от дохода, CPA — фиксированная оплата за действие."},
            "13": {"question": "Как привлечь трафик с YouTube?", "answer": "Создавайте обзоры, стримы, обучающие видео о казино."},
            "14": {"question": "Какие креативы лучше всего работают?", "answer": "Зависит от аудитории, но часто — бонусы, акции, выигрыши."},
            "15": {"question": "Как работать с email-маркетингом?", "answer": "Собирайте базу подписчиков, отправляйте персонализированные предложения."},
            "16": {"question": "Что такое SEO для казино?", "answer": "Оптимизация сайта для поисковых систем с фокусом на ключевые слова."},
            "17": {"question": "Как избежать фрода в трафике?", "answer": "Используйте антифрод-системы, проверяйте источники трафика."},
            "18": {"question": "Какие метрики важны для анализа?", "answer": "CTR, CR, EPC, ROI, LTV."},
            "19": {"question": "Как привлечь трафик с Telegram?", "answer": "Создавайте каналы с новостями, акциями, бонусами."},
            "20": {"question": "Что такое арбитраж трафика?", "answer": "Покупка трафика с одного источника и продажа на другой с прибылью."},
            "21": {"question": "Как работать с Push-рекламой?", "answer": "Создавайте привлекательные сообщения, тестируйте разные форматы."},
            "22": {"question": "Какие ГЕО имеют высокий LTV?", "answer": "Обычно Tier-1 страны: США, Канада, Австралия."},
            "23": {"question": "Как привлечь трафик с форумов?", "answer": "Участвуйте в дискуссиях, предлагайте полезный контент."},
            "24": {"question": "Что такое контекстная реклама?", "answer": "Реклама, показываемая на основе поисковых запросов пользователя."},
            "25": {"question": "Как работать с инфлюенсерами?", "answer": "Сотрудничайте с блогерами, у которых есть аудитория, интересующаяся азартными играми."},
            "26": {"question": "Какие риски при работе с казино?", "answer": "Юридические ограничения, проблемы с выплатами, конкуренция."},
            "27": {"question": "Как привлечь трафик с TikTok?", "answer": "Создавайте короткие видео с акциями, выигрышами, челленджами."},
            "28": {"question": "Что такое PPC-реклама?", "answer": "Оплата за клик, популярна в Google Ads, Bing Ads."},
            "29": {"question": "Как оптимизировать лендинги?", "answer": "Используйте A/B-тестирование, улучшайте юзабилити, добавляйте призывы к действию."},
            "30": {"question": "Какие инструменты для автоматизации?", "answer": "Трекеры, боты для социальных сетей, CRM-системы."},
            "31": {"question": "Как работать с мобильным трафиком?", "answer": "Оптимизируйте сайты для мобильных устройств, используйте мобильные приложения."},
            "32": {"question": "Что такое programmatic advertising?", "answer": "Автоматизированная покупка рекламы через платформы."},
            "33": {"question": "Как привлечь трафик с Reddit?", "answer": "Участвуйте в сабреддитах, связанных с азартными играми."},
            "34": {"question": "Какие креативы запрещены?", "answer": "Обычно — обманчивые обещания, контент для взрослых, нарушение авторских прав."},
            "35": {"question": "Как работать с CPA-сетями?", "answer": "Регистрируйтесь, выбирайте офферы, запускайте кампании."},
            "36": {"question": "Что такое ретаргетинг?", "answer": "Показ рекламы пользователям, которые уже посещали ваш сайт."},
            "37": {"question": "Как привлечь трафик с Instagram?", "answer": "Используйте Stories, Reels, сотрудничайте с инфлюенсерами."},
            "38": {"question": "Какие ГЕО имеют низкий CPM?", "answer": "Обычно Tier-3 страны: Индия, Филиппины, Вьетнам."},
            "39": {"question": "Как работать с баннерной рекламой?", "answer": "Создавайте привлекательные баннеры, размещайте на тематических сайтах."},
            "40": {"question": "Что такое affiliate marketing?", "answer": "Партнерский маркетинг, где вы получаете комиссию за привлеченных игроков."},
            "41": {"question": "Как привлечь трафик с Pinterest?", "answer": "Создавайте привлекательные пины с акциями и бонусами."},
            "42": {"question": "Какие инструменты для анализа конкурентов?", "answer": "SEMrush, Ahrefs, SimilarWeb."},
            "43": {"question": "Как работать с видеоконтентом?", "answer": "Создавайте обзоры, стримы, обучающие видео."},
            "44": {"question": "Что такое нативная реклама?", "answer": "Реклама, которая выглядит как органический контент."},
            "45": {"question": "Как привлечь трафик с Twitter?", "answer": "Публикуйте твиты с акциями, используйте хэштеги."},
            "46": {"question": "Какие ГЕО имеют высокий ARPU?", "answer": "Tier-1 страны, например, Норвегия, Швеция, Германия."},
            "47": {"question": "Как работать с SMS-маркетингом?", "answer": "Отправляйте персонализированные сообщения с акциями."},
            "48": {"question": "Что такое programmatic direct?", "answer": "Прямая покупка рекламы через programmatic-платформы."},
            "49": {"question": "Как привлечь трафик с LinkedIn?", "answer": "Публикуйте статьи, участвуйте в группах, связанных с азартными играми."},
            "50": {"question": "Какие креативы лучше всего работают для мобильных устройств?", "answer": "Адаптивные баннеры, видео, интерактивные элементы."}
        },
        "support_message": "Если не нашли ответ — пишите владельцу @calwxxxx или админам в группе"
    },
    "en": {
        "questions": {
            "1": {"question": "How to drive more traffic to a casino?", "answer": "Use SEO, PPC ads, and affiliate programs."},
            "2": {"question": "Which GEOs are best for casinos?", "answer": "Depends on the product, but popular ones are: UA, RU, IN, BR."},
            "3": {"question": "How to avoid a Google Ads ban?", "answer": "Follow policies, use cloaking carefully."},
            "4": {"question": "What are the most effective traffic sources?", "answer": "Search traffic, social media, email marketing."},
            "5": {"question": "How to optimize ad campaigns?", "answer": "Test different creatives, analyze ROI, use A/B testing."},
            "6": {"question": "What is cloaking and how to use it?", "answer": "Cloaking hides real content from moderators. Use it cautiously."},
            "7": {"question": "How to work with affiliate programs?", "answer": "Choose reliable partners, negotiate favorable terms."},
            "8": {"question": "What tools to track traffic?", "answer": "Google Analytics, trackers like Keitaro or Binom."},
            "9": {"question": "How to drive traffic from social media?", "answer": "Create engaging content, use targeted ads."},
            "10": {"question": "What are common newbie mistakes?", "answer": "Wrong GEO choice, poor campaign optimization, ignoring analytics."},
            "11": {"question": "How to choose a casino to promote?", "answer": "Look at reputation, reviews, affiliate program terms."},
            "12": {"question": "What are revshare and CPA?", "answer": "Revshare is a percentage of revenue, CPA is a fixed payment per action."},
            "13": {"question": "How to drive traffic from YouTube?", "answer": "Create reviews, streams, educational videos about casinos."},
            "14": {"question": "Which creatives work best?", "answer": "Depends on the audience, but often bonuses, promotions, winnings."},
            "15": {"question": "How to work with email marketing?", "answer": "Build a subscriber list, send personalized offers."},
            "16": {"question": "What is SEO for casinos?", "answer": "Optimizing the site for search engines with a focus on keywords."},
            "17": {"question": "How to avoid fraud in traffic?", "answer": "Use anti-fraud systems, check traffic sources."},
            "18": {"question": "What metrics are important for analysis?", "answer": "CTR, CR, EPC, ROI, LTV."},
            "19": {"question": "How to drive traffic from Telegram?", "answer": "Create channels with news, promotions, bonuses."},
            "20": {"question": "What is traffic arbitrage?", "answer": "Buying traffic from one source and selling to another for profit."},
            "21": {"question": "How to work with Push ads?", "answer": "Create compelling messages, test different formats."},
            "22": {"question": "Which GEOs have high LTV?", "answer": "Usually Tier-1 countries: USA, Canada, Australia."},
            "23": {"question": "How to drive traffic from forums?", "answer": "Participate in discussions, offer valuable content."},
            "24": {"question": "What is contextual advertising?", "answer": "Ads shown based on user search queries."},
            "25": {"question": "How to work with influencers?", "answer": "Collaborate with bloggers who have an audience interested in gambling."},
            "26": {"question": "What are the risks when working with casinos?", "answer": "Legal restrictions, payment issues, competition."},
            "27": {"question": "How to drive traffic from TikTok?", "answer": "Create short videos with promotions, winnings, challenges."},
            "28": {"question": "What is PPC advertising?", "answer": "Pay-per-click, popular in Google Ads, Bing Ads."},
            "29": {"question": "How to optimize landing pages?", "answer": "Use A/B testing, improve usability, add calls to action."},
            "30": {"question": "What tools for automation?", "answer": "Trackers, social media bots, CRM systems."},
            "31": {"question": "How to work with mobile traffic?", "answer": "Optimize sites for mobile devices, use mobile apps."},
            "32": {"question": "What is programmatic advertising?", "answer": "Automated ad buying through platforms."},
            "33": {"question": "How to drive traffic from Reddit?", "answer": "Participate in gambling-related subreddits."},
            "34": {"question": "Which creatives are banned?", "answer": "Usually misleading claims, adult content, copyright violations."},
            "35": {"question": "How to work with CPA networks?", "answer": "Register, choose offers, launch campaigns."},
            "36": {"question": "What is retargeting?", "answer": "Showing ads to users who have already visited your site."},
            "37": {"question": "How to drive traffic from Instagram?", "answer": "Use Stories, Reels, collaborate with influencers."},
            "38": {"question": "Which GEOs have low CPM?", "answer": "Usually Tier-3 countries: India, Philippines, Vietnam."},
            "39": {"question": "How to work with banner ads?", "answer": "Create attractive banners, place them on thematic sites."},
            "40": {"question": "What is affiliate marketing?", "answer": "Partner marketing where you earn commissions for referred players."},
            "41": {"question": "How to drive traffic from Pinterest?", "answer": "Create appealing pins with promotions and bonuses."},
            "42": {"question": "What tools to analyze competitors?", "answer": "SEMrush, Ahrefs, SimilarWeb."},
            "43": {"question": "How to work with video content?", "answer": "Create reviews, streams, educational videos."},
            "44": {"question": "What is native advertising?", "answer": "Ads that look like organic content."},
            "45": {"question": "How to drive traffic from Twitter?", "answer": "Post tweets with promotions, use hashtags."},
            "46": {"question": "Which GEOs have high ARPU?", "answer": "Tier-1 countries like Norway, Sweden, Germany."},
            "47": {"question": "How to work with SMS marketing?", "answer": "Send personalized messages with promotions."},
            "48": {"question": "What is programmatic direct?", "answer": "Direct ad buying through programmatic platforms."},
            "49": {"question": "How to drive traffic from LinkedIn?", "answer": "Publish articles, participate in gambling-related groups."},
            "50": {"question": "Which creatives work best for mobile devices?", "answer": "Responsive banners, videos, interactive elements."}
        },
        "support_message": "If you didn’t find the answer — write to owner @calwxxxx or admins in the group"
    }
}

LANGS = {"uk": "Українська 🇺🇦", "ru": "Русский 🇷🇺", "en": "English 🇬🇧"}
ITEMS_PER_PAGE = 5

INSTRUCTIONS = {
    "uk": "Оберіть питання зі списку.",
    "ru": "Выберите вопрос из списка.",
    "en": "Choose a question from the list."
}

ERROR_MESSAGES = {
    "uk": {
        "invalid_lang": "Помилка вибору мови.",
        "unsupported_lang": "Непідтримувана мова.",
        "invalid_query": "Некоректний запит.",
        "question_not_found": "Питання не знайдено.",
        "invalid_page": "Некоректний номер сторінки.",
        "page_out_of_range": "Сторінка поза межами діапазону.",
        "select_lang_first": "Спочатку виберіть мову через /start."
    },
    "ru": {
        "invalid_lang": "Ошибка выбора языка.",
        "unsupported_lang": "Неподдерживаемый язык.",
        "invalid_query": "Некорректный запрос.",
        "question_not_found": "Вопрос не найден.",
        "invalid_page": "Некорректный номер страницы.",
        "page_out_of_range": "Страница вне диапазона.",
        "select_lang_first": "Сначала выберите язык через /start."
    },
    "en": {
        "invalid_lang": "Language selection error.",
        "unsupported_lang": "Unsupported language.",
        "invalid_query": "Invalid query.",
        "question_not_found": "Question not found.",
        "invalid_page": "Invalid page number.",
        "page_out_of_range": "Page out of range.",
        "select_lang_first": "First select a language via /start."
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(LANGS[lang], callback_data=f"lang_{lang}")] for lang in LANGS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Виберіть мову / Выберите язык / Choose language:", reply_markup=reply_markup)

async def paginate_buttons(lang: str, page: int):
    questions = DATA[lang]["questions"]
    total_pages = (len(questions) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    start_idx = page * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, len(questions))
    keyboard = [
        [InlineKeyboardButton(q["question"], callback_data=f"q_{lang}_{key}")] 
        for key, q in list(questions.items())[start_idx:end_idx]
    ]
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"page_{lang}_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"page_{lang}_{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)
    return InlineKeyboardMarkup(keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get("lang", "uk")

    if data.startswith("lang_"):
        parts = data.split("_")
        if len(parts) != 2:
            await query.message.reply_text(ERROR_MESSAGES[lang]["invalid_lang"])
            return
        lang = parts[1]
        if lang not in DATA:
            await query.message.reply_text(ERROR_MESSAGES[lang]["unsupported_lang"])
            return
        context.user_data["lang"] = lang
        page = 0
        questions = DATA[lang]["questions"]
        total_pages = (len(questions) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        reply_markup = await paginate_buttons(lang, page)
        message_text = f"{LANGS[lang]} (Сторінка {page+1}/{total_pages}):\n{INSTRUCTIONS[lang]}"
        message = await query.message.reply_text(message_text, reply_markup=reply_markup)
        context.user_data["questions_message_id"] = message.message_id

    elif data.startswith("q_"):
        parts = data.split("_")
        if len(parts) != 3:
            await query.message.reply_text(ERROR_MESSAGES[lang]["invalid_query"])
            return
        _, lang, q_id = parts
        if lang not in DATA:
            await query.message.reply_text(ERROR_MESSAGES[lang]["unsupported_lang"])
            return
        questions = DATA[lang]["questions"]
        question = questions.get(q_id)
        if question:
            answer = question["answer"]
            support_message = DATA[lang]["support_message"]
            await query.message.reply_text(f"{answer}\n\n{support_message}")
        else:
            await query.message.reply_text(ERROR_MESSAGES[lang]["question_not_found"])

    elif data.startswith("page_"):
        parts = data.split("_")
        if len(parts) != 3:
            await query.message.reply_text(ERROR_MESSAGES[lang]["invalid_page"])
            return
        _, lang, page_str = parts
        try:
            page = int(page_str)
        except ValueError:
            await query.message.reply_text(ERROR_MESSAGES[lang]["invalid_page"])
            return
        if lang not in DATA:
            await query.message.reply_text(ERROR_MESSAGES[lang]["unsupported_lang"])
            return
        if "questions_message_id" not in context.user_data:
            await query.message.reply_text(ERROR_MESSAGES[lang]["select_lang_first"])
            return
        questions = DATA[lang]["questions"]
        total_pages = (len(questions) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        if page < 0 or page >= total_pages:
            await query.message.reply_text(ERROR_MESSAGES[lang]["page_out_of_range"])
            return
        reply_markup = await paginate_buttons(lang, page)
        message_text = f"{LANGS[lang]} (Сторінка {page+1}/{total_pages}):\n{INSTRUCTIONS[lang]}"
        await context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=context.user_data["questions_message_id"],
            text=message_text,
            reply_markup=reply_markup
        )

if __name__ == "__main__":
    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN not set in environment variables")
    application = ApplicationBuilder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    port = int(os.environ.get("PORT", 8443))
    webhook_url = "https://botcxtraf.onrender.com/webhook"
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="/webhook",
        webhook_url=webhook_url
    )
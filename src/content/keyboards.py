reserved_buttons = {
    "main_menu_button": {
        "emoji": "🏠",
        "ua": "Головне меню",
        "ru": "Главное меню",
        "en": "Main menu"
    },
    "next_page_button": {
        "emoji": "➡️",
        "ua": "Вперед",
        "ru": "Вперед",
        "en": "Next"
    },
    "previous_page_button": {
        "emoji": "⬅️",
        "ua": "Назад",
        "ru": "Назад",
        "en": "Back"
    }
}

keyboards = [
    {
        "language_keyboard": [
            {
                "localized": False,
                "paginated": False
            },
            [
                {
                    "ua": {
                        "emoji": "🇺🇦",
                        "text": "Українська"
                    },
                    "ru": {
                        "emoji": "️🏳️",
                        "text": "Русский"
                    },
                    "en": {
                        "emoji": "🇬🇧",
                        "text": "English"
                    }
                }
            ]
        ],
        "confirm_keyboard": [
            {
                "localized": True,
                "paginated": False
            },
            [
                {
                    "confirm": {
                        "emoji": "✅",
                        "ua": "Так",
                        "ru": "Да",
                        "en": "Yes"
                    },
                    "cancel": {
                        "emoji": "❌",
                        "ua": "Ні",
                        "ru": "Нет",
                        "en": "No"
                    }
                }
            ]
        ],
        "main_keyboard": [
            {
                "localized": True,
                "paginated": False
            },
            [
                {
                    "profile_button": {
                        "emoji": "👤",
                        "ua": "Профіль",
                        "ru": "Профиль",
                        "en": "Profile"
                    },
                    "notifications_button": {
                        "emoji": "🔔",
                        "ua": "Повідомлення",
                        "ru": "Уведомления",
                        "en": "Notifications"
                    },
                    "info_button": {
                        "emoji": "ℹ️",
                        "ua": "Інформація",
                        "ru": "Информация",
                        "en": "Information"
                    },
                    "admin_menu_button": {
                        "emoji": "👑",
                        "ua": "Адміністрування",
                        "ru": "Администрирование",
                        "en": "Administration"
                    }
                }
            ]
        ],
        "admin_keyboard": [
            {
                "localized": True,
                "paginated": True,
                "individual_buttons": [
                    "main_menu_button",
                    "next_page_button",
                    "previous_page_button"
                ]
            },
            [
                {
                    1: {
                        "manage_users_button": {
                            "emoji": "👥",
                            "ua": "Користувачі",
                            "ru": "Пользователи",
                            "en": "Users"
                        },
                        "bot_settings_button": {
                            "emoji": "⚙️",
                            "ua": "Налаштування бота",
                            "ru": "Настройки бота",
                            "en": "Bot settings"
                        },
                        "next_page_button": reserved_buttons["next_page_button"],
                        "main_menu_button": reserved_buttons["main_menu_button"]
                    },
                    2: {
                        "mailing_menu_button": {
                            "emoji": "✉️",
                            "ua": "Створити розсилку",
                            "ru": "Сделать рассылку",
                            "en": "Create mailing"
                        },
                        "analytics_menu_button": {
                            "emoji": "📊",
                            "ua": "Аналітика",
                            "ru": "Аналитика",
                            "en": "Analytics"
                        },
                        "previous_page_button": reserved_buttons["previous_page_button"],
                        "main_menu_button": reserved_buttons["main_menu_button"]
                    }
                }
            ]
        ]
    }
]

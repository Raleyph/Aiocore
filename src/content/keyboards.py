
# RESERVED BUTTONS

main_menu_button = {
    "emoji": "🏠",
    "ua": "Головне меню",
    "ru": "Главное меню",
    "en": "Main menu"
}

next_page_button = {
    "emoji": "➡️",
    "ua": "Вперед",
    "ru": "Вперед",
    "en": "Next"
}

previous_page_button = {
    "emoji": "⬅️",
    "ua": "Назад",
    "ru": "Назад",
    "en": "Back"
}

# KEYBOARDS

set_language_keyboard = [
    {
        "keyboard_name": "set_language_keyboard",
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
]

confirm_keyboard = [
    {
        "keyboard_name": "confirm_keyboard",
        "localized": True,
        "paginated": False
    },
    [
        {
            "confirm_button": {
                "emoji": "✅",
                "ua": "Так",
                "ru": "Да",
                "en": "Yes"
            },
            "cancel_button": {
                "emoji": "❌",
                "ua": "Ні",
                "ru": "Нет",
                "en": "No"
            }
        }
    ]
]

main_keyboard = [
    {
        "keyboard_name": "main_keyboard",
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
            "information_button": {
                "emoji": "ℹ️",
                "ua": "Інформація",
                "ru": "Информация",
                "en": "Information"
            },
            "notifications_button": {
                "variables": [
                    "notifications_count"
                ],

                "emoji": "🔔",
                "ua": "Повідомлення {notifications_count}",
                "ru": "Уведомления {notifications_count}",
                "en": "Notifications {notifications_count}"
            }
        }
    ]
]

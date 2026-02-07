from functools import wraps


def safe_handler(bot):
    """
    Декоратор, который ловит все исключения и отправляет пользователю сообщение.
    Используется как @safe_handler(bot)
    """
    def decorator(func):
        from functools import wraps
        @wraps(func)
        def wrapper(message, *args, **kwargs):
            try:
                return func(message, *args, **kwargs)
            except Exception as e:
                # Отправляем пользователю
                try:
                    bot.reply_to(
                        message,
                        "⚠ Произошла непредвиденная ошибка при обработке вашей команды.\n"
                        "Пожалуйста, свяжитесь с разработчиком.\n"
                        f"[ERROR] Ошибка в {func.__name__}: {e!r}"
                    )
                except Exception as inner:
                    print(f"[CRITICAL] Не удалось отправить сообщение пользователю: {inner!r}")

                # Логируем ошибку
                print(f"[ERROR] Ошибка в {func.__name__}: {e!r}")
                import traceback
                traceback.print_exc()
        return wrapper
    return decorator

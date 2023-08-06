from loguru import logger


def show_step_info(func, selected):
    selected = True

    def deco():
        if selected:
            logger.info(f'Running {func.__name__}')
        else:
            logger.info(f'Skipping {func.__name__}')

    return deco

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.log(level=logging.INFO, msg=f'Starting program')
while True:
    weight = float(input('Weight: '))
    if weight == 1:
        logger.log(level=logging.INFO, msg=f'Exiting program')
        break
    logger.log(level=logging.INFO, msg=f'Weight is {weight}')
    height = float(input('Height: '))
    logger.log(level=logging.INFO, msg=f'Height is {height}')

    bmi = weight / height**2
    logger.log(level=logging.INFO, msg=f'BMI is {int(bmi)}%')


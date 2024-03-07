from src.selenium_script import Flujo
import sys

with Flujo() as bot:
    bot.flujo_decretos(input_fecha_inicio=sys.argv[1],input_fecha_fin=sys.argv[2])
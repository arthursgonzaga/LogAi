import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

LOG_PROMPT = """
    Gere um arquivo .log com 1.000.000 linhas. Não um código para gerar as linhas.
    Cada linha deve conter uma mensagem de log aleatória referente a um sistema de pagamentos.
    Esse log deve conter informações sobre o serviço (como uma query lenta de um banco) ou throttling, ou seja, algo que o desenvolvedor deve se preocupar, mas não sobre a transação.
    Cada linha segue o formato timestamp | log_level | message, facilitando a análise de registros específicos. O formato de log pode ser o seguinte:
    2024-11-08 10:00:00 INFO User admin logged in
    2024-11-08 10:01:20 ERROR Failed to connect to database
    2024-11-08 10:02:15 DEBUG Query executed in 120ms
    2024-11-08 10:05:30 INFO User admin accessed dashboard
    2024-11-08 10:10:00 WARN Connection pool running low
    O formato de saida deve ser um arquivo .log, somente com textos e cada linha deve ser uma mensagem de log aleatória.
"""

class LogGenerator:
    def __init__(self, model='gpt-4o', log_file_path='logs/app.log'):
        self.model = model
        self.log_file_path = log_file_path
        self.open_ai_client = OpenAI()

    def generate_log(self, prompt):
        logger.info("Generating log...")
        if not prompt:
            logger.error("Prompt is empty.")
            return None
        response = self.open_ai_client.responses.create(
            model=self.model,
            input=prompt
        )
        if not response.output_text:
            logger.error("No output text received from OpenAI API.")
            return None
        logger.info("Log generated successfully.")
        return response.output_text

    def save_log(self, log_data):
        with open(self.log_file_path, 'w') as log_file:
            log_file.write(log_data)
        logger.info(f"Log saved to {self.log_file_path}")

    def generate_and_save_log(self, prompt):
        log_data = self.generate_log(prompt)
        self.save_log(log_data)

if __name__ == "__main__":
    log_generator = LogGenerator()
    log_generator.generate_and_save_log(LOG_PROMPT)
    logger.info("Log generation process completed.")
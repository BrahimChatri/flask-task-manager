import logging

# Create a formatter for both info and error logs
logging_format = logging.Formatter("[%(asctime)s | %(name)s] %(message)s")
second_format = logging.Formatter("-> %(message)s")

# Log handler for writing logs to /tmp/logs.log (Vercel allows writing to /tmp)


# Stream handler to output logs to console (visible in Vercel logs)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(second_format)

# Setting up the Info logger
Info_logger = logging.getLogger("INFO")
Info_logger.setLevel(logging.INFO)  # INFO level is 20

Info_logger.addHandler(stream_handler)

# Setting up the Error logger
Error_logger = logging.getLogger("ERROR")
Error_logger.setLevel(logging.ERROR)  # ERROR level is 40
Error_logger.addHandler(stream_handler)

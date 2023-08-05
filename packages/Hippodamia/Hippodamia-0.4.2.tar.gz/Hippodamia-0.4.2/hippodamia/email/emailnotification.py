import pprint
from hippodamia.email.sendemail import SendEmail
from hippodamia.email.digest import Digest
from hippodamia.email.minimal import Minimal
from hippodamia.email.spontaneous import Spontaneous
from pelops.logging.mylogger import get_child


class EmailNotification:
    _config = None
    _logger = None
    _send_email = None

    _spontaneous = None
    _digest = None
    _minimal = None

    def __init__(self, config, logger, mqtt_client, agentshadows, heartbeat, hierarchical_view, onboarding, archive,
                 agentfactory):
        self._config = config
        self._logger = get_child(logger, self.__class__.__name__)
        self._logger.info("__init__ - begin")

        self._send_email = SendEmail(self._config["config"], self._logger)

        try:
            self._digest = Digest(self._config["digest"], self._send_email.send_message, self._logger, mqtt_client,
                                  agentshadows, heartbeat, hierarchical_view, onboarding, archive)
        except KeyError:
            self._logger.info("Digest is deactivated")

        try:
            self._minimal = Minimal(self._config["minimal"], self._send_email.send_message, self._logger, mqtt_client,
                                    agentshadows, heartbeat, hierarchical_view, onboarding, archive)
        except KeyError:
            self._logger.info("Minimal is deactivated")

        try:
            self._spontaneous = Spontaneous(self._config["spontaneous"], self._send_email.send_message, self._logger,
                                            agentshadows, agentfactory)
        except KeyError:
            self._logger.info("Spontaneous is deactivated")

        if self._digest is None and self._spontaneous is None and self._minimal is None:
            self._logger.error("Digest, Minimal, and Spontaneous are deactived - at least one must be set.")
            raise RuntimeError("Digest, Minimal, and Spontaneous are deactived - at least one must be set.")

        self._logger.info("__init__ - completed")

    def send_digest(self):
        self._logger.info("send_digest manually triggered.")
        if self._digest is not None:
            self._digest.send_message()
            return "digest email notification sent."
        else:
            return "digest email notification not activated."

    def send_minimal(self):
        self._logger.info("send_minimal manually triggered.")
        if self._minimal is not None:
            self._minimal.send_message()
            return "minimal email notification sent."
        else:
            return "minimal email notification not activated."

    def start(self):
        self._logger.info("start - begin")
        if self._digest is not None:
            self._digest.start()
        if self._minimal is not None:
            self._minimal.start()
        if self._spontaneous is not None:
            self._spontaneous.start()
        self._logger.info("start - completed")

    def stop(self):
        self._logger.info("stop - begin")
        if self._digest is not None:
            self._digest.stop()
        if self._minimal is not None:
            self._minimal.stop()
        if self._spontaneous is not None:
            self._spontaneous.stop()
        self._logger.info("stop - completed")

    def get_stats(self):
        stats = {
            "sendemail": self._send_email.get_stats()
        }
        if self._digest is not None:
            stats["digest"] = self._digest.get_stats()
        if self._minimal is not None:
            stats["minimal"] = self._minimal.get_stats()
        if self._spontaneous is not None:
            stats["spontaneous"] = self._spontaneous.get_stats()
        return stats

    def get_string_stats(self):
        text = "stats:\n"
        text += pprint.pformat(self.get_stats(), indent=4)
        return text

import pprint
from hippodamia.enums import ViewDetails
from hippodamia.enums import StatType
from hippodamia.email.ainfo import AInfo


class Digest(AInfo):
    def _render_body(self):
        message  = "<h1>Hierarchical View</h1>\n"
        message += "<pre>{}</pre>\n".format(self._hierarchical_view.pformat(details=ViewDetails.FULL))

        message += "<h1>Micro-Service Overview</h1>\n"
        keys = list(self._agentshadows.keys())
        keys.sort()
        for k in keys:
            microservice = self._agentshadows[k]
            message += "<h2>[{}] {}</h2>\n".format(microservice.properties.gid, microservice.properties.name)
            message += "<pre>{}</pre>\n".format(microservice.get_string_stats(StatType.GENERAL))

        message += "<h1>Micro-Service Archive</h1>\n"
        if len(self._archive) == 0:
            message += "<div>Archive is empty.</div>\n"
        else:
            message = "<ul>\n"
            for microservice in self._archive:
                message += " <li>[{}] {}</li>\n".format(microservice.properties.gid, microservice.properties.name)
            message += "</ul>\n"

        message += "<h1>Heartbeat</h1>\n"
        message += "<pre>{}</pre>\n".format(self._heartbeat.get_string_stats())

        message += "<h1>Onboarding</h1>\n"
        message += "<pre>{}</pre>\n".format(self._onboarding.get_string_stats())

        message += "<h1>MQTT</h1>\n"
        message += "<div>mqtt client connection active: <div>{}</div>\n".format(self._mqtt_client.is_connected.is_set())
        message += "<h2>active subscriptions</h2>\n"
        message += "<ul>\n"
        for sub, func in self._mqtt_client.subscribed_topics().items():
            message += " - {}: [{}]\n".format(sub, func)
        message += "</ul>\n"
        message += "<h2>send/receive statistics</h2>\n"
        message += "<pre>{}</pre>\n".format(pprint.pformat(self._mqtt_client.stats.get_stats(), indent=2))

        return message

from hippodamia.email.ainfo import AInfo


class Minimal(AInfo):
    def _render_body(self):
        message = "<h1>List of Micro-Services</h1>\n"
        message += "<ul>\n"
        for gid, shadow in self._agentshadows.items():
            message += "<li>{} {} {} {}</li>\n".format(shadow.properties.name, shadow.properties.health.name,
                                                       shadow.get_state_id().name, gid)
        message += "</ul>\n"
        return message

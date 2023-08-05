import OUtils.configurations
import OUtils.Kafka.metrics as metrics
import OUtils.Kafka.checks as checks


def get_nodes(port=False):
    result = []
    nodes = OUtils.configurations.get(module="kafka", key="nodes")

    for node in nodes:
        if port is False:
            result.append(node["host"])

        elif port not in node["ports"]:
            raise KeyError("Port '%s' not supported" % port)

        else:
            result.append("%s:%d" % (node["host"], node["ports"][port]))

    assert len(result) >= 3, "Too few nodes (%s) loaded. Please check configuration file." % len(result)

    return result


def get_configuration_files():
    result = OUtils.configurations.get(module="kafka", key="configuration_files")

    assert len(result) > 0, "Too few (%d) configuration files loaded. Please check configurations file." % len(result)

    return result

import re

from prometheus_client.core import GaugeMetricFamily


METRIC_INVALID_CHARS = re.compile(r'[^a-zA-Z0-9_:]')
METRIC_INVALID_START_CHARS = re.compile(r'^[^a-zA-Z_:]')
LABEL_INVALID_CHARS = re.compile(r'[^a-zA-Z0-9_]')
LABEL_INVALID_START_CHARS = re.compile(r'^[^a-zA-Z_]')
LABEL_START_DOUBLE_UNDER = re.compile(r'^__+')


def format_label_key(label_key):
    """
    Construct a label key.

    Disallowed characters are replaced with underscores.
    """
    label_key = LABEL_INVALID_CHARS.sub('_', label_key)
    label_key = LABEL_INVALID_START_CHARS.sub('_', label_key)
    label_key = LABEL_START_DOUBLE_UNDER.sub('_', label_key)
    return label_key


def format_label_value(*values):
    """
    Construct a label value.

    If multiple value components are provided, they are joined by underscores.
    """
    return '_'.join(values)


def format_metric_name(*names):
    """
    Construct a metric name.

    If multiple name components are provided, they are joined by underscores.
    Disallowed characters are replaced with underscores.
    """
    metric = '_'.join(names)
    metric = METRIC_INVALID_CHARS.sub('_', metric)
    metric = METRIC_INVALID_START_CHARS.sub('_', metric)
    return metric


def group_metrics(metrics):
    """
    Groups metrics with the same name but different label values.

    Takes metrics as a list of tuples containing:
    * metric name,
    * metric documentation,
    * dict of label key -> label value,
    * metric value.

    The metrics are grouped by metric name. All metrics with the same metric
    name must have the same set of label keys.

    A dict keyed by metric name is returned. Each metric name maps to a tuple
    containing:
    * metric documentation
    * label keys tuple,
    * dict of label values tuple -> metric value.
    """

    metric_dict = {}
    for (metric_name, metric_doc, label_dict, value) in metrics:
        curr_label_keys = tuple(label_dict.keys())

        if metric_name in metric_dict:
            label_keys = metric_dict[metric_name][1]
            assert set(curr_label_keys) == set(label_keys), \
                'Not all values for metric {} have the same keys. {} vs. {}.'.format(
                    metric_name, curr_label_keys, label_keys)
        else:
            label_keys = curr_label_keys
            metric_dict[metric_name] = (metric_doc, label_keys, {})

        label_values = tuple([label_dict[k] for k in label_keys])

        metric_dict[metric_name][2][label_values] = value

    return metric_dict


def gauge_generator(metrics):
    """
    Generates GaugeMetricFamily instances for a list of metrics.

    Takes metrics as a list of tuples containing:
    * metric name,
    * metric documentation,
    * dict of label key -> label value,
    * metric value.

    Yields a GaugeMetricFamily instance for each unique metric name, containing
    children for the various label combinations. Suitable for use in a collect()
    method of a Prometheus collector.
    """
    metric_dict = group_metrics(metrics)

    for metric_name, (metric_doc, label_keys, value_dict) in metric_dict.items():
        # If we have label keys we may have multiple different values,
        # each with their own label values.
        if label_keys:
            gauge = GaugeMetricFamily(metric_name, metric_doc, labels=label_keys)

            for label_values in sorted(value_dict.keys()):
                value = value_dict[label_values]
                gauge.add_metric(label_values, value)

        # No label keys, so we must have only a single value.
        else:
            gauge = GaugeMetricFamily(metric_name, metric_doc, value=list(value_dict.values())[0])

        yield gauge

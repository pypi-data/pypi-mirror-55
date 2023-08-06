### CDP Resiliency Experiment Report
#### {{today}}

### Experiment Title: *{{experiment.title}}*
### Description: *{{experiment.description}}*

### Summary

{% if export_format != "pdf" %}
{{experiment.title}}

{{experiment.description}}
{% endif %}

|                               |                     |
| ----------------------------- | ------------------- |
| **Microservice**              | {{experiment.configuration.service_name}} |
| **Fault Type**                | {{experiment.title}} |
| **Status**                    | {{status}} |
| **Instance**                  | {{node}} |
| **Platform**                  | {{platform}} |
| **Started**                   | {{start | pretty_date}} |
| **Completed**                 | {{end | pretty_date}} |
| **Duration**                  | {{pretty_duration(start, end)}} |
| **Tags**                    | {% for tag in experiment.tags %}{% if loop.last %}{{tag}}{% else %}{{tag}}, {% endif %}{% endfor %} |

### Experiment Details

------------


The resiliency experiment {{experiment.title}} was made of {{num_actions}} actions, to vary conditions in the CDP system, and {{num_probes}} probes to collect objective data from the system during the experiment.

#### Steady State

------------


	{% if not hypo %} No steady-state was defined in this experiment. This run was exploratory.
	{% else %}
	The steady state(health check) this experiment tried was: &ldquo;**{{hypo.title}}**&rdquo;.
	{% endif %}

- ##### Before the experiment

	The steady state was {%if steady_states.before.steady_state_met %} verified {% else %} not verified. {% endif %}

    {% for probe in steady_states.before.probes %}

    |   |   |
    | ------------ | ------------ |
    | **Probe**                     | {{probe.activity.name}} |
    | **Status**                    | {{probe.tolerance_met}} |
    | **Expected**                  | {{probe.activity.tolerance}}  |

    {% endfor %}

- ##### After the experiment

	The steady state was {%if steady_states.after.steady_state_met %} verified {% else %} not verified. {% endif %}

    {% for probe in steady_states.before.probes %}

    |                               |                     |
    | ----------------------------- | ------------------- |
    | **Probe**                     | {{probe.activity.name}} |
    | **Status**                    | {{probe.tolerance_met}} |
    | **Expected**                  | {{probe.activity.tolerance}}  |

    {% endfor %}

#### Sequence of Activities conducted as part of experiment

------------

{% for activity in experiment.method %}

|  Type      | Name                                                           |
| ---------- | --------------------------------------------------------------- |
| {{activity.type}} | {{activity.name}} |

{% endfor %}

### Result

------------


The experiment was conducted on {{start|pretty_date}} and lasted roughly
{{pretty_duration(start, end)}}. Detailed results of each action/probe present in the sequence is described below.

Alternatively, view the results on Splunk dashboard:   [Splunk dashboard]({{experiment.configuration.splunk_dashboard}} "Splunk dashboard")


{% for item in run %}

#### {{item.activity.type | title}}: *{{item.activity.name}}*

|                       |               |
| --------------------- | ------------- |
| **Status**            | {{item.status}} |
| **Background**        | {{item.activity.get("background", False)}} |
| **Started**           | {{item.start | pretty_date}} |
| **Ended**             | {{item.end | pretty_date}} |
| **Duration**          | {{pretty_duration(item.start, item.end)}} | {% if item.activity.get("pauses", {}).get("before") %}
| **Paused Before**     | {{item.activity.pauses.before}}s | {% endif %} | {% if item.activity.get("pauses", {}).get("after") %}
| **Paused After**      | {{item.activity.pauses.after}}s |{% endif %}

The *{{item.activity.type}}* returned the following result:

```javascript
{{item.output | pprint}}
```

{% if item.exception %}
The *{{item.activity.name}}* {{item.activity.type}} raised the following error
while running:

{% if export_format == "pdf" %}

```python
{{item.exception|join|wordwrap(70, break_long_words=False)}}
```

{% else %}

```python
{{item.exception|join}}
```

{% endif %}
{% endif %}

{%if item.text %}

  {% if export_format not in ["html", "html5"] %}

```python
{{item.text}}
```

  {% else %}
<figure>
    {{item.text}}
</figure>
  {% endif %}
{% endif %}

{%if item.charts %}
{% for chart in item.charts %}
  {% if export_format not in ["html", "html5"] %}
![](data:image/png;base64,{{chart}})
\

  {% else %}
<figure>
    {{chart}}
</figure>
  {% endif %}
  {% endfor %}
{% endif %}

{% endfor %}

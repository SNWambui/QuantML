### Metrics to measure

- Sharpe ratio
- Calmar ratio

```python
graph = fig.to_html(full_html=False, default_height=500, default_width=700)
context = {'graph': graph}
response = render(request, 'graph.html', context)

{% if graph %}
{{ graph|safe }}
{% else %}
<p>No graph was provided.</p>
{% endif %}
```

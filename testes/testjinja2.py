from jinja2 import Template
html="""
<table style="width:100%">
{% for boxtype, caption in content %}
 <tr>
   <td>
   {% if boxtype=='info' %}
    <i class="fas fa-info fa-2x"  style="color: #0066ff;"></i>
   {% endif %}
   </td>
   <td>
    {{ caption }}
    boxtype: {{ boxtype }}
    caption: {{ caption }}
   </td>
 </tr>
{% endfor %}
</table>"""


content=[('info','Depender do tempo não implica que o circuito possui um sinal de _clock_, apesar disso ser verdadeiro na maioria das vezes.'),]

template = Template(html)
print(template.render(content=content))

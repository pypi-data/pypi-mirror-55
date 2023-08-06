@prefix atom: <http://lv2plug.in/ns/ext/atom#> .
@prefix lv2: <http://lv2plug.in/ns/lv2core#> .
@prefix pset: <http://lv2plug.in/ns/ext/presets#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix state: <http://lv2plug.in/ns/ext/state#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

{% for bank in banks %}
<{{plugin_name}}_bank_{{bank}}>
	a pset:bank ;
	lv2:appliesTo <{{plugin_url}}> ;
	rdfs:label "{{bank}}" .
{% end %}

{% for preset in presets %}
<{{preset['bank']}}_{{preset['name']}}.ttl>
	a pset:Preset ;
	pset:bank <{{plugin_name}}_bank_{{preset['bank']}}> ;
	rdfs:seeAlso <{{preset['bank']}}_{{preset['name']}}.ttl> ;
	lv2:appliesTo <{{plugin_url}}> .
{% end %}

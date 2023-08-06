@prefix atom: <http://lv2plug.in/ns/ext/atom#> .
@prefix lv2: <http://lv2plug.in/ns/lv2core#> .
@prefix pset: <http://lv2plug.in/ns/ext/presets#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix state: <http://lv2plug.in/ns/ext/state#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<{{bank}}_{{name}}.ttl>
	a pset:Preset ;
	lv2:appliesTo <{{ plugin_url }}> ;
	rdfs:label "{{ name }}" ;
	lv2:port{% set i = 1 %}{% for k in ports %} [
		lv2:symbol "{{ k }}" ;
		pset:value {{ ports[k] }}
	] {{ "," if len(ports)>i else "." }}{% set i=i+1 %}{% end %}

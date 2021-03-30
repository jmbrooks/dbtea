General Methods to Create LookML View from dbt:

- Within dbt...
    - dbt simple macro (most basic, no descriptions though... just a nice template)
    - dbt macro with info schema reading (relies on persist_docs: true... which I think most ppl do)
    - Limitations - can't grab PK

- OR outside dbt...
    - Read YAML file for defined model
    - dbt codegen united with existing models file
    - Read dbt artifacts for node details: alias, db and schema, create programmatically
    - Advanced: hook up to each repo, immutable folder for LookML views, push based on auto-generated PR or on set
    cadence, maybe CI pipeline when new dbt release goes out
- Theme: connectivity between dbt and Looker

Challenges:
  - Data type handling
  - Looker's more advanced stuff, like dimension_groups

Cool ideas:
  - Allow meta to be used to pass LookML params to dimensions, hide fields, set fields as metrics, etc.

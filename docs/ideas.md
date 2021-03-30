# Roadmap

## Core

### Productivity & Properties Automation

- Bulk codegen
    - Automatically generate new source, and base model for all tables in source
    - KEY: Maintain later on? Perhaps check if source matches base model? Won't work exactly, but perhaps some method to
    either monitor or push changes from source table changes (e.g. column addition) to base models
    - Automatically create model YAML for all models in directory (once finished base model stuff); need to append to
    one file
    - KEY: Maintain as well, take new column outputs from model views, compare against existing YAML, and either notify
    or potentially edit the file to include new column(s), perhaps on set schedule?

- Automatic bulk rules
    - Allow for automatic rules, for example, Anytime see certain column (i.e. _fivetran_synced) apply description from
    a docs.md file to it upon bulk codegen, and certain tests

- Ad-Hoc Tasks
    - Compare dbt relations to warehouse, identify warehouse objects no longer in dbt
    - Retry failed and skipped dbt components from last run; run all models that have changed

- Dry Runs
    - Run a dry run, so compile all objects and then dry run it (db-dependent; BigQuery has feature for it, Snowflake we
    would use Explain to basically do it) to be sure all SQL (or that of selected files) is valid

- Views into dbt run data for analytics (Looker section for more details)

### QA and dbt Project Health

- Test coverage
    - Determine what percentage of models have defined properties
    - What percentage of models have descriptions
    - Percentage of description coverage, test coverage
    - That every model has at least one column with unique and not null tests applied (PK test)

- Data Warehouse Design
    - Confirm all tables registered as dim tables (i.e. tag, meta, or _maybe_ naming convention to identify) have 
    not_null tests on all columns
    - Foreign keys in facts not null
    - Maybe configure a series of generic rules, which can be applied
    - Enforce certain columns are included (and perhaps have certain behavior) for all tables in a path (e.g. all mart
    tables must have an `inserted_at` column that is not_null, and a column ending with `_key` that is a PK)
    
- Test coverage overrides
    - For tests above, allow user option specify a tag/meta to override certain test(s), probably by applying a tag or
    comment that we can scan for to ignore that one

- Enforce behavior at model level
    - Example, for all resources tagged/meta'd a certain way, they must have a block to test if target is dev (i.e. to
    limit data processed in dev)
    - Quick tests, such as the one above, which someone doing QA can run when reviewing a PR (or is automated)
    
### Admin

- Lens into full system (probably visual, monitoring dashboard)
    - Use logs from extract and load tool, dbt, warehouse and BI tool (Looker) to understand full pipeline
    - Look at data freshness, last models run time, monitor length of runs, last push of dbt metadata to Looker, any 
    PDTs in Looker which should be queued for productionization in dbt, historical dbt tests results
    - Historical frequency of when each snapshot table had the snapshot command run against it
    - Usage by team and target

- Project-level Behavior Oversight (similar to coverage tests from QA, but higher level)
    - Ability to set project-level rules about materializations (i.e. all staging files, besides list of exceptions,
    should be views)
    - All sources should have docs, freshness tests, and certain set of meta tags
    - Model files in certain directories should match regex pattern
    - View dbt test result of PR from that dev user's results when reviewing PR automatically

## BI

### Looker

- Pass dbt descriptions to Looker
    - Need to a) find the model properties, b) 
    - Need to handle for multi-line descriptions
    - For now, create a standard clean LookML view, perhaps allow someone to BYOT (bring your own template) for LookML
    views files in the future
    - KEY: Able to pass correct data type to Looker type, emulate Looker's create view behavior
    - More managed state: pull down Looker project(?), confirm files that need changes and push/open PR
    - For managed: maybe also do things like allow a Looker config file in dbt project, for certain top-level params
    and choices on the Looker project (default datagroup, attach datagroups to freshness tests (and refresh cache when
    new data arrives?), manifest file & constants, model file(s) and names)
    
- Manage LookML views (based on meta? tags?)
    - Example: Define some fields as measure(s), drill field sets, label
- Add LookML components to dimensions/measures/etc. (based on meta? tags?)
    - Example: access grants (list of required access grants for some view, dimension, measure, join?, explore?)
    - So many examples here, maybe allow arbitrary, or confirm against allowed list (if wanna maintain)
    - hidden, drilling, value_format_name
    
- Manage Looker Explores (based on exposures?)
    - Idea is we can specify which fact/dim tables are related, construct explores programmatically
    - Also some simpler ones (descriptions, labels, group_labels)
    - Need to determine if compatible with allowing users to user refinements on views
    - Could extend these, make mandatory, part of immutable project

- Extra
    - Confirm Exposure URLs are valid, perhaps extra behavior with dashboard exposures w/ Looker

# Dataflow Awesome Managing Engine

The easiest dataflow managing framework - **currently under construction.**

DAME solves/facilitates:
 - Building datasets from files / folders
 - Transforming data in the right order
 - Saving transformed data - once computed never compute it again
 - Choosing the best transformation from a few configurations

Great for working with numpy, pyTorch and more.

## Vision

**Technically**:
 - Compute stages:
   1. Sources - get data element
   2. Transforms - compute something out of available data
   3. Reducers - compute something on the whole dataset
 - Combining data sources
 - Compute only what you need - optimized performance via DAGs
 - Backup and cache, after stages, support for custom serializers
 - Ranking various configurations
 - (Optional) Parallel processing

**Priorities**:
 - Easy to use
 - Batteries included
 - Little overhead - take advantage of fastest tools available
 - Integrates seamlessly with other tools
 - Expandable

**Nice to have**:
 - Few python dependencies
 - Integrate tqdm
 - DAG output

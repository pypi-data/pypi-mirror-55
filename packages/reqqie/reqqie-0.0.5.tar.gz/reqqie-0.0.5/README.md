# Reqqie - text based requirement management tool

## Overview
Reqqie is a text based tool to manage requirements. It does so by parsing text files, rewriting them and output reports.
Future feature is to use git to automatically check versions/changes to requirements.
The input files uses the tdbase format.

## Getting started
1. Install reqqie: "pip install reqqie"
2. Create a file "test.req1" with the following content:

```
.config:
  top_requirement -> R1

.req R1:
descr: This describes requirement R1
depends:
  -> R2

.req R2:
descr: This describes requirement R2
```

3. Run reqqie: "reqqie test1.req". Note that if <python-path>/Scripts are not in your path, you will have to use the full path to reqqie.


## Concepts:

Reqqie uses tdbase to read a database of different records.
Record types are defined in the "input file format" section.
The most important one is naturally a requirement (req).

The idea is that all requirements are connected in a Directed Acyclic Graph (DAG). In addition:

* all requirements should be connected through exactly one DAG. Ie, floating/free requirements are not allowed.
* There should be exactly one top requirement. All other requirements should be connected from "higher level" requirement(s).

A simple example:

* R1 - top requirement. Depends on R2,R3,R4
* R2 - Leaf requirement (does not depend on other requirements)
* R3 - middle requirement (not top, but depends on other requirement(s)). Depends on R4
* R4 - Leaf requirement.

This can be shown as (note that R4 appears twice, but is actually the same requirement):

```
R1
  R2
  R3
    R4
  R4
```

Another way to show this is:

```
    R1
    |
  +-+-+--+
  |   |  |
 R2   R3 |
      |  |
       R4
```

Depending on the position in the DAG, every requirement get a numeric level. The top level requirement is always 1, and the others are "max(level of requirements that depends on it)+1". Ie:

* R1, numeric lvl 1
* R2, numeric lvl 2
* R3, numeric lvl 2
* R4, numeric lvl 3

This numeric level is calculated by reqqie, and is an indication of how low level/high level a requirement is.

In addition to the numeric levels, there can be "main levels", defined by the "main_levels" attribute in the config file. The main level is always manually given to each attribute. However, Reqqie will asure that no requirement from a lower level will depend on a requirement from a higher level. It is OK to depend on requirements in the same level though (but the numeric/automatic/fine grain levels assure that the graph is a DAG).

A simple example of main levels are:

```
    main_levels:
        - system
        - design
        - module
```

This is a quite common distinction in simple projects. Ie, some requirements are on the "system" level, defining things on the overall system level, often more from usage point of view. More detailed requirements are on the "design" level, defining more from the design point of view. Lowest level in this simple model defines requirements on the module level.

Besides the levels, requirement can have other metadata, further helping the understanding of the complete requirement set:

* categories. Categories are records in a parallell DAG. They define more what a requirement is about. For instance, categories for a SW product could be:
 - System - top level category.
 - Doc - documentation
 - SW - software category

 SW could be further divided in PC, Frontend, backend etc.
* tags. There are just free text tags.
* release. For project management, requirements can be attached to different releases, and then in reporting, requirement fulfillment per release can be tracked.
* stage: Every requirement goes through different stages. These are propagated up in the requirement DAG. See separate section regarding stages.



## Input file format
Input files are tdbase formatted. The record types supported are:
* .config - singleton record defining structure
* .category - tree structured data used to categorize requirement records
* .release - used to divide requirements into releases
* .req - an actual requirement

### .config
Singleton record which defines structure etc for the requirements

Attributes:

* paths - list of paths (strs) where external files are checked.
* tags - list of strings. These are possible tags to further define what a requirement is. Completely optional.
* top_category - pointer to the top level category record
* top_requirement - pointer to the top level/main requirement
* main_levels - list of strings which gives names to the main levels. There are sub levels automatically assigned, so no requirement ever depends on a requirement at the same or higher level.


### .category
Every requirement should belong to a category. From a definition point of view, this normally reflects how broad or detailed a requirement is. There are some similarities with "level", but those are two different things.

### .release
For project management, it is possible to tag requirements with different releases. Ie, a first release can normally not fulfill all requirements, but by tagging future requirements with later releases, it is possible to get status reports regarding requirement fulfillment for different releases.

### .req
This record defines one requirement.

Attributes:

* descr - text string which describes the requirement. Ie, "General requirement for requirements"
* def - text string which defines the requirement. Normally a short sentence which "Shall" in it. Ie, "Requirements shall be testable and possible to measure. A clear pass/fail criteria shall exist."
* test-spec: either a text string or a link to external document that defines how to test the requirement
* test: link to test report document that shows the test results
* stage:
* depends: list of links to other requirements which must be fulfilled for this requirement to be fulfilled
* category: link to category record
* release: link to the release where this requirement must be fulfilled in.
* level: which main_level this requirement belongs to
* background: string or link to external document. Describes the reason for the requirement. This can be a very helpful information later on when revisiting requirements.



# Examples

## 1. Minimal
```
.config:
  top_category -> only_category
  top_requirement -> top_req
  
.category only_category:
  name: The one and only category
  
.req top_req:
  descr: Top requirement which links all other requirements.
  def: All dependant requirements shall be fulfilled and tested.
  depends:
    -> R2
    
.req R2:
  descr: Example requirement
```

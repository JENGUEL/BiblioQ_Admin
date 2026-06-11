# Graph Report - website  (2026-06-12)

## Corpus Check
- 3 files · ~13,656 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 32 nodes · 35 edges · 4 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bbb6deb1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]

## God Nodes (most connected - your core abstractions)
1. `escapeHtml()` - 5 edges
2. `BiblioQ Marketing Website` - 5 edges
3. `showToast()` - 3 edges
4. `showScanToast()` - 2 edges
5. `header()` - 2 edges
6. `initDashboardDemo()` - 2 edges
7. `initAttendanceDemo()` - 2 edges
8. `initModals()` - 2 edges
9. `initMockSidebarNav()` - 2 edges
10. `Pages` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (4 total, 0 thin omitted)

### Community 1 - "Community 1"
Cohesion: 0.24
Nodes (3): initMockSidebarNav(), initModals(), showToast()

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (5): BiblioQ Marketing Website, Deployment, Download links, Local preview, Pages

### Community 3 - "Community 3"
Cohesion: 0.40
Nodes (5): escapeHtml(), header(), initAttendanceDemo(), initDashboardDemo(), showScanToast()

## Knowledge Gaps
- **4 isolated node(s):** `Pages`, `Local preview`, `Deployment`, `Download links`
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `escapeHtml()` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **What connects `Pages`, `Local preview`, `Deployment` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
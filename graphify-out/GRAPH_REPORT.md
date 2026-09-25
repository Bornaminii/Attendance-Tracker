# Graph Report - Attendance-Tracker  (2026-09-25)

## Corpus Check
- 40 files · ~25,582 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 225 nodes · 199 edges · 30 communities (28 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `db479d25`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 20|Community 20]]

## God Nodes (most connected - your core abstractions)
1. `Implementation Plan` - 16 edges
2. `API Design` - 15 edges
3. `Architecture Overview` - 13 edges
4. `Frontend Architecture (React Native)` - 13 edges
5. `expo` - 10 edges
6. `Database Design` - 9 edges
7. `Tables` - 9 edges
8. `Backend Architecture` - 7 edges
9. `scripts` - 6 edges
10. `Attendance Tracker` - 6 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (30 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (21): Ambiguities Resolved (Without User Input), API Documentation, Architectural Principles, Architecture Overview, Authentication Strategy, Backend Architecture, Configuration, Docker (Development) (+13 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (13): App(), queryClient, RootNavigator(), RootStackParamList, Stack, HomeScreen(), authSlice, AuthState (+5 more)

### Community 2 - "Community 2"
Cohesion: 0.10
Nodes (19): devDependencies, jest, jest-expo, @types/jest, @types/react, typescript, jest, preset (+11 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (18): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, predictiveBackGestureEnabled, expo, android (+10 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (17): `accounts_user`, `attendance_attendance`, Attendance Status Extensibility, Cascades and Deletes, `classes_class`, Database Design, Entity Relationship (Logical), ER Diagram (Mermaid) (+9 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (16): API Design, Attendance, Auth, Classes, CORS, Dashboard, Enrollments, Errors (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (16): Accessibility, Auth + Query integration, Environment, Forms and Validation, Frontend Architecture (React Native), Navigation Structure, Performance, Project Structure (`mobile/src/`) (+8 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (16): Dependency Graph, Implementation Plan, Phase 10: Dashboard & statistics, Phase 11: Frontend polish, Phase 12: Testing & hardening, Phase 13: Production readiness, Phase 1: Project setup, Phase 2: Database models (+8 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (17): dependencies, axios, babel-preset-expo, expo, expo-status-bar, nativewind, react, react-native (+9 more)

### Community 9 - "Community 9"
Cohesion: 0.25
Nodes (4): Shared Django settings., Local and Docker development settings., Production settings. Secrets and hosts must come from the environment., Settings for the local/CI test suite. Uses SQLite so Postgres is not required.

### Community 10 - "Community 10"
Cohesion: 0.29
Nodes (6): Attendance Tracker, Run the API, Run the mobile app, Setup, Stack, Tests

### Community 11 - "Community 11"
Cohesion: 0.33
Nodes (5): Building with EAS, Commands, Expo has changed — do not trust your training data, Navigation & Routing, Rules

### Community 12 - "Community 12"
Cohesion: 0.40
Nodes (4): Documentation (pre-implementation), Implementation phases, Implementation Progress, Phase 1 notes

### Community 13 - "Community 13"
Cohesion: 0.40
Nodes (4): compilerOptions, strict, types, extends

### Community 14 - "Community 14"
Cohesion: 0.50
Nodes (3): config, { getDefaultConfig }, { withNativeWind }

## Knowledge Gaps
- **151 isolated node(s):** `entrypoint.sh script`, `queryClient`, `name`, `slug`, `version` (+146 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `dependencies` connect `Community 8` to `Community 2`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **What connects `Shared Django settings.`, `Local and Docker development settings.`, `Production settings. Secrets and hosts must come from the environment.` to the rest of the system?**
  _155 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.11578947368421053 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Should `Community 4` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
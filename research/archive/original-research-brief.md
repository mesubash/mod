# Kathmandu Mobility Problem Exploration & Research Brief

**Working title:** Kathmandu Adaptive Mobility / Demand Distribution\
**Status:** Problem-definition and research-discovery document\
**Purpose:** A working brief to refine the problem, study existing work,
identify gaps, and decide what should actually be built.\
**Important:** This document deliberately does **not** prescribe a
technology stack or software architecture. Those decisions should come
later.

------------------------------------------------------------------------

## 1. Why this document exists

The original idea is roughly:

> Kathmandu has many possible roads and public-transport routes, but
> during peak periods a relatively small number of major corridors
> become heavily congested. Instead of allowing everyone to
> independently choose the same obvious route, can we understand the
> whole mobility network, identify where demand is concentrated, and
> help distribute travel across better alternatives?

That idea is still intentionally broad.

The goal at this stage is **not** to jump into implementation. The
difficult part is to answer:

1.  What is the actual problem?
2.  Is the problem already solved?
3.  What has already been researched in Kathmandu?
4.  What solutions have already been proposed?
5.  Why have those solutions not been sufficient?
6.  What part of the problem is still poorly addressed?
7.  What could a new project contribute?
8.  How can the contribution be measured?
9.  What should be in scope, and what should explicitly be out of scope?

The final project should emerge from those answers rather than from a
predetermined technology or feature list.

------------------------------------------------------------------------

# 2. The original idea

The starting intuition is:

-   Kathmandu has many roads and routes.
-   Travel demand is not evenly distributed.
-   Major corridors become overloaded during peak periods.
-   Alternative roads/routes may exist but may not be used effectively.
-   Individuals generally optimize their own journey rather than the
    network as a whole.
-   A system could potentially understand demand, congestion and
    available alternatives and recommend a better distribution of
    journeys.
-   The objective would not simply be "find the fastest route."
-   The objective would be closer to **improving the overall mobility
    network while keeping individual journeys acceptable**.

A simplified example:

``` text
Current situation:

                    Major Corridor
Demand  ───────────────► ███████████████  OVERLOADED
        ───────────────► ███████████████
        ───────────────► ███████████████

Alternative A ─────────► █████             UNDERUSED
Alternative B ─────────► ████              UNDERUSED
```

The proposed idea is to investigate whether some demand can be
intelligently shifted:

``` text
                  Major Corridor
Demand  ─────────► ██████████       HEALTHIER

Alternative A ───► ███████          MORE UTILIZED

Alternative B ───► █████            MORE UTILIZED
```

The important question is whether this redistribution can reduce **total
network congestion/delay** without creating an unacceptable burden for
travelers.

------------------------------------------------------------------------

# 3. The idea should NOT be framed as "another navigation app"

This distinction is critical.

A normal navigation system asks:

> What is the best route for this traveler?

The proposed research direction asks:

> How can travel demand be distributed across the available network so
> that the network performs better?

Those are different optimization problems.

A route can be individually fastest but collectively harmful if
thousands of travelers are sent onto it.

Therefore, the project should investigate the difference between:

-   **individual route optimization**
-   **network-level mobility optimization**

This is the strongest conceptual direction in the current idea.

------------------------------------------------------------------------

# 4. The real problem may be broader than route choice

The initial hypothesis should not be treated as proven.

Kathmandu's mobility problem appears to involve several interacting
factors:

### 4.1 Concentrated demand

Travel demand concentrates on particular corridors and time periods.

### 4.2 Public-transport route overlap

Existing public transport has historically developed through fragmented
operations, producing overlapping/direct routes and an uneven network.

### 4.3 Uneven supply

Research on Kathmandu Valley public transportation has found cases where
some routes have more vehicles than required while others require more
than the available supply. One study analyzed 163 routes and explicitly
formulated a vehicle-distribution optimization problem. \[R1\]

### 4.4 Insufficient public-transport coverage/service

Older JICA work identified both chronic congestion on major roads and
insufficient public transport services to support increasing travel
demand. \[R2\]

### 4.5 Fragmented planning and governance

Kathmandu's transport problem is not only a traffic-flow problem.
Existing studies repeatedly identify institutional fragmentation and the
need to coordinate road development, public transport and land-use
planning. \[R2\]\[R5\]

### 4.6 Limited network-level coordination

The strongest possible gap for this project is not simply "there is
congestion."

It is:

> **There may be insufficient continuous coordination between travel
> demand, network capacity, public-transport supply, route choice and
> changing traffic conditions.**

This is a hypothesis that needs to be validated through further
research.

------------------------------------------------------------------------

# 5. What existing research already tells us

The first mistake would be to claim that nobody has tried to solve
Kathmandu's transportation problem.

They have.

In fact, Kathmandu has a long history of transport studies and proposed
interventions.

That is useful because the project can build on them instead of
pretending the problem is new.

------------------------------------------------------------------------

## 5.1 JICA traffic studies

JICA's Data Collection Survey on Traffic Improvement in Kathmandu Valley
identified:

-   chronic congestion on major roads;
-   increasing traffic demand;
-   insufficient public transport services;
-   disorderly urbanization;
-   weaknesses in the road-network system.

It argued that road development, public transport development and
land-use development need to be considered together. \[R2\]

This matters because it suggests that the problem is inherently
**network/systemic**, not merely a routing problem.

------------------------------------------------------------------------

## 5.2 Public transport route rationalization

A major previous study proposed restructuring Kathmandu's public
transport into a three-tier hierarchy:

-   8 primary routes
-   16 secondary routes
-   42 tertiary routes
-   66 routes in total

The proposed model was intended to replace a much larger collection of
overlapping direct routes with an integrated feeder/trunk/direct
network. \[R3\]

This is highly relevant to the current idea.

It means:

> "Kathmandu has overlapping routes and needs better demand
> distribution"

is **not a new observation**.

The project therefore should not simply recreate route rationalization.

Instead, it should ask:

> Why is static route restructuring insufficient, and can a
> dynamic/data-driven approach continuously adapt to actual demand and
> traffic conditions?

------------------------------------------------------------------------

## 5.3 Vehicle supply optimization already exists in research

Research on public transportation energy planning in Kathmandu Valley
studied the optimum number of vehicles required on major routes and
found mismatches between available vehicles and required vehicles.
\[R1\]

This is extremely close to one part of the proposed idea.

Therefore, a new project should not claim:

> "We discovered that some routes have too many buses and others too
> few."

That has already been studied.

A possible new direction is:

> **Can route and vehicle supply be evaluated dynamically against
> changing demand rather than through a mostly static route/fleet
> plan?**

That is a more defensible research direction.

------------------------------------------------------------------------

## 5.4 Comprehensive public transport planning already exists

The UNESCAP comprehensive public transport and mass-transit plan
reviewed decades of previous Kathmandu studies and concluded that public
transport still did not adequately meet mobility needs. It recommends
short-, medium- and long-term interventions and emphasizes coherent
public transport service as Kathmandu expands. \[R4\]

The report also identifies major mobility corridors and discusses
different mass-transit modes.

Again, this reinforces the idea that:

> The problem is known.

The opportunity is therefore not to "discover congestion" but to
investigate a **new operational/data-driven layer for managing a known
network problem**.

------------------------------------------------------------------------

## 5.5 Kathmandu is still actively being planned

This is especially important.

JICA's current Kathmandu Valley Urban Transport System Master Plan
project is intended to:

-   analyze transport and traffic data;
-   develop a traffic-demand forecast model;
-   create a comprehensive urban transportation master plan;
-   identify high-priority mass-transit routes and modes;
-   establish coordination mechanisms between stakeholders. \[R5\]

JICA's project documentation also describes route overlap and the
inability of the current public-transport system to adequately absorb
transport demand as part of Kathmandu's problem. \[R6\]

This means the project should be positioned as complementary research,
not as an attempt to replace official master planning.

------------------------------------------------------------------------

# 6. Existing solution categories

Before deciding what to build, existing solutions should be grouped into
categories.

## A. Infrastructure expansion

Examples:

-   road widening;
-   new roads;
-   intersections;
-   bridges;
-   mass transit infrastructure.

### Limitation

Kathmandu has geographic, historical and land-use constraints. Expanding
physical infrastructure is expensive and cannot be the only solution.

JICA's work explicitly recognizes the physical/geographical constraints
of the valley. \[R6\]

------------------------------------------------------------------------

## B. Public transport restructuring

Examples:

-   route rationalization;
-   feeder/trunk networks;
-   fleet restructuring;
-   higher-capacity buses;
-   mass transit.

### Limitation

These are often long-term/static interventions.

They do not necessarily answer:

> What should happen today between 7:30 and 9:30 when demand is
> different from the average?

------------------------------------------------------------------------

## C. Traffic-signal optimization

Examples:

-   adaptive signals;
-   intersection optimization;
-   queue management.

### Limitation

Useful at intersections, but this does not necessarily solve
**network-wide demand distribution**.

------------------------------------------------------------------------

## D. Bus priority

Examples:

-   bus priority lanes;
-   queue jump lanes;
-   BRT.

Kathmandu research has evaluated bus priority and queue-jump concepts.
\[R7\]\[R8\]

### Limitation

These focus on improving particular corridors or modes rather than
dynamically coordinating the entire travel-demand network.

------------------------------------------------------------------------

## E. Intelligent transportation systems

Examples:

-   sensors;
-   cameras;
-   traffic prediction;
-   adaptive signals;
-   centralized monitoring.

Recent Kathmandu research explicitly proposes AI/IoT-based
traffic-management approaches, including simulation-based evaluation.
\[R9\]\[R10\]

### Limitation

Many proposals focus on **detecting and controlling traffic**, rather
than explicitly solving the question:

> How should travel demand be distributed across alternative routes and
> modes?

------------------------------------------------------------------------

## F. Journey planning

Recent research has already proposed graph-based journey planning for
Kathmandu's semi-formal public-transport network because centralized
route information is limited. \[R11\]

### Limitation

Journey planning normally optimizes an individual's trip.

It does not necessarily optimize the **collective network outcome**.

This distinction may be the strongest opening for the proposed project.

------------------------------------------------------------------------

# 7. The potential research gap

The following should be treated as a **candidate research gap**, not a
final claim until a more systematic literature review is completed.

### Candidate gap

Kathmandu has research and proposals covering:

-   traffic prediction;
-   traffic management;
-   public transport restructuring;
-   route rationalization;
-   vehicle allocation;
-   journey planning;
-   intelligent transport systems;
-   mass transit;
-   intersection-level optimization.

However, there appears to be room to investigate a system that connects
these ideas around a single question:

> **How can travel demand be dynamically distributed across an existing
> multimodal network to reduce network-level congestion while preserving
> acceptable individual travel times?**

The novelty would therefore not be:

> "Use AI for traffic."

Nor:

> "Recommend alternative routes."

Nor:

> "Optimize bus routes."

It would potentially be:

> **Dynamic, network-level demand distribution for Kathmandu mobility.**

This distinction needs to be tested against the full literature before
being claimed as novel.

------------------------------------------------------------------------

# 8. The central hypothesis

A strong working hypothesis could be:

> **If travel demand is modeled at the network level and travelers are
> provided with congestion-aware alternatives rather than being routed
> independently toward the currently fastest corridors, overall network
> congestion and total travel delay can be reduced while keeping
> individual travel-time increases within an acceptable range.**

This creates a measurable experiment.

------------------------------------------------------------------------

# 9. The central research question

A candidate primary research question:

> **Can demand-aware journey recommendations improve the overall
> efficiency of Kathmandu's urban mobility network compared with
> conventional shortest/fastest-route choice?**

Possible secondary questions:

1.  Which Kathmandu corridors experience the greatest mismatch between
    travel demand and available network capacity?
2.  Are alternative routes currently capable of absorbing part of peak
    demand?
3.  How much demand can be redistributed before alternative corridors
    become congested?
4.  What is the trade-off between individual travel time and total
    network delay?
5.  Does including public transport change the optimal distribution of
    travel demand?
6.  How sensitive are results to inaccurate or incomplete traffic
    information?
7.  Which interventions provide the greatest benefit without requiring
    major new infrastructure?
8.  Can a system identify recurring network bottlenecks rather than only
    reacting to current congestion?

------------------------------------------------------------------------

# 10. The key conceptual model

The project can be understood as four interacting layers.

``` text
                    TRAVEL DEMAND
                         │
                         ▼
              ┌────────────────────┐
              │  NETWORK CAPACITY  │
              └─────────┬──────────┘
                        │
                        ▼
              CURRENT NETWORK STATE
                        │
                        ▼
                 ROUTE / MODE CHOICE
                        │
                        ▼
                 TRAFFIC DISTRIBUTION
                        │
                        ▼
                  NEW NETWORK STATE
                        │
                        └──────► feedback
```

This is important because traffic is a **feedback system**.

If a system tells 5,000 people to use the same alternative road, that
alternative may stop being an alternative.

Therefore, the project should model the effect of recommendations on the
network rather than assuming recommendations have no effect.

------------------------------------------------------------------------

# 11. The most important concept: individual optimum vs system optimum

This should become a central part of the research.

### Individual optimization

Each traveler chooses the route that appears best for them.

``` text
Traveler 1 → fastest route
Traveler 2 → fastest route
Traveler 3 → fastest route
...
```

This can create concentration.

### System optimization

The system considers all travelers together.

Some travelers may receive a route that is:

> 3--7 minutes slower

but that choice could reduce congestion enough that the overall network
becomes substantially better.

The research question is therefore not:

> "Can we make every journey faster?"

That is generally unrealistic.

It is:

> **Can we make the network better without imposing unreasonable costs
> on individuals?**

------------------------------------------------------------------------

# 12. A useful concept: congestion externality

A traveler choosing a road affects other travelers.

If one more vehicle enters a nearly saturated road, it can increase
delay for many others.

The traveler usually does not account for that external cost.

A demand-aware system can potentially account for it.

This gives the project a strong theoretical foundation in transportation
economics and network optimization.

------------------------------------------------------------------------

# 13. A useful phenomenon to investigate: Braess's paradox

The project should investigate concepts such as **Braess's paradox**,
where adding or enabling an apparently beneficial route can under
certain conditions make overall network performance worse because
individual route choices interact.

This supports the core argument:

> Routing cannot always be treated as independent shortest-path
> problems.

This does not mean Braess's paradox will necessarily occur in Kathmandu.

It is a theoretical concept that can help explain why network-level
evaluation matters.

------------------------------------------------------------------------

# 14. The project should probably not start by assuming cars are the only problem

Kathmandu is multimodal.

The study should consider, depending on scope:

-   private cars;
-   motorcycles;
-   taxis;
-   buses;
-   microbuses;
-   tempos;
-   walking;
-   cycling;
-   other relevant modes.

Public transport is particularly important because moving people
efficiently is different from simply moving vehicles efficiently.

A bus carrying many passengers should not be treated identically to a
private car.

------------------------------------------------------------------------

# 15. A possible expansion: public-transport demand distribution

There is another potentially strong branch of the project.

Instead of only asking:

> Which road should this traveler take?

ask:

> Which public-transport services should absorb which demand?

For example:

``` text
Peak demand

Route A
Demand: █████████████
Capacity: ███████

Route B
Demand: █████
Capacity: ███████████

Potential intervention:
shift some service / passengers from A toward B
```

However, this should remain a candidate direction until the research
establishes whether it adds meaningful novelty beyond existing Kathmandu
route-rationalization and vehicle-allocation studies.

------------------------------------------------------------------------

# 16. Another possible expansion: departure-time distribution

Route distribution is not the only way to reduce peak congestion.

If demand is:

``` text
07:30  ███
08:00  ███████
08:30  ███████████
09:00  █████████
09:30  █████
```

a system could potentially recommend:

> Leave at 8:00 rather than 8:30.

This creates **temporal demand distribution**.

The broader research problem could therefore become:

> **spatial and temporal travel-demand management**

rather than only route selection.

Again, this should be evaluated before being included.

------------------------------------------------------------------------

# 17. What the system could eventually answer

A mature version of the concept should be able to answer questions such
as:

### Traveler

> "I need to go from A to B. What should I take?"

### Network

> "Which corridors are likely to become overloaded in the next 30
> minutes?"

### Planner

> "What happens if 10% of demand moves from corridor A to corridor B?"

### Public transport planner

> "Where is service supply significantly mismatched with passenger
> demand?"

### City authority

> "Which interventions provide the greatest network benefit without new
> major infrastructure?"

These are different views of the same mobility system.

------------------------------------------------------------------------

# 18. The "what-if" component may be especially valuable

A strong project could eventually become a **mobility decision-support
system**, not merely a commuter app.

Example:

``` text
Scenario: Current network

Average travel time:       42 min
Total network delay:       18,400 min
Peak corridor congestion:  91%
```

Then:

``` text
Scenario: 15% demand redistributed

Average travel time:       40 min
Total network delay:       13,800 min
Peak corridor congestion:  77%
```

The numbers above are only illustrative.

The actual project must calculate them from a defined model.

This type of comparison gives the research a clear evaluation mechanism.

------------------------------------------------------------------------

# 19. Candidate intervention types

The system could evaluate several interventions.

## Traveler-level

-   alternative route;
-   alternative departure time;
-   alternative public-transport option;
-   multimodal alternative.

## Network-level

-   demand redistribution;
-   route allocation;
-   mode shift;
-   corridor balancing.

## Public-transport level

-   service frequency changes;
-   vehicle allocation;
-   route restructuring;
-   feeder/trunk relationships.

## Infrastructure/operations level

-   temporary restrictions;
-   lane allocation;
-   signal strategies;
-   incident response.

The project does **not** need to implement all of these.

They are the candidate intervention space from which the final scope
should be selected.

------------------------------------------------------------------------

# 20. What should NOT be claimed

The project should avoid unsupported claims such as:

-   "Nobody has solved Kathmandu traffic."
-   "Kathmandu has no route planning system."
-   "Alternative routes are unused."
-   "AI will solve traffic congestion."
-   "Our system will eliminate traffic jams."
-   "We are the first traffic optimization platform for Kathmandu."

Existing research clearly disproves the broad versions of these claims.

The defensible position is:

> Kathmandu has extensive previous planning and research, but persistent
> congestion and fragmented mobility indicate that existing measures
> have not fully solved the problem. This project investigates whether a
> dynamic, demand-aware, network-level approach can provide measurable
> improvements in travel-demand distribution.

------------------------------------------------------------------------

# 21. What could actually be new?

The following are candidate novelty directions.

They are **not all equally strong**.

## Candidate A --- Demand-aware routing

Instead of shortest-path routing:

> route users while considering the effect of their collective choices
> on network congestion.

**Strength:** Strong conceptual connection to the original idea.

**Risk:** Requires careful network modeling and comparison.

------------------------------------------------------------------------

## Candidate B --- Dynamic public-transport demand balancing

Continuously compare demand and service capacity and recommend service
redistribution.

**Strength:** Highly relevant to Kathmandu.

**Risk:** Existing route-rationalization and fleet-allocation work means
novelty must be demonstrated carefully.

------------------------------------------------------------------------

## Candidate C --- Spatial + temporal demand distribution

Recommend both:

-   where to travel;
-   when to travel.

**Strength:** Broader congestion-management perspective.

**Risk:** Could become too broad.

------------------------------------------------------------------------

## Candidate D --- What-if mobility simulation

Allow planners to test interventions and compare network outcomes.

**Strength:** Strong decision-support angle.

**Risk:** Simulation validity becomes important.

------------------------------------------------------------------------

## Candidate E --- Multimodal demand optimization

Consider private vehicles + public transport + walking together.

**Strength:** Strong alignment with sustainable mobility.

**Risk:** Significantly increases scope.

------------------------------------------------------------------------

## Candidate F --- Dynamic route/network restructuring

Instead of a fixed public-transport network, investigate whether route
structures should change according to demand.

**Strength:** Directly connected to Kathmandu's existing
route-rationalization problem.

**Risk:** Operational and policy complexity.

------------------------------------------------------------------------

# 22. What I currently think is the strongest direction

At this stage, the strongest candidate is:

> **A demand-aware urban mobility system that evaluates how individual
> route choices affect overall network congestion and recommends
> alternative routes or travel options to distribute demand more
> efficiently.**

Then optionally:

> Extend this into public transport and what-if planning if research
> shows that doing so adds meaningful value.

This keeps the original idea alive without prematurely locking the
project into a huge transportation platform.

------------------------------------------------------------------------

# 23. The project should be evaluated as a research experiment

The project should eventually compare at least two strategies.

### Baseline

Conventional shortest/fastest route selection.

### Proposed

Demand-aware routing/distribution.

Potential evaluation:

  Metric                            Baseline   Proposed
  ------------------------------- ---------- ----------
  Average travel time                      ?          ?
  Total travel delay                       ?          ?
  Peak congestion                          ?          ?
  Maximum corridor utilization             ?          ?
  Number of overloaded segments            ?          ?
  User inconvenience                       ?          ?

The goal is not necessarily to make every metric better.

There may be a trade-off.

A successful system could demonstrate:

> Small increase in individual travel time for some users → large
> decrease in network-wide delay.

That trade-off is potentially the core scientific result.

------------------------------------------------------------------------

# 24. The most important unanswered questions

Before implementation, these questions need research.

## Problem validation

1.  Which Kathmandu corridors actually experience demand concentration?
2.  Are alternative corridors genuinely underused?
3.  Is congestion caused primarily by route concentration, or by
    insufficient total capacity?
4.  How significant is public-transport route overlap?
5.  How much of congestion comes from intersections, road capacity,
    parking/curb activity, public transport stopping, traffic behavior,
    or sheer demand?

## Existing-solution validation

6.  Which existing Kathmandu projects already address demand
    distribution?
7.  Which proposed route-rationalization measures were implemented?
8.  Which were not?
9.  Why?
10. What data and operational limitations prevented them from
    succeeding?

## Research gap

11. Has demand-aware routing already been studied specifically for
    Kathmandu?
12. Has system-optimal traffic assignment been applied to Kathmandu?
13. Has public-transport demand and road congestion been jointly
    optimized for Kathmandu?
14. Has dynamic demand redistribution been evaluated using
    Kathmandu-specific data?
15. What existing academic projects are closest to this proposed system?

## Feasibility

16. What information is actually available?
17. What information would need to be collected?
18. What can reasonably be modeled rather than directly measured?
19. What study area is small enough to validate but meaningful enough to
    matter?

These questions should be answered **before finalizing the project
statement**.

------------------------------------------------------------------------

# 25. Recommended research process

Do not start by designing the application.

Start here:

``` text
PROBLEM
   ↓
Existing Kathmandu evidence
   ↓
Existing solutions
   ↓
Existing failures / limitations
   ↓
Existing research
   ↓
Research gap
   ↓
Candidate contribution
   ↓
Research question
   ↓
Evaluation methodology
   ↓
Scope
   ↓
Implementation
```

This order matters.

------------------------------------------------------------------------

# 26. Phase 1 --- Problem discovery

Collect and review:

-   Kathmandu transport master plans;
-   JICA studies;
-   ADB/UNESCAP reports;
-   Department of Roads/DoTM material;
-   Kathmandu Metropolitan City initiatives;
-   academic papers;
-   transportation theses;
-   existing mobility applications and services;
-   existing route maps and public-transport information.

Create a table:

  ----------------------------------------------------------------------------
  Source      Problem      Proposed    Implemented?   Limitation   Relevance
              identified   solution                                
  ----------- ------------ ----------- -------------- ------------ -----------

  ----------------------------------------------------------------------------

The purpose is to prevent reinventing existing work.

------------------------------------------------------------------------

# 27. Phase 2 --- Existing-solution map

Group existing interventions into:

``` text
Infrastructure
Public transport restructuring
Traffic management
Signal optimization
ITS
Route planning
Demand management
Mass transit
Parking/curb management
Pedestrian/cycling
Governance
```

Then identify what each category solves and what it does not solve.

------------------------------------------------------------------------

# 28. Phase 3 --- Gap analysis

Create a matrix:

  -----------------------------------------------------------------------
  Problem           Existing solution Current           Possible
                                      limitation        contribution
  ----------------- ----------------- ----------------- -----------------
  Peak corridor     Traffic           Reactive/local    Network-level
  overload          management                          redistribution

  Route overlap     Route             Mostly static     Demand-aware
                    rationalization                     adaptation

  Uneven transit    Fleet             Static/periodic   Dynamic demand
  supply            optimization                        balancing

  Individual route  Journey planners  User-centric      Network-aware
  choice                                                recommendations

  Future            Planning studies  Scenario-based    Interactive
  interventions                                         what-if
                                                        evaluation
  -----------------------------------------------------------------------

This table should eventually be replaced with evidence-backed findings
from the literature review.

------------------------------------------------------------------------

# 29. Phase 4 --- Select one actual problem

Do not solve all of Kathmandu's transport problems.

Choose one central problem.

The current strongest candidate is:

> **Peak-period concentration of travel demand on already-congested
> corridors and the lack of a mechanism to evaluate and encourage
> network-level redistribution of that demand.**

But this should remain provisional until the research confirms that this
is both important and insufficiently addressed.

------------------------------------------------------------------------

# 30. Phase 5 --- Define the contribution

A good contribution should be something like:

> A method for dynamically distributing travel demand across alternative
> routes based on network conditions, evaluated using Kathmandu-specific
> mobility scenarios.

Not:

> An app that shows traffic.

Not:

> A website with a Kathmandu map.

Not:

> An AI traffic predictor.

The contribution should be the **method/problem solution**, with
software serving as the demonstration mechanism.

------------------------------------------------------------------------

# 31. Phase 6 --- Define the evaluation before building

Decide what success means.

For example:

> Compared with conventional shortest-path routing, does the proposed
> strategy reduce total network delay and peak congestion while keeping
> individual travel-time penalties below a defined threshold?

If this cannot be measured, the project is not sufficiently defined.

------------------------------------------------------------------------

# 32. Scope strategy

A good final scope could be:

### Core

-   one defined Kathmandu study network;
-   peak-period demand;
-   road network;
-   congestion;
-   route choice;
-   demand redistribution;
-   comparison against baseline.

### Optional

-   public transport;
-   departure-time choice;
-   multimodal routing;
-   prediction;
-   what-if planning.

### Future work

-   city-wide deployment;
-   live government integration;
-   adaptive signals;
-   autonomous traffic control;
-   large-scale fleet management.

This keeps the research question manageable.

------------------------------------------------------------------------

# 33. Things to investigate before making the final decision

The next research pass should specifically search for:

### Kathmandu-specific

-   traffic assignment;
-   user equilibrium;
-   system optimum;
-   demand-aware routing;
-   dynamic traffic assignment;
-   OD estimation;
-   route choice modeling;
-   multimodal traffic assignment;
-   public transport route optimization;
-   transit network design;
-   bus fleet optimization;
-   congestion pricing/demand management;
-   departure-time choice;
-   traffic simulation;
-   SUMO-based Kathmandu studies.

### International

Find established solutions in cities where demand distribution has been
attempted.

Study:

-   what problem they solved;
-   what data they used;
-   how travelers were influenced;
-   whether the intervention actually reduced congestion;
-   what unintended effects occurred.

This provides the conceptual foundation without blindly copying another
city's system.

------------------------------------------------------------------------

# 34. Candidate final project vision

A mature version could be described as:

> **A decision-support and journey-recommendation system for Kathmandu
> that models travel demand and network conditions, evaluates the
> collective effect of route choices, and recommends demand-distribution
> strategies that reduce network congestion while maintaining acceptable
> individual mobility.**

The important words are:

**demand**

**network**

**collective effect**

**distribution**

**acceptable individual mobility**

Those words distinguish the project from ordinary navigation.

------------------------------------------------------------------------

# 35. What we should NOT decide yet

At this stage, deliberately leave these undecided:

-   programming language;
-   framework;
-   database;
-   microservices vs monolith;
-   mobile vs web;
-   cloud;
-   ML model;
-   routing library;
-   mapping library;
-   hardware;
-   real-time infrastructure.

Those are implementation decisions.

The research question comes first.

------------------------------------------------------------------------

# 36. Current working project definition

## Working title

**Kathmandu Adaptive Mobility**

Alternative titles:

-   Kathmandu Mobility Optimization
-   Kathmandu Demand-Aware Mobility
-   Kathmandu Urban Mobility Intelligence
-   Kathmandu Network Mobility Optimizer
-   Adaptive Urban Mobility for Kathmandu

The final name should come later.

------------------------------------------------------------------------

## Working problem statement

> Kathmandu Valley experiences recurring peak-period congestion despite
> having an extensive but fragmented road and public-transport network.
> Previous studies and planning initiatives have addressed
> infrastructure development, public-transport restructuring, route
> rationalization, traffic management and intelligent transportation
> systems. However, there remains a need to examine how travel demand
> itself can be dynamically distributed across the existing network. The
> proposed project investigates whether demand-aware route and mobility
> recommendations can reduce network-level congestion and total travel
> delay without imposing unacceptable travel-time costs on individual
> users.

This is a **working statement**, not the final thesis statement.

------------------------------------------------------------------------

# 37. Working research question

> **How can travel demand be dynamically distributed across Kathmandu's
> existing mobility network to reduce peak-period congestion while
> maintaining acceptable individual travel times?**

------------------------------------------------------------------------

# 38. Working hypothesis

> **A network-aware demand-distribution strategy can reduce total
> network delay and peak congestion compared with independent
> fastest-route selection, provided that the additional travel cost
> imposed on individual travelers remains within an acceptable
> threshold.**

------------------------------------------------------------------------

# 39. Working contribution

Potential contribution:

> **A Kathmandu-specific framework for evaluating and distributing
> travel demand across alternative mobility paths, together with an
> empirical comparison against conventional route-choice behavior.**

Whether this is actually novel must be established through the next
literature-review phase.

------------------------------------------------------------------------

# 40. What Claude should help with next

This document should be treated as a **research starting point**, not a
final specification.

The next step should be a critical literature and problem analysis.

Claude should challenge the assumptions rather than simply agreeing with
them.

Specifically:

1.  Find Kathmandu-specific research that is closest to this idea.
2.  Identify existing systems/projects that already perform similar
    functions.
3.  Determine whether "demand-aware route distribution" is actually a
    research gap.
4.  Identify existing transportation theories/models that apply.
5.  Compare individual shortest-path routing with
    system-optimal/network-level approaches.
6.  Investigate Kathmandu public-transport route rationalization work in
    depth.
7.  Investigate Kathmandu traffic-assignment and simulation studies.
8.  Identify what has already been implemented versus merely proposed.
9.  Identify why existing solutions have not solved the problem.
10. Generate 3--5 alternative problem definitions if the current one is
    weak.
11. Rank the candidate problems by:
    -   importance;
    -   novelty;
    -   feasibility;
    -   measurable impact;
    -   Kathmandu relevance;
    -   research depth.
12. Only after that, recommend the final problem statement and project
    scope.

------------------------------------------------------------------------

# 41. A critical principle for the project

The project should not start with:

> "I want to build X."

It should start with:

> "Kathmandu has problem Y. Existing approaches solve A, B and C but
> leave gap D. We propose E and will evaluate whether E improves
> measurable outcomes."

That is the difference between:

**building an interesting application**

and

**doing a defensible engineering/research project.**

------------------------------------------------------------------------

# 42. Initial source set

The following sources are a starting point for the literature review.

### \[R1\] Public Transportation Energy Planning by Network Analysis --- Kathmandu Valley

Research examining public-transport vehicle requirements across
Kathmandu Valley routes and identifying mismatches between available and
required vehicles.

Source: Journal of Advanced College of Engineering and Management.\
https://nepjol.info/index.php/JACEM/article/view/38273

### \[R2\] JICA --- Data Collection Survey on Traffic Improvement in Kathmandu Valley

Identifies chronic congestion, increasing demand, insufficient public
transport, disorderly urbanization and the need to integrate road,
public transport and land-use planning.

Source: JICA.\
https://openjicareport.jica.go.jp/pdf/12082459_03.pdf

### \[R3\] JICA --- Data Collection Survey on Urban Transport in Kathmandu Valley

Documents the 2014 public-transport restructuring proposal involving
primary, secondary and tertiary route hierarchies and route
rationalization.

Source: JICA / Ministry of Physical Infrastructure and Transport.\
https://openjicareport.jica.go.jp/pdf/12345484_01.pdf

### \[R4\] UNESCAP --- Comprehensive Public Transport and Mass Transit Plan for Kathmandu Valley

Reviews previous Kathmandu transport plans and provides short-, medium-
and long-term recommendations.

Source: UNESCAP.\
https://repository.unescap.org/items/4bb58cb4-1f85-4b6a-840a-869982761bb2

### \[R5\] JICA --- Kathmandu Valley Urban Transport System Master Plan

Current master-planning work focused on transport-data analysis,
traffic-demand forecasting, future public-transport networks, priority
projects and stakeholder coordination.

Source: JICA.\
https://www.jica.go.jp/english/about/policy/environment/id/asia/south/a_b_fi/nepal/pj8nfn000000o56i.html

### \[R6\] JICA --- Project on Kathmandu Valley Urban Transport System Master Plan

Project documentation describing Kathmandu's route overlap,
transport-demand issues and the need for comprehensive urban transport
planning.

Source: JICA.\
https://www.jica.go.jp/oda/project/202109574/

### \[R7\] Queue Jump Lane Study --- Narayan Gopal Intersection

Kathmandu-specific study of bus-priority/queue-jump intervention.

Source: International Journal on Engineering Technology.\
https://www.nepjol.info/index.php/injet/article/view/72572

### \[R8\] Bus Priority / BRT Study

Study examining bus-priority lanes and BRT feasibility in Kathmandu,
including operational, infrastructure and governance challenges.

Source: International Journal on Engineering Technology and
Infrastructure Development.\
https://nepjol.info/index.php/injetindev/article/view/82492

### \[R9\] AI-Driven Traffic Management Framework for Kathmandu

A Kathmandu-specific proposal using simulation to investigate AI-based
traffic-management approaches.

Source: Far Western Review.\
https://www.nepjol.info/index.php/fwr/article/view/79872

### \[R10\] IoT in Traffic Management in Kathmandu Metropolitan City

Research examining the potential role and challenges of IoT-based
traffic management in Kathmandu.

Source: Scientific Researches in Academia.\
https://nepjol.info/index.php/sra/article/view/74284

### \[R11\] Graph-Based Journey Planning for Kathmandu Valley

Recent research proposing graph-based public-transport journey planning
for Kathmandu's semi-formal transit network.

Source: International Journal on Engineering Technology.\
https://www.nepjol.info/index.php/injet/article/view/78657

### \[R12\] Recent Kathmandu Congestion Review

A 2025 review argues that Kathmandu's congestion requires a multimodal,
data-driven approach involving intelligent traffic systems,
public-transit investment and institutional reform.

Source: Journal of Advanced College of Engineering and Management.\
https://www.nepjol.info/index.php/JACEM/article/view/84536

------------------------------------------------------------------------

# 43. Current conclusion

The original idea is **worth investigating**, but the strongest version
is not:

> "Show people alternative roads so traffic is distributed."

It is:

> **Investigate whether Kathmandu's peak travel demand can be
> dynamically distributed across its existing mobility network in a way
> that improves overall network performance without imposing
> unreasonable costs on individual travelers.**

Existing Kathmandu work has already addressed:

-   route rationalization;
-   vehicle allocation;
-   public transport restructuring;
-   traffic management;
-   traffic prediction;
-   journey planning;
-   intelligent transport systems;
-   mass transit.

Therefore, the project's value must come from identifying what those
approaches do **not** address adequately.

The most promising candidate is the gap between:

**individual journey optimization**

and

**collective network optimization**.

But that is still a hypothesis.

The next stage should be a **much deeper literature review and gap
validation**, followed by selection of one precise problem.

Only after that should the project decide exactly what is going to be
built.

# Ad Buyer Agent

The Ad Buyer Agent is an automated advertising buying system built on [CrewAI](https://crewai.com/) and the [IAB OpenDirect 2.1](https://iabtechlab.com/standards/opendirect/) protocol. It receives a campaign brief, allocates budget across channels, researches seller inventory, builds recommendations, and books deals --- all through a single API.

Part of the IAB Tech Lab Agent Ecosystem --- see also the [Seller Agent](https://iabtechlab.github.io/seller-agent/).

## Key Capabilities

- Structured campaign briefing with objectives, budget, dates, audience, and KPIs
- Portfolio-manager agent splits budget across 4 channels (branding, CTV, mobile, performance)
- Multi-seller discovery via AAMP registry with trust verification and capability filtering
- Channel-specialist agents research seller catalogs via MCP and A2A protocols
- Progressive media-kit browsing from summary through full product details and pricing
- Tiered identity strategy with 4 access tiers (public, seat, agency, advertiser) and progressive rate discounts
- Multi-turn negotiation with pluggable strategies (threshold, adaptive, competitive) over A2A conversations
- Quote-then-book deal flow via IAB Deals API v1.0 with DealStore persistence
- Formal order state machine with 12 deal states, guard conditions, and audit trail
- Event bus with 13 event types, fail-open emission, subscriber dispatch, and SQLite persistence
- Human-in-the-loop approval gate before committing spend
- Persistent session management tracking conversation state, negotiation history, and deal context
- Linear TV scatter buying with DMA-level targeting, CPP/CPM pricing, and daypart selection
- Severity-based change request management for post-deal modifications

## Access Methods

The buyer agent communicates with seller agents using three protocols:

| Protocol | Use Case | Speed |
|----------|----------|-------|
| **[MCP](api/mcp-client.md)** | Automated tool calls --- structured, deterministic | Fast |
| **[A2A](api/a2a-client.md)** | Conversational discovery & negotiation | Moderate |
| **[REST](api/overview.md)** | Operator dashboards, legacy integration | Fast |

CrewAI tools use MCP by default. A2A is used for discovery and complex negotiations.
See [Protocol Overview](api/protocols.md) for detailed comparison.

## API Endpoints

The buyer agent exposes 7 endpoints across 3 categories:

| Category | Endpoints |
|----------|-----------|
| **Health** | `GET /health` |
| **Bookings** | `POST /bookings`, `GET /bookings/{job_id}`, `POST /bookings/{job_id}/approve`, `POST /bookings/{job_id}/approve-all`, `GET /bookings` |
| **Products** | `POST /products/search` |

See the [API Overview](api/overview.md) for full details.

## Documentation

### Getting Started

- [Quickstart](getting-started/quickstart.md) --- install, configure, and run your first booking

### Architecture & Reference

- [Agent Hierarchy](architecture/agent-hierarchy.md) --- portfolio manager, channel specialists, and tool agents
- [Tools Reference](architecture/tools.md) --- all CrewAI tools available to agents
- [Configuration](guides/configuration.md) --- environment variables, seller connections, and feature flags
- [API Reference](api/overview.md) --- all endpoints, models, and curl examples
- [Protocol Overview](api/protocols.md) --- comparison of MCP, A2A, and REST

### Guides

- [Negotiation](guides/negotiation.md) --- multi-turn negotiation strategies and deal flow
- [Identity Strategy](guides/identity.md) --- tiered pricing and buyer identity resolution
- [Sessions](guides/sessions.md) --- persistent session management across interactions
- [Multi-Seller Discovery](guides/multi-seller.md) --- AAMP registry and trust verification
- [Linear TV Buying](guides/linear-tv.md) --- scatter, upfront, DMA targeting, and CPP/CPM pricing
- [Media Kit Browsing](guides/media-kit.md) --- progressive disclosure of seller inventory
- [Deal Booking](guides/deal-booking.md) --- end-to-end quote-then-book workflow

### Integration

- [MCP Client](api/mcp-client.md) --- structured tool calls to seller agents
- [A2A Client](api/a2a-client.md) --- conversational discovery and negotiation
- [Seller Agent Integration](integration/seller-agent.md) --- connecting to seller agents and the OpenDirect protocol

### Planned Features

- [Multi-Seller Orchestration](guides/multi-seller-orchestration.md) --- cross-seller campaign optimization
- [Campaign Pipeline](guides/campaign-pipeline.md) --- end-to-end campaign lifecycle
- [Budget Pacing](guides/budget-pacing.md) --- real-time spend management
- [Creative Management](guides/creative-management.md) --- asset upload and assignment
- [Order State Machine](architecture/state-machine.md) --- formal order status transitions
- [Event Bus](architecture/event-bus.md) --- inter-agent event routing


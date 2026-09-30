# Relay Chat

A real-time chat backend built with FastAPI and WebSockets.

Relay Chat is a backend engineering learning project focused on understanding real-time communication and gradually building toward a production-oriented chat architecture.

## Goals

The project will explore:

- WebSocket communication
- Real-time messaging
- Connection management
- Global and private chat rooms
- Message persistence
- Presence and online status
- Reconnection and reliability
- Authentication and authorization
- Multi-device sessions
- Access and refresh tokens
- Token revocation
- Redis and multi-server communication
- Scalable event-driven architecture

## Planned Features

### Phase 1 — Anonymous Chat

- Temporary usernames
- Global chatroom
- WebSocket connections
- Real-time message broadcasting
- Join/leave events
- Message validation
- Message IDs
- Server-generated timestamps
- Basic rate limiting

### Phase 2 — Private Rooms

- Create rooms
- Room IDs
- Room passwords
- Join/leave rooms
- Room-specific broadcasting
- Room membership
- Room capacity limits
- Room expiration and cleanup

### Phase 3 — Persistence

- MongoDB integration
- Message persistence
- Message history
- Message pagination
- Cursor-based pagination
- Message ordering

### Phase 4 — Presence & Reliability

- Online/offline presence
- Heartbeats
- Ping/pong
- Reconnection
- Duplicate message handling
- Message acknowledgements
- Delivery state

### Phase 5 — Authentication

- User accounts
- Access tokens
- Refresh tokens
- Token rotation
- Token revocation
- Logout
- Logout from all devices
- Multi-device sessions

### Phase 6 — Advanced Chat Features

- Typing indicators
- Read receipts
- Message editing
- Message deletion
- Unread counts

### Phase 7 — Scaling

- Redis
- Pub/Sub
- Multiple WebSocket servers
- Load balancing
- Distributed connection management
- Event-driven architecture

## Architecture

The project will intentionally start simple and evolve as new requirements introduce new engineering problems.

Initial architecture:

    Client
       ↓
    WebSocket
       ↓
    FastAPI
       ↓
    Connection Manager
       ↓
    Global Chat

Later:

    Clients
       ↓
    Load Balancer
       ↓
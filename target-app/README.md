# Target App

A sample Node.js + TypeScript application for testing the Living README Agent.

## Overview

This is a simple Express-based REST API that demonstrates configuration management, environment variables, and port configuration - all elements that the Living README Agent will monitor and keep synchronized with this documentation.

<!-- MANAGED_SECTION:START:Requirements -->
## Requirements

- Node.js >= 18.0.0
- npm >= 9.0.0
- TypeScript >= 5.1.6

### Dependencies

- express: ^4.18.2
- dotenv: ^16.0.3
- cors: ^2.8.5

### Dev Dependencies

- @types/express: 4.17.17
- @types/node: 20.5.0
- @types/cors: 2.8.13
- typescript: 5.1.6
- ts-node: 10.9.1
<!-- MANAGED_SECTION:END:Requirements -->

<!-- MANAGED_SECTION:START:Installation -->
## Installation

1. Clone the repository
2. Navigate to the target-app directory
3. Install dependencies:

```bash
npm install
```

4. Create a `.env` file based on the example below
<!-- MANAGED_SECTION:END:Installation -->

<!-- MANAGED_SECTION:START:Configuration -->
## Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory:

### Required Variables

- `NODE_ENV`: Environment mode (development/production)
- `PORT`: Server port (default: 9000)
- `HOST`: Server host (default: localhost)

### Optional Variables

- `DB_HOST`: Database configuration
- `DB_PORT`: Database configuration
- `DB_NAME`: Database configuration
<!-- MANAGED_SECTION:END:Configuration -->

<!-- MANAGED_SECTION:START:Running -->
## Running the Application

### Development Mode

```bash
npm run dev
```

The server will start on `http://localhost:3000`

### Production Mode

1. Build the TypeScript code:

```bash
npm run build
```

2. Start the server:

```bash
npm start
```
<!-- MANAGED_SECTION:END:Running -->

## API Endpoints

### Health Check

```
GET /health
```

Returns the health status of the application.

### API Info

```
GET /api/info
```

Returns information about the API and available endpoints.

### Configuration

```
GET /api/config
```

Returns the current configuration (sanitized, without sensitive data).

<!-- CUSTOM -->
## Custom Notes

This section contains custom documentation that should be preserved by the Living README Agent.
Add any project-specific notes, architecture decisions, or team guidelines here.
<!-- /CUSTOM -->

## License

MIT
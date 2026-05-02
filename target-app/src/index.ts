import { Server } from './server';
import { config, validateConfig } from './config';

/**
 * Main application entry point
 * Initializes and starts the Express server
 */
async function main(): Promise<void> {
  try {
    console.log('Starting Target App...');
    console.log('=================================');
    
    // Validate configuration
    validateConfig();
    
    // Create and start server
    const server = new Server();
    server.start();
    
    // Graceful shutdown handlers
    process.on('SIGTERM', () => {
      console.log('\n⚠️  SIGTERM received, shutting down gracefully...');
      process.exit(0);
    });
    
    process.on('SIGINT', () => {
      console.log('\n⚠️  SIGINT received, shutting down gracefully...');
      process.exit(0);
    });
    
  } catch (error) {
    console.error('❌ Failed to start application:', error);
    process.exit(1);
  }
}

// Start the application
main();

// Made with Bob

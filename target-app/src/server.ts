import express, { Application, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import { config } from './config';

export class Server {
  private app: Application;
  private port: number;
  private host: string;

  constructor() {
    this.app = express();
    this.port = config.port;
    this.host = config.host;
    this.setupMiddleware();
    this.setupRoutes();
  }

  private setupMiddleware(): void {
    // Enable CORS if configured
    if (config.features.enableCors) {
      this.app.use(cors());
      console.log('✓ CORS enabled');
    }

    // Parse JSON bodies
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));

    // Logging middleware
    if (config.features.enableLogging) {
      this.app.use((req: Request, res: Response, next: NextFunction) => {
        console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
        next();
      });
    }
  }

  private setupRoutes(): void {
    // Health check endpoint
    this.app.get('/health', (req: Request, res: Response) => {
      res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        environment: config.nodeEnv,
        port: this.port,
      });
    });

    // API info endpoint
    this.app.get('/api/info', (req: Request, res: Response) => {
      res.json({
        name: 'Target App API',
        version: '1.0.0',
        description: 'Sample Node.js + TypeScript application',
        endpoints: {
          health: '/health',
          info: '/api/info',
          config: '/api/config',
        },
      });
    });

    // Configuration endpoint (sanitized)
    this.app.get('/api/config', (req: Request, res: Response) => {
      res.json({
        environment: config.nodeEnv,
        port: config.port,
        host: config.host,
        features: config.features,
        database: {
          host: config.database.host,
          port: config.database.port,
          name: config.database.name,
          // Don't expose sensitive data
        },
      });
    });

    // 404 handler
    this.app.use((req: Request, res: Response) => {
      res.status(404).json({
        error: 'Not Found',
        message: `Route ${req.method} ${req.path} not found`,
      });
    });

    // Error handler
    this.app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
      console.error('Error:', err.message);
      res.status(500).json({
        error: 'Internal Server Error',
        message: config.nodeEnv === 'development' ? err.message : 'Something went wrong',
      });
    });
  }

  public start(): void {
    this.app.listen(this.port, this.host, () => {
      console.log('=================================');
      console.log(`🚀 Server running on http://${this.host}:${this.port}`);
      console.log(`📝 Environment: ${config.nodeEnv}`);
      console.log(`✓ CORS: ${config.features.enableCors ? 'enabled' : 'disabled'}`);
      console.log(`✓ Logging: ${config.features.enableLogging ? 'enabled' : 'disabled'}`);
      console.log('=================================');
    });
  }

  public getApp(): Application {
    return this.app;
  }
}

// Made with Bob

import dotenv from 'dotenv';
import path from 'path';

// Load environment variables from .env file
dotenv.config({ path: path.join(__dirname, '..', '.env') });

export interface AppConfig {
  nodeEnv: string;
  port: number;
  host: string;
  database: {
    host: string;
    port: number;
    name: string;
    user: string;
    password: string;
  };
  apiKey: string;
  jwtSecret: string;
  features: {
    enableLogging: boolean;
    enableCors: boolean;
    enableRateLimiting: boolean;
  };
}

export const config: AppConfig = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000', 10),
  host: process.env.HOST || 'localhost',
  database: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432', 10),
    name: process.env.DB_NAME || 'myapp_db',
    user: process.env.DB_USER || 'admin',
    password: process.env.DB_PASSWORD || '',
  },
  apiKey: process.env.API_KEY || '',
  jwtSecret: process.env.JWT_SECRET || '',
  features: {
    enableLogging: process.env.ENABLE_LOGGING === 'true',
    enableCors: process.env.ENABLE_CORS === 'true',
    enableRateLimiting: process.env.ENABLE_RATE_LIMITING === 'true',
  },
};

// Validate required configuration
export function validateConfig(): void {
  const requiredVars = ['PORT', 'HOST', 'DB_HOST', 'DB_NAME'];
  const missing = requiredVars.filter(varName => !process.env[varName]);
  
  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
  }
  
  console.log('✓ Configuration validated successfully');
}

// Made with Bob

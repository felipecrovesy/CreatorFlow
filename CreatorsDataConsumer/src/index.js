import dotenv from 'dotenv';
dotenv.config();

import { startServer } from './server.js';
import { startRabbitConsumer } from './rabbitConsumer.js';

async function bootstrap() {
  try {
    await startServer();
    await startRabbitConsumer();
  } catch (error) {
    console.error('[App] Erro fatal durante a inicialização:', error);
    process.exit(1);
  }
}

bootstrap();

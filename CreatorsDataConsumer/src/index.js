import amqp from 'amqplib';
import dotenv from 'dotenv';
import Fastify from 'fastify';
import mongoose from 'mongoose';
import { TopCreatorModel } from './models/topCreatorModel.js';
import { parseMassTransitMessage } from './infrastructure/parsers/massTransitParser.js';
import {
  initExternalDb,
  initTopCreatorModel,
  saveTopCreator,
  getCreatorsResumeByContentType
} from './domain/services/topCreatorService.js';

dotenv.config();

async function start() {
  const mongoUri = process.env.MONGO_URI_EXTERNAL;
  const rabbitUri = process.env.RABBIT_URI;

  initExternalDb(mongoUri);
  initTopCreatorModel(TopCreatorModel);

  await mongoose.connect(mongoUri);
  console.log('[MongoDB External] Conectado.');

  const connection = await amqp.connect(rabbitUri);
  const channel = await connection.createChannel();
  const queue = 'creator-resume-message';

  await channel.assertQueue(queue, { durable: true });
  console.log(`[RabbitMQ] Consumindo da fila: ${queue}`);

  channel.consume(queue, async (msg) => {
    if (msg !== null) {
      const data = parseMassTransitMessage(msg);
      if (data) {
        await saveTopCreator(data);
        channel.ack(msg);
      } else {
        console.warn('[RabbitMQ] Mensagem ignorada por falha no parsing.');
      }
    }
  });

  const app = Fastify();

  app.get('/content-type-resume', async () => {
    const result = await getCreatorsResumeByContentType();
    return result;
  });

  await app.listen({ port: 3000, host: '0.0.0.0' });
}

start();
import amqp from 'amqplib';
import { parseMassTransitMessage } from './infrastructure/parsers/massTransitParser.js';
import { saveCreator } from './domain/services/creatorService.js';

export async function startRabbitConsumer() {
  const rabbitUri = process.env.RABBIT_URI;
  const connection = await amqp.connect(rabbitUri);
  const channel = await connection.createChannel();

  const queue = 'creator-resume-message';
  await channel.assertQueue(queue, { durable: true });

  console.log(`[RabbitMQ] Consumindo da fila: ${queue}`);

  channel.consume(queue, async (msg) => {
    if (!msg) return;

    const data = parseMassTransitMessage(msg);
    if (data) {
      await saveCreator(data);
      channel.ack(msg);
    } else {
      console.warn('[RabbitMQ] Mensagem ignorada: erro no parser.');
    }
  });
}

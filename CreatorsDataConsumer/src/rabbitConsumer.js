import amqp from 'amqplib';
import { parseMassTransitMessage } from './infrastructure/parsers/massTransitParser.js';
import { saveCreator } from './domain/services/creatorService.js';

const RABBIT_URI = process.env.RABBIT_URI || 'amqp://rabbitmq';
const QUEUE_NAME = 'creator-resume-message';
const ERROR_QUEUE = `${QUEUE_NAME}_error`;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function connectWithRetry(maxRetries = 10, delayMs = 5000) {
  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      console.log(`[RabbitMQ] Tentando conectar (${attempt + 1}/${maxRetries})...`);
      const connection = await amqp.connect(RABBIT_URI);
      console.log('[RabbitMQ] Conexão estabelecida.');
      return connection;
    } catch (err) {
      console.error(`[RabbitMQ] Erro ao conectar: ${err.message}`);
      attempt++;
      await sleep(delayMs);
    }
  }

  throw new Error('[RabbitMQ] Falha ao conectar após várias tentativas.');
}

export async function startRabbitConsumer() {
  const connection = await connectWithRetry();
  const channel = await connection.createChannel();

  await channel.assertQueue(QUEUE_NAME, { durable: true });
  await channel.assertQueue(ERROR_QUEUE, { durable: true });

  console.log(`[RabbitMQ] Consumindo da fila: ${QUEUE_NAME}`);

  channel.consume(QUEUE_NAME, async (msg) => {
    if (!msg) return;

    const data = parseMassTransitMessage(msg);

    if (data) {
      try {
        await saveCreator(data);
        channel.ack(msg);
        console.log(`[RabbitMQ] Criador salvo com sucesso: ${data.CreatorName}`);
      } catch (err) {
        console.error('[RabbitMQ] Erro ao salvar criador:', err.message);
        channel.nack(msg, false, false);
      }
    } else {
      console.warn('[RabbitMQ] Mensagem malformada. Redirecionando para fila de erro.');

      try {
        await channel.sendToQueue(ERROR_QUEUE, msg.content, {
          persistent: true,
          headers: msg.properties.headers,
        });
        channel.ack(msg);
      } catch (sendErr) {
        console.error('[RabbitMQ] Falha ao redirecionar mensagem para fila de erro:', sendErr.message);
        channel.nack(msg, false, false);
      }
    }
  });
}

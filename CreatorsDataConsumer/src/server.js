import Fastify from 'fastify';
import mongoose from 'mongoose';
import {
  initExternalDb,
  initCreatorModel,
  getCreatorsResumeByContentType,
  getAllCreatorsPaginated
} from './domain/services/creatorService.js';
import { CreatorModel } from './models/CreatorModel.js';

export async function startServer() {
  const app = Fastify();

  app.addHook('onSend', async (request, reply, payload) => {
    reply.header('Access-Control-Allow-Origin', '*');
    return payload;
  });

  app.get('/content-type-resume', async (_, reply) => {
    const data = await getCreatorsResumeByContentType();
    reply.send(data);
  });

  app.get('/creators', async (request, reply) => {
    const { page = 1, limit = 10 } = request.query;
    const data = await getAllCreatorsPaginated(page, limit);
    reply.send(data);
  });

  const mongoUri = process.env.MONGO_URI_EXTERNAL;
  initExternalDb(mongoUri);
  initCreatorModel(CreatorModel);
  await mongoose.connect(mongoUri);
  console.log('[MongoDB External] Conectado.');

  await app.listen({ port: 3000 });
  console.log('[Fastify] Servidor rodando em http://localhost:3000');
}

export function parseMassTransitMessage(msg) {
  try {
    const envelope = JSON.parse(msg.content.toString());
    if (envelope && envelope.message) {
      return envelope.message;
    }
    throw new Error('Formato inesperado: campo "message" ausente');
  } catch (error) {
    console.error('[Parser] Erro ao parsear mensagem MassTransit:', error);
    return null;
  }
}
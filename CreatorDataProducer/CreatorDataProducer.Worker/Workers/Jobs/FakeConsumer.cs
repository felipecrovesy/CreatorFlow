using MassTransit;
using CreatorDataProducer.Domain.Messages;

public class FakeCreatorResumeMessageConsumer : IConsumer<CreatorResumeMessage>
{
    public Task Consume(ConsumeContext<CreatorResumeMessage> context)
    {
        // Faz nada, só engana o MassTransit
        Console.WriteLine("[FakeConsumer] Mensagem recebida, ignorando.");
        return Task.CompletedTask;
    }
}
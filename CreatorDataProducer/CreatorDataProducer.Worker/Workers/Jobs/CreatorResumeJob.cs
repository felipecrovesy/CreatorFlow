using CreatorDataProducer.Application.Interfaces;
using CreatorDataProducer.Domain.Messages;
using MassTransit;
using Quartz;

namespace CreatorDataProducer.Worker.Workers.Jobs;

public class CreatorResumeJob : IJob
{
    private readonly ICreatorResumeRepository _creatorResumeRepository;
    private readonly IPublishEndpoint _publishEndpoint;

    public CreatorResumeJob(ICreatorResumeRepository creatorResumeRepository, IPublishEndpoint publishEndpoint)
    {
        _creatorResumeRepository = creatorResumeRepository;
        _publishEndpoint = publishEndpoint;
    }

    public async Task Execute(IJobExecutionContext context)
    {
        Console.WriteLine($"[Quartz] Iniciando job em {DateTime.Now}");

        var creators = await _creatorResumeRepository.GetUnprocessedAsync();

        Console.WriteLine($"[Quartz] Encontrados {creators.Count} criadores não processados.");
            
        foreach (var creator in creators)
        {
            try
            {
                var message = new CreatorResumeMessage
                {
                    Id = Guid.NewGuid().ToString(),
                    CreatorName = creator.CreatorName,
                    TotalFollowers = creator.TotalFollowers,
                    ContentType = creator.ContentType,
                    Revenue = creator.Revenue
                };

                await _publishEndpoint.Publish(message);

                await _creatorResumeRepository.MarkAsProcessedAsync(new[] { creator.Id });

                Console.WriteLine($"[Quartz] Criador {creator.CreatorName} publicado e marcado como processado.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Quartz] Erro ao processar criador {creator.CreatorName}: {ex.Message}");
            }
        }
    }
}
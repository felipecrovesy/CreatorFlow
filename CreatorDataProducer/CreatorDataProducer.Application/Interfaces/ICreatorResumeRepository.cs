using CreatorDataProducer.Domain.Entities;
using MongoDB.Bson;

namespace CreatorDataProducer.Application.Interfaces
{
    public interface ICreatorResumeRepository
    {
        Task<List<CreatorResume>> GetUnprocessedAsync();
        Task MarkAsProcessedAsync(IEnumerable<ObjectId> ids);
    }
}
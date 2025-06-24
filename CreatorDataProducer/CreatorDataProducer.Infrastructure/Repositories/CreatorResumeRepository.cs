using CreatorDataProducer.Application.Interfaces;
using CreatorDataProducer.Domain.Entities;
using MongoDB.Driver;
using MongoDB.Bson;

namespace CreatorDataProducer.Infrastructure.Repositories
{
    public class CreatorResumeRepository : ICreatorResumeRepository
    {
        private readonly IMongoCollection<CreatorResume> _collection;

        public CreatorResumeRepository(IMongoDatabase database)
        {
            _collection = database.GetCollection<CreatorResume>("resume_creators_info");
        }

        public async Task<List<CreatorResume>> GetUnprocessedAsync()
        {
            var projection = Builders<CreatorResume>.Projection
                .Include(x => x.CreatorName)
                .Include(x => x.TotalFollowers)
                .Include(x => x.ContentType)
                .Include(x => x.Revenue);

            var filter = Builders<CreatorResume>.Filter.Eq(x => x.IsProcessed, false);

            var results = await _collection.Find(filter)
                .Project<CreatorResume>(projection)
                .Limit(100)
                .ToListAsync();

            return results;
        }

        public async Task MarkAsProcessedAsync(IEnumerable<ObjectId> ids)
        {
            var filter = Builders<CreatorResume>.Filter.In(x => x.Id, ids);
            var update = Builders<CreatorResume>.Update.Set(x => x.IsProcessed, true);

            await _collection.UpdateManyAsync(filter, update);
        }
    }
}
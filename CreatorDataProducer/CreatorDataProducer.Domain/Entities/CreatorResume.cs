using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace CreatorDataProducer.Domain.Entities
{
    public class CreatorResume
    {
        [BsonId]
        public ObjectId Id { get; set; }

        [BsonElement("creatorName")]
        public string CreatorName { get; set; }

        [BsonElement("totalFollowers")]
        public int TotalFollowers { get; set; }

        [BsonElement("contentType")]
        public string ContentType { get; set; }

        [BsonElement("isProcessed")]
        public bool IsProcessed { get; set; }
        
        [BsonElement("revenue")]
        public decimal Revenue { get; set; }
    }
}
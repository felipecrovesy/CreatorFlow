namespace CreatorDataProducer.Domain.Messages;

public class CreatorResumeMessage
{
    public string Id { get; set; } = string.Empty;
    public string CreatorName { get; set; } = string.Empty;
    public int TotalFollowers { get; set; }
    public string ContentType { get; set; } = string.Empty;
    public decimal Revenue { get; set; }
}
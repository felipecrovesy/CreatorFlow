using CreatorDataProducer.Infrastructure.Configuration;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using MongoDB.Driver;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddMongoDb(this IServiceCollection services, IConfiguration configuration)
    {
        var settings = configuration.GetSection("MongoDb").Get<MongoDbSettings>();
        services.AddSingleton(settings);

        var client = new MongoClient(settings.ConnectionString);
        services.AddSingleton<IMongoClient>(client);

        services.AddScoped(sp =>
        {
            var client = sp.GetRequiredService<IMongoClient>();
            return client.GetDatabase(settings.DatabaseName);
        });

        return services;
    }
}
using CreatorDataProducer.Application.Interfaces;
using CreatorDataProducer.Infrastructure.Configuration;
using CreatorDataProducer.Infrastructure.Repositories;
using CreatorDataProducer.Worker.Workers.Jobs;
using Quartz;
using MassTransit;

var builder = Host.CreateDefaultBuilder(args)
    .ConfigureServices((hostContext, services) =>
    {
        var config = hostContext.Configuration;

        services.Configure<MongoDbSettings>(config.GetSection("MongoDb"));

        services.AddSingleton(sp =>
        {
            var settings = sp.GetRequiredService<Microsoft.Extensions.Options.IOptions<MongoDbSettings>>().Value;
            var client = new MongoDB.Driver.MongoClient(settings.ConnectionString);
            return client.GetDatabase(settings.DatabaseName);
        });

        services.AddScoped<ICreatorResumeRepository, CreatorResumeRepository>();

        var rabbitConfig = config.GetSection("RabbitMq").Get<RabbitMqSettings>();

        services.AddMassTransit(x =>
        {
            x.AddConsumer<FakeCreatorResumeMessageConsumer>();

            x.UsingRabbitMq((context, cfg) =>
            {
                cfg.Host(rabbitConfig.Host, "/", h =>
                {
                    h.Username(rabbitConfig.Username);
                    h.Password(rabbitConfig.Password);
                });
                
                cfg.UseRetry(r =>
                {
                    r.Interval(5, TimeSpan.FromSeconds(5));
                });

                cfg.ReceiveEndpoint("creator-resume-message", e =>
                {
                    e.ConfigureConsumeTopology = true;
                    e.ConfigureConsumer<FakeCreatorResumeMessageConsumer>(context);
                });
            });
        });

        services.AddQuartz(q =>
        {
            var initialDelay = config.GetSection("Quartz").GetValue<int>("InitialDelaySeconds");
            
            var jobKey = new JobKey("CreatorResumeJob");
            q.AddJob<CreatorResumeJob>(opts => opts.WithIdentity(jobKey));
            q.AddTrigger(opts => opts
                .ForJob(jobKey)
                .WithIdentity("CreatorResumeJob-trigger")
                .StartAt(DateBuilder.FutureDate(initialDelay, IntervalUnit.Second))
                .WithSimpleSchedule(x => x.WithIntervalInSeconds(200).RepeatForever()));
        });

        services.AddQuartzHostedService(q => q.WaitForJobsToComplete = true);
    });

var app = builder.Build();
await app.RunAsync();
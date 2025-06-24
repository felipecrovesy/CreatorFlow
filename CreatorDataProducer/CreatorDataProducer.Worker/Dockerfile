FROM mcr.microsoft.com/dotnet/runtime:9.0 AS base
USER $APP_UID
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["CreatorDataProducer.Worker/CreatorDataProducer.Worker.csproj", "CreatorDataProducer.Worker/"]
COPY ["CreatorDataProducer.Application/CreatorDataProducer.Application.csproj", "CreatorDataProducer.Application/"]
COPY ["CreatorDataProducer.Domain/CreatorDataProducer.Domain.csproj", "CreatorDataProducer.Domain/"]
COPY ["CreatorDataProducer.Infrastructure/CreatorDataProducer.Infrastructure.csproj", "CreatorDataProducer.Infrastructure/"]
RUN dotnet restore "CreatorDataProducer.Worker/CreatorDataProducer.Worker.csproj"
COPY . .
WORKDIR "/src/CreatorDataProducer.Worker"
RUN dotnet build "CreatorDataProducer.Worker.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "CreatorDataProducer.Worker.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "CreatorDataProducer.Worker.dll"]

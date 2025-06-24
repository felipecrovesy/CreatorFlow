import mongoose from 'mongoose';

let externalDb;
let ExternalTopCreator;

export function initExternalDb(uri) {
  externalDb = mongoose.createConnection(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  });
}

export function initTopCreatorModel(schema) {
  ExternalTopCreator = externalDb.model('TopCreator', schema, 'top_creators_by_content-type');
}

export async function saveTopCreator(data) {
  const creator = new ExternalTopCreator({
    creatorName: data.creatorName,
    totalFollowers: data.totalFollowers,
    contentType: data.contentType,
    revenue: data.revenue
  });
  await creator.save();
  console.log('[MongoDB External] Criador salvo com sucesso.');
}

export async function getCreatorsResumeByContentType() {
  return await ExternalTopCreator.aggregate([
    {
      $group: {
        _id: '$contentType',
        totalCreators: { $sum: 1 },
        totalFollowers: { $sum: '$totalFollowers' },
        totalRevenue: { $sum: '$revenue' }
      }
    },
    {
      $project: {
        _id: 0,
        contentType: '$_id',
        totalCreators: 1,
        totalFollowers: 1,
        totalRevenue: 1
      }
    }
  ]);
}
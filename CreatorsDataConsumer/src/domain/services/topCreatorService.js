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
  ExternalTopCreator = externalDb.model('TopCreator', schema, 'creators');
}

export async function saveCreator(data) {
  const creator = new ExternalTopCreator({
    creatorName: data.creatorName,
    totalFollowers: data.totalFollowers,
    contentType: data.contentType,
  });
  await creator.save();
  console.log('[MongoDB External] Criador salvo com sucesso.');
}

export async function getAllCreatorsPaginated(page = 1, pageSize = 10) {
  const skip = (page - 1) * pageSize;

  const creators = await ExternalTopCreator.find({}, {
    creatorName: 1,
    totalFollowers: 1,
    revenue: 1,
    contentType: 1,
    _id: 0
  })
  .skip(skip)
  .limit(pageSize)
  .lean();

  const totalCount = await ExternalTopCreator.countDocuments();

  return {
    total: totalCount,
    page,
    pageSize,
    totalPages: Math.ceil(totalCount / pageSize),
    data: creators
  };
}

export async function getCreatorsResumeByContentType() {
  const result = await ExternalTopCreator.aggregate([
    {
      $group: {
        _id: '$contentType',
        totalCreators: { $sum: 1 },
        totalFollowers: { $sum: '$totalFollowers' },
      }
    },
    {
      $project: {
        _id: 0,
        contentType: {
          $concat: [
            { $toUpper: { $substrCP: ['$_id', 0, 1] } },
            { $substrCP: ['$_id', 1, { $subtract: [{ $strLenCP: '$_id' }, 1] }] }
          ]
        },
        totalCreators: 1,
        totalFollowers: 1
      }
    },
    {
      $sort: { totalFollowers: -1 }
    }
  ]);

  return result;
}

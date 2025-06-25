import mongoose from 'mongoose';

let externalDb;
let Creator;

export function initExternalDb(uri) {
  externalDb = mongoose.createConnection(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  });
}

export function initCreatorModel(schema) {
  Creator = externalDb.model('Creator', schema, 'creators');
}

export async function saveCreator(data) {
  const creator = new Creator({
    creatorName: data.creatorName,
    totalFollowers: data.totalFollowers,
    contentType: data.contentType,
    revenue: data.revenue
  });
  await creator.save();
  console.log('[MongoDB External] Criador salvo com sucesso.');
}

export async function getAllCreatorsPaginated(page = 1, pageSize = 10) {
  const p = parseInt(page) || 1;
  const limit = parseInt(pageSize) || 10;
  const skip = (p - 1) * limit;

  const creators = await Creator.find({}, {
    creatorName: 1,
    totalFollowers: 1,
    revenue: 1,
    contentType: 1,
    _id: 0
  })
  .skip(skip)
  .limit(limit)
  .lean();

  const totalCount = await Creator.countDocuments();

  return {
   total: totalCount,
   page: p,
   pageSize: limit,
   totalPages: Math.ceil(totalCount / limit),
   data: creators
  };
}

export async function getCreatorsResumeByContentType() {
  const result = await Creator.aggregate([
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

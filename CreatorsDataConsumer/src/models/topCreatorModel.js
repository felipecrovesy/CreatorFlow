import mongoose from 'mongoose';

export const TopCreatorModel = new mongoose.Schema({
  creatorName: String,
  totalFollowers: Number,
  contentType: String,
  revenue: Number,
});
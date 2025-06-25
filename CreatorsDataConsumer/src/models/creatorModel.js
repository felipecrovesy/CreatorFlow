import mongoose from 'mongoose';

export const CreatorModel = new mongoose.Schema({
  creatorName: String,
  totalFollowers: Number,
  contentType: String,
  revenue: Number,
});
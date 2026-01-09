import { UserPlan } from '../../users/models/plan.enum';

export enum PlanPeriod {
  MONTHLY = 'monthly',
  WEEKLY = 'weekly',
  DAILY = 'daily',
}

export enum PlanFeatures {
  WRITINGS = 'writings',
}

export interface PlanFeature {
  feature: PlanFeatures;
  quantity: number;
  period: PlanPeriod;
}

export interface Plans {
  plan: UserPlan;
  price: number;
  features: [PlanFeature];
  created_at: Date;
  updated_at: Date;
}

export interface StripePlan {
  id: string;
  product_id: string;
  name: string;
  amount: number;
  currency: string;
  interval: string;
}

export interface Subscription {
  id: string;
  customer_id: string; // ID of the customer in Stripe
  subscription_id: string; // ID of the subscription in Stripe
  product_name: string;
  product_id: string;
  period_start: Date; // Start date of the billing period
  period_end: Date; // End date of the billing period
  event_id: string; // ID of the webhook event in Stripe
  event_created_at: Date; // Event creation date
  created_at: Date; // Date of creation in the database
}

export interface CustomerPortalResponse {
  portal_url: string;
}

export interface StripeSubscribePlan {
  price_id: string;
  fallback_url: string;
}

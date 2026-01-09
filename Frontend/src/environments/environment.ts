const address = window.location.origin.split('/')[2].split(':')[0];

export const api_google = {
  id: '**************************************',
};
export const environment = {
  googleAnalyticsKey: 'G-****************',
  production: false,
  apiUrl: `http://${address}:8000`,
};

export const stripe_pk =
  '********************************';

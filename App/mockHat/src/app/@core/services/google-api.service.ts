import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class GoogleApiService {
  constructor() {}

  load() {
    return new Promise<void>((resolve) => {
      const script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      script.onload = () => resolve();
      document.body.appendChild(script);
    });
  }
}

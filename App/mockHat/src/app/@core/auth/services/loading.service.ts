import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class LoadingService {
  private readonly isLoading = signal(false);
  private loadingCount = 0;
  start() {
    try {
      this.loadingCount++;
      this.isLoading.set(true);
    } catch {
      /* empty */
    }
  }

  stop() {
    try {
      if (this.loadingCount > 0) {
        this.loadingCount--;
      }

      if (this.loadingCount === 0) {
        this.isLoading.set(false);
      }
    } catch {
      /* empty */
    }
  }

  get status() {
    return this.isLoading.asReadonly();
  }
}

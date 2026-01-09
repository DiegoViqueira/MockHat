import { ErrorHandler, Injectable, Injector, NgZone } from '@angular/core';
import { BackendError } from '../models/backend-error.model';
import { TOAST_OPTION, ToastService } from './toast.service';

@Injectable({
  providedIn: 'root',
})
export class GlobalErrorHandler implements ErrorHandler {
  constructor(
    private readonly injector: Injector,
    private readonly ngZone: NgZone
  ) { }

  handleError(error: any): void {
    const service = this.injector.get(ToastService);
    this.ngZone.run(() => {
      const message = this.getMessage(error);
      const args = this.getArgs(error);
      service.display(TOAST_OPTION.ERROR, 'Error', message, args);
    });
  }

  private getMessage(error: any): string {
    if (error instanceof BackendError) {
      return error.name;
    }

    if (error instanceof Error) {
      return error.message;
    }

    return typeof error === 'string' ? error : '';
  }

  private getArgs(error: any) {
    if (error instanceof BackendError) {
      return { data: error.message };
    }
    return {};
  }
}

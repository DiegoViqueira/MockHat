import { Injectable, inject } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { MatSnackBar } from '@angular/material/snack-bar';

export const enum TOAST_OPTION {
  INFO,
  WARNING,
  ERROR,
  SUCCESS,
}

@Injectable({
  providedIn: 'root',
})
export class ToastService {
  private snackBar = inject(MatSnackBar);

  constructor(
    private readonly translate: TranslateService
  ) { }

  public display(
    toastOption: TOAST_OPTION,
    title: string,
    messageKey: string,
    interpolateParams?: object,
    durationInMs?: number
  ) {
    const defaultToastSettings = {
      timeOut: durationInMs || 7000,
      positionClass: 'toast-top-right',
      preventDuplicates: true,
    };

    this.displayCustomizedToast(
      title !== '' ? this.translate.instant(title) : '',
      this.translate.instant(messageKey, interpolateParams),
      toastOption,
      defaultToastSettings
    );
  }

  private displayCustomizedToast(
    title: string,
    message: string,
    toastOption: TOAST_OPTION,
    toastConfig: any
  ) {
    switch (toastOption) {
      case TOAST_OPTION.ERROR:
        this.snackBar.open(message, title, {
          duration: toastConfig.timeOut,
          panelClass: 'error-snackbar',
          horizontalPosition: 'right',
          verticalPosition: 'top',
        });
        break;
      case TOAST_OPTION.INFO:
        this.snackBar.open(message, title, {
          duration: toastConfig.timeOut,
          panelClass: 'info-snackbar',
          horizontalPosition: 'right',
          verticalPosition: 'top',
        });
        break;
      case TOAST_OPTION.WARNING:
        this.snackBar.open(message, title, {
          duration: toastConfig.timeOut,
          panelClass: 'warning-snackbar',
          horizontalPosition: 'right',
          verticalPosition: 'top',
        });
        break;
      case TOAST_OPTION.SUCCESS:
        this.snackBar.open(message, title, {
          duration: toastConfig.timeOut,
          panelClass: 'success-snackbar',
          horizontalPosition: 'right',
          verticalPosition: 'top',
        });
        break;
      default:
        this.snackBar.open(message, title, {
          duration: toastConfig.timeOut,
          panelClass: 'info-snackbar',
          horizontalPosition: 'right',
          verticalPosition: 'top',
        });
    }
  }
}

import { Injectable } from '@angular/core';
import { ToastController } from '@ionic/angular';
import { TranslateService } from '@ngx-translate/core';

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
    constructor(
        private readonly toastController: ToastController,
        private readonly translate: TranslateService
    ) { }

    /**
     * Display a toast message
     * @param toastOption - Type of toast (INFO, WARNING, ERROR, SUCCESS)
     * @param title - The title of the toast
     * @param messageKey - The translation key for the message
     * @param interpolateParams - Parameters to interpolate in the translation
     * @param durationInMs - Duration of the toast in milliseconds
     */
    public async display(
        toastOption: TOAST_OPTION,
        title: string,
        messageKey: string,
        interpolateParams?: object,
        durationInMs?: number
    ) {
        const message = this.translate.instant(messageKey, interpolateParams);
        const header = title ? this.translate.instant(title) : '';
        const color = this.getToastColor(toastOption);

        const toast = await this.toastController.create({
            header,
            message,
            duration: durationInMs || 5000,
            position: 'top',
            color,
            buttons: [
                {
                    text: this.translate.instant('dismiss'),
                    role: 'cancel',
                },
            ],
        });

        await toast.present();
    }

    /**
     * Get the Ionic color based on the toast option
     * @param toastOption - Type of toast (INFO, WARNING, ERROR, SUCCESS)
     * @returns The corresponding Ionic color
     */
    private getToastColor(toastOption: TOAST_OPTION): string {
        switch (toastOption) {
            case TOAST_OPTION.ERROR:
                return 'danger';
            case TOAST_OPTION.INFO:
                return 'primary';
            case TOAST_OPTION.WARNING:
                return 'warning';
            case TOAST_OPTION.SUCCESS:
                return 'success';
            default:
                return 'medium'; // Default color
        }
    }
}

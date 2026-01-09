import { ChangeDetectorRef, Component, computed, Signal } from '@angular/core';
import { LoadingService } from '../../../@core/auth/services/loading.service';

@Component({
    selector: 'wlk-spinner',
    templateUrl: './spinner.component.html',
    styleUrl: './spinner.component.scss',
    standalone: false
})
export class SpinnerComponent {
  constructor(protected loadingService: LoadingService) {}
}

// device-detection.service.ts
import { Injectable, OnDestroy, signal, Signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class DeviceDetectionService implements OnDestroy {
  private mobileQuery: MediaQueryList;
  private mobileQueryListener: () => void;

  // Reemplazamos BehaviorSubject con Signal
  private mobileScreenSize = signal<boolean>(false);

  constructor() {
    // Inicializar la detección reactiva de tamaño de pantalla
    this.mobileQuery = window.matchMedia('(max-width: 600px)');
    this.mobileScreenSize.set(this.mobileQuery.matches);

    this.mobileQueryListener = () => {
      this.mobileScreenSize.set(this.mobileQuery.matches);
    };

    // Usar addEventListener para compatibilidad moderna
    this.mobileQuery.addEventListener('change', this.mobileQueryListener);
  }



  ngOnDestroy(): void {
    // Limpiar el listener cuando el servicio se destruye
    this.mobileQuery.removeEventListener('change', this.mobileQueryListener);
  }

  isAndroid(): boolean {
    const userAgent = navigator.userAgent || navigator.vendor;
    return /android/i.test(userAgent);
  }

  isIOS(): boolean {
    const userAgent = navigator.userAgent || navigator.vendor;
    return /iPad|iPhone|iPod/.test(userAgent);
  }

  isMobile(): boolean {
    return this.isAndroid() || this.isIOS() || this.isMobileByScreenSize();
  }

  isMobileByScreenSize(maxWidth: number = 600): boolean {
    return window.innerWidth <= maxWidth;
  }

  // Exponemos el Signal directamente
  get isMobileScreen(): Signal<boolean> {
    return this.mobileScreenSize.asReadonly();
  }

  // Método para obtener el valor actual
  get isMobileScreenValue(): boolean {
    return this.mobileScreenSize();
  }
}

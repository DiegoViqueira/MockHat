/*
 * Copyright (c) Herta 2023. All Rights Reserved.
 *
 */
import { Component, OnInit, inject } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { DeviceDetectionService } from './@core/services/device-detection.service';
import { DomSanitizer } from '@angular/platform-browser';
import { MatIconRegistry } from '@angular/material/icon';
import { environment } from '../environments/environment';
import { NavigationEnd, Router } from '@angular/router';
import { SessionService } from './@core/auth/services/session.service';

declare let gtag: Function;
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  standalone: false
})
export class AppComponent implements OnInit {

  private readonly session = inject(SessionService);

  constructor(
    private router: Router,
    private matIconRegistry: MatIconRegistry,
    private domSanitizer: DomSanitizer,
    private translateService: TranslateService,
    private deviceDetectionService: DeviceDetectionService
  ) {
    this.translateService.setDefaultLang(this.getLang());

    this.matIconRegistry.addSvgIcon(
      'ai',
      this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/ai.svg')
    );
    this.matIconRegistry.addSvgIcon(
      'mockhat',
      this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/icon-mockhat.svg')
    );
  }

  ngOnInit(): void {


    this.session.onClose.subscribe(() => {
      this.router.navigateByUrl('auth/login');
    });

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd && typeof gtag === 'function') {
        gtag('config', environment.googleAnalyticsKey, {
          page_path: event.urlAfterRedirects,
        });
      }
    });

  }

  getLang() {
    let browserLang = navigator.language;
    if (browserLang.indexOf('-') !== -1) {
      browserLang = browserLang.split('-')[0];
    }
    if (browserLang !== 'es' && browserLang !== 'en') return 'en';

    return browserLang;
  }
}

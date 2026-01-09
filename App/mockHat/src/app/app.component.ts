import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
export class AppComponent {

  constructor(private translateService: TranslateService) {
    this.translateService.setDefaultLang(this.getLang());
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

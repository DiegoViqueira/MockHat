import { CUSTOM_ELEMENTS_SCHEMA, ErrorHandler, LOCALE_ID, NgModule, SecurityContext } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClient, provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
import { MAT_FORM_FIELD_DEFAULT_OPTIONS } from '@angular/material/form-field';
import { CoreModule } from './@core/core.module';
import { ModulesModule } from './modules/modules.module';
import localeES from '@angular/common/locales/es';
import { registerLocaleData } from '@angular/common';
import { GlobalErrorHandler } from './@core/auth/services/global-error-handler';
import { SharedModule } from './@shared/shared.module';
import { NgChartsModule } from 'ng2-charts';
import { NgxCaptchaModule } from 'ngx-captcha';
import { MarkdownModule } from 'ngx-markdown';
registerLocaleData(localeES);

@NgModule({
  declarations: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  bootstrap: [AppComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: HttpLoaderFactory,
        deps: [HttpClient],
      },
    }),
    NgxCaptchaModule,
    BrowserAnimationsModule,
    MarkdownModule.forRoot(),
    CoreModule.forRoot(),
    ModulesModule,
    SharedModule,
    NgChartsModule,

  ],
  providers: [
    { provide: LOCALE_ID, useValue: 'es-*' },
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: { appearance: 'fill' },
    },
    { provide: ErrorHandler, useClass: GlobalErrorHandler },
    provideHttpClient(withInterceptorsFromDi()),
  ],
})
export class AppModule { }

// required for AOT compilation
export function HttpLoaderFactory(http: HttpClient): TranslateHttpLoader {
  return new TranslateHttpLoader(http);
}

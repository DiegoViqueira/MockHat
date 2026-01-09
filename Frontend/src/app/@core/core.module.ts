import { ModuleWithProviders, NgModule, Optional, SkipSelf } from '@angular/core';
import { CommonModule } from '@angular/common';
import { throwIfAlreadyLoaded } from './module-import-guard';
import { AuthModule } from './auth/auth.module';
import { JwtModule } from '@auth0/angular-jwt';
import { HTTP_INTERCEPTORS, provideHttpClient, withInterceptors } from '@angular/common/http';
import { ErrorInterceptor } from './auth/interceptors/error.interceptor';
import { Token } from './auth/models/token';
import { loadingInterceptor } from './auth/interceptors/loading.interceptor';
import { authInterceptor } from './auth/interceptors/auth.interceptor';
import { LocalStorageService } from './auth/services/local-storage.service';

@NgModule({
  imports: [
    CommonModule,
    JwtModule.forRoot({
      config: {
        tokenGetter: (request) => {
          const token = new LocalStorageService().get<Token>('token');

          if (request.url.includes('refresh')) return token !== null ? token.Refresh : '';

          return token !== null ? token.Access : '';
        },
        allowedDomains: [
          /(api.mockhat.com)/,
          /(localhost)./,
          /(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})./,
        ],
      },
    }),
  ],
  exports: [AuthModule],
  declarations: [],
})
export class CoreModule {
  constructor(@Optional() @SkipSelf() parentModule: CoreModule) {
    throwIfAlreadyLoaded(parentModule, 'CoreModule');
  }

  static forRoot(): ModuleWithProviders<CoreModule> {
    return {
      ngModule: CoreModule,
      providers: [
        provideHttpClient(withInterceptors([loadingInterceptor, authInterceptor])),
        { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
      ],
    };
  }
}

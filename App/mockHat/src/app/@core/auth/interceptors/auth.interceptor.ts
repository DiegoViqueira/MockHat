import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { catchError, switchMap } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { SessionService } from '../services/session.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const session = inject(SessionService);
  const auth = inject(AuthService);

  if (
    session.isExpired() &&
    !req.url.includes('refresh') &&
    !req.url.includes('login') &&
    !req.url.includes('logout') &&
    session.accessToken()
  ) {
    return auth.refresh().pipe(
      switchMap((newToken) => {
        if (newToken) {
          req = req.clone({
            setHeaders: {
              Authorization: `Bearer ${newToken.Access}`,
            },
          });
        }
        return next(req);
      }),
      catchError(() => {
        auth.logout().subscribe(() => { });
        return throwError(() => 'CANNOT_REFRESH_AUTH');
      })
    );
  } else {
    return next(req);
  }
};

import { Injectable } from '@angular/core';
import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next
      .handle(request)
      .pipe(catchError((error: HttpErrorResponse) => this.handleError(error)));
  }

  private handleError(err: HttpErrorResponse): Observable<never> {
    if (!(err instanceof HttpErrorResponse)) {
      return throwError(() => new Error('UNKNOWN_ERROR'));
    }


    switch (err.status) {
      case 0:
        return throwError(() => new Error('serverConnectionError'));
      case 422:

        let errorMessages = '';

        err.error.detail.forEach((err: any) => {
          const field = err.loc[1];
          const message = err.msg;
          errorMessages += `${field}: ${message}\n`;
        });
        return throwError(() => new Error(errorMessages));

      case 400:
        return throwError(() => new Error(err.error.detail));
      default:
        return throwError(() => new Error(err.error.detail));
    }
  }
}

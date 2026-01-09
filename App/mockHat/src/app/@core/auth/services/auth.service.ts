/*
 * Copyright (c) Walken 2023. All Rights Reserved.
 *
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Token } from '../models/token';
import { HttpService } from '../../services/http.service';
import { finalize, map } from 'rxjs/operators';
import { SessionService } from './session.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(
    private readonly session: SessionService,
    private readonly api: HttpService
  ) { }

  login(Username: string, Password: string): Observable<void> {
    const data = { username: Username, password: Password };

    return this.api.post('auth/login', data).pipe(
      map((result) => {
        this.session.set({ Access: result.access_token, Refresh: result.refresh_token } as Token);
      })
    );
  }

  loginWithMicrosoft(token: any): Observable<any> {
    const google_token_request = { token: token };
    return this.api.post('auth/microsoft', google_token_request).pipe(
      map((result) => {
        this.session.set(
          { Access: result.access_token, Refresh: result.refresh_token } as Token,
          true
        );
      })
    );
  }

  loginWithGoogle(token: any): Observable<any> {
    const google_token_request = { token: token };
    return this.api.post('auth/google', google_token_request).pipe(
      map((result) => {
        this.session.set(
          { Access: result.access_token, Refresh: result.refresh_token } as Token,
          true
        );
      })
    );
  }

  logout(): Observable<void> {
    return this.api.post('auth/logout', {}).pipe(finalize(() => this.session.close()));
  }

  refresh(): Observable<Token> {
    return this.api.post('auth/refresh', {}).pipe(
      map((result) => {
        const token = { Access: result.access_token, Refresh: result.refresh_token } as Token;
        this.session.set(token);
        return token;
      })
    );
  }
}

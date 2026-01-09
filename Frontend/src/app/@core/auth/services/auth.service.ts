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
import { RegisterUser } from '../models/register-user.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(
    private readonly session: SessionService,
    private readonly api: HttpService
  ) { }

  login(Username: string, Password: string): Observable<void> {

    const formData = new FormData();
    formData.append('username', Username);
    formData.append('password', Password);

    return this.api.post('auth/login', formData).pipe(
      map((result) => {
        this.session.set({ Access: result.access_token, Refresh: result.refresh_token } as Token);
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

  register(user: RegisterUser): Observable<any> {
    return this.api.post('auth/signup', user);
  }

  verifyRegister(token: string): Observable<any> {
    return this.api.get(`auth/verify-register?token=${token}`);
  }

  forgotPassword(email: string): Observable<any> {
    return this.api.post('auth/forgot-password', { email: email });
  }

  resetPassword(token: string, password: string): Observable<any> {
    return this.api.post('auth/reset-password', { token: token, password: password });
  }
}

import { EventEmitter, Injectable, signal, WritableSignal } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { LocalStorageService } from './local-storage.service';
import { Token } from '../models/token';
import { User } from '../models/users';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SessionService {
  private readonly _user: WritableSignal<User | null> = signal(null);
  private readonly _onClose: EventEmitter<void> = new EventEmitter<void>();
  public accessToken: WritableSignal<string | null> = signal(null);
  public refreshToken: WritableSignal<string | null> = signal(null);
  public isGoogleUser: WritableSignal<boolean> = signal(false);
  constructor(
    private readonly jwtHelper: JwtHelperService,
    private readonly storage: LocalStorageService
  ) {
    this.recover();
  }

  get user() {
    return this._user.asReadonly();
  }


  isExpired() {
    return this.jwtHelper.isTokenExpired(this.accessToken(), 30);
  }

  private recover() {
    const user = this.storage.get<User>('user');
    this._user.set(user);
    const token = this.storage.get<Token>('token');
    this.accessToken.set(token?.Access ?? null);
    this.refreshToken.set(token?.Refresh ?? null);
  }

  set(token: Token, isGoogleUser: boolean = false) {
    const user = this.toUser(token.Access);
    this.storage.set('user', user);
    this.storage.set('token', token);
    this._user.set(user);
    this.accessToken.set(token.Access);
    this.refreshToken.set(token.Refresh);
    this.isGoogleUser.set(isGoogleUser);
  }

  private toUser(token: string): User {
    const decodeToken = this.jwtHelper.decodeToken(token);
    return {
      username: decodeToken.sub ?? '',
      role: decodeToken.role ?? '',
    } as User;
  }

  close() {
    this.storage.remove('token');
    this.storage.remove('user');
    this._user.set(null);
    this.accessToken.set(null);
    this.refreshToken.set(null);
    this._onClose.next();
  }

  get onClose(): Observable<void> {
    return this._onClose;
  }
}

import { SessionService } from './session.service';
import { JwtHelperService } from '@auth0/angular-jwt';
import { LocalStorageService } from './local-storage.service';
import { generateUserSystem } from '../../../../tests/factories/user-system.factory';
import { generateTokens } from '../../../../tests/factories/token.factory';

describe('SessionService', () => {
  let jwtHelper: JwtHelperService;
  let localStorage: LocalStorageService;

  beforeEach(() => {
    jwtHelper = new JwtHelperService();
    localStorage = new LocalStorageService();
  });

  it('should recover null data when there is no saved data in localstorage', () => {
    const sut = new SessionService(jwtHelper, localStorage);

    expect(sut.user()).toBeNull();
    expect(sut.accessToken()).toBeNull();
    expect(sut.refreshToken()).toBeNull();
  });

  it('should recover user data', () => {
    const user = generateUserSystem();
    localStorage.set('user', user);
    const token = generateTokens();
    localStorage.set('token', token);

    const sut = new SessionService(jwtHelper, localStorage);

    expect(sut.user()).toEqual(user);
    expect(sut.accessToken()).toEqual(token.Access);
    expect(sut.refreshToken()).toEqual(token.Refresh);
  });

  it('should set user session', () => {
    const sut = new SessionService(jwtHelper, localStorage);

    const expectedUser = { role: 'Administrator', username: 'admin' };
    const expectedTokens = generateTokens();
    sut.set(expectedTokens);

    expect(sut.user()).toEqual(expectedUser);
    expect(sut.accessToken()).toEqual(expectedTokens.Access);
    expect(sut.refreshToken()).toEqual(expectedTokens.Refresh);

    expect(localStorage.get('user')).toEqual(expectedUser);
    expect(localStorage.get('token')).toEqual(expectedTokens);
  });

  it('should delete information on close session', () => {
    const sut = new SessionService(jwtHelper, localStorage);
    sut.set(generateTokens());

    sut.close();

    expect(sut.user()).toBeNull();
    expect(sut.accessToken()).toBeNull();
    expect(sut.refreshToken()).toBeNull();

    expect(localStorage.get('user')).toBeNull();
    expect(localStorage.get('token')).toBeNull();
  });

  it('should test if token is expired', () => {
    const sut = new SessionService(jwtHelper, localStorage);
    jwtHelper.isTokenExpired = jest.fn().mockReturnValue(true);
    const expectedTokens = generateTokens();
    sut.set(expectedTokens);

    const response = sut.isExpired();

    expect(response).toBeTruthy();
    expect(jwtHelper.isTokenExpired).toHaveBeenCalledTimes(1);
    expect(jwtHelper.isTokenExpired).toHaveBeenCalledWith(expectedTokens.Access, 30);
  });

  it('should close emit', () => {
    const sut = new SessionService(jwtHelper, localStorage);

    let callTimes = 0;
    sut.onClose.subscribe(() => callTimes++);

    sut.close();

    expect(callTimes).toEqual(1);
  });
});

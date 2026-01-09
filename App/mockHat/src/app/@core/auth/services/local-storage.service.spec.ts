import { LocalStorageService } from './local-storage.service';
import { User } from '../models/users';
import { generateUserSystem } from '../../../../tests/factories/user-system.factory';

describe('LocalStorageService', () => {
  beforeEach(() => localStorage.clear());

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should return null when key data does not exist', () => {
    const sut = new LocalStorageService();

    const user = sut.get<User>('user');

    expect(user).toBeNull();
  });

  it('should return data when key data exist', () => {
    const expected = generateUserSystem();
    const sut = new LocalStorageService();
    sut.set('user', expected);

    const user = sut.get<User>('user');

    expect(user).toEqual(expected);
  });

  it('should return null when data was removed', () => {
    const sut = new LocalStorageService();
    sut.set('user', generateUserSystem());

    sut.remove('user');

    const user = sut.get<User>('user');
    expect(user).toBeNull();
  });
});

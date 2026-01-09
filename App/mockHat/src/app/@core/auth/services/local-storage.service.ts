import { Injectable } from '@angular/core';
import { User } from '../models/users';
import { Token } from '../models/token';

type values = {
  user: User;
  token: Token;
  selectedNodes: string[];
  alarmType: string;
};

type keys = keyof values;

@Injectable({
  providedIn: 'root',
})
export class LocalStorageService {
  get<T>(value: keys): T | null {
    const data = localStorage.getItem(value);
    if (data === null) return null;

    return JSON.parse(data) as T;
  }

  set<T>(value: keys, data: T) {
    const json = JSON.stringify(data);
    localStorage.setItem(value, json);
  }

  remove(value: keys) {
    localStorage.removeItem(value);
  }
}

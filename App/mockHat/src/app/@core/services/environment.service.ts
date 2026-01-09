import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class EnvironmentService {
  private readonly urlAddress = environment.apiUrl;

  address() {
    return this.urlAddress;
  }

  version() {
    return String('1.0.0');
  }
}



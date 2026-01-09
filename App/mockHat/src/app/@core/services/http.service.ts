import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { EnvironmentService } from './environment.service';

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  private readonly api: string;

  constructor(
    private http: HttpClient,
    env: EnvironmentService
  ) {
    this.api = env.address();
  }

  post(endpoint: string, data: object, options?: any): Observable<any> {
    return this.http.post(`${this.api}/${endpoint}`, data, options);
  }

  delete(endpoint: string, id: string, options?: any): Observable<any> {
    return this.http.delete(`${this.api}/${endpoint}/${id}`, options);
  }

  patch(endpoint: string, id: string, data: object, options?: any): Observable<any> {
    return this.http.patch(`${this.api}/${endpoint}/${id}`, data, options);
  }

  get(endpoint: string): Observable<any> {
    return this.http.get(`${this.api}/${endpoint}`);
  }
}

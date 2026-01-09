import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
@Injectable({
  providedIn: 'root',
})
export class HttpService {
  private readonly api: string;

  constructor(
    private http: HttpClient,
  ) {
    this.api = environment.apiUrl;
  }

  post(endpoint: string, data: object, options?): Observable<any> {
    return this.http.post(`${this.api}/${endpoint}`, data, options);
  }

  delete(endpoint: string, id: string, options?): Observable<any> {
    return this.http.delete(`${this.api}/${endpoint}/${id}`, options);
  }

  patch(endpoint: string, id: string, data: object, options?): Observable<any> {
    return this.http.patch(`${this.api}/${endpoint}/${id}`, data, options);
  }

  get(endpoint: string): Observable<any> {
    return this.http.get(`${this.api}/${endpoint}`);
  }
}

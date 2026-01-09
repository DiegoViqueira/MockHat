import { Injectable } from '@angular/core';
import { HttpService } from '../../../@core/services/http.service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Plans } from '../models/plan.model';

@Injectable({
  providedIn: 'root',
})
export class PlanService {
  constructor(private readonly api: HttpService) {}

  list(): Observable<Plans[]> {
    return this.api.get(`plans`).pipe(
      map((response) => {
        return response;
      })
    );
  }
}

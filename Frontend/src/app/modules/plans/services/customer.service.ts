import { Injectable } from '@angular/core';
import { HttpService } from '../../../@core/services/http.service';
import { Observable } from 'rxjs';
import { StripePlan } from '../models/plan.model';
import { map } from 'rxjs/operators';
import { CustomerPortalResponse, StripeSubscribePlan } from '../models/customer.model';
import { Subscription } from '../models/subscription.model';

@Injectable({
  providedIn: 'root',
})
export class CustomerService {
  constructor(private readonly api: HttpService) { }

  getPortal(return_url: string): Observable<CustomerPortalResponse> {
    const data = { fallback_url: return_url };
    return this.api.post('customers/portal', data).pipe(
      map((response) => {
        return response;
      })
    );
  }

  currentSubscription(): Observable<Subscription> {
    return this.api.get('customers/current-plan').pipe(
      map((response) => {
        return response;
      })
    );
  }
  suscribe(data: StripeSubscribePlan) {
    return this.api.post('customers/subscribe-to-plan', data).pipe(
      map((response) => {
        return response;
      })
    );
  }
  getPrices(): Observable<StripePlan[]> {
    return this.api.get('customers/get-stripe-plans').pipe(
      map((response) => {
        return response;
      })
    );
  }
}
